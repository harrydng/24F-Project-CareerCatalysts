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
        "pages/84_View_skills.py", label="Check Student Skills", icon="💪")

def ViewLeaderboard():
    st.sidebar.page_link(
        "pages/62_Leaderboard.py", label="Student Leaderboard", icon="🏆")

def AddSkills():
    st.sidebar.page_link(
        "pages/86_Add_skills.py", label = "Add Skills", icon = "🎯"
    )

def ViewProfile():
    st.sidebar.page_link(
        "pages/87_View_User_Details.py", label = "View Profile", icon = "👤"
    )

def JobRecs():
    st.sidebar.page_link(
        "pages/88_Job_recommendations.py", label = "Job Recommendations", icon = "📊"
    )

#### ------------------------ System Admin Role ------------------------
def AdvisorProfile():
    st.sidebar.page_link("pages/71_Advisor_Profile.py", label="Your Profile", icon="👤")
    st.sidebar.page_link("pages/72_Advisor_Students.py", label="Your Students", icon="👨‍🎓")
    st.sidebar.page_link("pages/62_Leaderboard.py", label="Leaderboard", icon="🏆")
    st.sidebar.page_link("pages/61_Job_Postings.py", label="Job Postings", icon="💼")
    st.sidebar.page_link("pages/87_View_User_Details.py", label="View Students", icon="🔲")
    st.sidebar.page_link("pages/80_Co_Op_Placements.py", label="View Statistics", icon="📊")

    


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

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()
            
        if st.session_state["role"] == "advisor":
            AdvisorProfile()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
