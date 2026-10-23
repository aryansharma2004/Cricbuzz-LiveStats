-- Question 5: Match wins per team
SELECT t.name AS team_name,
       COUNT(m.match_id) AS total_wins
FROM matches m
JOIN teams t ON m.winner_id = t.team_id
GROUP BY t.team_id, t.name
ORDER BY total_wins DESC;
