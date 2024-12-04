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
student_id = st.text_input("Student ID (nuId):", placeholder="Enter your Student ID")

# Button to fetch and view skills
if st.button("Fetch Skills"):
    if student_id.strip():  # Ensure student_id is not empty or just whitespace
        try:
            payload = {"nuId": student_id.strip()}  # Strip whitespace
            response = requests.get(f"http://api:4000/sk/skillRec", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    st.success(f"Skills for Student ID {student_id.strip()}")
                    skills_table = [
                        {"Skill Name": skill["name"], "Description": skill["description"]}
                        for skill in data
                    ]
                    st.table(skills_table)
                else:
                    st.warning("No skills found for the given Student ID.")
            else:
                st.error(f"Error fetching data: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please enter a valid Student ID.")

# Button to navigate back to the home page
if st.button("Go Back to Home"):
    st.experimental_set_query_params()
    st.switch_page("Student_Home_Page")
