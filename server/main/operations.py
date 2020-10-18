import json

from server.server_db import register_game, get_all_games


def register_session(session_params: dict):
    name = session_params.get("name")
    peer_id = session_params.get("peerId")
    # take the internal addresses from the host requesting to register a streaming session
    # at registration time as in the rest api there will be no way for the server to communicate
    # to host that someone wants to establish a connection
    addresses = session_params.get("addresses")

    row_id = register_game(name, peer_id, json.dumps(addresses))

    return row_id


def list_all_games():
    games = []
    for game in get_all_games():
        games.append({"name": game[0], "peerId": game[1]})
    return games
