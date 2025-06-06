import sys
from nba_dal import update_player_score

if len(sys.argv) != 4:
    print('Usage: update_player_score <game_id, player_id, change_amount>')
    exit(1)

game_id = int(sys.argv[1])
player_id = int(sys.argv[2])
change_amount = int(sys.argv[3])
try:
    result = update_player_score(game_id, player_id, change_amount)
    print(f'Update succesful')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{game_id}” is a valid Game ID.')