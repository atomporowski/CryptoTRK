from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    def __repr__(self):
        return f"Post('{self.email}', '{self.first_name}')"


class Portfolios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apiKey = db.Column(db.String(64))
    apiSecret = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# TODO : check tracking performance will work with csv - if so, remove below
#class Performance(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    date = db.Column(db.Integer(5))