import sys

from nba_dal import search_details_by_stat_combo

if len(sys.argv) != 7:
    print('Usage: search_details_by_stat_combos <ordering_criteria> <pts> <reb> <ast> <blk> <stl>')
    exit(1)

order = sys.argv[1] 
pts = sys.argv[2]
reb = sys.argv[3]
ast = sys.argv[4]
blk = sys.argv[5]
stl = sys.argv[6]
result = search_details_by_stat_combo(order, pts, reb, ast, blk, stl)

if len(result) == 0:
    print(f'No games match this stat criteria.')
    exit(0)

for game_detail in result:
    print(f'{game_detail[0]} - {game_detail[1]} - {game_detail[2]} pts, {game_detail[3]} rebounds, {game_detail[4]} assists, {game_detail[5]} blocks, {game_detail[6]} steals')
