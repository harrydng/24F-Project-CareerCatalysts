from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

##### Blueprint ######
users = Blueprint('users', __name__)

#### CRUD OPS ######

# Function to get user details
@users.route('/user', methods=['GET'])
def get_user_details():
    """
    Fetch all details about a specific user (student).
    """
    user_id = request.args.get('userId')

    query = f'''
        SELECT *
        FROM user u
        JOIN student_profile sp ON u.userId = sp.nuId
        WHERE u.userId = {user_id}
    '''

    # Fetch data
    cursor = db.get_db().cursor()
    cursor.execute(query)
    user_data = cursor.fetchone()

    # Prepare response
    response = make_response(jsonify(user_data))
    response.status_code = 200
    return response


# Function to add a new user
@users.route('/user', methods=['POST'])
def add_user():
    """
    Add a new user to the system.
    """
    data = request.json
    username = data['username']
    email = data['email']
    first_name = data['firstName']
    last_name = data['lastName']
    password_hash = data['password']
    role_id = data['roleId'] 
    major = data.get('major', None)
    minor = data.get('minor', None)
    year = data.get('year', None)
    dob = data.get('dob', None) 

    cursor = db.get_db().cursor()

    # Insert into the user table
    insert_user_query = f'''
        INSERT INTO user (username, email, firstName, middleName, lastName, password_hash, roleId)
        VALUES ("{username}", "{email}", "{first_name}", "{middle_name}", "{last_name}", "{password_hash}", {role_id})
    '''
    cursor.execute(insert_user_query)
    db.get_db().commit()
    user_id = cursor.lastrowid

    # Insert into the student_profile table (if relevant)
    if major or minor or year or dob:
        insert_student_query = f'''
            INSERT INTO student_profile (nuId, major, minor, year, dob)
            VALUES ({user_id}, "{major or 'NULL'}", "{minor or 'NULL'}", {year or 'NULL'}, "{dob or 'NULL'}")
        '''
        cursor.execute(insert_student_query)
        db.get_db().commit()

    # Return success response
    return make_response(jsonify({
        "message": "New user added successfully",
        "userId": user_id
    }), 201)


# Function to update user details
@users.route('/user', methods=['PUT'])
def update_user_details():
    """
    Update user details such as name, email, or student profile attributes.
    """
    data = request.json
    user_id = data['userId']
    updates = []

    # User table updates
    if 'email' in data:
        updates.append(f"email = '{data['email']}'")
    if 'firstName' in data:
        updates.append(f"firstName = '{data['firstName']}'")
    if 'middleName' in data:
        updates.append(f"middleName = '{data['middleName']}'")
    if 'lastName' in data:
        updates.append(f"lastName = '{data['lastName']}'")
    if 'status' in data:
        updates.append(f"status = {int(data['status'])}")

    if updates:
        user_update_query = f'''
            UPDATE user
            SET {', '.join(updates)}
            WHERE userId = {user_id}
        '''
        cursor = db.get_db().cursor()
        cursor.execute(user_update_query)
        db.get_db().commit()

    # Student profile updates
    profile_updates = []
    if 'major' in data:
        profile_updates.append(f"major = '{data['major']}'")
    if 'minor' in data:
        profile_updates.append(f"minor = '{data['minor']}'")
    if 'year' in data:
        profile_updates.append(f"year = {data['year']}")
    if 'dob' in data:
        profile_updates.append(f"dob = '{data['dob']}'")

    if profile_updates:
        profile_update_query = f'''
            UPDATE student_profile
            SET {', '.join(profile_updates)}
            WHERE nuId = {user_id}
        '''
        cursor.execute(profile_update_query)
        db.get_db().commit()

    # Return success response
    return make_response(jsonify({"message": "User details updated successfully"}), 200)


# Function to delete a user
@users.route('/user', methods=['DELETE'])
def delete_user():
    """
    Permanently delete a user from the database.
    """
    data = request.json
    user_id = data['userId']
    query = f'''
        DELETE FROM user
        WHERE userId = {user_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response(jsonify({"message": "User deleted successfully"}), 200)


#------------------------------------------------------------
# GET the if of the employer based on the given name
@users.route('/employerId', methods=['GET'])
def get_employer_id():
    the_data = request.json
    current_app.logger.info(the_data)
    
    companyName = the_data.get('company_name')
    
    query = f'''
    SELECT ep.employerId
    FROM employer_profile ep JOIN user u ON ep.employerId = u.userId
    WHERE u.firstName = %s
    '''
    
    current_app.logger.info(f'GET /employerId query={query}')

    
    cursor = db.get_db().cursor()
    cursor.execute(query, (companyName,))
    theData = cursor.fetchall()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

#------------------------------------------------------------
# POST all the top students from the database, package them up,
# and return them to the client
@users.route('/top_students', methods=['POST'])
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

#------------------------------------------------------------
# Filter out students based on specified qualifications
@users.route('/filterStudents', methods=['POST'])
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

#------------------------------------------------------------
# GET all the metrics and possible alerts from the website
@users.route('/metrics_and_alerts', methods=['GET'])
def get_metrics_and_alerts():
    """
    Retrieve all metrics and alerts from the database and return them in a structured JSON format.
    """
    try:
        # Get a database cursor
        cursor = db.get_db().cursor()

        # Query to get all metrics and alerts
        metrics_query = 'SELECT metricId, errorRate, serverLoad, responseTime, createdAt FROM metrics;'
        alerts_query = 'SELECT alertId, messages, priority, title FROM alert;'

        # Execute the metrics query
        cursor.execute(metrics_query)
        metrics_data = cursor.fetchall()

        # Execute the alerts query
        cursor.execute(alerts_query)
        alerts_data = cursor.fetchall()

        # Combine results into a single response
        response_data = {
            'metrics': metrics_data,
            'alerts': alerts_data
        }

        return jsonify(response_data), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving metrics and alerts: {e}")
        return jsonify({'error': 'Failed to retrieve metrics and alerts'}), 500


#------------------------------------------------------------
# PUT to update the user role
@users.route('/update_user_role', methods=['PUT'])
def update_user_role():
    data = request.json
    current_app.logger.info(data)

    # Extract userId and new roleId from the request data
    userId = data.get('userId')
    new_roleId = data.get('roleId')

    if not userId or not new_roleId:
        response = make_response(jsonify({'error': 'userId and roleId are required'}))
        response.status_code = 400
        return response

    cursor = db.get_db().cursor()

    # Update the user's role
    update_query = '''
        UPDATE user
        SET roleId = %s
        WHERE userId = %s
    '''
    current_app.logger.info(update_query)

    try:
        cursor.execute(update_query, (new_roleId, userId))
        db.get_db().commit()
        response = make_response(jsonify({'message': 'User role updated successfully'}))
        response.status_code = 200
    except Exception as e:
        current_app.logger.error('Error updating user role: %s', e)
        response = make_response(jsonify({'error': 'Failed to update user role'}))
        response.status_code = 500

    return response

