import sys

from nba_dal import delete_game

if len(sys.argv) != 2:
    print('Usage: delete_game <game_id>')
    exit(1)

game_id = sys.argv[1]

try:
    game = delete_game(game_id)
    print(f'Delete Succesful')
except:
    print(f'Sorry, something went wrong. Please ensure that {game_id} is a valid game id or that it\'s associated game_details have been deleted.')
