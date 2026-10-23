-- Question 2: Matches in last 30 days
SELECT m.description,
       t1.name AS team1,
       t2.name AS team2,
       v.name || ', ' || v.city AS venue_city,
       m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= date('now', '-30 days')
ORDER BY m.match_date DESC;
