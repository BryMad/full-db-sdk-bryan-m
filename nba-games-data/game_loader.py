import csv

"""
This program generates direct SQL statements from the source NBA Game Data files in order
to populate a relational database with those files’ data.

By taking the approach of emitting SQL statements directly, we bypass the need to import
some kind of database library for the loading process, instead passing the statements
directly into a database command line utility such as `psql`.
"""

# The INSERT approach is best used with a transaction. An introductory definition:
# instead of “saving” (committing) after every statement, a transaction waits on a
# commit until we issue the `COMMIT` command.
print('BEGIN;')

# For simplicity, we assume that the program runs where the files are located.
GAME_SOURCE = 'games_processed.csv'
with open(GAME_SOURCE, 'r+') as f:
    reader = csv.reader(f)
    for row in reader:
        id = row[1]
        game_date_est = row[0]
        home_team_id = row[3]
        visitor_team_id = row[4]
        season = row[5]
        team_id_home = row[6]
        # skips a few blank game entries
        if row[7] == '':
            continue
        pts_home = row[7]
        fg_pct_home = row[8]
        ft_pct_home = row[9]
        fg3_pct_home = row[10]
        ast_home = row[11]
        reb_home = row[12]
        team_id_away = row[13]
        pts_away = row[14]
        fg_pct_away = row[15]
        ft_pct_away = row[16]
        fg3_pct_away = row[17]
        ast_away = row[18]
        reb_away = row[19]
        home_team_wins = row[20]
        print(f'INSERT INTO game VALUES({id},\'{game_date_est}\',{home_team_id}, {visitor_team_id},{season}, {team_id_home}, {pts_home}, {fg_pct_home}, {ft_pct_home}, {fg3_pct_home}, {ast_home}, {reb_home}, {team_id_away}, {pts_away}, {fg_pct_away}, {ft_pct_away}, {fg3_pct_away}, {ast_away}, {reb_away}, {home_team_wins});')

# We wrap up by emitting an SQL statement that will update the database’s game ID
# counter based on the largest one that has been loaded so far.
print('SELECT setval(\'game_id_seq\', (SELECT MAX(id) from game));')

# _Now_ we can commit our transation.
print('COMMIT;')

