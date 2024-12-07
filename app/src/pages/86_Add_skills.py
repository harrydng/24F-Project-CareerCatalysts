import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# Set up the Streamlit page
st.set_page_config(
    page_title="Add Skills",
    layout="wide"
)

SideBarLinks()

# Header
st.title("Add a Skill to Your Profile")

# Input fields for adding skills
st.subheader("Enter details to add a skill")
student_id = st.text_input("Student ID (nuId):", placeholder="Enter your Student ID")
skill_name = st.text_input("Skill Name:", placeholder="Enter the skill name")
description = st.text_area("Description:", placeholder="Enter a brief description of the skill")

# Placeholder for success or error messages
message_placeholder = st.empty()

# Function to add a skill
def add_skill(student_id, skill_name, description):
    try:
        # Payload with the skill data
        payload = {
            "nuId": student_id,
            "name": skill_name,
            "description": description
        }

        logger.info(f"Adding skill with payload: {payload}")

        # API request
        response = requests.post('http://api:4000/r/skillAdd', json=payload)

        if response.status_code == 201:
            data = response.json()
            message_placeholder.success(data.get("message", f"Skill '{skill_name}' added successfully for Student ID {student_id}."))
        elif response.status_code == 400:
            data = response.json()
            st.warning(data.get("error", "Invalid student ID."))
        else:
            st.error(f"Error adding skill: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")


# Button to add skill
if st.button("Add Skill"):
    if student_id.strip() and skill_name.strip() and description.strip():
        add_skill(student_id.strip(), skill_name.strip(), description.strip())
    else:
        st.warning("Please fill out all fields before adding a skill.")
