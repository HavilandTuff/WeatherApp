from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY')
app.config['SECRET_KEY'] = os.getenv('SERET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weathers.db"
db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()

from weatherapp import routes, models, api_queries