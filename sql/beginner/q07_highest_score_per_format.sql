-- Question 7: Highest batting score per format
SELECT format,
       MAX(runs) AS highest_score
FROM batting_stats
GROUP BY format
ORDER BY highest_score DESC;
