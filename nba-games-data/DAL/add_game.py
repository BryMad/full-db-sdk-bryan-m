import sys

from nba_dal import add_game

if len(sys.argv) != 6:
    print('Usage: add_game <date in yyyy-mm-dd format> <home team name> <pts home> <away team name> <pts away>')
    exit(1)


game_date_est = sys.argv[1]
home_team = sys.argv[2]
pts_home = sys.argv[3]
away_team = sys.argv[4]
pts_away = sys.argv[5]

try:
    game = add_game(game_date_est, home_team, pts_home, away_team, pts_away)
    print(f'Game on “{game.game_date_est}” added with ID {game.id}.')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{game_date_est}” is a valid date in the format: yyyy-mm-dd .')
