from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


##### Blueprint ######

job_recommendations = Blueprint('jobRec', __name__)


#### CRUD OPS ######

# Job recommendations
@job_recommendations.route('/Recs', methods=['GET'])
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
@job_recommendations.route('/jobsRec', methods=['PUT'])
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


