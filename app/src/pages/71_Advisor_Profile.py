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

advisorId = 1

# Fetch the advisor name
def fetch_advisor_name(advisorId):
    try:
        logger.info(f"Fetching info for advisor ID: {advisorId}")
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            return f"{rows[0]['firstName']} {rows[0]['middleName']} {rows[0]['lastName']}"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"
    
# Fetch the advisor first name
def fetch_advisor_firstName(advisorId):
    try:
        logger.info(f"Fetching info for advisor ID: {advisorId}")
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            return f"{rows[0]['firstName']}"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"
    
# Fetch the advisor middle name
def fetch_advisor_middleName(advisorId):
    try:
        logger.info(f"Fetching info for advisor ID: {advisorId}")
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            return f"{rows[0]['middleName']}"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"
    
# Fetch the advisor last name
def fetch_advisor_lastName(advisorId):
    try:
        logger.info(f"Fetching info for advisor ID: {advisorId}")
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            return f"{rows[0]['lastName']}"
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"

# Fetch the advisor username
def fetch_advisor_userName(advisorId):
    try:
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            return rows[0]['username']
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"

# Fetch the advisor email
def fetch_advisor_email(advisorId):
    try:
        response = requests.get(f"http://api:4000/adv/info/{advisorId}")
        if response.status_code == 200:
            rows = response.json()
            return rows[0]['email']
        else:
            st.error(f"Error fetching advisor info: {response.text}")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return "Unknown"

# Display and fetch advisor details
advisorName = fetch_advisor_name(advisorId)
advisorFirstName = fetch_advisor_firstName(advisorId)
advisorMiddleName = fetch_advisor_middleName(advisorId)
advisorLastName = fetch_advisor_lastName(advisorId)

advisorUserName = fetch_advisor_userName(advisorId)
advisorEmail = fetch_advisor_email(advisorId)

# Display Name Section
st.subheader("Name")

#Update First Name Section
first_name = st.text_input("Update First Name", value=advisorFirstName)

# JSON payload with multiple fields
payloadName1 = {
    "firstName": first_name,
    "advisorId": advisorId
}

if st.button("Update First Name"):
    try:
        response = requests.put(f"http://api:4000/adv/updateFirstName/{advisorId}", json={payloadName1})
        if response.status_code == 200:
            st.success("Name updated successfully!")
        else:
            st.error(f"Error updating name: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

#Update middle name section
middle_name = st.text_input("Update Middle Name", value=advisorMiddleName)

#Update the middle name
# JSON payload with multiple fields
payloadName2 = {
    "middleName": middle_name,
    "advisorId": advisorId
}

if st.button("Update Middle Name"):
    try:
        response = requests.put(f"http://api:4000/adv/updateMiddleName/{advisorId}", json={payloadName2})
        if response.status_code == 200:
            st.success("Name updated successfully!")
        else:
            st.error(f"Error updating name: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")



last_name = st.text_input("Update Last Name", value=advisorLastName)

#Update the last name section
# JSON payload with multiple fields
payloadName3 = {
    "lastName": last_name,
    "advisorId": advisorId
}

if st.button("Update Last Name"):
    try:
        response = requests.put(f"http://api:4000/adv/updateLastName/{advisorId}", json={payloadName3})
        if response.status_code == 200:
            st.success("Name updated successfully!")
        else:
            st.error(f"Error updating name: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

# Display Username Section
st.subheader("Username")
new_username = st.text_input("Update Username", value=advisorUserName)

# JSON payload with multiple fields
payload2 = {
    "userName": new_username,
    "advisorId": advisorId
}

if st.button("Update Username"):
    try:
        response = requests.put(f"http://api:4000/adv/updateUserName/{advisorId}", json={payload2})
        if response.status_code == 200:
            st.success("Username updated successfully!")
        else:
            st.error(f"Error updating username: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

# Display Email Section
st.subheader("Email")
new_email = st.text_input("Update Email", value=advisorEmail)

# JSON payload with multiple fields
payload3 = {
    "email": new_email,
    "advisorId": advisorId
}
if st.button("Update Email"):
    try:
        response = requests.put(f"http://api:4000/adv/updateEmail/{advisorId}", json={payload3})
        if response.status_code == 200:
            st.success("Email updated successfully!")
        else:
            st.error(f"Error updating email: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

st.header("Id")
st.header(f'{advisorId}')
