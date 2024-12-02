import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title('Your Job Postings')

st.write('\n\n')

# API Base URL
BASE_API_URL = "http://api:4000/jp"

# Icon Buttons for Add and Info
col1, col2 = st.columns([0.1, 0.9])
with col1:
    if st.button("+", key="add_job"):
        st.session_state["add_job_form_visible"] = True
        st.session_state["update_job_form_visible"] = False
with col2:
    st.write("")  # Placeholder for alignment

# Initialize session states
if "add_job_form_visible" not in st.session_state:
    st.session_state["add_job_form_visible"] = False
if "update_job_form_visible" not in st.session_state:
    st.session_state["update_job_form_visible"] = False

# Fetch job postings
st.subheader("Your Active Job Postings")
try:
    response = requests.post(f"{BASE_API_URL}/jobPostings", json={"company_name": "Your Company Name"})  # Replace with company name
    if response.status_code == 200:
        job_postings = response.json()
        if job_postings:
            for job in job_postings:
                job_id = job['jobId']
                job_position = job['Position']
                job_description = job['Job Description']
                created_at = job['Created At']
                updated_at = job['Updated At']
                pay = job['Pay']
                time_period = job['Time Period']
                position_type = job['Position Type']
                employment_type = job['Employment Type']
                work_location = job['Location']
                is_active = job['Status']
                company_name = job['Company']

            with st.container():
                st.write(f"**{job_position}**")
                st.write(f"{job_description}")
                st.write(f"**Pay**: {pay}")
                st.write(f"**Employment Type**: {employment_type}")
                st.write(f"**Location**: {work_location}")
                st.write(f"**Company**: {company_name}")
                col1, col2 = st.columns([0.5, 0.5])
                    
                    # Update Button
                with col1:
                    if st.button("Update", key=f"update_{job_id}"):
                        st.session_state["update_job_form_visible"] = True
                        st.session_state["add_job_form_visible"] = False
                        st.session_state["current_job"] = job
                    
                    # Delete Button
                with col2:
                    if st.button("Delete", key=f"delete_{job_id}"):
                        if st.warning(f"Are you sure you want to delete '{job_position}'?"):
                            try:
                                delete_response = requests.delete(f"{BASE_API_URL}/jobPosting/{job_id}")
                                if delete_response.status_code == 200:
                                    st.success(f"'{job_position}' successfully deactivated.")
                                else:
                                    st.error(f"Failed to delete '{job_position}'.")
                            except requests.exceptions.RequestException as e:
                                st.error(f"Error connecting to server: {str(e)}")
        else:
            st.warning("No job postings found.")
    else:
        st.error(f"Error fetching job postings: {response.text}")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to job postings API: {str(e)}")

# Add Job Posting Form
if st.session_state["add_job_form_visible"]:
    st.subheader("Add a New Job Posting")
    with st.form("add_job_posting_form"):
        position = st.text_input("Job Name")
        description = st.text_area("Job Description")
        pay = st.number_input("Pay", min_value=0.0, step=0.01)
        time_period = st.text_input("Period")
        employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Internship"])
        work_location = st.selectbox("Work Location", ["Remote", "On-site", "Hybrid"])
        submit_button = st.form_submit_button("Create / Update")

        if submit_button:
            if not position or not description or not pay or not time_period:
                st.error("Please fill in all fields.")
            else:
                job_data = {
                    "position": position,
                    "description": description,
                    "pay": pay,
                    "time_period": time_period,
                    "employment_type": employment_type,
                    "work_location": work_location,
                    "employer": 1  # Example employer ID
                }
                try:
                    response = requests.post(f"{BASE_API_URL}/jobPosting", json=job_data)
                    if response.status_code == 200:
                        st.success("Job posting added successfully!")
                        st.session_state["add_job_form_visible"] = False
                    else:
                        st.error(f"Error adding job posting: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")

# Update Job Posting Form
if st.session_state["update_job_form_visible"] and "current_job" in st.session_state:
    job_to_update = st.session_state["current_job"]
    st.subheader(f"Update Job Posting: {job_to_update['Position']}")
    with st.form("update_job_posting_form"):
        position = st.text_input("Job Name", value=job_to_update['Position'])
        description = st.text_area("Job Description", value=job_to_update['Job Description'])
        pay = st.number_input("Pay", min_value=0.0, step=0.01)
        time_period = st.text_input("Period", value=job_to_update.get('time_period', ""))
        employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Internship"])
        work_location = st.selectbox("Work Location", ["Remote", "On-site", "Hybrid"])
        update_button = st.form_submit_button("Update")

        if update_button:
            updated_data = {
                "position": position,
                "description": description,
                "pay": pay,
                "time_period": time_period,
                "employment_type": employment_type,
                "work_location": work_location
            }
            try:
                response = requests.put(f"{BASE_API_URL}/jobPosting/{job_to_update['id']}", json=updated_data)
                if response.status_code == 200:
                    st.success("Job posting updated successfully!")
                    st.session_state["update_job_form_visible"] = False
                else:
                    st.error(f"Error updating job posting: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")