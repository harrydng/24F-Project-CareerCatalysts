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
if st.button("View Skills", 
             type='primary',
             use_container_width=True):
    st.switch_page("pages/74_View_skills.py")

# Button to add or link skills
if st.button("Add Skills", 
             type='primary',
             use_container_width=True):
    st.switch_page("pages/76_Add_skills.py")

# Button to view job recommendations
if st.button("View Job Recommendations", 
             type='primary',
             use_container_width=True):
    st.switch_page("pages/78_Job_recommendations.py")

# Button to view personal details
if st.button("View Profiles", 
             type='primary',
             use_container_width=True):
    st.switch_page("pages/77_View_User_Details.py")

# Button to view the leaderboard
if st.button("View Leaderboard", 
             type='primary',
             use_container_width=True):
    st.switch_page("pages/62_Leaderboard.py")
