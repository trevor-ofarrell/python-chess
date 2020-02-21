#!/usr/bin/python3
from flask import *
from . import db
from .models import User
from .models import pgn
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import requests

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
    gameslist = []
    games = db.session.query(pgn).all()
    for game in games:
        gameslist.append(game.game)
    return render_template('user_dashboard.html', games=gameslist)

@main.route('/lichessupload', methods=['POST', 'GET'])
def lichessupload():
    if request.method == 'POST':
        text = request.form['text']
        re = requests.get("{}/{}?{}".format('https://lichess.org/game/export',text,'pgnInJson=true'))
        game_name = text
        new_pgn = pgn(game=re.text, fileName=game_name)
        db.session.add(new_pgn)
        db.session.commit()
        return render_template('user_dashboard.html')
 
    return render_template('lichessupload.html')

@main.route('/uploadpgn', methods=['POST', 'GET'])
def uploadpgn():
    if request.method == 'POST':
        return render_template('dashboard.html')
        if 'file' not in request.files:
            flash('No file found')
            return redirect(request.url)

        file == request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            with open(file, 'r') as fp:
                filedata = fp.read()
                filename = secure_filename(file.filename)      
            new_pgn = pgn(game=filedata, fileName=filename)
            db.session.add(new_pgn)
            db.session.commit()
    return render_template('profile.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pgn']
