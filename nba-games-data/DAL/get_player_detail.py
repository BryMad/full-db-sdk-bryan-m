import sys
from nba_dal import get_player_detail

if len(sys.argv) != 3:
    print('Usage: get_player_detail<game_id, player_id>')
    exit(1)

game_id = int(sys.argv[1])
player_id = int(sys.argv[2])


try:
    result = get_player_detail(game_id, player_id)

    if len(result) == 0:
        print(f'The Game {game_id} does not have any Details in the database.')
        exit(0)

    for detail in result:
        print(f'Game: {detail.game_id} - {detail.team_city}: {detail.player_name}- {detail.pts} pts | {detail.reb} rebs | {detail.ast} asts')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{game_id}” is a valid Game ID.')