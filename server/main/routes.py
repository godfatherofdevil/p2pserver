from flask import request, jsonify


from server.main import bp
from server.errors import BadMessage
from server.main.operations import register_session, list_all_games


@bp.route("/root", methods=["GET", ])
def home():

    return jsonify({"p2pserver": "i am initialized"})


@bp.route("/register", methods=["POST", ])
def register():
    body = request.json
    if not body:
        raise BadMessage(f"register: body is missing")
    row = register_session(body)
    return jsonify({"success": f"registered your game = {row}!!!"})


@bp.route("/list", methods=["GET", ])
def list_games():
    games = list_all_games()

    return jsonify(games)
