from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
advisors = Blueprint('advisors', __name__)

#------------------------------------------------------------
# Get a all the advisor information of the advisor with the advisorId
@advisors.route('/info/<advisorId>', methods=['GET'])
def get_advisor_info(advisorId):

    current_app.logger.info('GET /info/<advisorId> route')
    cursor = db.get_db().cursor()
    cursor.execute(f'''SELECT user.username, user.email, user.firstName, user.middleName, user.lastName
                      FROM user
                      JOIN advisor_profile ON advisor_profile.advisorId = user.userId
                      WHERE advisor_profile.advisorId = {advisorId}''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Update username for advisor with specific advisorId
@advisors.route('/updateUsername/<advisorId>', methods=['PUT'])

def update_advisor_username(advisorId):
    current_app.logger.info('PUT /updateUsername/<advisorId>')
    username_info = request.json
    username = username_info['username']
    #userId = username_info['advisorId']

    query = f"UPDATE user SET username = '{username}' WHERE userId = {advisorId}"

    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()
    return 'Username updated!'

#------------------------------------------------------------
# Update email for advisor with specific advisorId
@advisors.route('/updateEmail/<advisorId>', methods=['PUT'])

def update_advisor_email(advisorId):
    current_app.logger.info('PUT /updateEmail/<advisorId>')
    email_info = request.json
    email = email_info['email']

    query = f"UPDATE user SET email = '{email}' WHERE userId = {advisorId}"

    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()
    return 'Email updated!'

#------------------------------------------------------------
# Update first name for advisor with specific advisorId
@advisors.route('/updateFirstName/<advisorId>', methods=['PUT'])

def update_advisor_firstName(advisorId):
    current_app.logger.info('PUT /updateName/<advisorId>')
    name_info = request.json
    firstName = name_info['firstName']

    query = f"UPDATE user SET firstName = '{firstName}' WHERE userId = {advisorId}"

    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()
    return 'Name updated!'

#------------------------------------------------------------
# Update middle name for advisor with specific advisorId
@advisors.route('/updateMiddleName/<advisorId>', methods=['PUT'])

def update_advisor_middleName(advisorId):
    current_app.logger.info('PUT /updateMiddleName/<advisorId>')
    name_info = request.json
    middleName = name_info['middleName']

    query = f"UPDATE user SET firstName = '{middleName}' WHERE userId = {advisorId}"

    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()
    return 'Name updated!'

#------------------------------------------------------------
# Update last name for advisor with specific advisorId
@advisors.route('/updateLastName/<advisorId>', methods=['PUT'])

def update_advisor_lastName(advisorId):
    current_app.logger.info('PUT /updateLastName/<advisorId>')
    name_info = request.json
    lastName = name_info['lastName']

    query = f"UPDATE user SET firstName = '{lastName}' WHERE userId = {advisorId}"

    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()
    return 'Name updated!'

#------------------------------------------------------------
# Get a all students which the advisor with the given Id manages
@advisors.route('/manages/<advisorId>', methods=['GET'])
def get_all_advised_student(advisorId):

    current_app.logger.info('GET /manages/<advisorId> route')
    cursor = db.get_db().cursor()
    cursor.execute(f'''SELECT user.firstName, user.middleName, user.lastName, student_profile.nuId
                       FROM user
                       JOIN student_profile ON student_profile.nuId = user.userId
                       JOIN advisor_profile ON advisor_profile.advisorId = student_profile.advisorId
                       WHERE advisor_profile.advisorId = {advisorId}''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get a student report for a student from the system
@advisors.route('/student_reports/<nuId>', methods=['GET'])
def get_reports(nuId):

    current_app.logger.info('GET /student_reports/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute(f'''SELECT student_reports.notes, student_reports.status, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM user
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN student_reports ON student_profile.nuId = student_reports.nuId
                      WHERE student_profile.nuId = {nuId}''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get notes on a student for a student from the system
@advisors.route('/student_reports/notes/<nuId>', methods=['GET'])
def get_reports_notes(nuId):

    current_app.logger.info('GET /student_reports/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT student_reports.notes 
                      FROM user
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN student_reports ON student_profile.nuId = student_reports.nuId
                      WHERE student_profile.nuId = %s''', (nuId))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get a student's advising status for a student from the system
@advisors.route('/student_reports/status/<nuId>', methods=['GET'])
def get_reports_status(nuId):

    current_app.logger.info('GET /student_reports/status/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT student_reports.status 
                      FROM user
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN student_reports ON student_profile.nuId = student_reports.nuId
                      WHERE student_profile.nuId = %s''', (nuId))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a student to the dashboard or create a new dashboard
@advisors.route('/student_reports', methods=['POST'])
def post_reports():
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting variables
    nuId = the_data['nuId']
    advisorId = the_data['advisorId']
    notes = the_data['notes']
    status = the_data['status']

    # Use parameterized query
    query = '''INSERT INTO student_reports (nuId, advisorId, notes, status)
               VALUES (%s, %s, %s, %s)'''
    values = (nuId, advisorId, notes, status)

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, values)
        db.get_db().commit()
        current_app.logger.info("Inserted into student_reports successfully.")
        return make_response("Successfully added new student to dashboard", 200)
    except Exception as e:
        current_app.logger.error(f"Error inserting into student_reports: {e}")
        return make_response(str(e), 400)

#------------------------------------------------------------
# Update notes info for student with particular nuId
@advisors.route('/student_reports/notes', methods=['PUT'])

def update_notes():
    current_app.logger.info('PUT /student_reports route')
    notes_info = request.json
    notes = notes_info['notes']
    nuId = notes_info['nuId']


    query = f"UPDATE student_reports SET notes = '{notes}' WHERE nuId = {nuId}"

    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()
    return 'Advising notes updated!'

#------------------------------------------------------------
# Delete the notes for student with particular nuId
@advisors.route('/student_reports/notes', methods=['DELETE'])

def delete_notes():
    current_app.logger.info('PUT /student_reports route')
    notes_info = request.json
  
    nuId = notes_info['nuId']


    query = f"UPDATE student_reports SET notes = NULL where nuId = {nuId}"

    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()
    return 'Advising notes deleted!'

#------------------------------------------------------------
# Update the advising status for student with particular nuId
@advisors.route('/student_reports/status', methods=['PUT'])

def update_advising_status():
    current_app.logger.info('PUT /student_reports route')
    status_info = request.json
    status = status_info['status']
    nuId = status_info['nuId']


    query = f'UPDATE student_reports SET status = {status} where nuId = {nuId}'

    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()
    return 'Advising status updated!'

#------------------------------------------------------------
# Delete the advising status for student with particular nuId
@advisors.route('/student_reports/status', methods=['DELETE'])

def delete_advising_status():
    current_app.logger.info('PUT /student_reports route')
    status_info = request.json
    nuId = status_info['nuId']

    query = f'UPDATE student_reports SET status = null where nuId = {nuId}'
    cursor = db.get_db().cursor()
    r = cursor.execute(query)
    db.get_db().commit()
    return 'Advising status set to none!'

#------------------------------------------------------------
# Get all the jobs the student with the given nuId applied to
@advisors.route('/student_profile/applied/<nuId>', methods=['GET'])
def get_student_applied(nuId):

    current_app.logger.info('GET /student_profile/applied/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute(f'''SELECT job_posting.position, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM user
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN job_applications ON job_applications.nuId = student_profile.nuId
                      JOIN job_posting ON job_posting.jobId = job_applications.jobId
                      WHERE student_profile.nuId = {nuId}''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all the jobs the student with the given nuId has worked at
@advisors.route('/student_profile/jobs/<nuId>', methods=['GET'])
def get_student_jobs(nuId):

    current_app.logger.info('GET /student_profile/worked/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute(f'''SELECT job_posting.position, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM user
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN job_students ON job_students.nuId = student_profile.nuId
                      JOIN job_posting ON job_posting.jobId = job_students.jobId
                      WHERE student_profile.nuId = {nuId}''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all the students which have worked at the job at the job with the given jobId
@advisors.route('/job_posting/students/<jobId>', methods=['GET'])
def get_job_students(jobId):

    current_app.logger.info('GET /student_profile/worked/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute(f'''SELECT job_posting.position, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM user
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN job_students ON job_students.nuId = student_profile.nuId
                      JOIN job_posting ON job_posting.jobId = job_students.jobId
                      WHERE job_posting.jobId = {jobId}''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get all the students which have applied to the job at the job with the given jobId
@advisors.route('/job_posting/applicants/<jobId>', methods=['GET'])
def get_job_applicants(jobId):

    current_app.logger.info('GET /student_profile/worked/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT job_posting.position, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM users
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN job_applications ON job_application.nuId = student_profile.nuId
                      JOIN job_posting ON job_posting.jobId = job_applications.jobId
                      WHERE job_applications.jobId = %s''', (jobId,))
    
#     theData = cursor.fetchall()
    
#     the_response = make_response(jsonify(theData))
#     the_response.status_code = 200
#     return the_response

#------------------------------------------------------------
# Get all the qualifiications the student with the given nuId has
@advisors.route('/qualifications/<nuId>', methods=['GET'])
def get_student_qualifications(nuId):

    current_app.logger.info('GET /student_profile/applied/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute(f'''SELECT job_posting.description, courses.courseName, courses.description, 
                             courses.courseNumber, certifications.name, projects.description, 
                             projects.name, skills.name, skills.description, user.firstName, 
                             user.middleName, user.lastName, student_profile.nuId
                      FROM user
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN job_applications ON job_applications.nuId = student_profile.nuId
                      JOIN job_posting ON job_posting.jobId = job_applications.jobId
                      NATURAL JOIN student_projects
                      NATURAL JOIN projects
                      NATURAL JOIN student_certifications
                      NATURAL JOIN certifications
                      JOIN student_courses ON student_courses.nuId = student_profile.nuId
                      JOIN courses ON student_courses.courseId = courses.courseId
                      JOIN student_skills ON student_skills.nuId = student_profile.nuId
                      JOIN skills ON student_skills.skillId = skills.skillId
                      WHERE student_profile.nuId = {nuId}''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


