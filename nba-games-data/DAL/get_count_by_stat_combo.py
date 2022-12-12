import sys

from nba_dal import get_count_by_stat_combo

if len(sys.argv) != 6:
    print('Usage: get_count_by_stat_combo <pts> <reb> <ast> <blk> <stl>')
    exit(1)

pts = sys.argv[1]
reb = sys.argv[2]
ast = sys.argv[3]
blk = sys.argv[4]
stl = sys.argv[5]
result = get_count_by_stat_combo(pts, reb, ast, blk, stl)

if len(result) == 0:
    print(f'No players played a game that matches this stat combo.')
    exit(0)

for player in result:
    print(f'{player[0]}: {player[1]} games with at least | {pts} pts | {reb} rebs | {ast} asts | {blk} blks | {stl} stls')
