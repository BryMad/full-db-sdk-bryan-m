import sys

from nba_dal import search_games_by_date

if len(sys.argv) != 2:
    print('Usage: search_by_date <date in format: yyyy-mm-dd')
    exit(1)

query = sys.argv[1]
result = search_games_by_date(query)

if len(result) == 0:
    print(f'No games match “{query}.”')
    exit(0)

for game in result:
    print(f'Gameid = {game[0]} played on {game[1]}')
