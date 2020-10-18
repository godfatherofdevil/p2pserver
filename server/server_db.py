import sqlite3
import os

from server.const import GameStatus


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
        id integer primary key autoincrement,
        peer_id text not null
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
        host integer ,
        status integer default 0,
        foreign key (host) 
        references peers (id) 
        on delete cascade 
        )
        '''
    )

    # create table addresses
    cursor.execute(
        '''
        create table if not exists addresses
        (
        id integer primary key autoincrement,
        host varchar(100),
        guest varchar(100),
        host_addresses json,
        guest_addresses json,
        game integer,
        foreign key (game) 
        references games (id) 
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


def register_game(name, peer_id):
    db = get_db()
    cursor = db.cursor()

    peer = (peer_id, )
    game = (name, peer_id)
    peer_sql = ''' 
    replace into peers (peer_id) values (?)
    '''
    game_sql = ''' insert into games (game_name, host) values (?, ?)'''
    cursor.execute(peer_sql, peer)
    cursor.execute(game_sql, game)
    db.commit()
    insert_row = cursor.lastrowid
    cursor.close()
    return insert_row


def delete_game(game_name: str):
    db = get_db()
    cursor = db.cursor()
    delete_sql = ''' delete from games where game_name=?'''
    cursor.execute(delete_sql, (game_name, ))
    db.commit()
    cursor.close()


def update_game(game_name: str, new_name):
    db = get_db()
    cursor = db.cursor()
    update_sql = '''update games set game_name=? where game_name=?'''
    cursor.execute(update_sql, (new_name, game_name))
    db.commit()
    cursor.close()


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


def game_status(game_name: str):
    db = get_db()
    cursor = db.cursor()
    status_sql = ''' select status from games where game_name=?'''
    cursor.execute(status_sql, (game_name,))
    db.commit()
    status = cursor.fetchone()
    cursor.close()

    return status


def set_game_status(game_name: str, status=GameStatus.waiting):
    db = get_db()
    cursor = db.cursor()
    set_status_sql = ''' update games set status=? where game_name=?'''
    cursor.execute(set_status_sql, (status, game_name,))
    status_sql = ''' select status from games where game_name=?'''
    status = cursor.execute(status_sql, (game_name, )).fetchone()
    db.commit()
    cursor.close()

    return status


def update_host_addresses(host_id, addresses, game_name):
    db = get_db()
    cursor = db.cursor()
    game_sql = '''select id from games where game_name=?'''
    game_id = cursor.execute(game_sql, (game_name, )).fetchone()
    if not game_id:
        return []
    game_id = game_id[0]
    host_sql = ''' replace into addresses (host, host_addresses, game) values (?,?,?)'''
    cursor.execute(host_sql, (host_id, addresses, game_id))
    db.commit()
    cursor.close()


def update_guest_addresses(guest_id, addresses, game_name):
    db = get_db()
    cursor = db.cursor()
    game_sql = ''' select id from games where game_name=?'''
    game_id = cursor.execute(game_sql, (game_name,)).fetchone()
    if not game_id:
        return []
    game_id = game_id[0]
    guest_sql = ''' replace into addresses (guest, guest_addresses, game) values (?,?,?)'''
    cursor.execute(guest_sql, (guest_id, addresses, game_id))
    db.commit()
    cursor.close()


def get_host_addresses(game_name):
    db = get_db()
    cursor = db.cursor()
    game_sql = ''' select id from games where game_name=?'''
    game_id = cursor.execute(game_sql, (game_name,)).fetchone()
    if not game_id:
        return []
    game_id = game_id[0]
    host_address_sql = ''' select host_addresses from addresses where game=?'''
    cursor.execute(host_address_sql, (game_id, ))

    host_address = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    return host_address


def get_guest_addresses(game_name):
    db = get_db()
    cursor = db.cursor()
    game_sql = ''' select id from games where game_name=?'''
    game_id = cursor.execute(game_sql, (game_name,)).fetchone()
    if not game_id:
        return []
    game_id = game_id[0]
    guest_address_sql = ''' select guest_addresses from addresses where game=?'''
    cursor.execute(guest_address_sql, (game_id, ))

    guest_address = cursor.fetchone()
    db.commit()
    cursor.close()
    return guest_address

