import streamlit as st
import requests

# Define the API base URL
BASE_URL = "http://localhost:4000"  

# Set up the Streamlit page
st.set_page_config(
    page_title="View Skills",
    layout="wide"
)

# Header
st.title("View Your Skills")

# Input for Student ID
st.subheader("Enter your Student ID to fetch your skills")
student_id = st.text_input("Student ID (nuId):", placeholder="Enter your Student ID")

# Button to fetch and view skills
if st.button("Fetch Skills"):
    if student_id:
        # Call the API to fetch skills
        try:
            response = requests.get(f"{BASE_URL}/sk/skillRec", params={"nuId": student_id})
            if response.status_code == 200:
                data = response.json()
                if data:
                    st.success(f"Skills for Student ID {student_id}")
                    # Only display the skills data in a table
                    # Assuming `data` contains "name" and "description" fields
                    skills_table = [{"Skill Name": skill["name"], "Description": skill["description"]} for skill in data]
                    st.table(skills_table)
                else:
                    st.warning("No skills found for the given Student ID.")
            else:
                st.error(f"Error fetching data: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to fetch data from the API: {str(e)}")
    else:
        st.warning("Please enter a valid Student ID.")

# Button to navigate back to the home page
if st.button("Go Back to Home"):
    st.experimental_set_query_params()  # Clear query params if needed
    st.switch_page("Student_Home_Page")
