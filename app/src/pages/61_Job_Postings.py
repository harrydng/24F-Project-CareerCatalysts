import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title('Your Job Postings')
st.write('\n\n')

# Initialize session states for buttons
if "add_job_clicked" not in st.session_state:
    st.session_state["add_job_clicked"] = False

if "fetch_jobs_clicked" not in st.session_state:
    st.session_state["fetch_jobs_clicked"] = False

def fetch_job_postings(company_name):
    """
    Fetch job postings for a given company name.
    """
    try:
        payload = {"company_name": company_name}
        logger.info(f"Fetching job postings with payload: {payload}")
        response = requests.post(f"http://api:4000/jp/jobPostings", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching job postings: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return []

def delete_job_posting(job_id):
    """
    Delete a job posting by its ID.
    """
    try:
        payload = {"job_id": job_id}
        response = requests.delete(f"http://api:4000/jp/jobPosting/{job_id}")
        if response.status_code == 200:
            st.success(f"Job posting with ID {job_id} successfully deleted.")
        else:
            st.error(f"Error deleting job posting: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

def update_job_posting(job_id, updated_data):
    """
    Update a job posting by its ID with new data.
    """
    try:
        response = requests.put(f"http://api:4000/jp/jobPosting/{job_id}", json=updated_data)
        if response.status_code == 200:
            st.success(f"Job posting with ID {job_id} successfully updated.")
        else:
            st.error(f"Error updating job posting: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        
def add_job_posting(data):
    """
    Add a job posting by its Employer ID with new data.
    """
    try:
        payload = {"company_name": data}
        response = requests.post(f"http://api:4000/jp/jobPosting", json=payload)
        if response.status_code == 200:
            st.success(f"Job posting successfully added.")
        else:
            st.error(f"Error adding job posting: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

def find_employer_id(company_name):
    """
    Find employer ID for a given company name.
    """
    try:
        payload = {'company_name' : company_name}
        response = requests.get(f"http://api:4000/e/employerId", json=payload)
        if response.status_code == 200:
            employer_data = response.json()
            if employer_data:
                return employer_data[0]['employerId']
            else:
                st.warning(f"No employer found for company name: {company_name}")
                return None
        else:
            st.error(f"Error finding the employer: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        

# Fetch categories from API
try:
    responses = requests.get('http://api:4000/jp/jobTypes')
    if responses.status_code == 200:
        responses_data = responses.json()
        employment_type_options = [""] + responses_data["Employment Types"]
        position_type_options = [""] + responses_data["Position Types"]
        work_location_options = [""] + responses_data["Work Locations"]
    else:
        st.error("Failed to fetch job types")
        employment_type_options = []
        position_type_options = []
        work_location_options = []
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to job types API: {str(e)}")
    employment_type_options = []
    position_type_options = []
    work_location_options = []

# Input Form for Company Name
st.write("### Search for Job Postings")
company_name = st.text_input("Enter the company name:", placeholder="Enter a company name (e.g., Innovate)")

col1, col2 = st.columns(2)

with col1:
    if st.button("Add a New Job"):
        st.session_state["add_job_clicked"] = not st.session_state["add_job_clicked"]

    if st.session_state["add_job_clicked"] and company_name:
        with st.form(f"Add new Job"):
            new_position = st.text_input("Position")
            new_description = st.text_area("Job Description")
            new_pay = st.text_input("Pay")
            new_time_period = st.text_input("Time Period")
            
            new_position_type = st.selectbox("Position Type", options=position_type_options, index=0)
            new_employment_type = st.selectbox("Employment Type", options=employment_type_options, index=0)
            new_work_location = st.selectbox("Work Location", options=work_location_options, index=0)
        
            submit_update = st.form_submit_button("Add Job")
            if submit_update:
                if not new_position:
                    st.error("Please enter a position name")
                elif not new_description:
                    st.error("Please enter a job description")
                elif not new_pay:
                    st.error("Please enter pay")
                elif not new_time_period:
                    st.error("Please enter a time period")
                elif not new_position_type:
                    st.error("Please select a position type")
                elif not new_employment_type:
                    st.error("Please select an employment type")
                elif not new_work_location:
                    st.error("Please select a work location")    
                else:
                    try:
                        formatted_pay = float(new_pay)  # Convert input to float
                        if formatted_pay < 0:
                            st.error("Pay must be a positive value.")
                        else:
                            formatted_pay = "{:.2f}".format(formatted_pay)  # Format to two decimals
                    except ValueError:
                        st.error("Invalid input for pay. Please enter a valid decimal number.")
                    employer_id = find_employer_id(company_name)
                    if employer_id:
                        data = {
                            "position": new_position,
                            "description": new_description,
                            "pay": formatted_pay,
                            "time_period": new_time_period,
                            "position_type": new_position_type,
                            "employment_type": new_employment_type,
                            "work_location": new_work_location,
                            "employerId": employer_id,                
                        }
                        logger.info(f"New Job added: {data}")
                        
                        add_job_posting(data)
                    else:
                        st.error("Failed to find a valid employer ID. Please verify the company name.")

with col2:
    if st.button("Fetch Job Postings"):
        st.session_state["fetch_jobs_clicked"] = not st.session_state["fetch_jobs_clicked"]

    if st.session_state["fetch_jobs_clicked"] and company_name:
        job_postings = fetch_job_postings(company_name)
        logger.info(f"Job postings fetched: {job_postings}")
        if job_postings:
            for job in job_postings:
                st.markdown("---")
                st.subheader(f"**Position: {job['Position']}**")
                st.write(f"**Description:** {job['Job Description']}")
                st.write(f"**Pay:** {job['Pay']}")
                st.write(f"**Time Period:** {job['Time Period']}")
                st.write(f"**Position Type:** {job['Position Type']}")
                st.write(f"**Employment Type:** {job['Employment Type']}")
                st.write(f"**Location:** {job['Location']}")
                st.write(f"**Company:** {job['Company']}")
                st.write(f"**Created At:** {job['Created At']}")
                st.write(f"**Updated At:** {job['Updated At']}")

                action_col1, action_col2 = st.columns(2)
                
                with action_col1:
                    if st.button("Delete", key=f"delete_{job['jobId']}"):
                        delete_job_posting(job['jobId'])
                        logger.info(f"Job deleted: {job['jobId']}")

                # Update button in the "Update" section
                with action_col2:
                    if st.button("Update", key=f"update_{job['jobId']}"):
                        st.session_state[f"update_{job['jobId']}_clicked"] = not st.session_state.get(f"update_{job['jobId']}_clicked", False)

                    if st.session_state.get(f"update_{job['jobId']}_clicked", False):
                        with st.form(f"Update Job {job['jobId']}"):
                            new_position = st.text_input("Position", value=job["Position"])
                            new_description = st.text_area("Description", value=job["Job Description"])
                            new_pay = st.text_input("Pay", value=job["Pay"])
                            new_time_period = st.text_input("Time Period", value=job["Time Period"])
                            
                            new_position_type = st.selectbox("Position Type", options=position_type_options)
                            new_employment_type = st.selectbox("Employment Type", options=employment_type_options)
                            new_work_location = st.selectbox("Work Location", options=work_location_options)

                            submit_update = st.form_submit_button("Submit Update")  # This is the Submit Button
                            if submit_update:  # Trigger form submission
                                updated_data = {
                                    "position": new_position,
                                    "description": new_description,
                                    "pay": new_pay,
                                    "time_period": new_time_period,
                                    
                                    "position_type": new_position_type,
                                    "employment_type": new_employment_type,
                                    "work_location": new_work_location,
                                }
                                logger.info(f"Job updated: {updated_data}")
                                update_job_posting(job["jobId"], updated_data)
                                st.session_state[f"update_{job['jobId']}_clicked"] = False  # Reset the button state after submission
        else:
            st.warning(f"No job postings found for {company_name}.")