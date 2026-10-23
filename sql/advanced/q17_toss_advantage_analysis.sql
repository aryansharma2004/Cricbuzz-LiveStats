-- Question 17: Toss advantage analysis (Bat vs Bowl first)
SELECT m.toss_decision,
       COUNT(*) AS total_matches,
       SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) AS toss_winner_wins,
       ROUND(100.0 * SUM(CASE WHEN m.toss_winner_id = m.winner_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_percentage
FROM matches m
WHERE m.winner_id IS NOT NULL AND m.toss_decision IS NOT NULL
GROUP BY m.toss_decision
ORDER BY win_percentage DESC;
