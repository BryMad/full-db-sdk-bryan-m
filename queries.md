## 1. A query that selects a subset of a particular entity in your dataset

Returns the games and the players who had the ignominious distinction of turning the ball over more times than they scored in a given game. (Ranked by highest amount of turnovers per game and limited to top 20 offenders).

SELECT game_id, player_name, turnover, pts FROM game_detail WHERE turnover > pts ORDER BY turnover DESC, player_name LIMIT 20;

![screenshot](/screenshots/nba-query1.png)


## 2. Another such query, with a specific sort order ORDER BY

Criteria: Return the games and players where a player attempted at least nine 3 pointers (aka a high volume of 3 points) and rank them by player with the highest 3 pt. percentage in a given game. Limit to the top 10 best games. 

SELECT game_date_est, player_name, fg3m, fg3_pct, pts FROM game INNER JOIN game_detail ON game.id = game_detail.game_id WHERE fg3a > 8 ORDER by fg3_pct DESC LIMIT 10;

![screenshot](/screenshots/nba-query2.png)

## 3. A query that combines information from more than one table using INNER JOIN

Critera: Return the games in our dataset where a single player has scored more than 60 pts, sorted with highest individual score by a player in a game listed first.

SELECT game_date_est, player_name, pts FROM game INNER JOIN game_detail ON game.id = game_detail.game_id WHERE pts > 60 ORDER by pts DESC;

![screenshot](/screenshots/nba-query3.png)

## 4. An aggregate query that provides counts for certain groups in your dataset using GROUP BY and COUNT

Critera: Returns the total amont of time an individual player has gotten 21 or more rebounds in a game (limited to the top 15 players with the highest amount of these games).

SELECT player_name, COUNT(*) FROM game INNER JOIN game_detail ON game.id = game_detail.game_id WHERE reb > 20 GROUP BY player_name ORDER BY count DESC, player_name LIMIT 15;

![screenshot](/screenshots/nba-query4.png)

## 5. A ranking query that provides the “top” or “bottom” n records based on some metric using LIMIT

Criteria: Return the top 10 games with the highest field goal percentage (aka highest % of shots made) of a home team.

SELECT game_date_est, home_team_id, fg_pct_home FROM game ORDER BY fg_pct_home DESC LIMIT 10;

![screenshot](/screenshots/nba-query5.png)


## Additional searches:

## 1A

Query 1 specifically asks for a SINGLE entity, but this search is more useful when combined with the game table to get an actual date for when the game occurred, so this search gets that info by joining the two tables.

Returns the games and the players who had the ignominious distinction of turning the ball over more than they scored in a given game. Ranked by highest amount of turnovers per game and limited to top 20.

SELECT game_date_est, player_name, turnover, pts FROM game INNER JOIN game_detail ON game.id = game_detail.game_id WHERE turnover > pts ORDER BY turnover DESC, player_name LIMIT 20;

![screenshot](/screenshots/nba-query1A.png)


## 5A.

A slightly more convoluted query for #5 to also return the name of the team who had the highest field goal percentage (since we don't  have a "team" table to connect teamids, this uses some convoluted WHERE and ORDER BY logic to leverage the "team_city" field from game_detail information).

SELECT game_date_est, home_team_id, team_city, fg_pct_home FROM game INNER JOIN game_detail ON game.id = game_detail.game_id WHERE game.home_team_id = game_detail.team_id GROUP by game_date_est, fg_pct_home, home_team_id, team_city, fg_pct_home ORDER BY fg_pct_home DESC LIMIT 10;

![screenshot](/screenshots/nba-query5A.png)

