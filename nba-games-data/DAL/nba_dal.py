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


# Raw SQL-style implementation of a game query.
def search_games_by_date(query, limit=100):
    with db.connect() as connection:
        result_set = connection.execute(f"""
            SELECT * FROM game WHERE game_date_est = '{query}' ORDER BY game_date_est LIMIT {limit}
        """)
        result = result_set.fetchall()
        return list(result)

# Raw SQL-style implementation of a stats query.
def search_details_by_stat_combo(order, pts, reb, ast, blk, stl, limit=100):
    with db.connect() as connection:
        result_set = connection.execute(f"""
            SELECT game_date_est, player_name, pts, reb, ast, blk, stl FROM game INNER JOIN game_detail ON game.id = game_detail.game_id WHERE pts >= {pts} AND reb >= {reb} AND ast >= {ast} AND blk >= {blk} and stl >= {stl} ORDER by {order} DESC LIMIT {limit};
        """)
        result = result_set.fetchall()
        return list(result)


# Raw SQL-style implementation of a stats counting query.
def get_count_by_stat_combo(pts, reb, ast, blk, stl, limit=100):
    with db.connect() as connection:
        result_set = connection.execute(f"""
            SELECT player_name, COUNT(*) 
            FROM game INNER JOIN game_detail ON game.id = game_detail.game_id 
            WHERE pts >= {pts} AND reb >= {reb} AND ast >= {ast} AND blk >= {blk} AND stl >= {stl} GROUP BY player_name 
            ORDER BY count DESC;
        """)
        result = result_set.fetchall()
        return list(result)


# Raw SQL-style implementation of a user readable search function.
def search_game_id(team, season, location, limit=100):
    with db.connect() as connection:
        result_set = connection.execute(f"""
            SELECT game_date_est, game.id, nickname FROM game INNER JOIN team ON game.{location}_team_id = team.id WHERE nickname ILIKE '{team}' AND season = {season} LIMIT {limit};
        """)
        result = result_set.fetchall()
        return list(result)

# Raw SQL-style implementation of a Get-one-entity-by-ID function.
def get_game_id(game_id, limit=100):
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

# Raw SQL-style implementation of a delete function.
def delete_game(game_id):
    with db.connect() as connection:
        result_set = connection.execute(f"""
            DELETE FROM game WHERE id = {game_id};
        """)
  #      result = result_set.fetchall()
#     return list(result)


# For ORM-style implementations, we need to define a few things first.
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




# The notion of a Session is a multifaceted one whose usage and implementation may change depending on the type
# of application that is using this DAL (particularly, a standalone application vs. a web service). It is implemented
# here in the simplest possible way. Note that if this DAL is to be used in other contexts, code surrounding sessions
# may have to change.
#
# At a minimum, we follow the basic SQLAlchemy rule that sessions should be external to the functions that use them.
# Thus, we define current_session at this upper level, and not within each function.
Session = sessionmaker(bind=db)
current_session = Session()

#def update_game(new away )
# might have to close session then reopen


# ORM-style implementation of a creation function for creating new game entry
#Creation function
def add_game(game_date_est, home_team_id, visitor_team_id, pts_home, pts_away):
    game = Game(game_date_est=game_date_est, home_team_id=home_team_id, visitor_team_id=visitor_team_id, pts_home=pts_home, pts_away=pts_away)
    current_session.add(game)
    current_session.commit() # Make the change permanent.
    return game

def update_player_score(game_id, player_id, change_amount):
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

# ORM-style implementation of a rating query.
def get_game_details(game_id, limit=100):
    query = current_session.query(GameDetail).\
        filter(GameDetail.game_id == game_id).\
        limit(limit)
    return query.all()


def get_game_by_id_orm(game_id):
    query = current_session.query(Game).\
        filter(Game.id == game_id)
    return query.all()

def get_player_detail_orm(game_id, player_id):
    query = current_session.query(GameDetail).\
        filter(GameDetail.game_id == game_id).\
        filter(GameDetail.player_id == player_id)
    return query.all()