import sys
from nba_dal import get_game_details

if len(sys.argv) != 2:
    print('Usage: get_game_details <game_id>')
    exit(1)

game_id = sys.argv[1]
try:
    result = get_game_details(game_id)

    if len(result) == 0:
        print(f'The Game {game_id} does not have any Details in the database.')
        exit(0)

    for details in result:
        print(f'{details.player_name} scored {details.pts} points.')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{game_id}” is a valid Game ID.')