from flask import jsonify


from server.main import bp


@bp.route("/root", methods=["GET", ])
def home():

    return jsonify({"p2pserver": "i am initialized"})
