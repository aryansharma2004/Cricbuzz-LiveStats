"""
🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics
Main application entry point.
"""

import streamlit as st
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import APP_TITLE, APP_ICON, LAYOUT
from utils.db_connection import init_database

# Configure Streamlit page layout
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Initialize database on startup
if "db_initialized" not in st.session_state:
    try:
        init_database()
        st.session_state.db_initialized = True
    except Exception as e:
        st.sidebar.error(f"DB Init note: {e}")

# Define pages for modern unified navigation
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
live_page = st.Page("pages/live_matches.py", title="Live Matches", icon="🏏")
players_page = st.Page("pages/top_players.py", title="Top Players", icon="⭐")
analytics_page = st.Page("pages/analytics.py", title="SQL Analytics", icon="📊")
crud_page = st.Page("pages/crud.py", title="CRUD Operations", icon="🛠️")

# Single unified navigation sidebar
nav = st.navigation({
    "Overview": [home_page, live_page, players_page],
    "Analytics & Database": [analytics_page, crud_page]
})

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.info("🏏 **Cricbuzz LiveStats**\n\nBuilt with Python, SQL, Streamlit & RapidAPI.")

# Execute active page
nav.run()
