import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome {st.session_state['first_name']}.")

if st.button('View Your profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/71_Advisor_Profile.py')

if st.button('View Students', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/72_Advisor_Students.py')