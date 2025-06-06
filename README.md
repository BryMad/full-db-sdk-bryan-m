# HoopStats - NBA Database & Analysis System

A comprehensive PostgreSQL-based database system and Python SDK for managing and analyzing NBA game statistics. Built as part of a database systems course, this project demonstrates advanced database design, performance optimization, and full-stack development skills.

## What This Does

HoopStats transforms raw NBA statistics into a queryable, high-performance database system that enables complex basketball analytics. The system features:

- **Advanced Player Performance Queries** - Search for players by statistical combinations (e.g., "Find all 30+ point, 10+ rebound, 10+ assist games")
- **Complete CRUD Operations** - Full create, read, update, delete functionality through a Python SDK
- **Transaction-Safe Operations** - Ensures data integrity across complex multi-table operations
- **Command-Line Interface** - User-friendly CLI for accessing data without SQL knowledge
- **Performance Optimized** - Custom indexing reduces query times by ~75%

## Tech Stack

- **Database**: PostgreSQL
- **Backend**: Python 3
- **Data Processing**: Custom ETL pipeline
- **Performance**: Strategic B-tree indexing
- **Dataset**: NBA Games 2004-2022 (from Kaggle)

## Performance Highlights

The centerpiece query (`search_details_by_stat_combo`) searches for players meeting specific statistical thresholds across multiple categories. Through strategic indexing:

- **Before optimization**: ~0.078 seconds average query time
- **After optimization**: ~0.023 seconds average query time
- **Performance improvement**: 70%+ faster queries

### Indexing Strategy

```sql
CREATE INDEX game_detail_pts_idx on game_detail(pts);
CREATE INDEX game_detail_ast_idx on game_detail(ast);
CREATE INDEX game_detail_reb_idx on game_detail(reb);
CREATE INDEX game_detail_blk_idx on game_detail(blk);
CREATE INDEX game_detail_stl_idx on game_detail(stl);
```

## Setup & Installation

### Prerequisites

- PostgreSQL server installed and running
- Python 3.x
- NBA dataset from [Kaggle](https://www.kaggle.com/datasets/nathanlauga/nba-games)

### Step 1: Data Preprocessing

After downloading the NBA dataset and placing it in the `nba-games-data` folder:

```bash
cd nba-games-data
python3 preprocess_games.py
```

### Step 2: Database Schema Setup

Load the database schema:

```bash
psql -f schema.sql postgresql://localhost/postgres
```

### Step 3: Data Loading

Load the data tables in the correct order:

```bash
python3 game_loader.py | psql postgresql://localhost/postgres
python3 team_loader.py | psql postgresql://localhost/postgres
python3 game_detail_loader.py | psql postgresql://localhost/postgres
```

### Step 4: Performance Optimization

Create indexes for optimal query performance:

```bash
psql postgresql://localhost/postgres
```

Then run the indexing commands:

```sql
CREATE INDEX game_detail_pts_idx on game_detail(pts);
CREATE INDEX game_detail_ast_idx on game_detail(ast);
CREATE INDEX game_detail_reb_idx on game_detail(reb);
CREATE INDEX game_detail_blk_idx on game_detail(blk);
CREATE INDEX game_detail_stl_idx on game_detail(stl);
```

## Usage Examples

### Command Line Interface

```bash
# Search for triple-double performances (order_by, min_pts, min_reb, min_ast, min_blk, min_stl)
python3 search_by_stat_combo.py pts 10 10 10 0 0

# Get count of how many times players achieved specific stat combos (min_pts, min_reb, min_ast, min_blk, min_stl)
python3 get_count_by_stat_combo.py 30 10 10 1 1

# Search for games by team and season
python3 search_game_id.py Mavericks 2019

# Add a new game (date, home_team, home_score, away_team, away_score)
python3 add_game.py 2022-12-01 Suns 108 Mavericks 115

# Update a player's score (game_id, player_id, point_change)
python3 update_player_score.py 22101008 203114 1
```

### Python SDK

```python
from nba_dal import *

# Search for elite performances (30+ pts, 10+ reb, 10+ ast)
performances = search_by_stat_combo("pts", 30, 10, 10, 0, 0)

# Get specific game details
game = get_game_by_id(22101005)

# Add new game (date, home_team, home_score, away_team, away_score)
new_game = add_game("2022-12-01", "Suns", 108, "Mavericks", 115)

# Update player statistics with transaction safety
update_player_score(22101008, 203114, 1)
```

## Database Architecture

The system uses a normalized relational design with three core entities:

- **games** - Game-level information (date, teams, scores)
- **teams** - NBA team information and metadata
- **game_details** - Individual player performance statistics

Key relationships enable complex queries across games, teams, and individual player performances while maintaining data integrity.

## Key Features

### Advanced Analytics Queries

- **Multi-stat performance searches** - Find players meeting specific statistical thresholds across multiple categories
- **Statistical counting queries** - Count how many times players achieved certain stat combinations
- **Team-based game searches** - Find games by team and season with date ordering

### Complete CRUD Operations for Games

- **Create**: Add new games with automatic team ID lookup
- **Read**: Search games by team/season and retrieve detailed game information by ID
- **Update**: Modify player scores with automatic game score adjustment (transaction-protected)
- **Delete**: Remove games and associated details with proper foreign key handling

### Transaction Safety

The `update_player_score()` function demonstrates proper transaction management - when updating a player's individual game statistics, it simultaneously updates the team's overall game score, ensuring both changes succeed or both fail to maintain data consistency.

## What I Learned

This project was built as part of a database systems course focused on:

- **Database Design**: Normalizing complex sports data into efficient relational structures
- **Performance Optimization**: Using indexing strategies to dramatically improve query performance
- **Transaction Management**: Ensuring data integrity in multi-step operations
- **SDK Development**: Creating user-friendly abstractions over complex database operations
- **ETL Pipeline Development**: Processing and cleaning real-world datasets for database storage

The project demonstrates practical application of database theory including relational algebra, normalization, and query optimization in a real-world context.

## Project Structure

```
├── nba-games-data/
│   ├── schema.sql
│   ├── preprocess_games.py
│   ├── game_loader.py
│   ├── team_loader.py
│   └── game_detail_loader.py
├── src/
│   ├── nba_dal.py
│   ├── cli_search.py
│   └── cli_game_manager.py
├── screenshots/
│   └── performance_comparisons/
└── README.md
```

## Data Source

Dataset: [NBA Games 2004-2022](https://www.kaggle.com/datasets/nathanlauga/nba-games) by Nathan Lauga on Kaggle

## Future Enhancements

- Web-based dashboard for data visualization
- Real-time data integration with NBA APIs
- Machine learning models for performance prediction
- Advanced statistical analysis features
