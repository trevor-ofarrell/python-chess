#!/usr/bin/python3
from flask import *
from . import db
from .models import User
from .models import pgn
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import requests
import sys

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

@main.route('/deletepgn', methods=['POST'])
def deletepgn():
    pg = request.form['pgntodel']
    print(pg, file=sys.stderr)
    q = db.session.query(pgn).filter_by(pgnId=pg).one()
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/filterdb', methods=['POST'])
def filterdb():
    Folder = request.form['folder']
    #Folder = "{}{}{}".format('ll', Folder, 'lll')
    gamelist = []
    games = db.session.query(pgn).all()
    for game in games:
        gamelist.append(game.game)
    pgnlist = []
    pgns = db.session.query(pgn).filter_by(folder=Folder).all()
    for pg in pgns:
        pgnlist.append({'name': str(pg.fileName), 'game': pg.game, 'folder': pg.folder, 'frame': pg.frame, 'pgnId': pg.pgnId})
    return render_template('filterdb.html', games=gamelist, folder=Folder, pgnlist=pgnlist)

@main.route('/dashboard')
def dashboard():
    gamelist = []
    games = db.session.query(pgn).all()
    for game in games:
        gamelist.append(game.game)
    pgnlist = []
    pgns = db.session.query(pgn).all()
    for pg in pgns:
        pgnlist.append({'name': str(pg.fileName), 'game': pg.game, 'folder': pg.folder, 'frame': pg.frame, 'pgnId': pg.pgnId})
    folderlist = []
    folders = db.session.query(pgn.folder).all()
    for folder in folders:
        folderlist.append(str(folder))
    folderlist = list(dict.fromkeys(folderlist))
    return render_template('user_dashboard.html', games=gamelist, folders=folderlist, pgnlist=pgnlist)

@main.route('/lichessupload', methods=['POST', 'GET'])
def lichessupload():
    if request.method == 'POST':
        game_string = request.form['gamestring']
        if request.form['name']:
            game_name = request.form['name']
        game_folder = request.form['folder']
        lciframe = "https://lichess.org/embed/" + game_string + "?theme=auto&bg=auto"
        print(lciframe, file=sys.stderr)
        re = requests.get("{}/{}?{}".format('https://lichess.org/game/export',game_string,'pgnInJson=true'))
        new_pgn = pgn(game=re.text, fileName=game_name, folder=game_folder, frame=lciframe)
        db.session.add(new_pgn)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
 
    return render_template('lichessupload.html')

@main.route('/lichessliterate', methods=['POST', 'GET'])
def lichessliterate():
    if request.method == 'POST':
        game_string = request.form['gamestring']
        re = requests.get("{}/{}?{}".format('https://lichess.org/game/export',game_string,'literate=true'))
        if request.form['name']:
            game_name = request.form['name']
        game_folder = request.form['folder']
        lciframe = "{}{}{}".format("https://lichess.org/embed/", game_string, "?theme=auto&bg=auto")
        print(lciframe, file=sys.stderr)
        new_pgn = pgn(game=re.text, fileName=game_name, folder=game_folder, frame=lciframe)
        db.session.add(new_pgn)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
 
    return render_template('lichessupload.html')

@main.route('/mydatabase', methods=['POST', 'GET'])
def mydatabase():
    gamelist = []
    games = db.session.query(pgn).all()
    for game in games:
        gamelist.append(game.game)
    pgnlist = []
    pgns = db.session.query(pgn).all()
    for pg in pgns:
        pgnlist.append({'name': str(pg.fileName), 'game': pg.game, 'folder': pg.folder, 'frame': pg.frame})
    folderlist = []
    folders = db.session.query(pgn.folder).all()
    for folder in folders:
        folderlist.append(str(folder))
    folderlist = list(dict.fromkeys(folderlist))
    return render_template('users_database.html', games=gamelist, folders=folderlist, pgnlist=pgnlist)

@main.route('/uploadpgn', methods=['POST', 'GET'])
def uploadpgn():
    if request.method == 'POST':
        if 'pgnfile' not in request.files:
            flash('No file found')
            return redirect(request.url)

        pgnfile = request.files['pgnfile']
        if pgnfile.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if pgnfile:
            pgndata = pgnfile.read()    
            new_pgn = pgn(game=pgndata, fileName=pgnfile.filename, folder="system uploads")
            db.session.add(new_pgn)
            db.session.commit()
    return redirect(url_for('main.dashboard'))
