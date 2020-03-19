#!/usr/bin/python3
from flask import *
from . import db
from .models import User
from .models import pgn
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import requests
import sys
from datetime import datetime

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
    q = db.session.query(pgn).filter_by(pgnId=pg).one()
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for('main.dashboard'))


@main.route('/filterdb', methods=['POST'])
def filterdb():
    Folder = request.form['folder']
    gamelist = []
    games = db.session.query(pgn).all()
    for game in games:
        gamelist.append(game.game)

    pgnlist = []
    pgns = db.session.query(pgn).filter_by(folder=Folder).all()
    for pg in pgns:
        pgnlist.append({
            'name': str(pg.fileName),
            'game': pg.game,
            'folder': pg.folder,
            'frame': pg.frame,
            'pgnId': pg.pgnId
        })
    return render_template(
        'filterdb.html',
        games=gamelist,
        folder=Folder,
        pgnlist=pgnlist
    )


@main.route('/dashboard')
def dashboard():
    try:
        current_user = User.query.filter_by(email=session['email']).first()
    except:
        return render_template('webindex.html')
    games = db.session.query(pgn).filter_by(userId=current_user.id).all()

    gamelist = []
    for game in games:
        gamelist.append(game.game)

    pgnlist = []
    pgns = db.session.query(pgn).filter_by(userId=current_user.id).all()
    for pg in pgns:
        pgnlist.append({
            'name': str(pg.fileName),
            'game': pg.game,
            'folder': pg.folder,
            'frame': pg.frame,
            'pgnId': pg.pgnId
        })
    folderlist = []
    folders = db.session.query(pgn.folder).filter_by(
        userId=current_user.id).all()

    for folder in folders:
        folderlist.append(str(folder))
    folderlist = list(dict.fromkeys(folderlist))

    return render_template(
        'user_dashboard.html',
        games=gamelist,
        folders=folderlist,
        pgnlist=pgnlist
    )


@main.route('/lichessupload', methods=['POST', 'GET'])
def lichessupload():
    if request.method == 'POST':
        try:
            current_user = User.query.filter_by(email=session['email']).first()
        except:
            return render_template('webindex.html')

        if request.form['name']:
            game_name = request.form['name']

        game_string = request.form['gamestring']
        print(len(game_string), file=sys.stderr)

        if str(game_string)[:5] == "liche":
            game_string = game_string[12:]

        elif str(game_string)[:5] == "http:":
            game_string = game_string[19:]
            print(game_string, file=sys.stderr)

        elif str(game_string)[:5] == "https":
            game_string = game_string[20:]

        if len(game_string) != 8:
            game_string = game_string[:8]

        game_folder = request.form['folder']
        lciframe = "https://lichess.org/embed/" + game_string + "?theme=auto&bg=auto"
        uid = current_user.id

        re = requests.get("{}/{}?{}".format(
            'https://lichess.org/game/export',
            game_string,
            'pgnInJson=true'
        ))
        new_pgn = pgn(
            userId=uid,
            game=re.text,
            fileName=game_name,
            folder=game_folder,
            frame=lciframe
        )
        db.session.add(new_pgn)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    try:
        current_user = User.query.filter_by(email=session['email']).first()
    except:
        return render_template('webindex.html')

    return render_template('lichessupload.html')


@main.route('/lichessliterate', methods=['POST', 'GET'])
def lichessliterate():
    if request.method == 'POST':
        try:
            current_user = User.query.filter_by(email=session['email']).first()
        except:
            return render_template('webindex.html')

        uid = current_user.id
        game_string = request.form['gamestring']

        if str(game_string)[:5] == "liche":
            game_string = game_string[12:]

        elif str(game_string)[:5] == "http:":
            game_string = game_string[19:]
            print(game_string, file=sys.stderr)

        elif str(game_string)[:5] == "https":
            game_string = game_string[20:]

        if len(game_string) != 8:
            game_string = game_string[:8]

        re = requests.get("{}/{}".format(
            'https://lichess.org/game/export',
            game_string),
            params={"clocks": "false", "literate": "true", "evals": "true"}
        )
        if request.form['name']:
            game_name = request.form['name']
    
        game_folder = request.form['folder']
        lciframe = "{}{}{}".format(
            "https://lichess.org/embed/",
            game_string,
            "?theme=auto&bg=auto"
        )
        new_pgn = pgn(
            userId=uid,
            game=re.text,
            fileName=game_name,
            folder=game_folder,
            frame=lciframe
        )
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
        pgnlist.append({
            'name': str(pg.fileName),
            'game': pg.game,
            'folder': pg.folder,
            'frame': pg.frame
        })

    folderlist = []
    folders = db.session.query(pgn.folder).all()

    for folder in folders:
        folderlist.append(str(folder))

    folderlist = list(dict.fromkeys(folderlist))

    return render_template(
        'users_database.html',
        games=gamelist,
        folders=folderlist,
        pgnlist=pgnlist
    )


@main.route('/uploadpgn', methods=['POST', 'GET'])
def uploadpgn():
    if request.method == 'POST':
        try:
            current_user = User.query.filter_by(email=session['email']).first()
        except:
            return render_template('webindex.html')

        uid = current_user.id

        if 'pgnfile' not in request.files:
            flash('No file found')
            return redirect(request.url)

        pgnfile = request.files['pgnfile']

        if pgnfile.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if pgnfile:
            pgndata = pgnfile.read()
            new_pgn = pgn(
                userId=uid,
                game=pgndata,
                fileName=pgnfile.filename,
                folder="system uploads"
            )
            db.session.add(new_pgn)
            db.session.commit()
    return redirect(url_for('main.dashboard'))


@main.route('/exportall', methods=['GET', 'POST'])
def exportall():
    if request.method == 'POST':
        username = request.form['username']
        re = requests.get("{}{}".format(
            "https://lichess.org/api/games/user/",
            username
            ), 
            params={
                "pgnInJson": "true",
                "max": "500"
            },
            headers={
                "Accept": "application/x-ndjson"
            },
            stream=True
        )
        with open("Trevor_lichess_download.json", 'w') as fp:
            #json.dump(re.json, fp)
            fp.write(dict(re.text))
        #print(re.text, file=sys.stderr)
        for line in re.json():
            print((line, type(line)), file=sys.stderr)
            #time_stamp = line["createdAt"]
            time_stamp = datetime.utcfromtimestamp(
                time_stamp).strftime('%Y-%m-%d %H:%M:%S')
            print(time_stamp, file=sys.stderr)
            #db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('lichessexportall.html')


@main.route('/nothingyet', methods=['GET', 'POST'])
def nothingyet():
    pass

@main.route('/editpgn', methods=['GET', 'POST'])
def editpgn():
    pg = request.form['editpgn']
    q = db.session.query(pgn).filter_by(pgnId=pg).one()
    return render_template('editpgn.html', pgn=q.game)