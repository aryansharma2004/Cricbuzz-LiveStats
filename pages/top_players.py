"""
Top Players page for Cricbuzz LiveStats.
Provides batting leaders, bowling leaders, format filters, Plotly visualizations, and player profile drilldown.
"""

import streamlit as st
import os
import sys

# Ensure project root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pandas as pd
import plotly.express as px
from services.player_service import get_all_players, get_player_stats
from utils.db_connection import execute_query


def render():
    """Render the Top Players page."""
    st.title("⭐ Top Player Statistics & Leaderboards")
    st.markdown("Analyze batting and bowling records across Test, ODI, and T20 formats.")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🏏 Batting Leaderboard", "🎳 Bowling Leaderboard", "👤 Player Deep Dive"])

    with tab1:
        st.markdown("### 🏏 Top Batting Performers")
        sel_format = st.selectbox("Filter Format", ["All", "ODI", "Test", "T20"], key="bat_leader_fmt")

        query = """
            SELECT p.name AS player_name,
                   p.country,
                   bs.format,
                   SUM(bs.runs) AS total_runs,
                   COUNT(*) AS innings_played,
                   ROUND(AVG(bs.runs), 2) AS batting_avg,
                   MAX(bs.runs) AS highest_score,
                   ROUND(AVG(bs.strike_rate), 2) AS avg_strike_rate,
                   SUM(CASE WHEN bs.runs >= 100 THEN 1 ELSE 0 END) AS centuries,
                   SUM(CASE WHEN bs.runs >= 50 AND bs.runs < 100 THEN 1 ELSE 0 END) AS fifties
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
        """
        if sel_format != "All":
            query += f" WHERE bs.format = '{sel_format}'"
        query += """
            GROUP BY p.player_id, p.name, p.country, bs.format
            ORDER BY total_runs DESC
            LIMIT 15;
        """
        try:
            df = execute_query(query)
            if not df.empty:
                # Podium KPI metrics
                kpi1, kpi2, kpi3 = st.columns(3)
                if len(df) > 0:
                    kpi1.metric(f"🥇 1st: {df.iloc[0]['player_name']}", f"{int(df.iloc[0]['total_runs'])} Runs", f"Avg {df.iloc[0]['batting_avg']}")
                if len(df) > 1:
                    kpi2.metric(f"🥈 2nd: {df.iloc[1]['player_name']}", f"{int(df.iloc[1]['total_runs'])} Runs", f"Avg {df.iloc[1]['batting_avg']}")
                if len(df) > 2:
                    kpi3.metric(f"🥉 3rd: {df.iloc[2]['player_name']}", f"{int(df.iloc[2]['total_runs'])} Runs", f"Avg {df.iloc[2]['batting_avg']}")

                st.markdown("---")

                # Plotly chart
                fig = px.bar(
                    df.head(10),
                    x='player_name',
                    y='total_runs',
                    color='country',
                    title=f"Top 10 Run Scorers ({sel_format})",
                    labels={'player_name': 'Player', 'total_runs': 'Total Runs', 'country': 'Country'},
                    text_auto=True,
                    color_discrete_sequence=px.colors.qualitative.Dark24
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No batting records found for the selected filter.")
        except Exception as e:
            st.error(f"Error loading batting leaderboard: {e}")

    with tab2:
        st.markdown("### 🎳 Top Bowling Performers")
        sel_format_bowl = st.selectbox("Filter Format", ["All", "ODI", "Test", "T20"], key="bowl_leader_fmt")

        query = """
            SELECT p.name AS player_name,
                   p.country,
                   bw.format,
                   SUM(bw.wickets) AS total_wickets,
                   COUNT(*) AS matches_bowled,
                   ROUND(AVG(bw.economy), 2) AS avg_economy,
                   ROUND(CAST(SUM(bw.runs_conceded) AS FLOAT) / NULLIF(SUM(bw.wickets), 0), 2) AS bowling_average,
                   SUM(CASE WHEN bw.wickets >= 5 THEN 1 ELSE 0 END) AS five_wicket_hauls
            FROM bowling_stats bw
            JOIN players p ON bw.player_id = p.player_id
        """
        if sel_format_bowl != "All":
            query += f" WHERE bw.format = '{sel_format_bowl}'"
        query += """
            GROUP BY p.player_id, p.name, p.country, bw.format
            ORDER BY total_wickets DESC
            LIMIT 15;
        """
        try:
            df = execute_query(query)
            if not df.empty:
                kpi1, kpi2, kpi3 = st.columns(3)
                if len(df) > 0:
                    kpi1.metric(f"🥇 1st: {df.iloc[0]['player_name']}", f"{int(df.iloc[0]['total_wickets'])} Wickets", f"Eco {df.iloc[0]['avg_economy']}")
                if len(df) > 1:
                    kpi2.metric(f"🥈 2nd: {df.iloc[1]['player_name']}", f"{int(df.iloc[1]['total_wickets'])} Wickets", f"Eco {df.iloc[1]['avg_economy']}")
                if len(df) > 2:
                    kpi3.metric(f"🥉 3rd: {df.iloc[2]['player_name']}", f"{int(df.iloc[2]['total_wickets'])} Wickets", f"Eco {df.iloc[2]['avg_economy']}")

                st.markdown("---")

                fig = px.bar(
                    df.head(10),
                    x='player_name',
                    y='total_wickets',
                    color='country',
                    title=f"Top 10 Wicket Takers ({sel_format_bowl})",
                    labels={'player_name': 'Player', 'total_wickets': 'Total Wickets', 'country': 'Country'},
                    text_auto=True,
                    color_discrete_sequence=px.colors.qualitative.Prism
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No bowling records found for the selected filter.")
        except Exception as e:
            st.error(f"Error loading bowling leaderboard: {e}")

    with tab3:
        st.markdown("### 👤 Player Performance Profile")
        players_df = get_all_players()
        if not players_df.empty:
            sel_player_name = st.selectbox("Select Player", players_df['name'].tolist(), key="profile_player_select")
            player_row = players_df[players_df['name'] == sel_player_name].iloc[0]
            pid = player_row['player_id']

            col_pinfo, col_pstats = st.columns([1, 2])
            with col_pinfo:
                st.markdown(f"#### {player_row['name']}")
                st.caption(f"Full Name: {player_row['full_name']}")
                st.write(f"**Country:** {player_row['country']}")
                st.write(f"**Role:** {player_row['playing_role']}")
                st.write(f"**Batting Style:** {player_row['batting_style']}")
                if player_row['bowling_style']:
                    st.write(f"**Bowling Style:** {player_row['bowling_style']}")

            with col_pstats:
                batting_df, bowling_df = get_player_stats(pid)
                if not batting_df.empty:
                    st.markdown("##### 🏏 Batting Career Summary")
                    st.dataframe(batting_df, use_container_width=True, hide_index=True)
                if not bowling_df.empty:
                    st.markdown("##### 🎳 Bowling Career Summary")
                    st.dataframe(bowling_df, use_container_width=True, hide_index=True)
                if batting_df.empty and bowling_df.empty:
                    st.info("No recorded stats for this player yet.")
        else:
            st.warning("No players registered in database.")


# Render immediately when script is executed
render()
