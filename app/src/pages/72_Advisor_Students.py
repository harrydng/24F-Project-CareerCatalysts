import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Student Progress")

st.header("Students you manage")

advisorId = 187

def fetch_advisor_students(advisorId):
    """
    Fetch all students who an advisor advises
    """
    try:
        payload = {"advised_students": advisorId}
        logger.info(f"Fetching job postings with payload: {payload}")
        
        response = requests.get(f"http://api:4000/manages/{payload}", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching students: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []
