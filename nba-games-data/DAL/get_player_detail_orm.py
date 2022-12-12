import sys
from nba_dal import get_player_detail_orm

if len(sys.argv) != 3:
    print('Usage: get_game_details <game_id>')
    exit(1)

game_id = int(sys.argv[1])
player_id = int(sys.argv[2])


try:
    result = get_player_detail_orm(game_id, player_id)

    if len(result) == 0:
        print(f'The Game {game_id} does not have any Details in the database.')
        exit(0)

    for game in result:
        print(f'{game.player_name}, {game.pts}')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{game_id}” is a valid Game ID.')