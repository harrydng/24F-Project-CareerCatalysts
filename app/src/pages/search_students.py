import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Sidebar navigation
SideBarLinks()

# Page Title
st.title('Search for Students')
st.write('\n\n')

# Form for filtering students
with st.form("filter_students_form"):
    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        dob = st.text_input("Date of Birth (MM/DD/YYYY)", placeholder="MM/DD/YYYY")
        major = st.text_input("Major")

    with col2:
        minor = st.text_input("Minor")
        year = st.text_input("Year")
        advisor = st.text_input("Advisor")
        email = st.text_input("Email")

    skills = st.text_input("Skills (comma-separated)")
    courses = st.text_input("Courses (comma-separated)")


    submit_button = st.form_submit_button("Search")
if submit_button:
    # Prepare filters
    filters = {
        "first_name": first_name,
        "last_name": last_name,
        "dob": dob,
        "major": major,
        "minor": minor,
        "year": year,
        "advisor": advisor,
        "email": email,
        "skills": [skill.strip() for skill in skills.split(",") if skill],
        "courses": [course.strip() for course in courses.split(",") if course]
    }
    
    try:
        # Send request to Flask backend
        response = requests.post("http://127.0.0.1:5000/filterStudents", json=filters)
        if response.status_code == 200:
            students = response.json()
            st.success("Students found:")
            st.write(students)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    
    