import os
import csv
import re
import sys


from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, func
from sqlalchemy import Float
from sqlalchemy.orm import sessionmaker, relationship

db = create_engine(os.environ['DB_URL'])
metadata = MetaData(db)
game_table = Table('game', metadata, autoload=True)
game_detail_table = Table('game_detail', metadata, autoload=True)


# Featured Query Functions

# Raw SQL-style implementation of a stats search query.
def search_by_stat_combo(order, pts, reb, ast, blk, stl, limit=100):
    """
    search_by_stat_combo() takes an ordering criteria and a minimum desired value for any combination of the "big 5" 
    game stats and returns the games and player who achieved at least this minimum combination of stats.

    EXAMPLE: Return the game and players who have had at least 30 points, 10 rebounds, 10 assists, and 4 blocks in a game,
    order the results by who scored the most points (in this example, we don't care about steals, so steals should be set to 0)

    PYTHON: search_by_stat_combo(pts, 30, 10, 10, 4, 0)
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 search_by_stat_combo.py pts 30 10 10 4 0

    :param str order: criteria to order results by, abbreviated version of stats (pts, reb, ast, blk, stl)  
    :param int pts: minimum desired points
    :param int reb: minimum desired rebounds
    :param int ast: minimum desired assists
    :param int blk: minimum desired blocks
    :param int stl: minimum desired steals
    :param int limit (optional): limit of how many results
    :return: list of results
    """
    with db.connect() as connection:
        result_set = connection.execute(f"""
            SELECT game_date_est, player_name, pts, reb, ast, blk, stl 
            FROM game INNER JOIN game_detail ON game.id = game_detail.game_id 
            WHERE pts >= {pts} AND reb >= {reb} AND ast >= {ast} AND blk >= {blk} and stl >= {stl} 
            ORDER by {order} DESC LIMIT {limit};
        """)
        result = result_set.fetchall()
        return list(result)


# Raw SQL-style implementation of a stats counting query.
def get_count_by_stat_combo(pts, reb, ast, blk, stl):
    """
    get_count_by_stat_combo() takes minimum desired value for any combination of the "big 5" game stats and returns a list of players and a count 
    of how many times they have achieved this minimum combination of stats in a game, ordered by count descending.

    EXAMPLE: Return the players and the count of games where players have had at least 30 points, 10 rebounds, 10 assists, and 4 blocks in a game.

    PYTHON: get_count_by_stat_combo(30, 10, 10, 4, 0)    
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 get_count_by_stat_combo.py 30 10 10 4 0

    :param int pts: minimum desired points
    :param int reb: minimum desired rebounds
    :param int ast: minimum desired assists
    :param int blk: minimum desired blocks
    :param int stl: minimum desired steals
    :return: list of results
    """
    with db.connect() as connection:
        result_set = connection.execute(f"""
            SELECT player_name, COUNT(*) 
            FROM game INNER JOIN game_detail ON game.id = game_detail.game_id 
            WHERE pts >= {pts} AND reb >= {reb} AND ast >= {ast} AND blk >= {blk} AND stl >= {stl} 
            GROUP BY player_name 
            ORDER BY count DESC;
        """)
        result = result_set.fetchall()
        return list(result)


# Full-Cycle CRUD for For Game Entity

# CRUD User-readable search function to retrieve game ID's.
def search_game_id(team, season, limit=100):
    """
    search_game_id() takes a team and a season start year and returns the dates and game ids of all games from 
    the desired season, ordered by date ascending .

    EXAMPLE: Return the games and game ids of the Mavericks' 2019-2020 season.

    PYTHON: search_game_id(Mavericks, 2019)
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 search_game_id.py Mavericks 2019

    :param str team: team name minimum desired points
    :param int season: start year of season=
    :param int limit (optional): limit of how many results
    :return: list of results
    """
    with db.connect() as connection:
        result_set = connection.execute(f"""
            SELECT game_date_est, game.id, nickname 
            FROM game INNER JOIN team ON game.visitor_team_id = team.id OR game.home_team_id = team.id 
            WHERE nickname ILIKE '{team}' AND season = {season} 
            ORDER by game_date_est LIMIT {limit};;
        """)
        result = result_set.fetchall()
        return list(result)

