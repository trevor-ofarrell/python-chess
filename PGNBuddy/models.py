#!/usr/bin/python3
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class pgn(db.Model):
    __tablename__ = 'pgn'
    __table_args__ = {'extend_existing': True}
    #owner = db.relationship('User',backref = 'user')
    #userId = db.Column(db.Integer)
    game = db.Column(db.String(9999))
    fileName = db.Column(db.String(129))
    folder = db.Column(db.String(120))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    frame = db.Column(db.String(200))
    pgnId = db.Column(db.Integer, primary_key=True)
