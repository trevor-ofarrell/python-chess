#!/usr/bin/python3
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class pgn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(9999))
    name = db.Column(db.String(1000))