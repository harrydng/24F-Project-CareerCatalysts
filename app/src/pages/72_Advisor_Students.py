import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import re

# Set up logging
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Student Progress")
st.header("Select a student to manage")

# Input field for Advisor ID
st.subheader("Enter Advisor ID to view this page as")
advisor_id = st.text_input("Advisor ID (advisorId):", placeholder="Enter the Advisor ID")

# Placeholder for profile details or error messages
profile_placeholder = st.empty()

advisorId = None

# Validate and process the input
if advisor_id:  # Check if input is not empty
    try:
        advisorId = int(advisor_id)  # Try converting to an integer
        trial = requests.get(f"http://api:4000/adv/manages/{advisorId}")
        trial_data = trial.json()
        if trial_data:
                 profile_placeholder.success(f"Fetching profile for Advisor ID: {advisorId}")
        else:
            profile_placeholder.error("Invalid Advisor ID. Please enter a valid numeric ID.")
            advisorId = 0
    except ValueError:
        profile_placeholder.error("Invalid Advisor ID. Please enter a valid numeric ID.")
        advisorId = 0
else:
    profile_placeholder.info("Please enter an Advisor ID to view the profile.")


def fetch_advisor_students(advisorId):
    """
    Fetch all students who an advisor advises.
    """
    if not advisorId:
        return []
    try:
        logger.info(f"Fetching students for advisor ID: {advisorId}")
        response = requests.get(f"http://api:4000/adv/manages/{advisorId}")
        if response.status_code == 200:
            rows = response.json()  # Assuming the response is in JSON format
            options = [
                f"{row['firstName']} {row['middleName']} {row['lastName']} (ID: {row['nuId']})"
                for row in rows
            ]
            return options
        else:
            st.error(f"Error fetching students: {response.text}")
            logger.error(f"Failed to fetch students, status code: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        logger.error(f"RequestException: {str(e)}")
        return []


def fetch_student_notes(selected_nuId):
    """
    Fetch notes for a student using the existing route.
    """
    try:
        response = requests.get(f"http://api:4000/adv/student_reports/notes/{selected_nuId}")
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0].get("notes", "")
            else:
                st.warning("No notes found for this student.")
                return ""
        else:
            st.error(f"Error fetching notes for student {selected_nuId}: {response.text}")
            return ""
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return ""


# Fetch and display the students if advisorId is valid
students = fetch_advisor_students(advisorId) if advisorId else []

# Create a dropdown menu (selectbox) for the students
if students:
    selected_student = st.selectbox("Select a student:", students)

    # Extract nuId from the selected student using regex
    match = re.search(r"\(ID: (\d+)\)", selected_student) if selected_student else None
    selected_nuId = match.group(1) if match else None

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

    # Example usage
    has_notes = check_student_notes(selected_nuId)

    if has_notes:
        st.header(f"Manage Notes for Student ID: {selected_nuId}")

        # Fetch notes for the selected student
        notes = st.text_input("Update Note:", value=fetch_student_notes(selected_nuId))

        # Layout for Update and Delete buttons side by side
        col1, col2 = st.columns([1, 1], gap="small")

        with col1:
            # Update note
            payloadNote = {
                "nuId": selected_nuId,
                "notes": notes,
            }
            if st.button("Update Note"):
                try:
                    response = requests.put(f"http://api:4000/adv/student_reports/notes", json=payloadNote)
                    if response.status_code == 200:
                        st.success("Note updated successfully!")
                    else:
                        st.error(f"Error updating note: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to API: {str(e)}")

        with col2:
            # Delete note
            payloadDelete = {
                "nuId": selected_nuId,
            }
            if st.button("Delete Note"):
                try:
                    response = requests.delete(f"http://api:4000/adv/student_reports/notes", json=payloadDelete)
                    if response.status_code == 200:
                        st.success("Note deleted successfully!")
                    else:
                        st.error(f"Error deleting note: {response.text}")
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

    #Find the status of the student with the given nuId
    def check_student_status(selected_nuId):
            """
            Check if the student with the given nuId has notes using the existing route.
            """
            try:
                response = requests.get(f"http://api:4000/adv/student_reports/status/{selected_nuId}")
                if response.status_code == 200:
                    data = response.json()  # Assuming response is a list of student data
                    # Check if status exist by analyzing the response
                    for record in data:
                        if record.get("status") == 1:  # Check if status = 1
                            return True
                    return False
                else:
                    st.error(f"Error fetching status for student {selected_nuId}: {response.text}")
                    return False
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {str(e)}")
                return False

    # Example usage
    is_status = check_student_status(selected_nuId)

    st.write('')
    # Display the header with a green check mark if the student is ready
    if is_status:
        st.header(f"Student Readiness Status: ✅ Ready")

        #Update Status to not ready
        # JSON payload with multiple fields
        payloadTruth = {
            "nuId": selected_nuId,
            "status": 0
        }
        if st.button("Set Student to Not Ready"):
            try:
                response = requests.put(f"http://api:4000/adv/student_reports/status", json= payloadTruth)
                if response.status_code == 200:
                    st.success("Status updated successfully!")
                else:
                    st.error(f"Error updating status: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {str(e)}")
    else:
        st.header(f"Student Readiness Status: ❌ Not Ready")

        #Update Status to  ready
        # JSON payload with multiple fields
        payloadFalse = {
            "nuId": selected_nuId,
            "status": 1
        }
        if st.button("Set Student to Ready"):
            try:
                response = requests.put(f"http://api:4000/adv/student_reports/status", json= payloadFalse)
                if response.status_code == 200:
                    st.success("Status updated successfully!")
                else:
                    st.error(f"Error updating status: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {str(e)}")



