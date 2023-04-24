from flask import Flask
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO

# Configurations
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']
db = SQLAlchemy(app, session_options={"autoflush": False})
csrf = CSRFProtect(app)
socketio = SocketIO(app)

from app.routes import *
from app.api_routes import *
from app.socket_routes import *
from app.models import *
