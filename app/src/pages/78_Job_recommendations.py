import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# Set up the Streamlit page
st.set_page_config(
    page_title="Job Recommendations",
    layout="wide"
)

SideBarLinks()

# Header
st.title("Job Recommendations")

# Input for Student ID
st.subheader("Enter your Student ID to fetch job recommendations")
student_id = st.text_input(
    "Student ID (nuId):", 
    placeholder="Enter your Student ID"
)

# Placeholder for the job recommendations table
jobs_placeholder = st.empty()

# Function to fetch and display job recommendations
def fetch_and_display_jobs(student_id):
    try:
        # Payload with the student ID
        payload = {"nuId": student_id}
        logger.info(f"Fetching job recommendations for Student ID: {student_id}")

        # API request
        response = requests.get(
            'http://api:4000/jr/Recs', 
            params={"nuId": student_id}
        )

        if response.status_code == 200:
            data = response.json()
            if data:
                st.success(f"Job Recommendations for Student ID {student_id}")
                # Prepare and display the jobs table
                jobs_table = [
                    {
                        "Job ID": job["jobId"],
                        "Description": job["description"],
                        "Pay": job["pay"],
                        "Time Period": job["timePeriod"],
                        "Position Type": job["positionType"],
                        "Employment Type": job["employmentType"],
                        "Work Location": job["workLocation"],
                        "Matching Skills": job["MatchingSkills"],
                        "Posted At": job["createdAt"],
                    }
                    for job in data
                ]
                jobs_placeholder.table(jobs_table)
            else:
                st.warning("No job recommendations found for the given Student ID.")
        else:
            st.error(f"Error fetching job recommendations: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

# Fetch and display jobs when the button is clicked
if st.button("Fetch Job Recommendations"):
    if student_id.strip():  # Ensure the input is not empty
        fetch_and_display_jobs(student_id.strip())
    else:
        st.warning("Please enter a valid Student ID.")
