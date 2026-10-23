-- Question 14: Bowling performance by venue
SELECT p.name AS bowler_name,
       v.name AS venue_name,
       COUNT(*) AS matches_bowled,
       ROUND(AVG(bw.economy), 2) AS avg_economy_rate,
       SUM(bw.wickets) AS total_wickets
FROM bowling_stats bw
JOIN players p ON bw.player_id = p.player_id
JOIN matches m ON bw.match_id = m.match_id
LEFT JOIN venues v ON m.venue_id = v.venue_id
WHERE bw.overs >= 4.0
GROUP BY p.player_id, p.name, v.venue_id, v.name
HAVING matches_bowled >= 2
ORDER BY avg_economy_rate ASC;
