from flask import Flask

from server.server_db import init_db


def create_app(env=None):
    app = Flask("p2pserver")
    init_db()
    register_blueprints(app)

    return app


def register_blueprints(app):
    from server.main import bp

    app.register_blueprint(bp)
