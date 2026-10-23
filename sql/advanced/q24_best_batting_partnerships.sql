-- Question 24: Best batting partnerships combinations
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
