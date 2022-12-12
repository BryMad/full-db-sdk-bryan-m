import csv

# Create teams dictionary to aid add_game function
# For simplicity, we assume that the program runs where the files are located.
TEAMS = 'teams.csv'
teams = {}

with open(TEAMS, 'r+') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        name = row[5]
        id = row[1]
        teams.update({name:id})

print(teams.get('Mavericks'))