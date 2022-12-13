import sys

from nba_dal import search_game_id

if len(sys.argv) != 3:
    print('Usage: get_game_id <team_name> <season_start_year>')
    exit(1)

team = sys.argv[1]
season = sys.argv[2]
result = search_game_id(team, season)

if len(result) == 0:
    print(f'No games match for the {team} {season} season.”')
    exit(0)

for game in result:
    print(f'{game[2]} game on {game[0]}: GameID = {game[1]}')
