-- Question 8: Series started in 2024
SELECT name AS series_name,
       host_country,
       match_type,
       start_date,
       total_matches
FROM series
WHERE start_date LIKE '2024%'
ORDER BY start_date ASC;
