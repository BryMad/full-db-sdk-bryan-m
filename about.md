Author: Bryan Madole

# Link to dataset:

Description: this is my full-db-sdk final project using a trove of NBA Game Data created by Nathan Lauga (https://www.kaggle.com/datasets/nathanlauga/nba-games).

# What the dataset contains:

This dataset contains game, player, team, ranking, and game stat detail information for all nba games from 2004 through Dec. 2022, collecting the main stats (points, rebounds, assists, shooting percentages, turnovers, etc) at both a team level and individual player level for each game.

# Imagined application:

Sports networks, podcasts, social media accounts, etc are constantly churning out hyperspecific stat details such as this headline that splashed across monitors in 2019: "Luka Doncic Becomes Only The Third Player To Average A 30-Point Triple-Double For A Month."

While some might argue trivia stats like these are arbitrary and derived from cherry picking numbers, others would argue such stats can still offer interesting context and meaingful perspective to a player or team's achievements.

Regardless of the ultimate validity of these stats, there's no question that fans, pundits, and sports networks crave them, which is why the intended application for this project is to provide these type of fun stat nuggets that could used by NBA commentators and fans alike.

While this data set doesn't have minute to minute stats to give hyperspecific time based stats ("Most points scored by a team in the 3rd quarter"), it has great full game data to answer classic sportsfan trivia type questions about full games. "Who scored the most points in a game in recent NBA history?" "Which players have the highest count of 30 point triple doubles." etc.

# Why relational database:

Showing my age here, but my earliest experience with sports stats as a kid was excitedly waiting for Tuesdays, when the Dallas Morning News would publish extensive tables of the week's NBA box scores, stat leader boards, etc. As a result, I'm biased towards tables as a means of exploring sports data by default.

But it also makes sense because sports data is so RELATIONAL. A game is a discrete concept with its own stats, but it's related to the teams that play in that game. Then there are players playing for those teams (who can also change teams and therefore change their relationships to that team). These players also have individual stats in a given game. Sometimes we only care about these individual stats (independent of the game data and what happened in the game). Other times we might want to relate the individual stats to the game data, to see what role the individual stats played in the macro team level stats. A relational database allows us to consider these complex, interlocking relationships, linking tables in difference ways to satify different use cases.

Obviously a graph database could also show these relationships and perhaps even reveal visual connections one might miss with a dry table. But since the imagined application for this data set is getting dry trivia-based lists, facts, and figures (vs discovering secret insights from visual connections), a relational model still seemed more appropriate.

While I'm sure there are applications for this dataset for which a Document model might be useful, it seemed limiting for my intended use applications. With the single document approach and its reliance on nested objects/arrays in lieu of joining related tables, the document model seemed to flatten and compress the relationships rather than allowing them to be explored and considered on an as needed basis. For instance, individual player game stats becoming a nested array of game data seems to needlessly link data that (while obviously related) doesn't ALWAYS need to linked. Sometimes we might only care about individual stats regardless of game/team stats.

For these reasons, I have chosen a relational database was the best fit for this project.

# Assessment:

Now that the assignment is done, this group (of one) still feels that a relational database was the right choice. For the envisioned use cases, tables and relational databases do indeed seem like the best option.

# Schema:

![screenshot](/screenshots/schema.png)

# Tutorial Video Link

Tutorial Video on Natural Join:

[dropbox video tutorial](https://www.dropbox.com/s/p9kooddwla5vlyh/Natural%20Join.mov?dl=0)
