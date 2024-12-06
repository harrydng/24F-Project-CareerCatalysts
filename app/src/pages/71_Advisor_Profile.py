import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Show appropriate sidebar links for the role of the currently logged-in user
SideBarLinks()

st.title("Your Profile")
st.header("Your info")

# Input field for Student ID
st.subheader("Enter Advisor ID to view the profile")
advisor_id = st.text_input("Advisor ID (advisorId):", placeholder="Enter the Advisor ID")

# Placeholder for profile details or error messages
profile_placeholder = st.empty()

# Initialize advisorId to None
advisorId = None

# Validate and process the input
if advisor_id:  # Check if input is not empty
    try:
        advisorId = int(advisor_id)  # Try converting to an integer
        profile_placeholder.success(f"Fetching profile for Advisor ID: {advisorId}")
    except ValueError:
        profile_placeholder.error("Invalid Advisor ID. Please enter a valid numeric ID.")
        advisorId = None
else:
    profile_placeholder.info("Please enter an Advisor ID to view the profile.")


def fetch_advisor_name(advisorId):
    try:
        logger.info(f"Fetching info for advisor ID: {advisorId}")
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            if rows:  # Check if rows contain data
                return f"{rows[0]['firstName']} {rows[0]['middleName']} {rows[0]['lastName']}"
            else:
                st.warning("No data found for the given Advisor ID.")
                return "Please chose an advisor which exists"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"

    
def fetch_advisor_firstName(advisorId):
    try:
        logger.info(f"Fetching info for advisor ID: {advisorId}")
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            if rows:  # Check if rows contain data
                return f"{rows[0]['firstName']}"
            else:
                st.warning("No data found for the given Advisor ID.")
                return "Please chose an advisor which exists"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"

    
def fetch_advisor_middleName(advisorId):
    try:
        logger.info(f"Fetching info for advisor ID: {advisorId}")
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            if rows:
                return f"{rows[0]['middleName']}"
            else:
                st.warning("No data found for the given Advisor ID.")
                return "Please chose an advisor which exists"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"
    
def fetch_advisor_lastName(advisorId):
    try:
        logger.info(f"Fetching info for advisor ID: {advisorId}")
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            if rows:
                return f"{rows[0]['lastName']}"
            else:
                st.warning("No data found for the given Advisor ID.")
                return "Please chose an advisor which exists"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"

def fetch_advisor_userName(advisorId):
    try:
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            if rows:
                return rows[0]['username']
            else:
                st.warning("No data found for the given Advisor ID.")
                return "Please chose an advisor which exists"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"

def fetch_advisor_email(advisorId):
    try:
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            if rows:
                return rows[0]['email']
            else:
                st.warning("No data found for the given Advisor ID.")
                return "Please chose an advisor which exists"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"

# Display and fetch advisor details
#advisorName = fetch_advisor_name(advisorId)
#advisorFirstName = fetch_advisor_firstName(advisorId)
#advisorMiddleName = fetch_advisor_middleName(advisorId)
#advisorLastName = fetch_advisor_lastName(advisorId)

#advisorUserName = fetch_advisor_userName(advisorId)
#advisorEmail = fetch_advisor_email(advisorId)

# Fetch and display advisor details only if advisorId is valid
if advisorId is not None:
    # Fetch and display advisor details
    st.subheader("Name")

    # Update First Name Section
    first_name = st.text_input("Update First Name", value=fetch_advisor_firstName(advisorId))
    payloadName1 = {
        "firstName": first_name,
        "advisorId": advisorId
    }

    if st.button("Update First Name"):
        try:
            response = requests.put(f"http://api:4000/adv/updateFirstName/{advisorId}", json=payloadName1)
            if response.status_code == 200:
                st.success("Name updated successfully!")
            else:
                st.error(f"Error updating name: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {str(e)}")

    # Update Middle Name Section
    middle_name = st.text_input("Update Middle Name", value=fetch_advisor_middleName(advisorId))
    payloadName2 = {
        "middleName": middle_name,
        "advisorId": advisorId
    }

    if st.button("Update Middle Name"):
        try:
            response = requests.put(f"http://api:4000/adv/updateMiddleName/{advisorId}", json=payloadName2)
            if response.status_code == 200:
                st.success("Name updated successfully!")
            else:
                st.error(f"Error updating name: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {str(e)}")

    # Update Last Name Section
    last_name = st.text_input("Update Last Name", value=fetch_advisor_lastName(advisorId))
    payloadName3 = {
        "lastName": last_name,
        "advisorId": advisorId
    }

    if st.button("Update Last Name"):
        try:
            response = requests.put(f"http://api:4000/adv/updateLastName/{advisorId}", json=payloadName3)
            if response.status_code == 200:
                st.success("Name updated successfully!")
            else:
                st.error(f"Error updating name: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {str(e)}")

    # Update Username Section
    new_username = st.text_input("Update Username", value=fetch_advisor_userName(advisorId))
    payload2 = {
        "userName": new_username,
        "advisorId": advisorId
    }

    if st.button("Update Username"):
        try:
            response = requests.put(f"http://api:4000/adv/updateUsername/{advisorId}", json=payload2)
            if response.status_code == 200:
                st.success("Username updated successfully!")
            else:
                st.error(f"Error updating username: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {str(e)}")

    # Update Email Section
    new_email = st.text_input("Update Email", value=fetch_advisor_email(advisorId))
    payload3 = {
        "email": new_email,
        "advisorId": advisorId
    }
    if st.button("Update Email"):
        try:
            response = requests.put(f"http://api:4000/adv/updateEmail/{advisorId}", json=payload3)
            if response.status_code == 200:
                st.success("Email updated successfully!")
            else:
                st.error(f"Error updating email: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {str(e)}")
