-- Question 4: Venues with > 50,000 capacity
SELECT name AS venue_name, city, country, capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
