"""
Player-related business logic and database CRUD operations.
"""

import pandas as pd
from utils.db_connection import execute_query, execute_insert, execute_update


def get_all_players(country=None, role=None):
    """Fetch players with optional country and playing role filters."""
    query = """
        SELECT p.player_id, p.name, p.full_name, p.country,
               p.playing_role, p.batting_style, p.bowling_style,
               p.dob, t.name AS team_name
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        WHERE 1=1
    """
    params = []
    if country:
        query += " AND p.country = ?"
        params.append(country)
    if role:
        query += " AND p.playing_role = ?"
        params.append(role)
    query += " ORDER BY p.name ASC"
    return execute_query(query, params)


def get_player_by_id(player_id):
    """Fetch player by ID."""
    query = """
        SELECT p.*, t.name AS team_name
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        WHERE p.player_id = ?
    """
    return execute_query(query, [player_id])


def add_player(data):
    """Insert a new player record."""
    query = """
        INSERT INTO players (name, full_name, country, playing_role,
                           batting_style, bowling_style, dob, team_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = [
        data['name'],
        data.get('full_name', data['name']),
        data['country'],
        data['playing_role'],
        data.get('batting_style'),
        data.get('bowling_style'),
        data.get('dob'),
        data.get('team_id')
    ]
    return execute_insert(query, params)


def update_player(player_id, data):
    """Update an existing player record."""
    query = """
        UPDATE players SET
            name = ?, full_name = ?, country = ?,
            playing_role = ?, batting_style = ?,
            bowling_style = ?, dob = ?, team_id = ?
        WHERE player_id = ?
    """
    params = [
        data['name'],
        data.get('full_name', data['name']),
        data['country'],
        data['playing_role'],
        data.get('batting_style'),
        data.get('bowling_style'),
        data.get('dob'),
        data.get('team_id'),
        player_id
    ]
    return execute_update(query, params)


def delete_player(player_id):
    """Delete a player and all their associated statistics."""
    execute_update("DELETE FROM batting_stats WHERE player_id = ?", [player_id])
    execute_update("DELETE FROM bowling_stats WHERE player_id = ?", [player_id])
    execute_update("DELETE FROM fielding_stats WHERE player_id = ?", [player_id])
    return execute_update("DELETE FROM players WHERE player_id = ?", [player_id])


def get_player_stats(player_id):
    """Get summarized batting and bowling stats for a player."""
    batting = execute_query("""
        SELECT format,
               SUM(runs) AS total_runs,
               COUNT(*) AS innings,
               ROUND(AVG(runs), 2) AS avg_runs,
               ROUND(AVG(strike_rate), 2) AS avg_sr,
               SUM(CASE WHEN runs >= 100 THEN 1 ELSE 0 END) AS centuries,
               SUM(CASE WHEN runs >= 50 AND runs < 100 THEN 1 ELSE 0 END) AS fifties,
               MAX(runs) AS highest_score
        FROM batting_stats
        WHERE player_id = ?
        GROUP BY format
    """, [player_id])

    bowling = execute_query("""
        SELECT format,
               SUM(wickets) AS total_wickets,
               COUNT(*) AS innings,
               ROUND(AVG(economy), 2) AS avg_economy,
               SUM(runs_conceded) AS runs_conceded,
               ROUND(CAST(SUM(runs_conceded) AS FLOAT) / NULLIF(SUM(wickets), 0), 2) AS bowling_avg,
               SUM(CASE WHEN wickets >= 5 THEN 1 ELSE 0 END) AS five_wickets
        FROM bowling_stats
        WHERE player_id = ?
        GROUP BY format
    """, [player_id])

    return batting, bowling


def get_countries():
    """Get distinct player countries."""
    df = execute_query("SELECT DISTINCT country FROM players WHERE country IS NOT NULL ORDER BY country")
    return df['country'].tolist() if not df.empty else []


def get_roles():
    """Get distinct playing roles."""
    df = execute_query("SELECT DISTINCT playing_role FROM players WHERE playing_role IS NOT NULL ORDER BY playing_role")
    return df['playing_role'].tolist() if not df.empty else []
