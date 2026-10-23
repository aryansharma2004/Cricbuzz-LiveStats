"""
SQL Queries & Analytics page for Cricbuzz LiveStats.
Provides execution and visualization of 25 pre-built SQL questions plus custom SQL query console.
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
from services.stats_service import get_query_list, run_query
from utils.db_connection import execute_query


def render():
    """Render the SQL Analytics page."""
    st.title("📊 SQL Queries & Advanced Analytics")
    st.markdown("Run 25 production-grade SQL analytical questions on cricket matches and player performance.")
    st.markdown("---")

    queries = get_query_list()

    # Filter controls
    c1, c2 = st.columns([1, 3])
    with c1:
        lvl_filter = st.selectbox("Difficulty Level", ["All", "Beginner", "Intermediate", "Advanced"], key="analytics_lvl_filter")
    with c2:
        available_queries = queries if lvl_filter == "All" else [q for q in queries if q["level"] == lvl_filter]
        query_map = {f"Q{q['id']}: {q['title'].split(': ', 1)[-1]}": q['id'] for q in available_queries}
        selected_label = st.selectbox("Select SQL Question", list(query_map.keys()), key="analytics_query_select")

    if not selected_label:
        st.info("No queries found.")
        return

    selected_id = query_map[selected_label]
    q_data = next(q for q in queries if q['id'] == selected_id)

    # Question Details Card
    st.markdown("---")
    head_col, badge_col = st.columns([4, 1])
    with head_col:
        st.subheader(q_data['title'])
        st.write(f"**Business Problem:** {q_data['description']}")
        st.caption(f"🧠 **SQL Concepts:** `{q_data['concepts']}`")
    with badge_col:
        lvl = q_data['level']
        if lvl == "Beginner":
            st.success("🟢 Beginner (Q1-8)")
        elif lvl == "Intermediate":
            st.warning("🟡 Intermediate (Q9-16)")
        else:
            st.error("🔴 Advanced (Q17-25)")

    # Execute button
    run_btn = st.button("▶️ Execute Query", type="primary", key="btn_run_analytic_query")

    from services.stats_service import SQL_QUERIES
    sql_text = SQL_QUERIES[selected_id]["query"].strip()

    with st.expander("📝 View Raw SQL Query", expanded=False):
        st.code(sql_text, language="sql")

    # Automatically execute or on button click
    if run_btn or f"ran_q_{selected_id}" not in st.session_state:
        st.session_state[f"ran_q_{selected_id}"] = True
        with st.spinner("Executing SQL query on database..."):
            try:
                results, _ = run_query(selected_id)
                if not results.empty:
                    st.success(f"✅ Success! Returned {len(results)} record(s).")
                    st.dataframe(results, use_container_width=True, hide_index=True)

                    # Dynamic Visualizations
                    _render_chart(selected_id, results)

                    # CSV Download
                    csv_bytes = results.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv_bytes,
                        file_name=f"cricbuzz_q{selected_id}_results.csv",
                        mime="text/csv",
                        key=f"csv_dl_{selected_id}"
                    )
                else:
                    st.warning("Query executed successfully but returned 0 rows.")
            except Exception as e:
                st.error(f"Execution Error: {e}")

    st.markdown("---")

    # Custom SQL Query Console
    st.subheader("💻 Interactive SQL Query Console")
    st.caption("Execute custom SELECT queries directly against `cricbuzz.db`.")
    user_sql = st.text_area(
        "SQL Editor:",
        height=100,
        placeholder="SELECT p.name, p.country, COUNT(*) as matches FROM players p JOIN batting_stats bs ON p.player_id = bs.player_id GROUP BY p.player_id LIMIT 5;",
        key="custom_sql_input"
    )
    if st.button("▶️ Run Custom SQL", key="btn_custom_sql"):
        if user_sql.strip():
            forbidden = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "INSERT"]
            first_word = user_sql.strip().split()[0].upper()
            if first_word in forbidden:
                st.error("⚠️ Only SELECT queries are permitted in the SQL Analytics console. Use the CRUD Operations page for data modification.")
            else:
                try:
                    res = execute_query(user_sql)
                    st.success(f"Query returned {len(res)} record(s)")
                    st.dataframe(res, use_container_width=True, hide_index=True)
                except Exception as err:
                    st.error(f"SQL Error: {err}")
        else:
            st.warning("Please type a valid SQL query.")


def _render_chart(qid, df):
    """Render contextual Plotly visualizations for analytical queries."""
    try:
        if qid == 3 and 'player_name' in df.columns:
            fig = px.bar(df, x='player_name', y='total_runs', text_auto=True,
                         title="Top 10 ODI Run Scorers", color='total_runs', color_continuous_scale="Viridis")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 4 and 'venue_name' in df.columns:
            fig = px.bar(df, x='venue_name', y='capacity', text_auto=True,
                         title="Venues with > 50,000 Capacity", color='country')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 5 and 'team_name' in df.columns:
            fig = px.pie(df, names='team_name', values='total_wins',
                         title="Match Wins by Team", hole=0.35)
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 6 and 'playing_role' in df.columns:
            fig = px.pie(df, names='playing_role', values='player_count',
                         title="Player Roster Distribution by Playing Role")
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 7 and 'format' in df.columns:
            fig = px.bar(df, x='format', y='highest_score', text_auto=True,
                         title="Highest Individual Score per Format", color='format')
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 11 and 'player_name' in df.columns:
            melted = df.melt(id_vars=['player_name'], value_vars=['test_runs', 'odi_runs', 't20_runs'],
                             var_name='Format', value_name='Runs')
            fig = px.bar(melted, x='player_name', y='Runs', color='Format', barmode='group',
                         title="Cross-Format Performance Comparison")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 12 and 'team_name' in df.columns:
            fig = px.bar(df, x='team_name', y=['home_wins', 'away_wins'], barmode='group',
                         title="Home vs Away Wins Comparison")
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 17 and 'toss_decision' in df.columns:
            fig = px.bar(df, x='toss_decision', y='win_percentage', text_auto=True,
                         title="Toss Advantage: Win % by Toss Decision", color='toss_decision')
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 21 and 'player_name' in df.columns and 'total_rank_score' in df.columns:
            fig = px.bar(df.head(10), x='player_name', y=['batting_score', 'bowling_score', 'fielding_score'],
                         title="Top 10 Weighted Player Rankings (Batting + Bowling + Fielding)", barmode='stack')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 23 and 'player_name' in df.columns and 'form_category' in df.columns:
            fig = px.scatter(df, x='last_5_avg', y='recent_sr', color='form_category',
                             hover_name='player_name', title="Player Momentum & Form Quadrant",
                             labels={'last_5_avg': 'Last 5 Batting Avg', 'recent_sr': 'Recent Strike Rate'})
            st.plotly_chart(fig, use_container_width=True)

        elif qid == 24 and 'batsman1' in df.columns:
            df['pair'] = df['batsman1'] + " & " + df['batsman2']
            fig = px.bar(df, x='pair', y='avg_partnership_runs', text_auto=True,
                         title="Average Partnership Runs for Consecutive Batsmen")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    except Exception:
        pass


# Render immediately when script is executed
render()
