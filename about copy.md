Author: Bryan Madole

Description: this is my relational-db-mini-stack using a trove of NBA Game Data created by Nathan Lauga (https://www.kaggle.com/datasets/nathanlauga/nba-games). 

This dataset contains game, player, team, ranking, and game stat detail information for all nba games from 2004 through Dec. 2022. It collects your classic "meat and potatoes" game stats (points, rebounds, assists, shooting percentages, turnovers, etc) at both a team level and individual player level for each game.

While there isn't enough ball possestion data here for certain advanced metrics (Win Shares for instance), with a lot of work, it does seem like it would have the requisite detail to calculate advance stats (VORP, Box Plus Minus) (at least based on my limited knowledge of these things). 

The dataset certainly has the right data to do classic "sportsfan trivia" type questions (which is primarily the sort of queries I've done here). "Who scored the most points in a game in recent NBA history?" (Kobe!) "Who had the highest 3 point % of a player who shot more than 8 3 pointers?" (Ben Gordon!) 

Please see queries.md to see some of these queries in action.

There are a few other files in the nba-games-data folder to load this into postgres:

preprocess_games.py is there to pre-process games.csv (the dataset contains a few duplicate games with the same primary key id that need to be culled before they can be loaded into Postgres).

game_loader.py - loads the games data.

game_detail_loader.py - loads the game details data.

There is also a DAL layer with functions to add games and search games by date in the DAL folder.