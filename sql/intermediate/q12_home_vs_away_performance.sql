-- Question 12: Home vs away performance analysis
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
