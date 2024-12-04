from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

##### Blueprint ######
users = Blueprint('user', __name__)

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