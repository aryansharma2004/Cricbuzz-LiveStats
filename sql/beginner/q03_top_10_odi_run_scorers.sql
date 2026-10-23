-- Question 3: Top 10 highest run scorers in ODI cricket
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
