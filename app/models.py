from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mood_entries = db.relationship('MoodEntry', backref='user', lazy=True)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    tod = db.Column(db.String(50), nullable=True)
    energy_level = db.Column(db.Integer, nullable=True)
    sleep_quality = db.Column(db.Integer, nullable=True)
    activities = db.Column(db.String(255), nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    weather = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)