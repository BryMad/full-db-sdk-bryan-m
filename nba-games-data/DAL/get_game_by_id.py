import sys

from nba_dal import get_game_by_id

if len(sys.argv) != 2:
    print('Usage: get_game_id <Game ID number>')
    exit(1)

game_id = sys.argv[1]
result = get_game_by_id(game_id)

if len(result) == 0:
    print(f'No games match {game_id}.')
    exit(0)

for game in result:
    print(f'GameID: {game[1]} on {game[0]}: {game[7]}({game[5]}) at {game[6]}({game[4]})')

