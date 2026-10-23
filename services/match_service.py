"""
Match-related business logic and database CRUD operations.
"""

import pandas as pd
from utils.db_connection import execute_query, execute_insert, execute_update


def get_all_matches(limit=50):
    """Fetch all matches with team and venue details."""
    query = """
        SELECT m.match_id, m.description, m.match_format, m.match_date,
               m.match_status, m.result, m.victory_margin, m.victory_type,
               m.toss_decision,
               t1.name AS team1, t2.name AS team2,
               w.name AS winner, tw.name AS toss_winner,
               v.name AS venue, v.city
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN teams w ON m.winner_id = w.team_id
        LEFT JOIN teams tw ON m.toss_winner_id = tw.team_id
        LEFT JOIN venues v ON m.venue_id = v.venue_id
        ORDER BY m.match_date DESC
        LIMIT ?
    """
    return execute_query(query, [limit])


def get_match_by_id(match_id):
    """Fetch a specific match record by primary key."""
    query = """
        SELECT m.*, t1.name AS team1, t2.name AS team2,
               v.name AS venue, v.city, s.name AS series_name
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN venues v ON m.venue_id = v.venue_id
        LEFT JOIN series s ON m.series_id = s.series_id
        WHERE m.match_id = ?
    """
    return execute_query(query, [match_id])


def add_match(data):
    """Insert a new match record into the database."""
    query = """
        INSERT INTO matches (series_id, match_type, match_format, team1_id, team2_id,
                            venue_id, match_date, match_status, result, description,
                            toss_winner_id, toss_decision, winner_id, victory_margin, victory_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = [
        data.get('series_id'),
        data.get('match_type') or data.get('match_format', 'ODI'),
        data.get('match_format', 'ODI'),
        data['team1_id'],
        data['team2_id'],
        data.get('venue_id'),
        data.get('match_date'),
        data.get('match_status', 'Upcoming'),
        data.get('result'),
        data.get('description'),
        data.get('toss_winner_id'),
        data.get('toss_decision'),
        data.get('winner_id'),
        data.get('victory_margin'),
        data.get('victory_type')
    ]
    return execute_insert(query, params)


def update_match(match_id, data):
    """Update an existing match record."""
    query = """
        UPDATE matches SET
            match_format = ?, match_date = ?, match_status = ?,
            result = ?, description = ?, winner_id = ?,
            victory_margin = ?, victory_type = ?,
            toss_winner_id = ?, toss_decision = ?
        WHERE match_id = ?
    """
    params = [
        data.get('match_format'),
        data.get('match_date'),
        data.get('match_status'),
        data.get('result'),
        data.get('description'),
        data.get('winner_id'),
        data.get('victory_margin'),
        data.get('victory_type'),
        data.get('toss_winner_id'),
        data.get('toss_decision'),
        match_id
    ]
    return execute_update(query, params)


def delete_match(match_id):
    """Delete a match and associated batting/bowling statistics."""
    execute_update("DELETE FROM batting_stats WHERE match_id = ?", [match_id])
    execute_update("DELETE FROM bowling_stats WHERE match_id = ?", [match_id])
    return execute_update("DELETE FROM matches WHERE match_id = ?", [match_id])
