from flask import Flask


def create_app(env=None):
    app = Flask("p2pserver")
    register_blueprints(app)
    return app


def register_blueprints(app):
    from server.main import bp

    app.register_blueprint(bp)
