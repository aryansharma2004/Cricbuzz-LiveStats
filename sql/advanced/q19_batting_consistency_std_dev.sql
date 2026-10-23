-- Question 19: Batting consistency analysis (Standard deviation)
SELECT p.name AS player_name,
       ROUND(AVG(bs.runs), 2) AS avg_runs,
       COUNT(*) AS qualifying_innings,
       MAX(bs.runs) AS highest_score,
       MIN(bs.runs) AS lowest_score,
       ROUND(AVG(bs.runs * bs.runs) - (AVG(bs.runs) * AVG(bs.runs)), 2) AS run_variance,
       CASE
           WHEN (AVG(bs.runs * bs.runs) - (AVG(bs.runs) * AVG(bs.runs))) <= 600 THEN 'Very Consistent'
           WHEN (AVG(bs.runs * bs.runs) - (AVG(bs.runs) * AVG(bs.runs))) <= 1500 THEN 'Consistent'
           ELSE 'High Volatility'
       END AS consistency_grade
FROM batting_stats bs
JOIN players p ON bs.player_id = p.player_id
JOIN matches m ON bs.match_id = m.match_id
WHERE bs.balls_faced >= 10
  AND m.match_date >= '2022-01-01'
GROUP BY p.player_id, p.name
HAVING qualifying_innings >= 2
ORDER BY run_variance ASC;
