import streamlit as st
from modules.nav import SideBarLinks

# Set page configuration (must be the first Streamlit command)
st.set_page_config(layout='wide')

# Show appropriate sidebar links
SideBarLinks()

# Header
st.title(f"Welcome Student, {st.session_state['first_name']}.")
st.write("### What would you like to do today?")

# Button to fetch and view skills
if st.button("View My Skills and Courses"):
    st.switch_page("View_Skills_and_Courses")

# Button to add or link skills
if st.button("Add/Link Skills"):
    st.switch_page("Add_Skills_Page")

# Button to view job recommendations
if st.button("View Job Recommendations"):
    st.switch_page("View_Job_Recommendations")

# Button to update job opportunities
if st.button("Update Job Opportunities"):
    st.switch_page("Update_Job_Opportunities")

# Button to view personal details
if st.button("View My Profile"):
    st.switch_page("View_User_Details")

# Button to view the leaderboard
if st.button("View Leaderboard"):
    st.switch_page("View_Leaderboard")

# Button to view and manage the dashboard
if st.button("View Dashboard"):
    st.switch_page("View_Dashboard")