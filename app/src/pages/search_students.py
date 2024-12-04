import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title('Search for Students')

st.write('\n\n')


with st.form("filter_students_form"):
    first_name = st.text_input("first_name")
    last_name = st.text_input("last_name")
    dob = st.text_input("dob", placeholder="MM/DD/YYYY")
    major = st.text_input("major")
    minor = st.text_input("minor")
    year = st.text_input("year")
    advisor = st.text_input("advisor")
    email = st.text_input("email")
    
    skills = st.text_input("skills")
    courses = st.text_input("courses")
    
    
     