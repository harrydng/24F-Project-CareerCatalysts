import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# Set up the Streamlit page
st.set_page_config(
    page_title="View Student Profile",
    layout="wide"
)

SideBarLinks()

# Header
st.title("View Student Profile")

# Input field for Student ID
st.subheader("Enter Student ID to view the profile")
student_id = st.text_input("Student ID (nuId):", placeholder="Enter the Student ID")

# Placeholder for profile details or error messages
profile_placeholder = st.empty()

# Function to fetch and display student profile
def fetch_student_profile(student_id):
    try:
        # Payload with the student ID
        payload = {"nuId": student_id}

        logger.info(f"Fetching student profile with payload: {payload}")

        # API request
        response = requests.post('http://api:4000/sk/studentProfile', json=payload)

        if response.status_code == 200:
            data = response.json()
            if data:
                st.success(f"Profile for Student ID {student_id}")
                
                # Display student profile details in a table format
                profile_details = {
                    "NUID": data.get("nuId"),
                    "First Name": data.get("firstName"),
                    "Last Name": data.get("lastName"),
                    "Email": data.get("email"),
                    "Major": data.get("major"),
                    "Minor": data.get("minor"),
                    "Year": data.get("year"),
                    "Advisor ID": data.get("advisorId")
                }

                # Display profile details
                profile_placeholder.table(profile_details.items())
            else:
                st.warning("No profile found for the given Student ID.")
        elif response.status_code == 400:
            data = response.json()
            st.warning(data.get("error", "Invalid Student ID."))
        else:
            st.error(f"Error fetching student profile: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")


# Button to fetch and display student profile
if st.button("Fetch Profile"):
    if student_id.strip():  # Ensure the input is not empty
        fetch_student_profile(student_id.strip())
    else:
        st.warning("Please enter a valid Student ID.")

# Button to navigate back to the home page
if st.button("Go Back to Home"):
    st.experimental_set_query_params()
    st.switch_page("Student_Home_Page")
