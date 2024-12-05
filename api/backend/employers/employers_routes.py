from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
employers = Blueprint('employers', __name__)

#------------------------------------------------------------
# GET the if of the employer based on the given name
@employers.route('/employerId', methods=['GET'])
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