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

## 🧮 25 SQL Analytics Practice Queries

### 🟢 Beginner Level (Questions 1 - 8)
1. **Q1:** Find all players who represent India with full name, role, batting/bowling style.
2. **Q2:** Show all cricket matches played in the last 30 days sorted by recent first.
3. **Q3:** Top 10 highest run scorers in ODI cricket with average and centuries.
4. **Q4:** Cricket venues with seating capacity > 50,000 spectators.
5. **Q5:** Calculate how many matches each team has won.
6. **Q6:** Count how many players belong to each playing role.
7. **Q7:** Highest individual batting score in each cricket format (Test, ODI, T20).
8. **Q8:** Series started in 2024 with host country, type, start date, and total matches.

### 🟡 Intermediate Level (Questions 9 - 16)
9. **Q9:** All-rounders who scored > 1000 runs AND took > 50 wickets across their career.
10. **Q10:** Details of last 20 completed matches with teams, margin, and venue.
11. **Q11:** Cross-format player comparison (players who played at least 2 formats).
12. **Q12:** Home vs Away team performance (venue country matches team country).
13. **Q13:** 100+ run partnerships between consecutive batsmen in same innings.
14. **Q14:** Bowling performance by venue for bowlers with >= 3 matches at same venue.
15. **Q15:** Player performance in close matches (< 50 runs or < 5 wickets victory margin).
16. **Q16:** Year-wise batting trends since 2020 (average runs and strike rate per year).

### 🔴 Advanced Level (Questions 17 - 25)
17. **Q17:** Toss advantage analysis: win percentage by toss decision (bat vs bowl first).
18. **Q18:** Most economical bowlers in limited-overs cricket (ODI and T20).
19. **Q19:** Batting consistency analysis using statistical standard deviation / variance.
20. **Q20:** Format-wise match count and batting averages for Test, ODI, and T20.
21. **Q21:** Comprehensive weighted ranking system:
    - Batting points: `(runs × 0.01) + (average × 0.5) + (strike_rate × 0.3)`
    - Bowling points: `(wickets × 2) + ((50 - average) × 0.5) + ((6 - economy) × 2)`
    - Fielding points: `(catches × 3) + (stumpings × 5)`
22. **Q22:** Head-to-head match prediction analysis between teams.
23. **Q23:** Recent player form and momentum (last 5 vs last 10 innings, form category).
24. **Q24:** Best consecutive batting partnerships combinations and success rates.
25. **Q25:** Player career trajectory time-series evolution (Quarterly analysis).

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

## 🎓 Viva & Technical Interview Questions

### Q1: Why use 3NF normalization for cricket statistics?
**Answer:** In cricket, matches, players, and teams have complex many-to-many relationships. Splitting data into separate entities (`players`, `matches`, `batting_stats`, `bowling_stats`) avoids redundancy (e.g. repeating player country or venue capacity in every ball or innings row), prevents update anomalies, and ensures data integrity through foreign keys.

### Q2: How does the application handle RapidAPI rate limits?
**Answer:** The `CricbuzzClient` implements an exponential backoff retry mechanism. When an HTTP 429 status code is received, the client pauses for `retry_delay * attempt` seconds before retrying up to 3 times. If unconfigured or quota is exhausted, it gracefully falls back to structured mock data.

### Q3: How do you prevent SQL injection in Streamlit data apps?
**Answer:** In our `services/` and `utils/db_connection.py`, all user-supplied parameters are passed as parameterized bindings (`?` placeholders in SQLite or `%s` in PostgreSQL). Furthermore, in the custom SQL console, destructive commands (`DROP`, `DELETE`, `TRUNCATE`) are blocked.
