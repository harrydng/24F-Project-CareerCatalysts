import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    TalentTrail is a data-driven platform that empowers Northeastern University students 
    to explore personalized career pathways with unprecedented clarity. 
    TalentTrail delivers curated recommendations for classes, projects, and job opportunities 
    tailored to each user’s career aspirations by collecting and analyzing data 
    on students' majors, minors, skills, and interests. 
    
    Traditional career platforms lack the ability to integrate academic planning with personal interests
    in a way that feels engaging and intuitive—this is where TalentTrail excels.
    
    Our primary users include students, employers, co-op advisors/decision-makers, and system administrators. 
    Key features include a personalized career discovery pathway, 
    an advanced job search tool that matches students with roles based on personality tags, 
    and a gamified experience where students earn badges and climb leaderboards by achieving career milestones. 
    
    TalentTrail bridges the gap between education and employment, 
    transforming career planning into a proactive, personalized journey.
    """
        )
