from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config 

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from app import models

from .main import main
app.register_blueprint(main)

from .auth import auth
app.register_blueprint(auth)
