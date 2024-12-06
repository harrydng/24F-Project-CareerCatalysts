import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt

# Set up logging
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

st.title("Student Placement Statistics")


logger = logging.getLogger(__name__)

#Gets the average jobs per student per year
def get_avg_jobs():
    """
    Fetches year, student count, and job count from the API, and computes the 
    average number of jobs per student for each year.

    Returns:
        list of dict: A list of dictionaries with year and average jobs per student.
    """
    try:
        response = requests.get(f"http://api:4000/adv/job_posting/year/avg")
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format
            avg_jobs_per_student = []

            for record in data:
                year = record["student_year"]
                student_count = record["student_count"]
                job_count = record["job_count"]

                # Calculate average jobs per student (handle division by zero)
                avg_jobs = job_count / student_count if student_count > 0 else 0

                avg_jobs_per_student.append({
                    "year": year,
                    "avgJobs": avg_jobs,
                })

            return avg_jobs_per_student  # Return the list of dictionaries
        else:
            logger.error(f"Failed to fetch data: {response.status_code} - {response.text}")
            return []

    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to API: {str(e)}")
        return []

# Fetch the data
data_input = get_avg_jobs()

# Convert the data into a DataFrame
df = pd.DataFrame(data_input)

if df.empty:
    st.warning("No data available to display.")
else:
    # Streamlit UI
    st.title("Year vs Avg Jobs Taken")

    # Plot the data
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Line chart for job postings
    ax2 = ax1.twinx()
    ax2.plot(df["year"], df["avgJobs"], marker="o", label="Job Count", color="blue")

    # Label axes
    ax1.set_xlabel("Year")
    ax2.set_ylabel("Number of Jobs", color="black")

    # Title
    ax1.set_title("Year vs Avg Jobs Taken")

    # Streamlit plot
    st.pyplot(fig)
