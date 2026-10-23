"""
Cricbuzz API client for fetching real-time cricket data.
Handles authentication, request retrying, rate limiting, and response parsing.
"""

import requests
import time
import json
import logging
from config import RAPIDAPI_KEY, RAPIDAPI_HOST, API_HEADERS
from api import endpoints

logger = logging.getLogger(__name__)


class CricbuzzClient:
    """Client for Cricbuzz Cricket API via RapidAPI."""

    def __init__(self, api_key=None):
        self.api_key = api_key or RAPIDAPI_KEY
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        self.max_retries = 3
        self.retry_delay = 2

    def is_configured(self):
        """Check if valid API key is present."""
        return bool(self.api_key and self.api_key != "your_rapidapi_key_here")

    def _make_request(self, url, params=None):
        """
        Execute an HTTP GET request with retries and timeout.
        """
        if not self.is_configured():
            raise ValueError(
                "RapidAPI Key is not configured. Please add your key in the .env file or settings."
            )

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=12
                )
                if response.status_code == 429:
                    wait_time = self.retry_delay * attempt
                    logger.warning(f"Rate limited (429). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                if attempt == self.max_retries:
                    raise Exception(f"HTTP error from Cricbuzz API: {e} (Status: {response.status_code})")
                time.sleep(self.retry_delay)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt == self.max_retries:
                    raise Exception(f"Network error communicating with Cricbuzz API: {e}")
                time.sleep(self.retry_delay)
            except json.JSONDecodeError:
                raise Exception("Failed to decode JSON response from Cricbuzz API.")

        raise Exception("Max retries exceeded for Cricbuzz API request.")

    def get_recent_matches(self):
        """Fetch list of recent and ongoing matches."""
        try:
            return self._make_request(endpoints.MATCHES_RECENT)
        except Exception as e:
            # If not configured or failed, return sample data with warning
            logger.warning(f"API request failed: {e}. Providing mock live matches.")
            return self._get_mock_matches()

    def get_live_matches(self):
        """Fetch matches currently in progress."""
        try:
            return self._make_request(endpoints.MATCHES_LIVE)
        except Exception:
            return self.get_recent_matches()

    def get_match_scorecard(self, match_id):
        """Fetch full scorecard for a match."""
        url = endpoints.MATCH_SCORECARD.format(match_id=match_id)
        return self._make_request(url)

    def get_player_info(self, player_id):
        """Fetch player profile by Cricbuzz player ID."""
        url = endpoints.PLAYER_INFO.format(player_id=player_id)
        return self._make_request(url)

    def get_series_list(self):
        """Fetch list of active international cricket series."""
        return self._make_request(endpoints.SERIES_INTERNATIONAL)

    def get_rankings(self, category="batsmen", format_type="test"):
        """
        Fetch ICC rankings for batsmen, bowlers, or allrounders.
        category: 'batsmen' | 'bowlers' | 'allrounders'
        format_type: 'test' | 'odi' | 't20'
        """
        endpoints_map = {
            "batsmen": endpoints.RANKINGS_BATSMEN,
            "bowlers": endpoints.RANKINGS_BOWLERS,
            "allrounders": endpoints.RANKINGS_ALLROUNDERS
        }
        url = endpoints_map.get(category, endpoints.RANKINGS_BATSMEN)
        params = {"formatType": format_type}
        return self._make_request(url, params=params)

    def _get_mock_matches(self):
        """Fallback mock matches structure matching Cricbuzz API JSON schema."""
        return {
            "typeMatches": [
                {
                    "matchType": "International",
                    "seriesMatches": [
                        {
                            "seriesAdWrapper": {
                                "seriesName": "ICC Champions Trophy 2025",
                                "matches": [
                                    {
                                        "matchInfo": {
                                            "matchId": 90123,
                                            "matchDescription": "Final",
                                            "matchFormat": "ODI",
                                            "status": "India won by 4 wickets",
                                            "state": "Complete",
                                            "team1": {"teamName": "Australia", "teamSName": "AUS"},
                                            "team2": {"teamName": "India", "teamSName": "IND"},
                                            "venueInfo": {"ground": "Dubai International Stadium", "city": "Dubai"}
                                        },
                                        "matchScore": {
                                            "team1Score": {"inngs1": {"runs": 284, "wickets": 7, "overs": 50.0}},
                                            "team2Score": {"inngs1": {"runs": 288, "wickets": 6, "overs": 48.2}}
                                        }
                                    },
                                    {
                                        "matchInfo": {
                                            "matchId": 90124,
                                            "matchDescription": "Semi-Final 1",
                                            "matchFormat": "ODI",
                                            "status": "India won by 12 runs",
                                            "state": "Complete",
                                            "team1": {"teamName": "India", "teamSName": "IND"},
                                            "team2": {"teamName": "Pakistan", "teamSName": "PAK"},
                                            "venueInfo": {"ground": "Gaddafi Stadium", "city": "Lahore"}
                                        },
                                        "matchScore": {
                                            "team1Score": {"inngs1": {"runs": 310, "wickets": 5, "overs": 50.0}},
                                            "team2Score": {"inngs1": {"runs": 298, "wickets": 9, "overs": 50.0}}
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "seriesAdWrapper": {
                                "seriesName": "T20 International Series 2025",
                                "matches": [
                                    {
                                        "matchInfo": {
                                            "matchId": 90125,
                                            "matchDescription": "3rd T20I",
                                            "matchFormat": "T20",
                                            "status": "Live - England needs 34 runs in 18 balls",
                                            "state": "In Progress",
                                            "team1": {"teamName": "South Africa", "teamSName": "SA"},
                                            "team2": {"teamName": "England", "teamSName": "ENG"},
                                            "venueInfo": {"ground": "The Oval", "city": "London"}
                                        },
                                        "matchScore": {
                                            "team1Score": {"inngs1": {"runs": 195, "wickets": 4, "overs": 20.0}},
                                            "team2Score": {"inngs1": {"runs": 162, "wickets": 5, "overs": 17.0}}
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
