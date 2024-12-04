from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
job_postings = Blueprint('job_postings', __name__)

#------------------------------------------------------------
# POST all the job postings based on the company chosen from the database, 
# package them up, and return them to the client
@job_postings.route('/jobPostings', methods=['POST'])
def get_job_postings():
    the_data = request.json
    current_app.logger.info(the_data)
    
    # Extract the company name variable from the JSON body
    companyName = the_data['company_name']
    
    query = f'''
        SELECT jp.position AS 'Position', 
            jp.description AS 'Job Description', 
            jp.createdAt AS 'Created At', 
            jp.updatedAt AS 'Updated At', 
            jp.pay AS 'Pay', 
            jp.timePeriod AS 'Time Period', 
            jp.positionType AS 'Position Type', 
            jp.employmentType AS 'Employment Type', 
            jp.workLocation AS 'Location', 
            u.firstName AS 'Company',
            jp.jobId
        FROM job_posting jp
            JOIN employer_profile ep ON jp.employerId = ep.employerId
            JOIN user u ON ep.employerId = u.userId
        WHERE u.firstName = %s AND jp.isActive = 1;
    '''
    
    current_app.logger.info(query)
    
    cursor = db.get_db().cursor()
    cursor.execute(query, (companyName, ))
    theData = cursor.fetchall()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


# ------------------------------------------------------------
# POST route to add a new job given the datas.
@job_postings.route('/jobPosting', methods=['POST'])
def add_new_job_posting(): 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    position = the_data['position']
    description = the_data['description']
    pay = the_data['pay']
    timePeriod = the_data['time_period']
    positionType = the_data['position_type']
    employmentType = the_data['employment_type']
    workLocation = the_data['work_location']
    employerId = the_data['employer']
    
    query = f'''
        INSERT INTO job_posting (position, description, pay, timePeriod, positionType, employmentType, workLocation, employerId)
            VALUES ('{position}', '{description}', '{pay}', '{timePeriod}', '{positionType}', '{employmentType}', '{workLocation}', '{employerId}');
    '''
 
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added job")
    response.status_code = 200
    return response

# ------------------------------------------------------------
# DELETE route to deactivate a job given the id.
@job_postings.route('/jobPosting/<jobId>', methods=['DELETE'])
def delete_job_posting(jobId):
    query = f'''
        UPDATE job_posting
        SET isActive = 0
        WHERE jobId = {jobId}
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response(f"Job posting with ID {jobId} successfully deleted.")
    response.status_code = 200
    return response


# ------------------------------------------------------------
# PUT route to update a job given the id.
@job_postings.route('/jobPosting/<int:jobId>', methods=['PUT'])
def update_job_posting(jobId):
    the_data = request.json
    current_app.logger.info(the_data)

    # Extract variables to update
    position = the_data.get('position')
    description = the_data.get('description')
    pay = the_data.get('pay')
    timePeriod = the_data.get('time_period')
    positionType = the_data.get('position_type')
    employmentType = the_data.get('employment_type')
    workLocation = the_data.get('work_location')

    query = f'''
        UPDATE job_posting
        SET position = %s, 
            description = %s, 
            pay = %s, 
            timePeriod = %s, 
            positionType = %s
            employmentType = %s, 
            workLocation = %s
        WHERE jobId = %s
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query, (position, description, pay, timePeriod, positionType, employmentType, workLocation, jobId))
    db.get_db().commit()
    
    response = make_response(f"Job posting with ID {jobId} successfully updated.")
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Get all Job Types
@job_postings.route('/jobTypes', methods = ['GET'])
def get_job_type():
    query = '''
        SELECT DISTINCT jp.positionType AS 'Position Type',
            jp.employmentType AS 'Employment Type',
            jp.workLocation AS 'Work Location'
        FROM job_posting jp
        WHERE positionType IS NOT NULL
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
        
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
