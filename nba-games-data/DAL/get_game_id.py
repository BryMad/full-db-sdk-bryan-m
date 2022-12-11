import sys

from nba_dal import get_game_id

if len(sys.argv) != 2:
    print('Usage: get_game_id <Game ID number>')
    exit(1)

game_id = sys.argv[1]
result = get_game_id(game_id)

if len(result) == 0:
    print(f'No games match {game_id}.')
    exit(0)

print(f'GameID: {result[0][1]} - {result[0][0]} - {result[0][2]}({result[0][6]}) at {result[1][2]}({result[0][7]})')

