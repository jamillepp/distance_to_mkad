from flask import Flask
from app import getdistance


def create_app():

    app: Flask = Flask(__name__)
    app.register_blueprint(getdistance.bp)

    @app.route('/')
    def start():
        return ""

    return app
