"""
CRUD Operations page for Cricbuzz LiveStats.
Provides comprehensive form-based Create, Read, Update, and Delete operations for Players and Matches.
"""

import streamlit as st
import os
import sys

# Ensure project root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pandas as pd
from services.player_service import (
    get_all_players, get_player_by_id, add_player,
    update_player, delete_player, get_countries, get_roles
)
from services.match_service import (
    get_all_matches, get_match_by_id, add_match,
    update_match, delete_match
)
from utils.db_connection import execute_query


def render():
    """Render the CRUD Operations page."""
    st.title("🛠️ CRUD Operations Console")
    st.markdown("Create, Read, Update, and Delete records in the relational cricket database.")
    st.markdown("---")

    entity = st.radio("Choose Entity to Manage:", ["👤 Players", "🏆 Matches"], horizontal=True, key="crud_entity_radio")

    if entity == "👤 Players":
        _render_player_crud()
    else:
        _render_match_crud()


def _render_player_crud():
    """Handle Player CRUD tabs."""
    tab_create, tab_read, tab_update, tab_delete = st.tabs(
        ["➕ Add New Player", "👁️ View Players Roster", "✏️ Edit Player", "🗑️ Delete Player"]
    )

    # 1. CREATE
    with tab_create:
        st.subheader("➕ Register a New Player")
        with st.form("create_player_form"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Short Name *", placeholder="e.g. Jasprit Bumrah")
                full_name = st.text_input("Full Official Name", placeholder="e.g. Jasprit Jasbirsingh Bumrah")
                country = st.text_input("Country *", placeholder="e.g. India")
                dob = st.text_input("Date of Birth (YYYY-MM-DD)", placeholder="1993-12-06")

            with c2:
                role = st.selectbox("Playing Role *", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
                bat_style = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat"])
                bowl_style = st.text_input("Bowling Style", placeholder="e.g. Right-arm fast")

                teams_df = execute_query("SELECT team_id, name FROM teams ORDER BY name")
                team_map = {row['name']: row['team_id'] for _, row in teams_df.iterrows()} if not teams_df.empty else {}
                sel_team = st.selectbox("National / Franchise Team", list(team_map.keys()) if team_map else ["None"])

            submit_btn = st.form_submit_button("✅ Save Player to Database", type="primary")

            if submit_btn:
                if not name.strip() or not country.strip():
                    st.error("Validation Error: 'Short Name' and 'Country' are required fields.")
                else:
                    try:
                        p_data = {
                            "name": name.strip(),
                            "full_name": full_name.strip() or name.strip(),
                            "country": country.strip(),
                            "playing_role": role,
                            "batting_style": bat_style,
                            "bowling_style": bowl_style.strip() if bowl_style else None,
                            "dob": dob.strip() if dob else None,
                            "team_id": team_map.get(sel_team)
                        }
                        new_id = add_player(p_data)
                        st.success(f"🎉 Success! Player '{name}' created with Player ID #{new_id}.")
                    except Exception as err:
                        st.error(f"Database Error: {err}")

    # 2. READ
    with tab_read:
        st.subheader("👁️ Current Players Directory")
        c1, c2 = st.columns(2)
        with c1:
            countries = ["All"] + get_countries()
            sel_country = st.selectbox("Filter Country", countries, key="read_country_sel")
        with c2:
            roles = ["All"] + get_roles()
            sel_role = st.selectbox("Filter Role", roles, key="read_role_sel")

        f_country = None if sel_country == "All" else sel_country
        f_role = None if sel_role == "All" else sel_role

        try:
            players_df = get_all_players(country=f_country, role=f_role)
            if not players_df.empty:
                st.metric("Total Matching Players", len(players_df))
                st.dataframe(players_df, use_container_width=True, hide_index=True)
            else:
                st.info("No players match the chosen filters.")
        except Exception as e:
            st.error(f"Fetch Error: {e}")

    # 3. UPDATE
    with tab_update:
        st.subheader("✏️ Update Player Information")
        players_df = get_all_players()
        if not players_df.empty:
            p_map = {f"{row['name']} (ID: {row['player_id']}, {row['country']})": row['player_id'] for _, row in players_df.iterrows()}
            chosen_label = st.selectbox("Select Player to Update", list(p_map.keys()), key="update_player_select")
            pid = p_map[chosen_label]
            target_p = get_player_by_id(pid).iloc[0]

            with st.form("edit_player_form"):
                c1, c2 = st.columns(2)
                with c1:
                    u_name = st.text_input("Name", value=target_p['name'])
                    u_full_name = st.text_input("Full Name", value=target_p['full_name'] or "")
                    u_country = st.text_input("Country", value=target_p['country'] or "")
                    u_dob = st.text_input("DOB", value=target_p['dob'] or "")
                with c2:
                    role_list = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
                    role_idx = role_list.index(target_p['playing_role']) if target_p['playing_role'] in role_list else 0
                    u_role = st.selectbox("Playing Role", role_list, index=role_idx)

                    bat_list = ["Right-hand bat", "Left-hand bat"]
                    bat_idx = bat_list.index(target_p['batting_style']) if target_p['batting_style'] in bat_list else 0
                    u_bat = st.selectbox("Batting Style", bat_list, index=bat_idx)

                    u_bowl = st.text_input("Bowling Style", value=target_p['bowling_style'] or "")

                    teams_df = execute_query("SELECT team_id, name FROM teams ORDER BY name")
                    team_list = teams_df['name'].tolist() if not teams_df.empty else []
                    curr_team = target_p.get('team_name')
                    t_idx = team_list.index(curr_team) if curr_team in team_list else 0
                    u_team = st.selectbox("Team", team_list, index=t_idx)
                    u_team_id = int(teams_df[teams_df['name'] == u_team]['team_id'].iloc[0]) if team_list else None

                save_update = st.form_submit_button("💾 Update Player", type="primary")
                if save_update:
                    try:
                        updated_data = {
                            "name": u_name,
                            "full_name": u_full_name,
                            "country": u_country,
                            "playing_role": u_role,
                            "batting_style": u_bat,
                            "bowling_style": u_bowl or None,
                            "dob": u_dob or None,
                            "team_id": u_team_id
                        }
                        update_player(pid, updated_data)
                        st.success(f"✅ Player ID #{pid} successfully updated! Refresh tab to see changes.")
                    except Exception as e:
                        st.error(f"Update failed: {e}")
        else:
            st.info("No players available to update.")

    # 4. DELETE
    with tab_delete:
        st.subheader("🗑️ Delete Player Record")
        players_df = get_all_players()
        if not players_df.empty:
            p_map = {f"{row['name']} (ID: {row['player_id']}, {row['country']})": row['player_id'] for _, row in players_df.iterrows()}
            del_label = st.selectbox("Select Player to Delete", list(p_map.keys()), key="delete_player_select")
            del_id = p_map[del_label]

            st.warning("⚠️ Deleting a player removes all their historical batting, bowling, and fielding statistics.")
            confirm_box = st.checkbox(f"Yes, I want to permanently remove {del_label}")

            if st.button("🚨 Permanently Delete Player", type="primary", disabled=not confirm_box):
                try:
                    delete_player(del_id)
                    st.success(f"Player #{del_id} and associated statistics were deleted.")
                except Exception as e:
                    st.error(f"Delete failed: {e}")
        else:
            st.info("No players available to delete.")


def _render_match_crud():
    """Handle Match CRUD tabs."""
    tab_create, tab_read, tab_update, tab_delete = st.tabs(
        ["➕ Add New Match", "👁️ View Matches Archive", "✏️ Edit Match", "🗑️ Delete Match"]
    )

    teams_df = execute_query("SELECT team_id, name FROM teams ORDER BY name")
    team_dict = {row['name']: row['team_id'] for _, row in teams_df.iterrows()} if not teams_df.empty else {}

    venues_df = execute_query("SELECT venue_id, name, city FROM venues ORDER BY name")
    venue_dict = {f"{row['name']} ({row['city']})": row['venue_id'] for _, row in venues_df.iterrows()} if not venues_df.empty else {}

    # 1. CREATE MATCH
    with tab_create:
        st.subheader("➕ Create Match Record")
        with st.form("create_match_form"):
            c1, c2 = st.columns(2)
            with c1:
                desc = st.text_input("Match Description *", placeholder="e.g. IND vs AUS, 1st ODI")
                team1 = st.selectbox("Team 1 *", list(team_dict.keys()), key="cm_t1")
                team2 = st.selectbox("Team 2 *", list(team_dict.keys()), key="cm_t2")
                venue = st.selectbox("Venue", list(venue_dict.keys()))
                m_date = st.text_input("Match Date (YYYY-MM-DD)", value="2025-03-01")

            with c2:
                m_fmt = st.selectbox("Format *", ["ODI", "Test", "T20"])
                m_status = st.selectbox("Status", ["Completed", "In Progress", "Upcoming"])
                result_str = st.text_input("Result Summary", placeholder="e.g. India won by 6 wickets")
                winner_sel = st.selectbox("Winner Team", ["None"] + list(team_dict.keys()))
                v_type = st.selectbox("Victory Type", ["", "Runs", "Wickets"])
                v_margin = st.number_input("Victory Margin", min_value=0, value=0)

            btn_submit = st.form_submit_button("💾 Save Match to Database", type="primary")
            if btn_submit:
                if not desc.strip() or team1 == team2:
                    st.error("Please enter a valid match description and ensure Team 1 and Team 2 are different.")
                else:
                    try:
                        m_data = {
                            "description": desc.strip(),
                            "team1_id": team_dict[team1],
                            "team2_id": team_dict[team2],
                            "venue_id": venue_dict.get(venue),
                            "match_date": m_date.strip(),
                            "match_format": m_fmt,
                            "match_status": m_status,
                            "result": result_str.strip() if result_str else None,
                            "winner_id": team_dict.get(winner_sel),
                            "victory_type": v_type if v_type else None,
                            "victory_margin": v_margin if v_margin > 0 else None
                        }
                        mid = add_match(m_data)
                        st.success(f"🎉 Match registered successfully with ID #{mid}!")
                    except Exception as e:
                        st.error(f"Error adding match: {e}")

    # 2. READ MATCHES
    with tab_read:
        st.subheader("👁️ Matches Archive")
        try:
            matches_df = get_all_matches(limit=100)
            if not matches_df.empty:
                st.dataframe(matches_df, use_container_width=True, hide_index=True)
            else:
                st.info("No matches stored in database.")
        except Exception as e:
            st.error(f"Error fetching matches: {e}")

    # 3. UPDATE MATCH
    with tab_update:
        st.subheader("✏️ Edit Match Record")
        matches_df = get_all_matches(limit=100)
        if not matches_df.empty:
            m_map = {f"{row['description']} (ID #{row['match_id']})": row['match_id'] for _, row in matches_df.iterrows()}
            chosen_m = st.selectbox("Select Match to Modify", list(m_map.keys()))
            mid = m_map[chosen_m]
            target_m = get_match_by_id(mid).iloc[0]

            with st.form("edit_match_form"):
                c1, c2 = st.columns(2)
                with c1:
                    u_desc = st.text_input("Description", value=target_m['description'])
                    u_date = st.text_input("Date", value=target_m['match_date'])
                    fmt_list = ["ODI", "Test", "T20"]
                    u_fmt = st.selectbox("Format", fmt_list, index=fmt_list.index(target_m['match_format']) if target_m['match_format'] in fmt_list else 0)
                with c2:
                    st_list = ["Completed", "In Progress", "Upcoming"]
                    u_status = st.selectbox("Status", st_list, index=st_list.index(target_m['match_status']) if target_m['match_status'] in st_list else 0)
                    u_result = st.text_input("Result", value=target_m['result'] or "")
                    u_margin = st.number_input("Victory Margin", value=int(target_m['victory_margin'] or 0))
                    vt_list = ["", "Runs", "Wickets"]
                    u_vt = st.selectbox("Victory Type", vt_list, index=vt_list.index(target_m['victory_type']) if target_m['victory_type'] in vt_list else 0)

                if st.form_submit_button("💾 Update Match Details", type="primary"):
                    try:
                        u_data = {
                            "description": u_desc,
                            "match_date": u_date,
                            "match_format": u_fmt,
                            "match_status": u_status,
                            "result": u_result,
                            "victory_margin": u_margin or None,
                            "victory_type": u_vt or None
                        }
                        update_match(mid, u_data)
                        st.success(f"Match #{mid} updated successfully! Refresh tab to see changes.")
                    except Exception as e:
                        st.error(f"Update Error: {e}")
        else:
            st.info("No matches available to edit.")

    # 4. DELETE MATCH
    with tab_delete:
        st.subheader("🗑️ Delete Match Record")
        matches_df = get_all_matches(limit=100)
        if not matches_df.empty:
            m_map = {f"{row['description']} (ID #{row['match_id']})": row['match_id'] for _, row in matches_df.iterrows()}
            chosen_del = st.selectbox("Select Match to Delete", list(m_map.keys()), key="del_m_sel")
            del_mid = m_map[chosen_del]

            st.warning("⚠️ Deleting a match will cascade delete its scorecards and player innings records.")
            conf = st.checkbox(f"Confirm deletion of Match #{del_mid}")
            if st.button("🚨 Permanently Delete Match", type="primary", disabled=not conf):
                try:
                    delete_match(del_mid)
                    st.success(f"Match #{del_mid} deleted successfully!")
                except Exception as e:
                    st.error(f"Delete Error: {e}")
        else:
            st.info("No matches available to delete.")


# Render immediately when script is executed
render()
