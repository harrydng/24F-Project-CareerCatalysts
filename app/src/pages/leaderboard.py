import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title('Student Leaderboard')

st.write('\n\n')

# Default limit
limit_default = 10

# Placeholder for the table
table_placeholder = st.empty()

# Function to fetch and display students
def fetch_and_display_students(limit):
    try:
        # Payload with the limit
        payload = {"limit": limit}
        logger.info(f"Fetching top students with payload: {payload}")
        
        # API request
        response = requests.post('http://api:4000/s/top_students', json=payload)

        if response.status_code == 200:
            students_data = response.json()
            if students_data:
                # Rearrange data for display
                reordered_data = [
                    {
                        'Student ID': student['Student ID'],
                        'Total Courses': student['Total Courses'],
                        'Total Skills': student['Total Skills'],
                        'Total Score': student['Total Score'],
                    }
                    for student in students_data
                ]
                # Update the placeholder with the new table
                table_placeholder.table(reordered_data)
            else:
                st.warning("No students found!")
        else:
            st.error(f"Error fetching students: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

# Fetch and display default top 10 students on page load
fetch_and_display_students(limit_default)

# Create a form to allow limit change
with st.form("top_students_form"):
    limit = st.number_input(
        "Enter the number of top students to display:",
        min_value=1,
        value=limit_default,
        step=1
    )
    submit_button = st.form_submit_button("Fetch Students")

# Fetch and update table based on user input
if submit_button:
    fetch_and_display_students(limit)