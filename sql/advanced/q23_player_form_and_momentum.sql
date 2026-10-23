-- Question 23: Recent player form and momentum analysis
WITH ranked_batting AS (
    SELECT bs.player_id,
           p.name AS player_name,
           bs.runs,
           bs.strike_rate,
           ROW_NUMBER() OVER (PARTITION BY bs.player_id ORDER BY m.match_date DESC) AS match_rank
    FROM batting_stats bs
    JOIN players p ON bs.player_id = p.player_id
    JOIN matches m ON bs.match_id = m.match_id
)
SELECT player_name,
       ROUND(AVG(CASE WHEN match_rank <= 5 THEN runs END), 2) AS last_5_avg,
       ROUND(AVG(CASE WHEN match_rank <= 10 THEN runs END), 2) AS last_10_avg,
       ROUND(AVG(CASE WHEN match_rank <= 5 THEN strike_rate END), 2) AS recent_sr,
       SUM(CASE WHEN match_rank <= 10 AND runs >= 50 THEN 1 ELSE 0 END) AS fifties_last_10,
       CASE
           WHEN AVG(CASE WHEN match_rank <= 5 THEN runs END) >= 65 THEN 'Excellent Form'
           WHEN AVG(CASE WHEN match_rank <= 5 THEN runs END) >= 45 THEN 'Good Form'
           WHEN AVG(CASE WHEN match_rank <= 5 THEN runs END) >= 25 THEN 'Average Form'
           ELSE 'Poor Form'
       END AS form_category
FROM ranked_batting
WHERE match_rank <= 10
GROUP BY player_id, player_name
ORDER BY last_5_avg DESC;
