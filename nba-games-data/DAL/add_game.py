import sys

from nba_dal import insert_game

if len(sys.argv) != 2:
    print('Usage: add_game <date> [in format yyyy-mm-dd]>')
    exit(1)

game_date_est = sys.argv[1]
try:
    game = insert_game(game_date_est)
    print(f'Game on “{game.game_date_est}” added with ID {game.id}.')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{game_date_est}” is a valid date in the format: yyyy-mm-dd .')
