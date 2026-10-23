-- Question 18: Most economical bowlers in limited-overs cricket
SELECT p.name AS bowler_name,
       bw.format,
       ROUND(SUM(bw.runs_conceded) * 1.0 / NULLIF(SUM(bw.overs), 0), 2) AS overall_economy,
       SUM(bw.wickets) AS total_wickets,
       COUNT(*) AS matches_bowled
FROM bowling_stats bw
JOIN players p ON bw.player_id = p.player_id
WHERE bw.format IN ('ODI', 'T20')
  AND bw.overs >= 2.0
GROUP BY p.player_id, p.name, bw.format
HAVING matches_bowled >= 2
ORDER BY overall_economy ASC;
