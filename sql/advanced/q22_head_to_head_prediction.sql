-- Question 22: Head-to-head match prediction between teams
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
