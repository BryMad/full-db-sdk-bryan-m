import sys

from nba_dal import get_team_id

if len(sys.argv) != 2:
    print('Usage: get_team_id <team_name>')
    exit(1)

team = sys.argv[1]
result = get_team_id(team)

if len(result) == 0:
    print(f'{team} not in database')
    exit(0)

if len(result) >= 2:
    print(f'Error. Multiple ids for {team}.')
    exit(0)

for team_id in result:
    print(f'Team ID for {team} = {team_id[0]}') 
