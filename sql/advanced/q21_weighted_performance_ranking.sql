-- Question 21: Weighted performance ranking system
-- Batting points: (runs_scored * 0.01) + (batting_average * 0.5) + (strike_rate * 0.3)
-- Bowling points: (wickets_taken * 2) + ((50 - bowling_average) * 0.5) + ((6 - economy_rate) * 2)
-- Fielding points: (catches * 3) + (stumpings * 5)

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
