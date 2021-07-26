from flask import Flask
from flask_cors import CORS

from frux_chat.api import api


def create_app():

    app = Flask(__name__)
    api.init_app(app)
    CORS(app)

    return app
