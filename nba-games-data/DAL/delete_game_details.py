import sys

from nba_dal import delete_game_details

if len(sys.argv) != 2:
    print('Usage: delete_game_details <game_id>')
    exit(1)

game_id = sys.argv[1]

try:
    game = delete_game_details(game_id)
    print(f'Delete Succesful')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that {game_id} is a valid game id.')
