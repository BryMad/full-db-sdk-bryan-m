import sys
from nba_dal import get_game_by_id_orm

if len(sys.argv) != 2:
    print('Usage: get_game_details <game_id>')
    exit(1)

game_id = int(sys.argv[1])
try:
    result = get_game_by_id_orm(game_id)

    if len(result) == 0:
        print(f'The Game with ID: {game_id} does not have any Details in the database.')
        exit(0)

    for game in result:
        print(f'{game.id})
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{game_id}” is a valid Game ID.')