# CRUD Get-one-Game-by-ID function.
def get_game_by_id(game_id):
    """
    get_game_by_id() takes a game_id returns the basic information of game (date, teams, and score).

    EXAMPLE: Return the basic information for game 22101005.

    PYTHON: get_game_by_id(22101005)
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 get_game_by_id.py 22101005

    :param int game_id: id of the game whose information we wish to retrieve
    :return: single game information
    """
    with db.connect() as connection:
        result_set = connection.execute(f"""
            SELECT gam.game_date_est, 
                gam.id, 
                gam.home_team_id, 
                gam.visitor_team_id, 
                gam.pts_home, 
                gam.pts_away,
                home_team.nickname as home_team,
                visitor_team.nickname as visitor_team
            FROM game gam 
            JOIN team home_team
            ON gam.home_team_id=home_team.id
            JOIN team visitor_team
            ON gam.visitor_team_id=visitor_team.id
            WHERE gam.id = {game_id};
   
        """)
        result = result_set.fetchall()
        return list(result)

# CRUD Delete function part 1.
def delete_game_details(game_id):
    """
    delete_game_details() takes a game_id and deletes the associated game_details from the database. Must be performed before
    delete_game, since game_details.game_id is a foreign key constraint on "game_detail." (know this is kind of a workaround 
    and might be better served by a transaction, but already doing a transaction for Updating and had issues 
    getting this to work as a transaction as well).

    EXAMPLE: Delete the game_details associated with game 22101005 from the database.

    PYTHON: delete_game_details(22101005)
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 delete_game_details.py 22101005

    :param int game_id: id of the game whose information we wish to delete game_details for
    :return: message whether operation was sucessful
    """
    
    with db.connect() as connection:
        result_set = connection.execute(f"""
            DELETE FROM game_detail WHERE game_id = {game_id};
        """)

# CRUD Delete function part 2.
def delete_game(game_id):
    """
    delete_game() takes a game_id and deletes the associated game from the database. Should be run after delete_game_details to ensure game_details associated 
    with the game_id have been deleted to prevent key constraint errors.

    EXAMPLE: Delete game 22101005 from the database.

    PYTHON: delete_game(22101005)
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 delete_game.py 22101005

    :param int game_id: id of the game whose information we wish to delete
    :return: message saying whether operation was succesful
    """
    
    with db.connect() as connection:
        result_set = connection.execute(f"""
            DELETE FROM game WHERE id = {game_id};
        """)

# User-readable search function to retrieve team IDs
def get_team_id(team_name):
    """
    get_team_id() takes a team name returns that team's team.id number

    EXAMPLE: Get the Celtics team.id.

    PYTHON: get_team_id(Celtics)
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 get_team_id.py Celtics

    :param str team: team name
    :return: team.id number
    """
    with db.connect() as connection:
        result_set = connection.execute(f"""
            SELECT id 
            FROM team
            WHERE nickname ILIKE '{team_name}'
        """)
        result = result_set.fetchall()
        return list(result)

# ORM setup for remaining CRUD functions
ORM_Base = declarative_base()

class Game(ORM_Base):
    __tablename__ = 'game'
    id = Column(Integer, Sequence('game_id_seq'), primary_key=True)
    game_date_est = Column(String)
    home_team_id = Column(String)
    visitor_team_id = Column(String)
    pts_home = Column(String)
    pts_away = Column(String)

class Team(ORM_Base):
    __tablename__ = 'team'
    id = Column(Integer, Sequence('team_id_seq'), primary_key=True)
    nickname = Column(String)
    city = Column(String)

class GameDetail(ORM_Base):
    __tablename__ = 'game_detail'
    game_id = Column(Integer, ForeignKey('game.id'), primary_key=True) # ForeignKey takes table properties…
    team_id = Column(Integer, ForeignKey('team.id'), primary_key=True) # ForeignKey takes table properties…
    team_abbreviation = Column(String)
    team_city = Column(String)
    player_id = Column(Integer, primary_key=True) #removed foreign key
    player_name = Column(String)
    nickname = Column(String)
    start_position = Column(String)
    comment = Column(String)
    minutes = Column(String)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    o_reb = Column(Integer)
    d_reb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    turnover = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Integer)

