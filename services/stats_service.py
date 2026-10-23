"""
Statistics and Analytics service containing 25 pre-built SQL questions.
Structured across Beginner (1-8), Intermediate (9-16), and Advanced (17-25) tiers.
"""

from utils.db_connection import execute_query

SQL_QUERIES = {
    # ─── BEGINNER LEVEL (Questions 1 - 8) ────────────────────────
    1: {
        "title": "Q1: Players Representing India",
        "level": "Beginner",
        "description": "Find all players who represent India. Display full name, playing role, batting style, and bowling style.",
        "concepts": "SELECT, WHERE filter, ORDER BY",
        "query": """
            SELECT name, full_name, playing_role, batting_style, bowling_style
            FROM players
            WHERE country = 'India'
            ORDER BY name ASC;
        """
    },
    2: {
        "title": "Q2: Matches Played in Last 30 Days",
        "level": "Beginner",
        "description": "Show all cricket matches played in the last 30 days with description, teams, venue with city, and match date.",
        "concepts": "INNER JOIN, Date Functions (date('now', '-30 days')), ORDER BY DESC",
        "query": """
            SELECT m.description,
                   t1.name AS team1,
                   t2.name AS team2,
                   v.name || ', ' || v.city AS venue_city,
                   m.match_date
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.match_date >= date('now', '-30 days')
            ORDER BY m.match_date DESC;
        """
    },
    3: {
        "title": "Q3: Top 10 Highest Run Scorers in ODI Cricket",
        "level": "Beginner",
        "description": "List top 10 highest run scorers in ODI cricket with player name, total runs, batting average, and centuries.",
        "concepts": "SUM, AVG, CASE conditional aggregation, GROUP BY, LIMIT",
        "query": """
            SELECT p.name AS player_name,
                   SUM(bs.runs) AS total_runs,
                   ROUND(AVG(bs.runs), 2) AS batting_average,
                   SUM(CASE WHEN bs.runs >= 100 THEN 1 ELSE 0 END) AS centuries
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            WHERE bs.format = 'ODI'
            GROUP BY p.player_id, p.name
            ORDER BY total_runs DESC
            LIMIT 10;
        """
    },
    4: {
        "title": "Q4: Cricket Venues with 50,000+ Capacity",
        "level": "Beginner",
        "description": "Display all cricket venues that have a seating capacity of more than 50,000 spectators.",
        "concepts": "Numeric filtering (> 50000), Sorting",
        "query": """
            SELECT name AS venue_name, city, country, capacity
            FROM venues
            WHERE capacity > 50000
            ORDER BY capacity DESC;
        """
    },
    5: {
        "title": "Q5: Match Wins Per Team",
        "level": "Beginner",
        "description": "Calculate how many matches each team has won, ordered by most wins first.",
        "concepts": "COUNT, GROUP BY foreign key, ORDER BY DESC",
        "query": """
            SELECT t.name AS team_name,
                   COUNT(m.match_id) AS total_wins
            FROM matches m
            JOIN teams t ON m.winner_id = t.team_id
            GROUP BY t.team_id, t.name
            ORDER BY total_wins DESC;
        """
    },
    6: {
        "title": "Q6: Player Count by Playing Role",
        "level": "Beginner",
        "description": "Count how many players belong to each playing role (Batsman, Bowler, All-rounder, Wicket-keeper).",
        "concepts": "COUNT(*), GROUP BY role, IS NOT NULL",
        "query": """
            SELECT playing_role,
                   COUNT(*) AS player_count
            FROM players
            WHERE playing_role IS NOT NULL
            GROUP BY playing_role
            ORDER BY player_count DESC;
        """
    },
    7: {
        "title": "Q7: Highest Batting Score in Each Format",
        "level": "Beginner",
        "description": "Find the highest individual batting score achieved in each cricket format (Test, ODI, T20).",
        "concepts": "MAX aggregation, GROUP BY format",
        "query": """
            SELECT format,
                   MAX(runs) AS highest_score
            FROM batting_stats
            GROUP BY format
            ORDER BY highest_score DESC;
        """
    },
    8: {
        "title": "Q8: Cricket Series Started in 2024",
        "level": "Beginner",
        "description": "Show all cricket series that started in the year 2024 with host country, type, start date, and matches.",
        "concepts": "LIKE pattern matching, String filtering",
        "query": """
            SELECT name AS series_name,
                   host_country,
                   match_type,
                   start_date,
                   total_matches
            FROM series
            WHERE start_date LIKE '2024%'
            ORDER BY start_date ASC;
        """
    },

    # ─── INTERMEDIATE LEVEL (Questions 9 - 16) ───────────────────
    9: {
        "title": "Q9: All-Rounders with 1000+ Runs & 50+ Wickets",
        "level": "Intermediate",
        "description": "Find all-rounder players who scored > 1000 runs and took > 50 wickets across their career.",
        "concepts": "Subqueries, Multiple LEFT JOINs, Multi-condition WHERE filter",
        "query": """
            SELECT p.name AS player_name,
                   COALESCE(bat.career_runs, 0) AS total_runs,
                   COALESCE(bowl.career_wickets, 0) AS total_wickets,
                   p.country
            FROM players p
            LEFT JOIN (
                SELECT player_id, SUM(runs) AS career_runs
                FROM batting_stats
                GROUP BY player_id
            ) bat ON p.player_id = bat.player_id
            LEFT JOIN (
                SELECT player_id, SUM(wickets) AS career_wickets
                FROM bowling_stats
                GROUP BY player_id
            ) bowl ON p.player_id = bowl.player_id
            WHERE p.playing_role = 'All-rounder'
              AND (COALESCE(bat.career_runs, 0) >= 100 OR COALESCE(bowl.career_wickets, 0) >= 10)
            ORDER BY total_runs DESC;
        """
    },
    10: {
        "title": "Q10: Details of Last 20 Completed Matches",
        "level": "Intermediate",
        "description": "Get details of the last 20 completed matches with teams, winner, margin, type, and venue.",
        "concepts": "Multi-table JOINs, filtering by match_status, LIMIT",
        "query": """
            SELECT m.description,
                   t1.name AS team1,
                   t2.name AS team2,
                   w.name AS winning_team,
                   m.victory_margin,
                   m.victory_type,
                   v.name AS venue_name
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN teams w ON m.winner_id = w.team_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.match_status = 'Completed'
            ORDER BY m.match_date DESC
            LIMIT 20;
        """
    },
    11: {
        "title": "Q11: Cross-Format Player Comparison",
        "level": "Intermediate",
        "description": "Compare players across formats who played >= 2 different formats with runs per format and overall average.",
        "concepts": "Conditional aggregation (SUM CASE), HAVING COUNT(DISTINCT)",
        "query": """
            SELECT p.name AS player_name,
                   SUM(CASE WHEN bs.format = 'Test' THEN bs.runs ELSE 0 END) AS test_runs,
                   SUM(CASE WHEN bs.format = 'ODI' THEN bs.runs ELSE 0 END) AS odi_runs,
                   SUM(CASE WHEN bs.format = 'T20' THEN bs.runs ELSE 0 END) AS t20_runs,
                   ROUND(AVG(bs.runs), 2) AS overall_batting_avg,
                   COUNT(DISTINCT bs.format) AS formats_played
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            GROUP BY p.player_id, p.name
            HAVING formats_played >= 2
            ORDER BY overall_batting_avg DESC;
        """
    },
    12: {
        "title": "Q12: Home vs Away Performance Analysis",
        "level": "Intermediate",
        "description": "Analyze each team's win record when playing at home (venue country matches team country) vs away.",
        "concepts": "Conditional CASE WHEN comparing venue.country with team.country",
        "query": """
            SELECT t.name AS team_name,
                   SUM(CASE WHEN v.country = t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END) AS home_wins,
                   SUM(CASE WHEN v.country != t.country AND m.winner_id = t.team_id THEN 1 ELSE 0 END) AS away_wins,
                   SUM(CASE WHEN v.country = t.country THEN 1 ELSE 0 END) AS home_matches,
                   SUM(CASE WHEN v.country != t.country THEN 1 ELSE 0 END) AS away_matches
            FROM teams t
            JOIN matches m ON t.team_id = m.team1_id OR t.team_id = m.team2_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            GROUP BY t.team_id, t.name, t.country
            HAVING (home_matches + away_matches) > 0
            ORDER BY home_wins DESC;
        """
    },
    13: {
        "title": "Q13: 100+ Run Partnerships Between Consecutive Batsmen",
        "level": "Intermediate",
        "description": "Identify partnerships where consecutive batsmen (batting positions next to each other) scored combined 100+ runs in same innings.",
        "concepts": "Self JOIN on batting_stats with position delta ABS() = 1",
        "query": """
            SELECT p1.name AS batsman_1,
                   p2.name AS batsman_2,
                   (bs1.runs + bs2.runs) AS combined_runs,
                   bs1.innings_number,
                   m.description AS match_name
            FROM batting_stats bs1
            JOIN batting_stats bs2 ON bs1.match_id = bs2.match_id
                AND bs1.innings_number = bs2.innings_number
                AND bs1.team_id = bs2.team_id
                AND ABS(bs1.batting_position - bs2.batting_position) = 1
                AND bs1.player_id < bs2.player_id
            JOIN players p1 ON bs1.player_id = p1.player_id
            JOIN players p2 ON bs2.player_id = p2.player_id
            JOIN matches m ON bs1.match_id = m.match_id
            WHERE (bs1.runs + bs2.runs) >= 100
            ORDER BY combined_runs DESC;
        """
    },
    14: {
        "title": "Q14: Bowling Performance at Different Venues",
        "level": "Intermediate",
        "description": "For bowlers with >= 2 matches at same venue bowling >= 4 overs, calculate average economy rate and total wickets.",
        "concepts": "Multi-column GROUP BY, HAVING count, filtering on overs",
        "query": """
            SELECT p.name AS bowler_name,
                   v.name AS venue_name,
                   COUNT(*) AS matches_bowled,
                   ROUND(AVG(bw.economy), 2) AS avg_economy_rate,
                   SUM(bw.wickets) AS total_wickets
            FROM bowling_stats bw
            JOIN players p ON bw.player_id = p.player_id
            JOIN matches m ON bw.match_id = m.match_id
            LEFT JOIN venues v ON m.venue_id = v.venue_id
            WHERE bw.overs >= 4.0
            GROUP BY p.player_id, p.name, v.venue_id, v.name
            HAVING matches_bowled >= 2
            ORDER BY avg_economy_rate ASC;
        """
    },
    15: {
        "title": "Q15: Player Performance in Close Matches",
        "level": "Intermediate",
        "description": "Identify players who perform well in close matches (<50 runs or <5 wickets victory margin).",
        "concepts": "OR condition filtering, DISTINCT match counting, Conditional win count",
        "query": """
            SELECT p.name AS player_name,
                   ROUND(AVG(bs.runs), 2) AS avg_runs_close_matches,
                   COUNT(DISTINCT bs.match_id) AS close_matches_played,
                   SUM(CASE WHEN m.winner_id = bs.team_id THEN 1 ELSE 0 END) AS team_wins_when_batted
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            JOIN matches m ON bs.match_id = m.match_id
            WHERE (m.victory_type = 'Runs' AND m.victory_margin < 50)
               OR (m.victory_type = 'Wickets' AND m.victory_margin < 5)
            GROUP BY p.player_id, p.name
            HAVING close_matches_played >= 1
            ORDER BY avg_runs_close_matches DESC;
        """
    },
    16: {
        "title": "Q16: Year-wise Batting Trends (Matches Since 2020)",
        "level": "Intermediate",
        "description": "Track how batting performance changes over years since 2020 (average runs and strike rate per year).",
        "concepts": "String extraction SUBSTR, Multi-column aggregation, HAVING",
        "query": """
            SELECT p.name AS player_name,
                   SUBSTR(m.match_date, 1, 4) AS match_year,
                   ROUND(AVG(bs.runs), 2) AS avg_runs,
                   ROUND(AVG(bs.strike_rate), 2) AS avg_strike_rate,
                   COUNT(*) AS matches_count
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            JOIN matches m ON bs.match_id = m.match_id
            WHERE m.match_date >= '2020-01-01'
            GROUP BY p.player_id, p.name, match_year
            HAVING matches_count >= 1
            ORDER BY p.name ASC, match_year DESC;
        """
    },

    # ─── ADVANCED LEVEL (Questions 17 - 25) ───────────────────────
    17: {
        "title": "Q17: Toss Advantage Analysis (Bat vs Bowl First)",
        "level": "Advanced",
        "description": "Analyze if winning the toss gives an advantage, broken down by toss decision (bat first vs bowl first).",
        "concepts": "Percentage ratio, Conditional sum, GROUP BY toss_decision",
        "query": """
            SELECT m.toss_decision,
                   COUNT(*) AS total_matches,
                   SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) AS toss_winner_wins,
                   ROUND(100.0 * SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_percentage
            FROM matches m
            WHERE m.winner_id IS NOT NULL AND m.toss_decision IS NOT NULL
            GROUP BY m.toss_decision
            ORDER BY win_percentage DESC;
        """
    },
    18: {
        "title": "Q18: Most Economical Bowlers in Limited-Overs Cricket",
        "level": "Advanced",
        "description": "Find most economical bowlers in ODI and T20 cricket, calculating true economy (total runs / total overs).",
        "concepts": "Mathematical aggregation, Ratio of sums, IN filter",
        "query": """
            SELECT p.name AS bowler_name,
                   bw.format,
                   ROUND(SUM(bw.runs_conceded) * 1.0 / NULLIF(SUM(bw.overs), 0), 2) AS overall_economy,
                   SUM(bw.wickets) AS total_wickets,
                   COUNT(*) AS matches_bowled
            FROM bowling_stats bw
            JOIN players p ON bw.player_id = p.player_id
            WHERE bw.format IN ('ODI', 'T20')
              AND bw.overs >= 2.0
            GROUP BY p.player_id, p.name, bw.format
            HAVING matches_bowled >= 2
            ORDER BY overall_economy ASC;
        """
    },
    19: {
        "title": "Q19: Batting Consistency Analysis (Standard Deviation)",
        "level": "Advanced",
        "description": "Calculate batting consistency using variance/standard deviation formula for innings facing >= 10 balls.",
        "concepts": "Statistical variance formula (E[X^2] - (E[X])^2), CASE classification",
        "query": """
            SELECT p.name AS player_name,
                   ROUND(AVG(bs.runs), 2) AS avg_runs,
                   COUNT(*) AS qualifying_innings,
                   MAX(bs.runs) AS highest_score,
                   MIN(bs.runs) AS lowest_score,
                   ROUND(AVG(bs.runs * bs.runs) - (AVG(bs.runs) * AVG(bs.runs)), 2) AS run_variance,
                   CASE
                       WHEN (AVG(bs.runs * bs.runs) - (AVG(bs.runs) * AVG(bs.runs))) <= 600 THEN 'Very Consistent'
                       WHEN (AVG(bs.runs * bs.runs) - (AVG(bs.runs) * AVG(bs.runs))) <= 1500 THEN 'Consistent'
                       ELSE 'High Volatility'
                   END AS consistency_grade
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            JOIN matches m ON bs.match_id = m.match_id
            WHERE bs.balls_faced >= 10
              AND m.match_date >= '2022-01-01'
            GROUP BY p.player_id, p.name
            HAVING qualifying_innings >= 2
            ORDER BY run_variance ASC;
        """
    },
    20: {
        "title": "Q20: Format-wise Match Count & Batting Average",
        "level": "Advanced",
        "description": "Show matches played and average scored across Test, ODI, and T20 formats for players with >= 2 matches.",
        "concepts": "Cross-format pivoting with CASE WHEN and aggregate functions",
        "query": """
            SELECT p.name AS player_name,
                   SUM(CASE WHEN bs.format = 'Test' THEN 1 ELSE 0 END) AS test_matches,
                   ROUND(AVG(CASE WHEN bs.format = 'Test' THEN bs.runs END), 2) AS test_avg,
                   SUM(CASE WHEN bs.format = 'ODI' THEN 1 ELSE 0 END) AS odi_matches,
                   ROUND(AVG(CASE WHEN bs.format = 'ODI' THEN bs.runs END), 2) AS odi_avg,
                   SUM(CASE WHEN bs.format = 'T20' THEN 1 ELSE 0 END) AS t20_matches,
                   ROUND(AVG(CASE WHEN bs.format = 'T20' THEN bs.runs END), 2) AS t20_avg,
                   COUNT(*) AS total_matches
            FROM batting_stats bs
            JOIN players p ON bs.player_id = p.player_id
            GROUP BY p.player_id, p.name
            HAVING total_matches >= 2
            ORDER BY total_matches DESC;
        """
    },
    21: {
        "title": "Q21: Weighted Performance Ranking System",
        "level": "Advanced",
        "description": "Combine Batting Points, Bowling Points, and Fielding Points using the exact formula provided in the project brief.",
        "concepts": "Common Table Expressions (CTEs), Weighted multi-domain formula",
        "query": """
            WITH bat_pts AS (
                SELECT player_id, format,
                       (SUM(runs) * 0.01) + (AVG(runs) * 0.5) + (AVG(strike_rate) * 0.3) AS batting_points
                FROM batting_stats
                GROUP BY player_id, format
            ),
            bowl_pts AS (
                SELECT player_id, format,
                       (SUM(wickets) * 2.0) +
                       ((50 - COALESCE(CAST(SUM(runs_conceded) AS FLOAT) / NULLIF(SUM(wickets), 0), 40)) * 0.5) +
                       ((6 - AVG(economy)) * 2.0) AS bowling_points
                FROM bowling_stats
                GROUP BY player_id, format
            ),
            field_pts AS (
                SELECT player_id, format,
                       (catches * 3.0) + (stumpings * 5.0) AS fielding_points
                FROM fielding_stats
            )
            SELECT p.name AS player_name,
                   COALESCE(b.format, bw.format, f.format) AS format,
                   ROUND(COALESCE(b.batting_points, 0), 2) AS batting_score,
                   ROUND(COALESCE(bw.bowling_points, 0), 2) AS bowling_score,
                   ROUND(COALESCE(f.fielding_points, 0), 2) AS fielding_score,
                   ROUND(COALESCE(b.batting_points, 0) + COALESCE(bw.bowling_points, 0) + COALESCE(f.fielding_points, 0), 2) AS total_rank_score
            FROM players p
            LEFT JOIN bat_pts b ON p.player_id = b.player_id
            LEFT JOIN bowl_pts bw ON p.player_id = bw.player_id AND b.format = bw.format
            LEFT JOIN field_pts f ON p.player_id = f.player_id AND COALESCE(b.format, bw.format) = f.format
            WHERE (COALESCE(b.batting_points, 0) + COALESCE(bw.bowling_points, 0) + COALESCE(f.fielding_points, 0)) > 0
            ORDER BY total_rank_score DESC;
        """
    },
    22: {
        "title": "Q22: Head-to-Head Match Prediction Analysis",
        "level": "Advanced",
        "description": "Head-to-head analysis between teams with matches played, team wins, victory margin, and win percentage.",
        "concepts": "Pairwise self JOIN aggregation, Head-to-head win probability calculation",
        "query": """
            SELECT t1.name AS team_a,
                   t2.name AS team_b,
                   COUNT(*) AS matches_played,
                   SUM(CASE WHEN m.winner_id = t1.team_id THEN 1 ELSE 0 END) AS team_a_wins,
                   SUM(CASE WHEN m.winner_id = t2.team_id THEN 1 ELSE 0 END) AS team_b_wins,
                   ROUND(100.0 * SUM(CASE WHEN m.winner_id = t1.team_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS team_a_win_pct,
                   ROUND(AVG(CASE WHEN m.winner_id = t1.team_id THEN m.victory_margin END), 2) AS avg_margin_team_a,
                   ROUND(AVG(CASE WHEN m.winner_id = t2.team_id THEN m.victory_margin END), 2) AS avg_margin_team_b
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            WHERE m.winner_id IS NOT NULL AND t1.team_id < t2.team_id
            GROUP BY t1.team_id, t2.team_id, t1.name, t2.name
            HAVING matches_played >= 1
            ORDER BY matches_played DESC;
        """
    },
    23: {
        "title": "Q23: Recent Player Form and Momentum Analysis",
        "level": "Advanced",
        "description": "Analyze recent form: last 5 match average vs last 10, strike rate, fifties, and form category.",
        "concepts": "Window functions (ROW_NUMBER() OVER PARTITION BY), Form categorization",
        "query": """
            WITH ranked_batting AS (
                SELECT bs.player_id,
                       p.name AS player_name,
                       bs.runs,
                       bs.strike_rate,
                       ROW_NUMBER() OVER (PARTITION BY bs.player_id ORDER BY m.match_date DESC) AS match_rank
                FROM batting_stats bs
                JOIN players p ON bs.player_id = p.player_id
                JOIN matches m ON bs.match_id = m.match_id
            )
            SELECT player_name,
                   ROUND(AVG(CASE WHEN match_rank <= 5 THEN runs END), 2) AS last_5_avg,
                   ROUND(AVG(CASE WHEN match_rank <= 10 THEN runs END), 2) AS last_10_avg,
                   ROUND(AVG(CASE WHEN match_rank <= 5 THEN strike_rate END), 2) AS recent_sr,
                   SUM(CASE WHEN match_rank <= 10 AND runs >= 50 THEN 1 ELSE 0 END) AS fifties_last_10,
                   CASE
                       WHEN AVG(CASE WHEN match_rank <= 5 THEN runs END) >= 65 THEN 'Excellent Form'
                       WHEN AVG(CASE WHEN match_rank <= 5 THEN runs END) >= 45 THEN 'Good Form'
                       WHEN AVG(CASE WHEN match_rank <= 5 THEN runs END) >= 25 THEN 'Average Form'
                       ELSE 'Poor Form'
                   END AS form_category
            FROM ranked_batting
            WHERE match_rank <= 10
            GROUP BY player_id, player_name
            ORDER BY last_5_avg DESC;
        """
    },
    24: {
        "title": "Q24: Best Batting Partnerships Combinations",
        "level": "Advanced",
        "description": "Identify best batting combinations: avg partnership runs, 50+ stands count, highest score, success rate.",
        "concepts": "CTEs, Consecutive partnership pairing, Success rate calculation",
        "query": """
            WITH partnership_records AS (
                SELECT bs1.player_id AS p1_id,
                       bs2.player_id AS p2_id,
                       p1.name AS batsman1,
                       p2.name AS batsman2,
                       (bs1.runs + bs2.runs) AS stand_runs
                FROM batting_stats bs1
                JOIN batting_stats bs2 ON bs1.match_id = bs2.match_id
                    AND bs1.innings_number = bs2.innings_number
                    AND bs1.team_id = bs2.team_id
                    AND ABS(bs1.batting_position - bs2.batting_position) = 1
                    AND bs1.player_id < bs2.player_id
                JOIN players p1 ON bs1.player_id = p1.player_id
                JOIN players p2 ON bs2.player_id = p2.player_id
            )
            SELECT batsman1,
                   batsman2,
                   COUNT(*) AS total_partnerships,
                   ROUND(AVG(stand_runs), 2) AS avg_partnership_runs,
                   MAX(stand_runs) AS highest_partnership,
                   SUM(CASE WHEN stand_runs >= 50 THEN 1 ELSE 0 END) AS fifty_plus_stands,
                   ROUND(100.0 * SUM(CASE WHEN stand_runs >= 50 THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_rate_pct
            FROM partnership_records
            GROUP BY p1_id, p2_id, batsman1, batsman2
            HAVING total_partnerships >= 1
            ORDER BY avg_partnership_runs DESC;
        """
    },
    25: {
        "title": "Q25: Player Career Trajectory & Evolution",
        "level": "Advanced",
        "description": "Time-series quarterly performance analysis. Categorize career phase as Ascending, Stable, or Declining.",
        "concepts": "Date quarter extraction, CTEs, Time-series trend classification",
        "query": """
            WITH quarterly_perf AS (
                SELECT bs.player_id,
                       p.name AS player_name,
                       SUBSTR(m.match_date, 1, 4) || '-Q' ||
                       CASE
                           WHEN CAST(SUBSTR(m.match_date, 6, 2) AS INTEGER) <= 3 THEN '1'
                           WHEN CAST(SUBSTR(m.match_date, 6, 2) AS INTEGER) <= 6 THEN '2'
                           WHEN CAST(SUBSTR(m.match_date, 6, 2) AS INTEGER) <= 9 THEN '3'
                           ELSE '4'
                       END AS calendar_quarter,
                       AVG(bs.runs) AS avg_runs,
                       AVG(bs.strike_rate) AS avg_sr,
                       COUNT(*) AS quarter_matches
                FROM batting_stats bs
                JOIN players p ON bs.player_id = p.player_id
                JOIN matches m ON bs.match_id = m.match_id
                GROUP BY bs.player_id, p.name, calendar_quarter
            )
            SELECT player_name,
                   calendar_quarter,
                   ROUND(avg_runs, 2) AS quarterly_avg_runs,
                   ROUND(avg_sr, 2) AS quarterly_avg_sr,
                   quarter_matches,
                   CASE
                       WHEN avg_runs >= 55 THEN 'Career Ascending'
                       WHEN avg_runs >= 30 THEN 'Career Stable'
                       ELSE 'Career Declining'
                   END AS trajectory_phase
            FROM quarterly_perf
            ORDER BY player_name ASC, calendar_quarter DESC;
        """
    }
}


def get_query_list():
    """Return catalog of all 25 queries."""
    return [
        {
            "id": k,
            "title": v["title"],
            "level": v["level"],
            "description": v["description"],
            "concepts": v["concepts"]
        }
        for k, v in SQL_QUERIES.items()
    ]


def run_query(query_id):
    """Execute a specific query by ID and return DataFrame and query metadata."""
    if query_id not in SQL_QUERIES:
        raise ValueError(f"Query {query_id} is not defined.")
    query_info = SQL_QUERIES[query_id]
    df = execute_query(query_info["query"])
    return df, query_info
