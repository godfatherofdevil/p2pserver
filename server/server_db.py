import sqlite3
import os


here = os.path.abspath(os.path.dirname(__file__))
pr_root_path = os.path.dirname(here)


def init_db():
    """
    initialize a new sqlite db and create the necessary tables
    :return:
    """
    db_path = os.path.join(pr_root_path, "p2pserver.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    # create table peers
    cursor.execute(
        '''
        create table if not exists peers 
        (
        peer_id text primary key,
        addresses json
        )
        '''
    )

    # create table games
    cursor.execute(
        '''
        create table if not exists games
        (
        id integer primary key autoincrement,
        game_name varchar(100),
        host text,
        foreign key (host) 
        references peers (peer_id) 
        on delete cascade 
        )
        '''
    )

    connection.close()


def get_db():
    """
    return the connection object of p2pserver sqlite database
    :return:
    """
    db_path = os.path.join(pr_root_path, "p2pserver.db")
    connection = sqlite3.connect(db_path)

    return connection


def register_game(name, peer_id, addresses):
    db = get_db()
    cursor = db.cursor()

    peer = (peer_id, addresses, )
    game = (name, peer_id)
    peer_sql = ''' 
    replace into peers (peer_id, addresses) values (?, ?)
    '''
    game_sql = ''' insert into games (game_name, host) values (?, ?)'''
    cursor.execute(peer_sql, peer)
    cursor.execute(game_sql, game)
    db.commit()
    insert_row = cursor.lastrowid
    cursor.close()
    return insert_row


def get_all_games():
    db = get_db()
    cursor = db.cursor()

    games_sql = ''' 
    select distinct games.game_name as name, p.peer_id as peerId 
    from games 
    join 
    peers p 
    on games.host = p.peer_id;
    '''
    cursor.execute(games_sql)
    games = cursor.fetchall()
    cursor.close()

    return games
