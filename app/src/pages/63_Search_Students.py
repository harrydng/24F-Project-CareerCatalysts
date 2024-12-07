import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Sidebar navigation
SideBarLinks()

def filter(data):
    try:
        # Send request to Flask backend
        payload = {"data" : data}
        response = requests.post("http://api:4000/e/filterStudents", json=payload)
        if response.status_code == 200:
            students = response.json()
            st.success("Students found:")

            # Loop through each student and display their information in a collapsible box
            for student in students:
                with st.expander(f"Student: {student.get('FullName')}"):
                    st.write(f"**NuId:** {student.get('StudentID')}")
                    st.write(f"**Major:** {student.get('Major')}")
                    st.write(f"**Minor:** {student.get('Minor')}")
                    st.write(f"**Year:** {student.get('Year')}")
                    st.write(f"**Email:** {student.get('Email')}")
                    st.write(f"**Skills:** {student.get('Skills')}")
                    st.write(f"**Courses:** {student.get('Courses')}")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}") 

# Page Title
st.title('Search for Students')
st.write('\n\n')

# Form for filtering students
with st.form("filter_students_form"):
    col1, col2 = st.columns(2)  # Create two columns

    with col1:
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        major = st.text_input("Major")
        nuId = st.text_input("nuId")

    with col2:
        minor = st.text_input("Minor")
        year = st.text_input("Year")
        email = st.text_input("Email")

    skills = st.text_input("Skills (comma-separated)")
    courses = st.text_input("Courses (comma-separated)")

    submit_button = st.form_submit_button("Search")

if submit_button:
    # Prepare filters
    filters = {
        "first_name": first_name,
        "nu_id": nuId,
        "last_name": last_name,
        "major": major,
        "minor": minor,
        "year": year,
        "email": email,
        "skills": [skill.strip() for skill in skills.split(",") if skill],
        "courses": [course.strip() for course in courses.split(",") if course]
    }
    logger.info(f"{filters}")
    filter(filters)