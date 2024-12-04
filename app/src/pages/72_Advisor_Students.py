import logging
import sqlite3
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Student Progress")

st.header("Students you manage")

# Specify the database file
db_path = 'database.db'
sql_file_path = 'C:/Users/exons/Documents/GitHub/24F-Project-CareerCatalysts/database-files/DDL_for_Submission_Two.sql'

# Connect to the generated database file
conn = sqlite3.connect('database.db')

# Use the connection as needed
cursor = conn.cursor()

# Connect to the database
#conn = sqlite3.connect('C:/Users/exons/Documents/GitHub/24F-Project-CareerCatalysts/database-files/DDL_for_Submission_Two.sql')
#cursor = conn.cursor()

# Fetch options from the database
# Backend API URL
#API_URL = "http://localhost:4000/api/manages/<advisorId>"
#response = requests.get(API_URL)
#students = response.json() 

#options = [students[0] for user in students]  # Convert tuples to a list

# Dropdown menu
#selected_option = st.selectbox("Select a student:", options)

# Fetch options from the database

advisorId = 187
cursor.execute('''SELECT user.firstName, user.middleName, user.lastName, student_profile.nuId 
                      FROM users
                      JOIN advisor_profile ON advisor_profile.advisorId = user.userIdd
                      JOIN student_profile ON student_profile.nuId = user.userId
                      JOIN student_reports ON student_profile.nuId = student_reports.nuId
                      WHERE advisor_profile.advisorId = %s''', (advisorId,))  # Replace with your query
rows = cursor.fetchall()
options = [row[0] for row in rows]  # Convert tuples to a list

# Dropdown menu
selected_option = st.selectbox("Select a student:", options)
