import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title('Student Leaderboard')

st.write('\n\n')


# Fetch the top students data
try:
    # Set default limit
    limit_default = 100

    # Create a form to input limit
    with st.form("top_students_form"):
        limit = st.number_input("Enter the number of top students to display:", min_value=1, value=limit_default)
        submit_button = st.form_submit_button("Fetch Students")
    
    if submit_button:
        # Send POST request to fetch students
        payload = {"limit": limit}
        logger.info(f"Fetching top students with payload: {payload}")
        
        response = requests.post('http://api:4000/s/top_students', json=payload)
        
        if response.status_code == 200:
            students_data = response.json()
            if students_data:
                st.success("Top students fetched successfully!")
                st.write(students_data)
            else:
                st.warning("No students found!")
        else:
            st.error(f"Error fetching students: {response.text}")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to API: {str(e)}")