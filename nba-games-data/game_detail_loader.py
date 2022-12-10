from contextlib import nullcontext
import csv
import re
from unicodedata import decimal

"""
This program generates direct SQL statements from the source NBA Game Data files in order
to populate a relational database with those files’ data.

By taking the approach of emitting SQL statements directly, we bypass the need to import
some kind of database library for the loading process, instead passing the statements
directly into a database command line utility such as `psql`.
"""



# Emit the initiating COPY statement. From this point, PostgreSQL will expect the COPY format.
print('COPY game_detail(game_id , team_id, team_abbreviation, team_city, player_id, player_name, nickname, start_position, comment, minutes, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, o_reb, d_reb, reb, ast, stl, blk, turnover, pf, pts, plus_minus) FROM STDIN WITH(NULL \'null\');')

# For simplicity, we assume that the program runs where the files are located.
# Read the files line by line and write them out as INSERT statements.
GAME_DETAILS_SOURCE = 'games_details.csv'
with open(GAME_DETAILS_SOURCE, 'r+') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        game_id = int(row[0])
        team_id = int(row[1])
        team_abbreviation = row[2]
        team_city = row[3] 
        player_id = int(row[4])
        player_name = row[5]
        nickname = row[6]
        start_position = row[7]
        comment = row[8]
        minutes = row[9]  
        fgm = 'null' if row[10] == '' else int(float(row[10]))
        fga = 'null' if row[11] == '' else int(float(row[11]))
        fg_pct = 'null' if row[12] == '' else float(row[12])
        fg3m = 'null' if row[13] == '' else int(float(row[13]))
        fg3a = 'null' if row[14] == '' else int(float(row[14]))
        fg3_pct = 'null' if row[15] == '' else float(row[15])
        ftm = 'null' if row[16] == '' else int(float(row[16]))
        fta = 'null' if row[17] == '' else int(float(row[17]))
        ft_pct = 'null' if row[18] == '' else float(row[18])
        o_reb = 'null' if row[19] == '' else int(float(row[19]))
        d_reb = 'null' if row[20] == '' else int(float(row[20]))
        reb = 'null' if row[21] == '' else int(float(row[21]))
        ast = 'null' if row[22] == '' else int(float(row[22]))
        stl = 'null' if row[23] == '' else int(float(row[23]))
        blk = 'null' if row[24] == '' else int(float(row[24]))
        turnover = 'null' if row[25] == '' else int(float(row[25]))
        pf = 'null' if row[26] == '' else int(float(row[26]))
        pts = 'null' if row[27] == '' else int(float(row[27]))
        plus_minus = 'null' if row[28] == '' else int(float(row[28]))
        print(f'{game_id}\t{team_id}\t{team_abbreviation}\t{team_city}\t{player_id}\t{player_name}\t{nickname}\t{start_position}\t{comment}\t{minutes}\t{fgm}\t{fga}\t{fg_pct}\t{fg3m}\t{fg3a}\t{fg3_pct}\t{ftm}\t{fta}\t{ft_pct}\t{o_reb}\t{d_reb}\t{reb}\t{ast}\t{stl}\t{blk}\t{turnover}\t{pf}\t{pts}\t{plus_minus}')

# All done---the \. sequence indicates this.
print('\\.')

