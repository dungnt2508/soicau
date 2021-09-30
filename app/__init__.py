from flask import Flask, session
from flask_session import Session
from flask_login import LoginManager
from flask_socketio import SocketIO
import os

from .db import get_user

socketio = SocketIO()
session = Session()


def create_app():
    """setup config"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dungnt1200'
    app.config[
        'APP_DB_URI'] = 'mongodb+srv://dungnt196:25Tuananh08@1stcluster17032020.dabsg.azure.mongodb.net/test?retryWrites=true&w=majority'
    app.config['APP_NS'] = 'snake_bot'
    app.config['SESSION_TYPE'] = 'mongodb'

    """setup Login manager"""
    login_manager = LoginManager()
    login_manager.login_view = 'bp.login'
    login_manager.init_app(app)

    """setup socketio"""
    socketio.init_app(app, cors_allowed_origins='*')

    """setup session"""
    session.init_app(app)

    """setup google login"""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    @login_manager.user_loader
    def load_user(email):
        return get_user(email)

    from .bp import bp as bp
    app.register_blueprint(bp)

    return app
