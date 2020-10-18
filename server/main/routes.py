from flask import request, jsonify


from server.main import bp
from server.errors import BadMessage
from server.main.operations import register_session, list_all_games, delete_one_game, \
    update_one_game, get_game_status, set_addresses, activate_game_status, get_addresses
from server.const import PeerTypes, GameStatus


@bp.route("/register", methods=["POST", ])
def register():
    body = request.json
    if not body:
        raise BadMessage(f"register: body is missing")
    row = register_session(body)
    return jsonify({"success": f"registered your game = {row}!!!"}), 200


@bp.route("/games", methods=["GET"])
def list_games():
    all_games = list_all_games()
    return jsonify(all_games), 200


@bp.route("/games/<name>", methods=["PUT", "DELETE"])
def games_update_delete(name: str):
    if not name:
        raise BadMessage(f"games: name is missing")
    return_msg, status = {}, None
    if request.method == "DELETE":
        status = delete_one_game(game_name=name)
    elif request.method == "PUT":
        new_name = request.args.get("newName")
        if not new_name:
            raise BadMessage(f"games: can't update without new game name")
        status = update_one_game(game_name=name, new_name=new_name)
        return_msg["newName"] = new_name
    return_msg["operation"] = request.method
    return_msg["status"] = status
    return jsonify(return_msg)


@bp.route("/games/poll", methods=["POST", ])
def poll_games():
    """
    a client which registered a game session should poll this endpoint to know if another client
    is ready to engage or not, {"status": 0} -> not ready, {"status": 1} -> ready
    when for a given game, another client is ready to engage then this endpoint
    will return addresses for the guest client otherwise it will update the hosts addresses
    and return game_status and empty list of addresses
    request model:
    {
    "name": <game_name>,
    "peerId": <peerId>,
    "addresses": <host_candidate_addresses>,
    }
    :return:
    """
    body = request.json
    if not body:
        raise BadMessage(f"poll_games: game name, peerId required to poll")
    game = body.get("name")
    peer_id = body.get("peerId")
    addresses = body.get("addresses")
    game_status = get_game_status(game_name=game)
    set_addresses(peer_id, PeerTypes.host, addresses, game)
    if game_status == GameStatus.active:
        guest_addresses = get_addresses(PeerTypes.guest, game_name=game)
    else:
        guest_addresses = []
    return jsonify({"addresses": guest_addresses, "status": game_status}), 200


@bp.route("/games/start", methods=["POST", ])
def start_a_game():
    """
    this endpoint should be used by the client which wants to join one of the existing games
    request model:
    {
    "name": <game_name>,
    "peerId": <peerId>,
    "addresses": <guest_candidate_addresses>,
    }
    :return:
    """
    body = request.json
    if not body:
        raise BadMessage(f"start_a_game: request body is missing")
    game = body.get("name")
    peer_id = body.get("peerId")
    addresses = body.get("addresses")
    game_status = activate_game_status(game_name=game)
    set_addresses(peer_id, PeerTypes.guest, addresses, game)
    host_addresses = get_addresses(PeerTypes.host, game_name=game)

    return jsonify({"addresses": host_addresses, "status": game_status}), 200





