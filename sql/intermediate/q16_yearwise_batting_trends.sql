-- Question 16: Year-wise batting trends (Matches since 2020)
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
