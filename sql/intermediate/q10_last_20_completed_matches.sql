-- Question 10: Details of last 20 completed matches
SELECT m.description,
       t1.name AS team1,
       t2.name AS team2,
       w.name AS winning_team,
       m.victory_margin,
       m.victory_type,
       v.name AS venue_name
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams w ON m.winner_id = w.team_id
LEFT JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_status = 'Completed'
ORDER BY m.match_date DESC
LIMIT 20;
