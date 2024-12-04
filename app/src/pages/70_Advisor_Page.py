import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}.")

# Use session state to track button clicks
if "button_clicked" not in st.session_state:
    st.session_state["button_clicked"] = None

# Buttons
if st.button("View Your profile", type='primary', use_container_width=True):
    st.session_state["button_clicked"] = "profile"

if st.button("View Students", type='primary', use_container_width=True):
    st.session_state["button_clicked"] = "students"

# Handle navigation based on the clicked button
if st.session_state["button_clicked"] == "profile":
    st.switch_page('pages/71_Advisor_Profile.py')
elif st.session_state["button_clicked"] == "students":
    st.switch_page('pages/72_Advisor_Students.py')
