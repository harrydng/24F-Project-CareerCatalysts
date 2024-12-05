# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

### --------------------- Employer Page ---------------------
def SearchForCandidates():
    st.sidebar.page_link(
        "pages/63_Search_Students.py", label="Search For Students", icon="👤")

def JobPostings():
    st.sidebar.page_link(
        "pages/61_Job_Postings.py", label="My Job Postings", icon="🏦")

def ViewLeaderboard():
    st.sidebar.page_link(
        "pages/62_Leaderboard.py", label="Student Leaderboard", icon="🚨")
    

### --------------------- Student Page ---------------------
def ShowSkills():
    st.sidebar.page_link(
        "pages/74_View_skills.py", label="Check Student Skills", icon="💪")

def ViewLeaderboard():
    st.sidebar.page_link(
        "pages/62_Leaderboard.py", label="Student Leaderboard", icon="🏆")

def AddSkills():
    st.sidebar.page_link(
        "pages/76_Add_skills.py", label = "Add Skills", icon = "🎯"
    )

def ViewProfile():
    st.sidebar.page_link(
        "pages/77_View_User_Details.py", label = "View Profile", icon = "👤"
    )

def JobRecs():
    st.sidebar.page_link(
        "pages/78_Job_recommendations.py", label = "Job Recommendations", icon = "📊"
    )

#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤"
    )


def WorldBankVizNav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")


## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Metrics and Alerts", icon="📊")
    st.sidebar.page_link("pages/21_Update_User_Role.py", label="Update User Role", icon="🔄")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # If user role is employer, give access to all pages 
        if st.session_state["role"] == "employer":
            SearchForCandidates()
            JobPostings()
            ViewLeaderboard()
        
        if st.session_state["role"] == "student":
            ShowSkills()
            AddSkills()
            JobRecs()
            ViewProfile()
            ViewLeaderboard()

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "pol_strat_advisor": 
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "usaid_worker":
            PredictionNav()
            ApiTestNav()
            ClassificationNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
