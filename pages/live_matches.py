"""
Live Matches page for Cricbuzz LiveStats.
Presents real-time match data from Cricbuzz API and stored matches from the database.
"""

import streamlit as st
import os
import sys

# Ensure project root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from services.match_service import get_all_matches
from api.cricbuzz_client import CricbuzzClient


def render():
    """Render the Live Matches page."""
    st.title("🏏 Live & Recent Matches")
    st.markdown("Real-time match status, live scorecards, and venue information.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["📡 Live Cricbuzz API Feed", "🗄️ Database Archive Matches"])

    with tab1:
        st.markdown("### 📡 Real-Time Matches via Cricbuzz API")
        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            fetch_clicked = st.button("🔄 Refresh Live Matches", type="primary", key="refresh_live_btn")

        if fetch_clicked or "live_api_data" not in st.session_state:
            with st.spinner("Fetching matches from Cricbuzz API..."):
                try:
                    client = CricbuzzClient()
                    data = client.get_recent_matches()
                    st.session_state.live_api_data = data
                except Exception as e:
                    st.error(f"API Error: {e}")
                    st.info("💡 You can configure your RAPIDAPI_KEY in the `.env` file.")
                    st.session_state.live_api_data = None

        data = st.session_state.get("live_api_data")
        if data and "typeMatches" in data:
            for type_match in data["typeMatches"]:
                m_type = type_match.get("matchType", "Cricket Matches")
                st.markdown(f"#### 🏆 {m_type}")

                for series_match in type_match.get("seriesMatches", []):
                    series_wrap = series_match.get("seriesAdWrapper", {})
                    s_name = series_wrap.get("seriesName", "Tournament Series")
                    st.markdown(f"**Series:** `{s_name}`")

                    for m in series_wrap.get("matches", []):
                        m_info = m.get("matchInfo", {})
                        m_score = m.get("matchScore", {})

                        t1_name = m_info.get("team1", {}).get("teamName", "Team 1")
                        t2_name = m_info.get("team2", {}).get("teamName", "Team 2")
                        status = m_info.get("status", "Match Scheduled")
                        state = m_info.get("state", "Upcoming")
                        desc = m_info.get("matchDescription", "Match")
                        format_str = m_info.get("matchFormat", "Cricket")
                        venue = m_info.get("venueInfo", {}).get("ground", "Venue")
                        city = m_info.get("venueInfo", {}).get("city", "City")

                        # Card presentation
                        with st.container():
                            c1, c2 = st.columns([3, 1])
                            with c1:
                                st.markdown(f"##### {desc} ({format_str}): {t1_name} vs {t2_name}")
                                st.caption(f"📍 {venue}, {city}")

                                # Score displays
                                s1 = m_score.get("team1Score", {}).get("inngs1", {})
                                s2 = m_score.get("team2Score", {}).get("inngs1", {})

                                score_txt = []
                                if s1:
                                    score_txt.append(f"**{t1_name}**: {s1.get('runs', 0)}/{s1.get('wickets', 0)} ({s1.get('overs', 0)} ov)")
                                if s2:
                                    score_txt.append(f"**{t2_name}**: {s2.get('runs', 0)}/{s2.get('wickets', 0)} ({s2.get('overs', 0)} ov)")

                                if score_txt:
                                    st.markdown(" • ".join(score_txt))

                            with c2:
                                if state == "Complete":
                                    st.success(f"🏁 {status}")
                                elif state == "In Progress":
                                    st.warning(f"⚡ {status}")
                                else:
                                    st.info(f"⏳ {status}")

                            st.markdown("---")
        else:
            st.info("No live match data currently returned by API. Click 'Refresh Live Matches' above.")

    with tab2:
        st.markdown("### 🗄️ Matches in Relational Database")
        try:
            df = get_all_matches(limit=50)
            if not df.empty:
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    format_opts = ["All"] + sorted([x for x in df['match_format'].dropna().unique()])
                    sel_format = st.selectbox("Filter by Format", format_opts, key="live_m_filter")
                with col_f2:
                    st.metric("Total Matches in Database", len(df))

                filtered_df = df if sel_format == "All" else df[df['match_format'] == sel_format]

                display_cols = ['description', 'team1', 'team2', 'match_format',
                                'match_date', 'result', 'venue', 'city']
                st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)
            else:
                st.warning("Database contains no match records.")
        except Exception as e:
            st.error(f"Database error: {e}")


# Render immediately when script is executed
render()
