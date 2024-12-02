from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
courses = Blueprint('products', __name__)

#------------------------------------------------------------
# GET all the courses from the database, 
# package them up, and return them to the client
@courses.route('/jobPostings', methods=['GET'])
def get_courses():
    query = '''
        SELECT DISTINCT courseName FROM courses
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    response = make_response(jsonify(the_data))
    response.response_code = 200
    return response