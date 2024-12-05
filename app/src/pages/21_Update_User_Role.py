import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Include the sidebar links
SideBarLinks()

st.title('Update User Role')

st.write('\n\n')

# Function to update user role
def update_user_role(userId, roleId):
    try:
        payload = {"userId": userId, "roleId": roleId}
        logger.info(f"Updating user role with payload: {payload}")
        
        # API request to update the user role
        response = requests.put('http://api:4000/system/update_user_role', json=payload)

        if response.status_code == 200:
            data = response.json()
            st.success(data.get('message', 'User role updated successfully'))
        else:
            st.error(f"Error updating user role: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

# Create a form to input userId and new roleId
with st.form("update_user_role_form"):
    userId = st.number_input(
        "Enter User ID:",
        min_value=1,
        step=1
    )
    new_roleId = st.number_input(
        "Enter New Role ID:",
        min_value=1,
        step=1
    )
    submit_button = st.form_submit_button("Update Role")

# When the form is submitted
if submit_button:
    update_user_role(userId, new_roleId)
