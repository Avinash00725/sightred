# app/models.py

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Set hashed password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Search(db.Model):
    __tablename__ = 'searches'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subreddit = db.Column(db.String(100), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to the user
    user = db.relationship('User', backref=db.backref('searches', lazy='dynamic'))
