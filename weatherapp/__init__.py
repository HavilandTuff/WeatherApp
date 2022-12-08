from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weathers.db"
db = SQLAlchemy()
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from weatherapp import routes, models, api_queries
with app.app_context():
    db.create_all()

