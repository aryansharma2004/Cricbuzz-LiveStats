"""Cricbuzz RapidAPI endpoint definitions."""

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"

# Matches
MATCHES_RECENT = f"{BASE_URL}/matches/v1/recent"
MATCHES_LIVE = f"{BASE_URL}/matches/v1/live"
MATCH_SCORECARD = f"{BASE_URL}/mcenter/v1/{{match_id}}/hscard"
MATCH_INFO = f"{BASE_URL}/mcenter/v1/{{match_id}}"

# Players
PLAYER_INFO = f"{BASE_URL}/stats/v1/player/{{player_id}}"
PLAYER_CAREER = f"{BASE_URL}/stats/v1/player/{{player_id}}/career"
PLAYER_BATTING = f"{BASE_URL}/stats/v1/player/{{player_id}}/batting"
PLAYER_BOWLING = f"{BASE_URL}/stats/v1/player/{{player_id}}/bowling"

# Series & Tournaments
SERIES_INTERNATIONAL = f"{BASE_URL}/series/v1/international"
SERIES_MATCHES = f"{BASE_URL}/series/v1/{{series_id}}"

# Rankings
RANKINGS_BATSMEN = f"{BASE_URL}/stats/v1/rankings/batsmen"
RANKINGS_BOWLERS = f"{BASE_URL}/stats/v1/rankings/bowlers"
RANKINGS_ALLROUNDERS = f"{BASE_URL}/stats/v1/rankings/allrounders"
