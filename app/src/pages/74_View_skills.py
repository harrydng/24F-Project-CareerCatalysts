import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks


# Set up the Streamlit page
st.set_page_config(
    page_title="View Skills",
    layout="wide"
)

SideBarLinks()

# Header
st.title("View Your Skills")

# Input for Student ID
st.subheader("Enter your Student ID to fetch your skills")
student_id = st.text_input(
    "Student ID (nuId):", 
    placeholder="Enter your Student ID"
)

# Placeholder for the skills table
skills_placeholder = st.empty()

# Function to fetch and display skills
def fetch_and_display_skills(student_id):
    try:
        # Payload with the student ID
        payload = {"nuId": student_id}
        logger.info(f"Fetching skills with payload: {payload}")

        # API request
        response = requests.post('http://api:4000/sk/skillGet', json=payload)

        if response.status_code == 200:
            data = response.json()
            if data:
                st.success(f"Skills for Student ID {student_id}")
                # Prepare and display the skills table
                skills_table = [
                    {"Skill Name": skill["name"], "Description": skill["description"]}
                    for skill in data
                ]
                skills_placeholder.table(skills_table)
            else:
                st.warning("No skills found for the given Student ID.")
        else:
            st.error(f"Error fetching skills: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Fetch and display skills when the button is clicked
if st.button("Fetch Skills"):
    if student_id.strip():  # Ensure the input is not empty
        fetch_and_display_skills(student_id.strip())
    else:
        st.warning("Please enter a valid Student ID.")

# Button to navigate back to the home page
if st.button("Go Back to Home"):
    st.experimental_set_query_params()
    st.switch_page("Student_Home_Page")
