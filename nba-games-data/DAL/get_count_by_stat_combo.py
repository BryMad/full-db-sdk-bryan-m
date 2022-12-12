import sys

from nba_dal import get_count_by_stat_combo

if len(sys.argv) != 6:
    print('Usage: search_details_by_stat_combos <ordering_criteria> <pts> <reb> <ast> <blk> <stl>')
    exit(1)

pts = sys.argv[1]
reb = sys.argv[2]
ast = sys.argv[3]
blk = sys.argv[4]
stl = sys.argv[5]
result = get_count_by_stat_combo(pts, reb, ast, blk, stl)

if len(result) == 0:
    print(f'No games match this stat criteria.')
    exit(0)

for player in result:
    print(f'{player[0]}: {player[1]} games with {pts} pts, {reb} rebounds, {ast} assists, {blk} blocks, and {stl} steals')
