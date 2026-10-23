"""
Home page for Cricbuzz LiveStats application.
Provides project overview, system metrics, architecture explanation, and navigation guide.
"""

import streamlit as st
import os
import sys

# Ensure project root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from utils.db_connection import execute_query, init_database


def render():
    """Render the Home page."""
    # Ensure DB is populated
    try:
        init_database()
    except Exception:
        pass

    st.title("🏏 Cricbuzz LiveStats")
    st.markdown("### Real-Time Cricket Insights & SQL-Based Analytics")
    st.markdown("---")

    # Hero Banner
    st.info(
        "👋 Welcome to **Cricbuzz LiveStats** — an end-to-end sports analytics platform "
        "integrating live data from the Cricbuzz Cricket API with a relational SQL database "
        "and interactive Streamlit dashboard."
    )

    # Key Pillars
    st.markdown("#### 🎯 Core Capabilities")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### ⚡ Live Matches")
        st.caption("Live scorecards, ground details, match status, and API streaming.")

    with col2:
        st.markdown("#### ⭐ Top Players")
        st.caption("Rankings, format-wise batting & bowling leaderboards, and player cards.")

    with col3:
        st.markdown("#### 📊 SQL Analytics")
        st.caption("25 curated SQL practice questions spanning Beginner, Intermediate, and Advanced.")

    with col4:
        st.markdown("#### 🛠️ CRUD Operations")
        st.caption("Full database control: Create, Read, Update, and Delete players & matches.")

    st.markdown("---")

    # Live Database Metrics
    st.markdown("#### 📈 Database Health & Summary")
    try:
        col1, col2, col3, col4, col5 = st.columns(5)
        p_count = execute_query("SELECT COUNT(*) AS total FROM players")['total'].iloc[0]
        t_count = execute_query("SELECT COUNT(*) AS total FROM teams")['total'].iloc[0]
        m_count = execute_query("SELECT COUNT(*) AS total FROM matches")['total'].iloc[0]
        v_count = execute_query("SELECT COUNT(*) AS total FROM venues")['total'].iloc[0]
        s_count = execute_query("SELECT COUNT(*) AS total FROM series")['total'].iloc[0]

        col1.metric("🏏 Players", int(p_count))
        col2.metric("🛡️ Teams", int(t_count))
        col3.metric("🏆 Matches", int(m_count))
        col4.metric("🏟️ Venues", int(v_count))
        col5.metric("📅 Series", int(s_count))
    except Exception as e:
        st.warning(f"Database metric collection note: {e}")

    st.markdown("---")

    # Tech Stack Badges
    st.markdown("#### 🧰 Technology Stack")
    t1, t2, t3, t4, t5 = st.columns(5)
    t1.success("**Python 3.10+**\n\nCore Backend & Services")
    t2.info("**Streamlit**\n\nInteractive Multi-page Web UI")
    t3.warning("**SQLite / SQL**\n\nRelational Schema & 3NF Engine")
    t4.error("**RapidAPI**\n\nCricbuzz Live Cricket API")
    t5.success("**Pandas & Plotly**\n\nDataframes & Dynamic Charts")

    st.markdown("---")

    # Architecture Overview Expander
    with st.expander("🏗️ System Architecture & Data Flow", expanded=True):
        st.markdown("""
        ```
        [ RapidAPI Cricbuzz ]
                 │
                 ▼ (REST / JSON)
        [ api/cricbuzz_client.py ]
                 │
                 ├──► [ services/match_service.py ] ◄──► [ utils/db_connection.py ]
                 │                                                │
                 ├──► [ services/player_service.py ]              ▼
                 │                                         [ SQLite Database ]
                 └──► [ services/stats_service.py ]        (cricbuzz.db)
                                  │
                                  ▼
                     [ Streamlit UI Pages ]
        ```
        """)

    with st.expander("📖 User Guide & Navigation"):
        st.markdown("""
        - **🏏 Live Matches**: Switch between real-time API feeds and database records.
        - **⭐ Top Players**: View batting & bowling leaderboards with interactive Plotly graphs.
        - **📊 SQL Analytics**: Run any of the 25 SQL queries with explanations and SQL viewer.
        - **🛠️ CRUD Operations**: Create, edit, and delete players or matches with form validation.
        """)


# Render immediately when script is executed
render()
