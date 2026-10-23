-- Question 15: Player performance in close matches
SELECT p.name AS player_name,
       ROUND(AVG(bs.runs), 2) AS avg_runs_close_matches,
       COUNT(DISTINCT bs.match_id) AS close_matches_played,
       SUM(CASE WHEN m.winner_id = bs.team_id THEN 1 ELSE 0 END) AS team_wins_when_batted
FROM batting_stats bs
JOIN players p ON bs.player_id = p.player_id
JOIN matches m ON bs.match_id = m.match_id
WHERE (m.victory_type = 'Runs' AND m.victory_margin < 50)
   OR (m.victory_type = 'Wickets' AND m.victory_margin < 5)
GROUP BY p.player_id, p.name
HAVING close_matches_played >= 1
ORDER BY avg_runs_close_matches DESC;
