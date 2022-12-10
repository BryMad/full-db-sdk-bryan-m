import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, func
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
    


# For ORM-style implementations, we need to define a few things first.
ORM_Base = declarative_base()


class Game(ORM_Base):
    __tablename__ = 'game'
    id = Column(Integer, Sequence('game_id_seq'), primary_key=True)
    game_date_est = Column(String)


# The notion of a Session is a multifaceted one whose usage and implementation may change depending on the type
# of application that is using this DAL (particularly, a standalone application vs. a web service). It is implemented
# here in the simplest possible way. Note that if this DAL is to be used in other contexts, code surrounding sessions
# may have to change.
#
# At a minimum, we follow the basic SQLAlchemy rule that sessions should be external to the functions that use them.
# Thus, we define current_session at this upper level, and not within each function.
Session = sessionmaker(bind=db)
current_session = Session()

def update_game_detail({player id})
# might have to close session then reopen


# ORM-style implementation of a game inserter.
def insert_game(game_date_est):
    game = Game(game_date_est=game_date_est)
    current_session.add(game)
    current_session.commit() # Make the change permanent.
    return game

