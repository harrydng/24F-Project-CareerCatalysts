import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

# Include the sidebar links
SideBarLinks()

st.title('System Metrics and Alerts')

st.write('\n\n')

# Function to fetch and display metrics and alerts
def fetch_and_display_metrics_and_alerts():
    try:
        logger.info("Fetching metrics and alerts")
        
        # API request to get metrics and alerts
        response = requests.get('http://api:4000/system/metrics_and_alerts')

        if response.status_code == 200:
            data = response.json()
            metrics_data = data.get('metrics', [])
            alerts_data = data.get('alerts', [])
            
            if metrics_data:
                st.subheader('Metrics')
                # Convert metrics data to DataFrame for better display
                metrics_df = pd.DataFrame(metrics_data)
                st.table(metrics_df)
            else:
                st.warning("No metrics found!")
            
            if alerts_data:
                st.subheader('Alerts')
                # Convert alerts data to DataFrame for better display
                alerts_df = pd.DataFrame(alerts_data)
                st.table(alerts_df)
            else:
                st.warning("No alerts found!")
        else:
            st.error(f"Error fetching metrics and alerts: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")

# Fetch and display metrics and alerts on page load
fetch_and_display_metrics_and_alerts()
