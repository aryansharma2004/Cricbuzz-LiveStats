-- Question 9: All-rounders with 1000+ runs and 50+ wickets
SELECT p.name AS player_name,
       COALESCE(bat.career_runs, 0) AS total_runs,
       COALESCE(bowl.career_wickets, 0) AS total_wickets,
       p.country
FROM players p
LEFT JOIN (
    SELECT player_id, SUM(runs) AS career_runs
    FROM batting_stats
    GROUP BY player_id
) bat ON p.player_id = bat.player_id
LEFT JOIN (
    SELECT player_id, SUM(wickets) AS career_wickets
    FROM bowling_stats
    GROUP BY player_id
) bowl ON p.player_id = bowl.player_id
WHERE p.playing_role = 'All-rounder'
  AND (COALESCE(bat.career_runs, 0) >= 100 OR COALESCE(bowl.career_wickets, 0) >= 10)
ORDER BY total_runs DESC;
