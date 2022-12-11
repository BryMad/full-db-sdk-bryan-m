import csv

"""
This program generates direct SQL statements from the source NBA Team Data files in order
to populate a relational database with those files’ data.

By taking the approach of emitting SQL statements directly, we bypass the need to import
some kind of database library for the loading process, instead passing the statements
directly into a database command line utility such as `psql`.
"""

# The INSERT approach is best used with a transaction. An introductory definition:
# instead of “saving” (committing) after every statement, a transaction waits on a
# commit until we issue the `COMMIT` command.
print('BEGIN;')

# For simplicity, we assume that the program runs where the files are located.
TEAM_SOURCE = 'teams.csv'
with open(TEAM_SOURCE, 'r+') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        id = row[1]
        nickname = row[5]
        city = row[7]
        print(f'INSERT INTO team VALUES({id},\'{nickname}\',\'{city}\');')

# We wrap up by emitting an SQL statement that will update the database’s game ID
# counter based on the largest one that has been loaded so far.
print('SELECT setval(\'team_id_seq\', (SELECT MAX(id) from team));')

# _Now_ we can commit our transation.
print('COMMIT;')

