import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Admin, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Admin Home', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/20_Admin_Home.py')

if st.button('Update User Role', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Update_User_Role.py')
