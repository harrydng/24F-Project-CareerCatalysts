import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Employer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Search For Students', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/63_Search_Students.py')

if st.button('Your Job Postings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/61_Job_Postings.py')

if st.button('The Student Leaderboard', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/62_Leaderboard.py')
