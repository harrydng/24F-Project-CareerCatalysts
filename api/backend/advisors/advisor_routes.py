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
# Get a all students which the advisor with the given Id manages
@advisors.route('/manages/<advisorId>', methods=['GET'])
def get_all_advised_student(advisorId):

    current_app.logger.info('GET /manages/<advisorId> route')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM users
                      JOIN advisor_profile ON advisor_profile.advisorId = user.userIdd
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN student_reports ON student_profile.nuId = student_reports.nuId
                      WHERE advisor_profile.advisorId = %s''', (advisorId,))
    
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
    cursor.execute('''SELECT student_reports.notes, student_reports.status, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM users
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN student_reports ON student_profile.nuId = student_reports.nuId
                      WHERE student_profile.nuId = %s''', (nuId,))
    
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
    cursor.execute('''SELECT student_reports.status, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM users
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN student_reports ON student_profile.nuId = student_reports.nuId
                      WHERE student_profile.nuId = %s''', (nuId,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get a student's advising status for a student from the system
@advisors.route('/student_reports/status/<nuId>', methods=['GET'])
def get_reports_status(nuId):

    current_app.logger.info('GET /student_reports/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT student_reports.notes, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM users
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN student_reports ON student_profile.nuId = student_reports.nuId
                      WHERE student_profile.nuId = %s''', (nuId,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a student to the dashboard or create a new dashboard
@advisors.route('/student_reports', methods=['POST'])
def post_reports():

    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    nuId = the_data['nuId']
    advisorId = the_data['advisorId']
    notes = the_data['notes']
    status = the_data['status']

    cursor = db.get_db().cursor()
    cursor.execute('''INSERT INTO student_reports (nuId, advisorId, notes, status)
                          VALUES (%s, %s, %s, %s)''', (nuId, advisorId, notes, status))
    
    current_app.logger.info("Inserting into student_reports")
    cursor = db.get_db().cursor()
    #cursor.execute(query)
    db.get_db().commit()
    
    the_response = make_response("Successfully added new student to dashboard")
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Update notes info for student with particular nuId
@advisors.route('/student_reports/notes', methods=['PUT'])

def update_notes():
    current_app.logger.info('PUT /student_reports route')
    notes_info = request.json
    notes = notes_info['note']
    nuId = notes_info['nuId']


    query = 'UPDATE student_reports SET notes = %s WHERE nuId = %s'
    data = (notes, nuId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Advising notes updated!'

#------------------------------------------------------------
# Delete the notes for student with particular nuId
@advisors.route('/student_reports/notes', methods=['DELETE'])

def delete_notes():
    current_app.logger.info('PUT /student_reports route')
    notes_info = request.json
  
    nuId = notes_info['nuId']


    query = 'UPDATE student_reports SET notes = '' where nuId = %s'
    data = (nuId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Advising notes updated!'

#------------------------------------------------------------
# Update the advising status for student with particular nuId
@advisors.route('/student_reports/status', methods=['PUT'])

def update_advising_status():
    current_app.logger.info('PUT /student_reports route')
    status_info = request.json
    status = status_info['status']
    nuId = status_info['nuId']


    query = 'UPDATE student_reports SET notes = %s where nuId = %s'
    data = (status, nuId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Advising status updated!'

#------------------------------------------------------------
# Delete the advising status for student with particular nuId
@advisors.route('/student_reports/status', methods=['DELETE'])

def delete_advising_status():
    current_app.logger.info('PUT /student_reports route')
    status_info = request.json
    nuId = status_info['nuId']

    query = 'UPDATE student_reports SET status = null where nuId = %s'
    data = (nuId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'Advising status set to none!'

#------------------------------------------------------------
# Get all the jobs the student with the given nuId applied to
@advisors.route('/student_profile/applied/<nuId>', methods=['GET'])
def get_student_applied(nuId):

    current_app.logger.info('GET /student_profile/applied/<nuId> route')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT job_posting.position, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM users
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN job_applications ON job_applications.nuId = student_profile.nuId
                      JOIN job_posting ON job_posting.jobId = job_applications.jobId
                      WHERE student_profile.nuId = %s''', (nuId,))
    
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
    cursor.execute('''SELECT job_posting.position, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM users
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN job_students ON job_student.nuId = student_profile.nuId
                      JOIN job_posting ON job_posting.jobId = job_student.jobId
                      WHERE student_profile.nuId = %s''', (nuId,))
    
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
    cursor.execute('''SELECT job_posting.position, user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM users
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN job_students ON job_student.nuId = student_profile.nuId
                      JOIN job_posting ON job_posting.jobId = job_student.jobId
                      WHERE job_posting.jobId = %s''', (jobId,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# #------------------------------------------------------------
# # Get all the students which have applied to the job at the job with the given jobId
# @advisors.route('/job_posting/applicants/<jobId>', methods=['GET'])
# def get_job_students(jobId):

#     current_app.logger.info('GET /student_profile/worked/<nuId> route')
#     cursor = db.get_db().cursor()
#     cursor.execute('''SELECT job_posting.position, user.firstName, user.middleName, user.lastName, student_profile.nuId 
#                       FROM users
#                       JOIN student_profile ON student_profile.nuId = user.userId
#                       JOIN job_applications ON job_application.nuId = student_profile.nuId
#                       JOIN job_posting ON job_posting.jobId = job_applications.jobId
#                       WHERE job_applications.jobId = %s''', (jobId,))
    
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
    cursor.execute('''SELECT job_posting.description, courses.courseName, courses.description, 
                             courses.courseNumber, certifications.name, projects.description, 
                             projects.name, skills.name, skills.description, user.firstName, 
                             user.middleName, user.lastName, student_profile.nuId
                      FROM users
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
                      WHERE student_profile.nuId = %s''', (nuId,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


