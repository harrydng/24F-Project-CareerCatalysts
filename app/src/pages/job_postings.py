import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title('Your Job Postings')

st.write('\n\n')

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
        response = requests.post(f"http://api:4000/jp/jobPosting", json=data)
        if response.status_code == 200:
            st.success(f"Employer and Job posting successfully added.")
        else:
            st.error(f"Error updating job posting: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

def find_employer_id(company_name):
    """
    Add a job posting by its Employer ID with new data.
    """
    try:
        response = requests.post(f"http://api:4000/e/jobPosting", json=data)
        if response.status_code == 200:
            st.success(f"Employer and Job posting successfully added.")
        else:
            st.error(f"Error updating job posting: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        


# Fetch categories from API
# This has to be outside the form so the list of categories is 
# populated when form is displayed. 
try:
    # Access /p/categories with a GET request
    categories_response = requests.get('http://api:4000/p/categories')
    
    # 200 means the request was successful
    if categories_response.status_code == 200:
        # pull the data from the response object as json
        categories_data = categories_response.json()
        # create a list of categories from the json. The initial [""] is so 
        # there isn't a default category selected in the product category select widget
        category_options = [""] + [category['value'] for category in categories_data]
    else:
        # means we got back some HTTP code besides 200
        st.error("Failed to fetch categories")
        category_options = []
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to categories API: {str(e)}")
    category_options = []




# Input Form for Company Name
st.write("### Search for Job Postings")
company_name = st.text_input("Enter the company name:", placeholder="Enter a company name (e.g., Sundar)")

col1, col2 = st.columns(2)

with col1:
    if st.button("Add a New Job"):
        if company_name:
            with st.form(f"Add new Job"):
                new_position = st.text_input("Position")
                new_description = st.text_area("Job Description")
                new_pay = st.text_input("Pay")
                new_time_period = st.text_input("Time Period")
                
                new_position_type = st.text_input("Position Type")
                new_employment_type = st.text_input("Employment Type")
                new_work_location = st.text_input("Work Location")
            
                submit_update = st.form_submit_button("Add Job")
                if submit_update:
                    if not new_position:
                        st.error("Please enter a position name")
                    elif not new_description:
                        st.error("Please enter a job description")
                    elif not new_pay:
                        st.error("Please select a pay")
                    elif not new_time_period:
                        st.error("Please enter a time period")
                    elif not new_position_type:
                        st.error("Please select a position type")
                    elif not new_employment_type:
                        st.error("Please select a employment type")
                    elif not new_work_location:
                        st.error("Please select a work location")    
                    else:
                        data = {
                            "position": new_position,
                            "description": new_description,
                            "pay": new_pay,
                            "time_period": new_time_period,
                            "position_type": new_position_type,
                            "employment_type": new_employment_type,
                            "work_location": new_work_location,
                            "employerId": find_employer_id(company_name),                
                        }
                        logger.info(f"New Job have been added {new_position}")
                        add_job_posting(data)
    else:
        st.warning("Please enter a valid company name.")

with col2:
    if st.button("Fetch Job Postings"):
        if company_name:
            job_postings = fetch_job_postings(company_name)
            logger.info(f"The job postings {job_postings}")
            
            if job_postings:
                for job in job_postings:
                    st.markdown("---")  # Separator for visual clarity
                    st.subheader(f"**Position: {job['Position']}**")
                    st.write(f"**Description:** {job['Job Description']}")
                    st.write(f"**Pay:** {job['Pay']}")
                    st.write(f"**Time Period:** {job['Time Period']}")
                    st.write(f"**Employment Type:** {job['Employment Type']}")
                    st.write(f"**Location:** {job['Location']}")
                    st.write(f"**Company:** {job['Company']}")
                    st.write(f"**Created At:** {job['Created At']}")
                    
                    # Action Buttons
                    action_col1, action_col2 = st.columns(2)
                    
                    with action_col1:
                        if st.button("Delete", key=f"delete_{job['jobId']}"):
                            delete_job_posting(job['jobId'])
                            logger.info(f"Job have been Deleted {job['jobId']}")
                            st.experimental_rerun()

                    with action_col2:
                        if st.button("Update", key=f"update_{job['jobId']}"):
                            with st.form(f"Update Job {job['jobId']}"):
                                new_position = st.text_input("Position", value=job["Position"])
                                new_description = st.text_area("Description", value=job["Job Description"])
                                new_pay = st.text_input("Pay", value=job["Pay"])
                                new_time_period = st.text_input("Time Period", value=job["Time Period"])
                                new_employment_type = st.text_input("Employment Type", value=job["Employment Type"])
                                new_work_location = st.text_input("Work Location", value=job["Location"])

                                submit_update = st.form_submit_button("Submit Update")
                                if submit_update:
                                    updated_data = {
                                        "position": new_position,
                                        "description": new_description,
                                        "pay": new_pay,
                                        "time_period": new_time_period,
                                        "employment_type": new_employment_type,
                                        "work_location": new_work_location,
                                    }
                                    logger.info(f"Job have been Updated {updated_data}")
                                    update_job_posting(job["jobId"], updated_data)
            else:
                st.warning(f"No job postings found for {company_name}.")
        else:
            st.warning("Please enter a valid company name.")