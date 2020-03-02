#!/usr/bin/python3
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class pgn(User):
    __tablename__ = 'pgn'
    __table_args__ = {'extend_existing': True}
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    #owner = db.relationship('User',backref = 'user')
    pgnId = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(9999))
    frame = db.Column(db.String(200))
    fileName = db.Column(db.String(129))
    folder = db.Column(db.String(120))