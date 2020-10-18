from flask import Flask, jsonify

from server.server_db import init_db
from server.errors import BadMessage, OutOfOrderOperation


# error handlers
def bad_request(err):
    return jsonify({"error": str(err)}), 400


def unhandled(err):
    return jsonify({"error": str(err)}), 500


def handle_404(err):
    return jsonify({"error": str(err)}), 404


def create_app(env=None):
    app = Flask("p2pserver")
    init_db()
    app.register_error_handler(404, handle_404)
    app.register_error_handler(BadMessage, bad_request)
    app.register_error_handler(OutOfOrderOperation, bad_request)
    app.register_error_handler(Exception, unhandled)
    register_blueprints(app)

    return app


def register_blueprints(app):
    from server.main import bp

    app.register_blueprint(bp)
