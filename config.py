import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "your_rapidapi_key_here")
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"

API_HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

# Database Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "cricbuzz.db")

# App Configuration
APP_TITLE = "🏏 Cricbuzz LiveStats"
APP_ICON = "🏏"
LAYOUT = "wide"
