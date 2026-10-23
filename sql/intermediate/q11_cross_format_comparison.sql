-- Question 11: Cross-format player comparison
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
