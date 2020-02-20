#!/usr/bin/python3
from flask import *
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('webindex.html')

@main.route('/homescreen')
def home():
    return render_template('dashboard.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/dashboard')
def dashboard():
    return render_template('user_dashboard.html')

@main.route('/dashboard', methods=['POST', 'GET'])
def uploadpgn():
    if request.method == 'POST':
        new_game = pgn()