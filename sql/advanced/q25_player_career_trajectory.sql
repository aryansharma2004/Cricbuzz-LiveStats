-- Question 25: Player career trajectory and evolution
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
