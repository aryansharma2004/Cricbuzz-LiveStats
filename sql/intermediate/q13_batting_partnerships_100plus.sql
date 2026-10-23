-- Question 13: 100+ run partnerships between consecutive batsmen
SELECT p1.name AS batsman_1,
       p2.name AS batsman_2,
       (bs1.runs + bs2.runs) AS combined_runs,
       bs1.innings_number,
       m.description AS match_name
FROM batting_stats bs1
JOIN batting_stats bs2 ON bs1.match_id = bs2.match_id
    AND bs1.innings_number = bs2.innings_number
    AND bs1.team_id = bs2.team_id
    AND ABS(bs1.batting_position - bs2.batting_position) = 1
    AND bs1.player_id < bs2.player_id
JOIN players p1 ON bs1.player_id = p1.player_id
JOIN players p2 ON bs2.player_id = p2.player_id
JOIN matches m ON bs1.match_id = m.match_id
WHERE (bs1.runs + bs2.runs) >= 100
ORDER BY combined_runs DESC;
