import sys
import csv

from nba_dal import add_game

# Create teams dictionary to aid add_game function
# For simplicity, we assume that the program runs where the files are located.
TEAMS = 'teams.csv'
teams = {}

with open(TEAMS, 'r+') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        name = row[5].lower()
        id = row[1]
        teams.update({name:id})


if len(sys.argv) != 6:
    print('Usage: add_game <date in yyyy-mm-dd format> <home team name> <away team name> <pts home> <pts away>')
    exit(1)

if sys.argv[2].lower() not in teams:
    print(f'{sys.argv[2]} is not a valid team name')
    exit(1)

if sys.argv[3].lower() not in teams:
    print(f'{sys.argv[3]} is not a valid team name')
    exit(1)

game_date_est = sys.argv[1]
home_team_id = teams.get(sys.argv[2].lower()) 
away_team_id = teams.get(sys.argv[3].lower())
pts_home = sys.argv[4]
pts_away = sys.argv[5]

try:
    game = add_game(game_date_est, home_team_id, away_team_id, pts_home, pts_away)
    print(f'Game on “{game.game_date_est}” added with ID {game.id}.')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{game_date_est}” is a valid date in the format: yyyy-mm-dd .')
