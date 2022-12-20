from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from weatherapp.config import Config


app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY')
app.config.from_object(Config)
db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    from weatherapp.users.routes import users
    from weatherapp.main.routes import main
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from weatherapp import models
    with app.app_context():
        db.create_all()

    app.register_blueprint(users)
    app.register_blueprint(main)

    return app