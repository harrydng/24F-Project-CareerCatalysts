import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import re

# Set up logging
logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title("Student Progress")
st.header("Select a student to manage")

advisorId = 45

def fetch_advisor_students(advisorId):
    """
    Fetch all students who an advisor advises
    """
    try:
        logger.info(f"Fetching students for advisor ID: {advisorId}")
        
        # Corrected URL construction
        response = requests.get(f"http://api:4000/adv/manages/{advisorId}")
        
        if response.status_code == 200:
            rows = response.json()  # Assuming the response is in JSON format
            options = [
                f"{row['firstName']} {row['middleName']} {row['lastName']} (ID: {row['nuId']})"
                for row in rows
            ]  # Create a display string for each student
            return options
        else:
            st.error(f"Error fetching students: {response.text}")
            logger.error(f"Failed to fetch students, status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        logger.error(f"RequestException: {str(e)}")
        return []

# Fetch and display the students
students = fetch_advisor_students(advisorId)

# Create a dropdown menu (selectbox) for the students
selected_student = st.selectbox("Select a student:", students)




# Extract nuId from the selected student using regex
if selected_student:
    match = re.search(r"\(ID: (\d+)\)", selected_student)
    if match:
        selected_nuId = match.group(1)  # Extract the first capturing group

        def check_student_notes(selected_nuId):
            """
            Check if the student with the given nuId has notes using the existing route.
            """
            try:
                response = requests.get(f"http://api:4000/adv/student_reports/notes/{selected_nuId}")
                if response.status_code == 200:
                    data = response.json()  # Assuming response is a list of student data
                    # Check if notes exist by analyzing the response
                    for record in data:
                        if record.get("notes"):  # Check if 'notes' key exists and is not empty/None
                            return True
                    return False
                else:
                    st.error(f"Error fetching notes for student {selected_nuId}: {response.text}")
                    return False
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {str(e)}")
                return False
            
        #fetches the student note    
        def fetch_student_notes(selected_nuId):
            """
            Check if the student with the given nuId has notes using the existing route.
            """
            try:
                response = requests.get(f"http://api:4000/adv/student_reports/notes/{selected_nuId}")
                if response.status_code == 200:
                    data = response.json()  # Assuming response is a list of student data
                    # Check if notes exist by analyzing the response
                    return data[0]["notes"]
                else:
                    st.error(f"Error fetching notes for student {selected_nuId}: {response.text}")
                    return False
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {str(e)}")
                return False

        # Example usage
        has_notes = check_student_notes(selected_nuId)

        if has_notes:
            st.header(f"Notes")

            #Update notes section
            notes = st.text_input("Update Note: ", value = fetch_student_notes(selected_nuId))

            #Update note
            # JSON payload with multiple fields
            payloadNote = {
                "nuId": selected_nuId,
                "notes": notes,
            }

            if st.button("Update Note"):
                try:
                    response = requests.put(f"http://api:4000/adv/student_reports/notes", json= payloadNote)
                    if response.status_code == 200:
                        st.success("Note updated successfully!")
                    else:
                        st.error(f"Error updating name: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to API: {str(e)}")

            #Deleted note
            # JSON payload with multiple fields
            payloadDelete = {
                "nuId": selected_nuId,
            }

            if st.button("Delete Note"):
                try:
                    response = requests.delete(f"http://api:4000/adv/student_reports/notes", json= payloadDelete)
                    if response.status_code == 200:
                        st.success("Note deleted successfully!")
                    else:
                        st.error(f"Error updating name: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to API: {str(e)}")

        else:
            #Add note section section
            notes = st.text_input("Add Note", value="")

            #Add a new note
            # JSON payload with multiple fields
            payloadDashboard = {
                "nuId": selected_nuId,
                "advisorId": advisorId,
                "notes": notes,
                "status": 0
            }

            if st.button("Add Note"):
                try:
                    response = requests.post(f"http://api:4000/adv/student_reports", json= payloadDashboard)
                    if response.status_code == 200:
                        st.success("Note updated successfully!")
                    else:
                        st.error(f"Error updating name: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to API: {str(e)}")


    else:
        st.error("Unable to extract nuId from the selected student.")

        
