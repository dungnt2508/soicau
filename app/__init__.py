from flask import Flask
from flask_session import Session
from flask_login import LoginManager
from flask_socketio import SocketIO
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from .db import get_user

socketio = SocketIO()

def create_app():
    """setup config"""
    app = Flask(__name__)
    app.config['APP_NS'] = 'snake_bot'
    app.config['SECRET_KEY'] = 'dungnt2200'
    app.config['APP_DB_URI'] = "mongodb+srv://dungnt196:25Tuananh08@1stcluster17032020.dabsg.azure.mongodb.net/?retryWrites=true&w=majority&appName=1stCluster17032020"

    """ Thiết lập MongoDB Client cho session """
    app.config['SESSION_TYPE'] = 'mongodb'
    app.config['SESSION_MONGODB'] = MongoClient(app.config['APP_DB_URI'], server_api=ServerApi('1'))
    app.config['SESSION_MONGODB_DB'] = "session_db"  # Database dùng để lưu session
    app.config['SESSION_MONGODB_COLLECTION'] = "sessions"  # Collection dùng để lưu session

    """setup Login manager"""
    login_manager = LoginManager()
    login_manager.login_view = 'bp.login'
    login_manager.init_app(app)

    """setup socketio"""
    socketio.init_app(app, cors_allowed_origins='*')

    """setup session"""
    Session(app)  # Thay vì `session.init_app(app)`, dùng `Session(app)`

    """setup google login"""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    @login_manager.user_loader
    def load_user(email):
        return get_user(email)

    from .bp import bp as bp
    app.register_blueprint(bp)

    return app
