import sqlite3
import json

from server.server_db import delete_game, get_all_games, register_game, update_game, game_status, \
    update_host_addresses, update_guest_addresses, set_game_status, get_guest_addresses, \
    get_host_addresses
from server.const import PeerTypes, GameStatus


def register_session(session_params: dict):
    name = session_params.get("name")
    peer_id = session_params.get("peerId")
    row_id = register_game(name, peer_id)

    return row_id


def list_all_games():
    games = []
    for game in get_all_games():
        games.append({"name": game[0], "peerId": game[1]})
    return games


def delete_one_game(game_name):

    try:
        delete_game(game_name)
    except sqlite3.OperationalError:
        status = "failure"
    else:
        status = "success"

    return status


def update_one_game(game_name, new_name):
    try:
        update_game(game_name, new_name)
    except sqlite3.OperationalError:
        status = "failure"
    else:
        status = "success"

    return status


def get_game_status(game_name):
    return game_status(game_name)


def activate_game_status(game_name):
    set_game_status(game_name, status=GameStatus.active)


def set_addresses(peer_id, peer_type, addresses, game_name):
    if peer_type == PeerTypes.host:
        update_host_addresses(peer_id, json.dumps(addresses), game_name)
    elif peer_type == PeerTypes.guest:
        update_guest_addresses(peer_id, json.dumps(addresses), game_name)


def get_addresses(peer_type, game_name):
    if peer_type == PeerTypes.host:
        return json.loads(get_host_addresses(game_name))
    elif peer_type == PeerTypes.guest:
        return json.loads(get_guest_addresses(game_name))


def start_a_game_session(session_params: dict):
    name = session_params.get("name")
    peer_id = session_params.get("peerId")

