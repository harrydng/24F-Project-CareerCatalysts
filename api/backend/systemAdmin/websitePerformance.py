from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Create a new Blueprint for system-related routes
system = Blueprint('system', __name__)

#------------------------------------------------------------
# GET all the metrics and possible alerts from the website
@system.route('/metrics_and_alerts', methods=['GET'])
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
@system.route('/update_user_role', methods=['PUT'])
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