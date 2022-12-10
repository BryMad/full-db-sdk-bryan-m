import csv
import re
import sys

# For simplicity, we assume that the program runs where the files are located.
SOURCE = 'games.csv'

DESTINATION = 'games_processed.csv'


post_processed_file = open(DESTINATION, 'w')
ids = set()

# Read the files line by line and write them out with the game ID prepended.
# Provide some visible output so that the user can see where we are.
print(f'Processing games file...')

with open('games.csv', 'r+') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if row[1] in ids:
            print("Found duplicate. Skipping")
            continue
        ids.add(row[1])
        result = ','.join(row)
        post_processed_file.write(f'{result}\n')

post_processed_file.close()