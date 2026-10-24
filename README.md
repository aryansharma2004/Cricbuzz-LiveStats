# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/SQL-SQLite%20%2F%20PostgreSQL-green.svg)](https://www.sqlite.org/)
[![RapidAPI](https://img.shields.io/badge/API-Cricbuzz%20RapidAPI-0055FF.svg)](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/)

---

## 🎯 Problem Statement & Business Overview

Cricket is followed by billions globally, generating vast streams of ball-by-ball events, player records, and venue metrics. However, consuming live cricket feeds while simultaneously performing relational multi-dimensional SQL analysis is often fragmented.

**Cricbuzz LiveStats** addresses this challenge by providing an end-to-end analytics platform that:
1. ⚡ **Streams live match scorecards & status** via Cricbuzz Cricket REST API (RapidAPI).
2. 🗄️ **Stores normalized cricket entities** (Teams, Players, Venues, Series, Matches, Batting/Bowling/Fielding Stats) in a 3NF relational SQL database.
3. 📊 **Executes 25 comprehensive SQL analytical queries** across Beginner, Intermediate, and Advanced tiers.
4. 🛠️ **Provides full CRUD data management** via responsive Streamlit forms.
5. 📈 **Renders interactive Plotly visual charts** (bar graphs, pie charts, scatter plots, stacked bars).

---

## 🏗️ System Architecture

```
                                [ Cricbuzz Cricket API ] (RapidAPI)
                                           │
                                           ▼ (HTTPS / REST JSON)
+─────────────────────────────────────────────────────────────────────────────+
|                               API LAYER (api/)                              |
|  - cricbuzz_client.py (Session, retries, 429 rate-limit handling, fallback) |
|  - endpoints.py (Endpoint URL mapping)                                      |
+─────────────────────────────────────────────────────────────────────────────+
                                           │
                                           ▼
+─────────────────────────────────────────────────────────────────────────────+
|                            SERVICES LAYER (services/)                       |
|  - match_service.py (Match queries, inserts, updates, cascade deletes)      |
|  - player_service.py (Player profile, format aggregations, CRUD)            |
|  - stats_service.py (Catalog of 25 SQL practice queries + runner)           |
+─────────────────────────────────────────────────────────────────────────────+
         ▲                                                     │
         │                                                     ▼
+───────────────────────────+                +────────────────────────────────+
|    DATABASE LAYER (database/)             |       FRONTEND LAYER (pages/)  |
|  - schema.sql (3NF DDL, Indexes)          |  - 🏠 Home.py                  |
|  - seed_data.sql (Rich seed data)         |  - 🏏 Live_Matches.py          |
|  - utils/db_connection.py                 |  - ⭐ Top_Players.py           |
|    (SQLite connection pool)               |  - 📊 Analytics.py             |
|                                           |  - 🛠️ CRUD.py                  |
+───────────────────────────+                +────────────────────────────────+
```

---

## 🗄️ Database Schema & Entities

The database is designed with full 3NF normalization and foreign key integrity:

| Table | Primary Key | Foreign Keys | Key Attributes |
|---|---|---|---|
| `teams` | `team_id` | - | `name`, `short_name`, `country`, `image_url` |
| `players` | `player_id` | `team_id` | `name`, `full_name`, `country`, `playing_role`, `batting_style`, `bowling_style` |
| `venues` | `venue_id` | - | `name`, `city`, `country`, `capacity` |
| `series` | `series_id` | - | `name`, `host_country`, `match_type`, `start_date`, `total_matches` |
| `matches` | `match_id` | `series_id`, `team1_id`, `team2_id`, `venue_id`, `winner_id` | `match_date`, `match_format`, `match_status`, `result`, `victory_margin`, `toss_decision` |
| `batting_stats` | `stat_id` | `match_id`, `player_id`, `team_id` | `runs`, `balls_faced`, `fours`, `sixes`, `strike_rate`, `batting_position` |
| `bowling_stats` | `stat_id` | `match_id`, `player_id`, `team_id` | `overs`, `maidens`, `runs_conceded`, `wickets`, `economy` |
| `fielding_stats` | `stat_id` | `player_id` | `format`, `catches`, `stumpings`, `run_outs` |

---


## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone & Environment Setup
```bash
git clone <repository_url>
cd "Cricket API"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. API Key Configuration
Create or edit your `.env` file in the root directory:
```ini
RAPIDAPI_KEY=your_rapidapi_key_here
```
> **Note:** If no RapidAPI key is provided, the application automatically uses mock Cricbuzz match feeds so you can test all features offline without interruption!

### 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Unit & Integration Tests

Execute the automated test suite covering database connections, API fallback, and all 25 SQL queries:

```bash
# Run all tests
python3 -m unittest discover tests/
```

---

## 📂 Project Directory Structure

```
Cricket API/
├── app.py                     # Streamlit main entry point & router
├── config.py                  # Central configuration & RapidAPI headers
├── requirements.txt           # Python library dependencies
├── .env                       # Environment secrets (RapidAPI key)
├── .gitignore                 # Version control ignores
├── README.md                  # Comprehensive project documentation
│
├── database/                  # SQL Schema & Seed scripts
│   ├── schema.sql             # 3NF CREATE TABLE statements & indexes
│   └── seed_data.sql          # Full international teams, players, stats
│
├── api/                       # API integration layer
│   ├── endpoints.py           # RapidAPI Cricbuzz endpoint URLs
│   └── cricbuzz_client.py     # CricbuzzClient with retry & mock fallback
│
├── services/                  # Business logic & Database layer
│   ├── match_service.py       # Match CRUD & filtering
│   ├── player_service.py      # Player CRUD & career statistics
│   └── stats_service.py       # 25 analytical SQL questions catalog
│
├── pages/                     # Streamlit multi-page UI
│   ├── home.py                # Home page with overview & metrics
│   ├── live_matches.py        # Live scorecards from API & DB
│   ├── top_players.py         # Batting & bowling leaderboards + charts
│   ├── analytics.py           # 25 SQL queries runner + custom console
│   └── crud.py                # Form-based CRUD for players and matches
│
├── sql/                       # Organized standalone .sql query files
│   ├── beginner/              # Questions 1 to 8
│   ├── intermediate/          # Questions 9 to 16
│   └── advanced/              # Questions 17 to 25
│
├── utils/                     # Utility modules
│   ├── db_connection.py       # Centralized SQLite connection management
│   └── helpers.py             # Date formatting & safe dictionary access
│
├── tests/                     # Unit test suite
│   ├── test_database.py       # DB connection and schema tests
│   ├── test_api.py            # API client initialization and mock tests
│   └── test_queries.py        # Automated test executing all 25 SQL queries
│
└── data/                      # Local SQLite database directory
    └── cricbuzz.db            # Auto-generated SQLite database
```

---

