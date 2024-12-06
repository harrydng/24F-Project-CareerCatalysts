from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
students = Blueprint('students', __name__)

#------------------------------------------------------------
# POST all the top students from the database, package them up,
# and return them to the client
@students.route('/top_students', methods=['POST'])
def get_products():
    the_data = request.json
    current_app.logger.info(the_data)

    # Extract the limit variable
    limit = the_data['limit']
    
    query = f'''
    SELECT *
    FROM (
        SELECT 
            sp.nuId                                                 AS 'Student ID',
            COUNT(DISTINCT ss.skillId)                              AS 'Total Skills',
            sp.major                                                AS 'Major',
            sp.minor                                                AS 'Minor',
            CONCAT(u.firstName, ' ', u.lastName)                    AS 'Full Name',
            COUNT(DISTINCT sc.courseId)                             AS 'Total Courses',
            (COUNT(DISTINCT ss.skillId) + COUNT(DISTINCT sc.courseId)) AS 'Total Score'
        FROM student_profile sp
            LEFT JOIN student_skills ss ON sp.nuId = ss.nuId
            LEFT JOIN student_courses sc ON sp.nuId = sc.nuId
            JOIN user u ON sp.nuId = u.userId
        GROUP BY sp.nuId
    ) AS subquery
    ORDER BY `Total Score` DESC
    LIMIT {limit};
    '''
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#
@students.route('/filterStudents', methods=['POST'])
def filter_students():
    filters = request.json['data']
    current_app.logger.info("Filters received: %s", filters)
    
    # Extract and validate input
    first_name = filters.get("first_name", "")
    last_name = filters.get("last_name", "")
    major = filters.get("major", None)
    nuId = filters.get("nuId", None)
    year = filters.get("year", None)
    minor = filters.get("minor", None)
    email = filters.get("email", "")
    skills = filters.get("skills", [])
    courses = filters.get("courses", [])

    # Dynamically build the WHERE clause
    conditions = []
    query_params = []

    if first_name:
        conditions.append("u.firstName = %s")
        query_params.append(first_name)

    if last_name:
        conditions.append("u.lastName = %s")
        query_params.append(last_name)

    if nuId:
        try:
            nuId = int(nuId)
            conditions.append("sp.nuId = %s")
            query_params.append(nuId)
        except ValueError:
            return jsonify({"error": "Invalid nuId format"}), 400

    if year:
        try:
            year = int(year)
            conditions.append("sp.year = %s")
            query_params.append(year)
        except ValueError:
            return jsonify({"error": "Invalid year format"}), 400

    if email:
        conditions.append("u.email = %s")
        query_params.append(email)

    if major:
        conditions.append("sp.major = %s")
        query_params.append(major)

    if minor:
        conditions.append("sp.minor = %s")
        query_params.append(minor)

    if skills:
        skills_placeholders = ", ".join(["%s"] * len(skills))
        conditions.append(f"s.name IN ({skills_placeholders})")
        query_params.extend(skills)

    if courses:
        courses_placeholders = ", ".join(["%s"] * len(courses))
        conditions.append(f"c.courseName IN ({courses_placeholders})")
        query_params.extend(courses)

    # Combine all conditions with AND
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f'''
        SELECT DISTINCT 
                sp.nuId                                                  AS StudentID,
                CONCAT(u.firstName, ' ', u.lastName)                     AS FullName,
                sp.major                                                 AS Major,
                sp.minor                                                 AS Minor,
                sp.year                                                  AS Year,
                u.email                                                  AS Email,
                GROUP_CONCAT(DISTINCT b.badgeName ORDER BY b.badgeName)  AS Badge,
                GROUP_CONCAT(DISTINCT s.name ORDER BY s.name)            AS Skills,
                GROUP_CONCAT(DISTINCT c.courseName ORDER BY c.courseName)AS Courses,
                COUNT(DISTINCT ss.skillId) + COUNT(DISTINCT sc.courseId) AS TotalScore
        FROM student_profile sp
            JOIN user u ON sp.nuId = u.userId
            LEFT JOIN student_skills ss ON sp.nuId = ss.nuId
            LEFT JOIN skills s ON ss.skillId = s.skillId
            LEFT JOIN student_badges sb ON sb.nuId = sp.nuId
            LEFT JOIN badge b ON b.badgeId = sb.badgeId
            LEFT JOIN student_courses sc ON sp.nuId = sc.nuId
            LEFT JOIN courses c ON sc.courseId = c.courseId
        WHERE {where_clause}
        GROUP BY sp.nuId, FullName, sp.major, sp.minor, sp.year, u.email
        ORDER BY TotalScore DESC, FullName;
    '''

    current_app.logger.info("Executing query: %s", query)

    cursor = db.get_db().cursor()
    cursor.execute(query, query_params)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
