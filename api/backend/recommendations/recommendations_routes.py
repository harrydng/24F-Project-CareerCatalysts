from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


##### Blueprint ######

recommendations = Blueprint('recommendations', __name__)


#### CRUD OPS ######

# Function to get all skills a student has
@recommendations.route('/skillGet', methods=['POST'])
def get_student_skills():
    # Read the input JSON payload
    the_data = request.json

    # Log the incoming data for debugging purposes
    current_app.logger.info(the_data)

    # Extract the nuId from the payload
    student_id = the_data.get('nuId')

    # Validate the input
    if not student_id:
        return make_response(jsonify({"error": "Student ID (nuId) is required"}), 400)

    # Use parameterized query to avoid SQL injection
    query = f'''
        SELECT s.skillId, s.name, s.description
        FROM student_skills ss
        JOIN skills s ON ss.skillId = s.skillId
        WHERE ss.nuId = {student_id}
    '''

    # Fetch data
    cursor = db.get_db().cursor()
    cursor.execute(query)
    skills_data = cursor.fetchall()

    # Prepare response
    response = make_response(jsonify(skills_data))
    response.status_code = 200
    return response



# Function to delete a skill.
@recommendations.route('/skillRec', methods=['DELETE'])
def delete_student_skill():
    """
    Delete a skill from the student's profile.
    """
    data = request.json
    student_id = data.get('nuId')
    skill_id = data.get('skillId')
    
    query = f'''
        DELETE FROM student_skills
        WHERE nuId = {student_id} AND skillId = {skill_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Skill deleted successfully.")
    response.status_code = 200
    return response


#### FUNCTION TO ADD SKILLS #####
@recommendations.route('/skillAdd', methods=['POST'])
def addSkill():
    """
    Add a new skill or link an existing skill to a student.
    """
    data = request.json
    current_app.logger.info(data)

    nu_id = data.get('nuId')
    skill_name = data.get('name') 
    skill_description = data.get('description')  
    skill_id = data.get('skillId')  

    cursor = db.get_db().cursor()

    # Validate nuId
    check_student_query = f'''
        SELECT *
        FROM student_profile 
        WHERE nuId = {nu_id}
    '''
    cursor.execute(check_student_query)
    is_student = cursor.fetchone()

    if not is_student:
        return make_response(jsonify({
            "error": f"No student found with ID {nu_id}"
        }), 400)

    # Case 1: If skillId is provided, link the existing skill to the student
    if skill_id:
        query_link_skill = f'''
            INSERT INTO student_skills (nuId, skillId)
            VALUES ({nu_id}, {skill_id})
        '''
        cursor.execute(query_link_skill)
        db.get_db().commit()
        return make_response(jsonify({
            "message": "Existing skill linked to student successfully",
            "skillId": skill_id
        }), 201)

    # Case 2: If no skillId, add the skill and then link it
    # Insert the new skill into the skills table
    insert_skill_query = f'''
        INSERT INTO skills (name, description)
        VALUES ("{skill_name}", "{skill_description}")
    '''
    cursor.execute(insert_skill_query)
    db.get_db().commit()
    new_skill_id = cursor.lastrowid

    # Link the newly added skill to the student
    query_link_skill = f'''
        INSERT INTO student_skills (nuId, skillId)
        VALUES ({nu_id}, {new_skill_id})
    '''
    cursor.execute(query_link_skill)
    db.get_db().commit()

    # Return a success response
    return make_response(jsonify({
        "message": "New skill added and linked to student successfully",
        "skillId": new_skill_id
    }), 201)


# Get all details of a student's profile
@recommendations.route('/studentProfile', methods=['POST'])
def student_profile():
    """
    Fetch a student's profile using their nuId.
    """
    # Parse input JSON
    data = request.json
    nu_id = data.get('nuId')  # Safely get the 'nuId' key

    # Validate input
    if not nu_id:
        return make_response(jsonify({"error": "Student ID (nuId) is required"}), 400)

    # Initialize cursor
    cursor = db.get_db().cursor()

    # Query to fetch student details
    query = '''
        SELECT u.userId AS nuId, u.firstName, u.lastName, u.email, sp.major, sp.minor, sp.year, sp.advisorId
        FROM user u
        JOIN student_profile sp ON u.userId = sp.nuId
        WHERE u.userId = %s
    '''
    cursor.execute(query, (nu_id,))
    theData = cursor.fetchone()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response 



# Job recommendations
@recommendations.route('/Recs', methods=['GET'])
def get_job_recommendations():
    """
    Fetch job recommendations based on the student's qualifications (skills).
    """
    student_id = request.args.get('nuId')  # Expecting 'nuId' as a query parameter
    
    query = f'''
        SELECT jp.jobId,
               jp.description,
               jp.pay,
               jp.timePeriod,
               jp.positionType,
               jp.employmentType,
               jp.workLocation,
               COUNT(DISTINCT jps.skillId) AS MatchingSkills,
               jp.createdAt
        FROM job_posting jp
        JOIN job_posting_skills jps ON jp.jobId = jps.jobId
        JOIN student_skills ss ON jps.skillId = ss.skillId
        WHERE ss.nuId = {student_id}
          AND jp.isActive = TRUE
        GROUP BY jp.jobId, jp.description, jp.pay, jp.timePeriod,
                 jp.positionType, jp.employmentType, jp.workLocation, jp.createdAt
        ORDER BY MatchingSkills DESC, jp.createdAt DESC
    '''
    
    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    job_recommendations = cursor.fetchall()
    
    # Prepare response
    response = make_response(jsonify(job_recommendations))
    response.status_code = 200
    return response



# Updating job Opportunities
@recommendations.route('/jobsRec', methods=['PUT'])
def update_job_opportunities():
    """
    Update the job list with new opportunities.
    """
    data = request.json 
    job_id = data.get('jobId')
    description = data.get('description')
    pay = data.get('pay')
    time_period = data.get('timePeriod')
    position_type = data.get('positionType')
    employment_type = data.get('employmentType')
    work_location = data.get('workLocation')
    is_active = data.get('isActive', True)

    query = f'''
        UPDATE job_posting
        SET description = "{description}",
            pay = {pay},
            timePeriod = "{time_period}",
            positionType = "{position_type}",
            employmentType = "{employment_type}",
            workLocation = "{work_location}",
            isActive = {is_active}
        WHERE jobId = {job_id}
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Job opportunities updated successfully.")
    response.status_code = 200
    return response