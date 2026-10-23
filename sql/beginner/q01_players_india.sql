-- Question 1: Find all players who represent India.
-- Display full name, playing role, batting style, and bowling style.

SELECT name, full_name, playing_role, batting_style, bowling_style
FROM players
WHERE country = 'India'
ORDER BY name ASC;
