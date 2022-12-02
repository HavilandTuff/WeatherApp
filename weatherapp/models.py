from weatherapp import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    weathers = db.relationship('Weather', backref='owner', lazy=True)

    def __repr__(self) -> str:
        return f"User: {self.username}, {self.email}"


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, unique=True, nullable=False)
    weather = db.Column(db.String, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"City: {self.city}, {self.last_update}"