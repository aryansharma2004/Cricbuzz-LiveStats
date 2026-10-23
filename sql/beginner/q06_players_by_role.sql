-- Question 6: Player count by playing role
SELECT playing_role,
       COUNT(*) AS player_count
FROM players
WHERE playing_role IS NOT NULL
GROUP BY playing_role
ORDER BY player_count DESC;
