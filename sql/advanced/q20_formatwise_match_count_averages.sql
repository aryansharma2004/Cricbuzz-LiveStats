-- Question 20: Format-wise match count & batting average
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
