import sys
from nba_dal import get_game_details_by_id

if len(sys.argv) != 2:
    print('Usage: get_game_details_by_id <game_id>')
    exit(1)

game_id = sys.argv[1]
try:
    result = get_game_details_by_id(game_id)

    if len(result) == 0:
        print(f'The Game {game_id} does not have any Details in the database.')
        exit(0)

    for detail in result:
        print(f'Game: {detail.game_id} - {detail.team_city}: {detail.player_name} (player_id:{detail.player_id}) - {detail.pts} pts | {detail.reb} rebs | {detail.ast} asts')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{game_id}” is a valid Game ID.')