Session = sessionmaker(bind=db)
current_session = Session()

# CRUD creation function
def add_game(game_date_est, home_team, pts_home, visitor_team, pts_away):
    """
    add_game creates a new game in the database based on user inputted values.

    EXAMPLE: Create a (fictitious) game between the Mavericks at the Suns that took place on 2022-12-01 where the glorious Mavericks broke
    all existing NBA records to score 300 points and the pitiful Suns only scored 20 points.

    PYTHON: add_game(2022-12-01, Suns, 20, Mavericks, 300)
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 add_game.py 2022-12-01, Suns 20 Mavericks 300

    :param str game_date_est: date of game in yyyy-mm-dd format
    :param str home_team: home team name
    :param int pts_home: points scored by home team
    :param visitor_team: visitor team name
    :param int pts_away: points scored by away team
    :return: message saying whether operation was succesful
    """
    home_team_id = get_team_id(home_team)[0][0]
    visitor_team_id = get_team_id(visitor_team)[0][0]
    game = Game(game_date_est=game_date_est, home_team_id=home_team_id, visitor_team_id=visitor_team_id, pts_home=pts_home, pts_away=pts_away)
    current_session.add(game)
    current_session.commit() # Make the change permanent.
    return game

# User-readable search function to retrieve Player IDs
def get_game_details_by_id(game_id, limit=100):
    """
    get_player_detail() takes a game_id and returns game_details for the associated game, including player_ids that can be used in the 
    update_player_score() function below.

    EXAMPLE: get game details (including player_ids) for game_id 22101005

    PYTHON: get_game_details_by_id(22101005)
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 get_game_details_by_id.py 22101005

    :param int game_id: id of the game whose game_details we wish to retrieve
    :return: list of game_details with desired information
    """
    query = current_session.query(GameDetail).\
        filter(GameDetail.game_id == game_id).\
        limit(limit)
    return query.all()

# CRUD Update Function + Required Transaction
def update_player_score(game_id, player_id, change_amount):
    """
    update_player_score() takes a game_id, a player_id, and a change amount, and updates a player's individual game_detail score as well
    as adjusting game's overall score. For help retrieving player_ids.

    EXAMPLE: The NBA has reviewed game 22101008 and determined Khris Middleton's shot that was recorded as a 2 pointer was actually a 3 pointer. 
    Update his game_detail stats and the Buck's game entry score, adding 1 point to each to reflect these point changes.

    PYTHON: update_player_score(22101008, 203114, 1)
    COMMAND LINE: DB_URL=postgresql://localhost/postgres python3 update_player_score.py 22101008 203114 1

    :param int game_id: id of the game to update
    :param int player_id: id of the player whose points need updating
    :param int change_amount: amount of points to add (or subtract if negative number given)
    :return: message saying whether operation was succesful
    """
    try:
        # first query.  a Connection is acquired
        # from the Engine, and a Transaction
        # started.
        game = current_session.query(Game).\
            filter(Game.id == game_id).first()
        # second query.  the same Connection/Transaction
        # are used.
        detail = current_session.query(GameDetail).\
            filter(GameDetail.game_id == game_id).\
            filter(GameDetail.player_id == player_id).first()

        detail.pts += change_amount

        if detail.team_id == game.home_team_id:
            game.pts_home += change_amount 
        if detail.team_id == game.visitor_team_id:
            game.pts_away += change_amount 

        # commit.  The pending changes above
        # are flushed via flush(), the Transaction
        # is committed, the Connection object closed
        # and discarded, the underlying DBAPI connection
        # returned to the connection pool.
        current_session.commit()
    except:
        # on rollback, the same closure of state
        # as that of commit proceeds.
        current_session.rollback()
        raise
    finally:
        # close the Session.  This will expunge any remaining
        # objects as well as reset any existing SessionTransaction
        # state.  Neither of these steps are usually essential.
        # However, if the commit() or rollback() itself experienced
        # an unanticipated internal failure (such as due to a mis-behaved
        # user-defined event handler), .close() will ensure that
        # invalid state is removed.
        current_session.close()         

