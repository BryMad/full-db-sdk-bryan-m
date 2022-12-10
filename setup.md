# Setup Instructions

# 1) Preprocess the files

After downloading the NBA dataset from Kaggle (https://www.kaggle.com/datasets/nathanlauga/nba-games) and placing it in the nba-games-data folder, the next step is to preprocess the data files.

The dataset contains a few duplicate games with the same primary key id that need to be culled before they can be loaded into Postgres. Navigate to the nba-games-data folder in your terminal and run:

`python3 preprocess_games.py`

# 2) Load the Schema

This tutorial assumes that you can set up your own PostgreSQL server and get it up and running.

Assuming that a PostgreSQL server is up and running, the next step is to load in the schema. Make sure you are still in the nba-games-data directory, and run this command in Terminal to feed the schema file to PostgresSQL:

`psql -f schema.sql postgresql://localhost/postgres`

# 3) Load the data

Assuming that the games.csv file has been preprocessed, the PostgreSQL server is up and running, and the schema has been loaded, the final step is to load the actual data tables into the server. Use the following commands (still within the nba-games-data folder) to load the games and game_details data:

`python3 game_loader.py | psql postgresql://localhost/postgres`

`python3 game_detail_loader.py | psql postgresql://localhost/postgres`

# 4) Indexing Performance/Instructions

A centerpiece query of the DAL is search_details_by_stat_combo, a search that can return a customized, ranked list of player performances based on a minimum desired combo of stats. (eg "Find the players who have had at least 30 points, 10 rebounds, 10 assists, 1 steal, and 1 block in a game").

After inputting the parameters via the DAL, this is how the search would look being fed into Postgres:

SELECT game_date_est, player_name, pts, reb, ast, blk, stl FROM game INNER JOIN game_detail ON game.id = game_detail.game_id WHERE pts >= 30 AND reb >= 10 AND ast >= 10 AND blk >= 1 and stl >= 1 ORDER by pts DESC LIMIT 100;

Using "time" output and running this query without indexing, the average times were coming in around 0.078, 0.081, 0.067 s.

![screenshot](/screenshots/index1_noIndex.png)

Using the "explain output" to see postgres's query plan revealed a sequential scan happening on game_detail for the each of the stats I was querying (pts, reb, ast, blk, stl):

![screenshot](/screenshots/index2_explain1.png)

I went ahead and indexed all 5 by inputting these commands at the database level:

`CREATE INDEX game_detail_pts_idx on game_detail(pts);`
`CREATE INDEX game_detail_ast_idx on game_detail(ast);`
`CREATE INDEX game_detail_reb_idx on game_detail(reb);`
`CREATE INDEX game_detail_blk_idx on game_detail(blk);`
`CREATE INDEX game_detail_stl_idx on game_detail(stl);`

After indexing, the query plan was changed to this, with the sequential scan through game_detail eliminated:

![screenshot](/screenshots/index2_explain2.png)

Running the search again post-indexing, using "time," showed a significant speed improvement, with the new search time being almost a 1/4th of what it previously was, with times in the 0.022, 0.023, 0.025 range:

![screenshot](/screenshots/index3_indexSearch.png)




