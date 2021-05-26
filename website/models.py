from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class Portfolios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apiKey = db.Column(db.String(64))
    apiSecret = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
