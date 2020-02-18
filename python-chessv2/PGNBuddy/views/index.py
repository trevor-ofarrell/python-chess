#!/usr/bin/python3
from flask import jsonify
import json
from PGNBuddy.views import app_views

@app_views.route('/status')
def status():
    """return status of app"""
    return jsonify({"status": "OK"})

@app_views.route('/<pgn>')
def viewpgn(pgn):
    """return status of app"""
    with open(pgn, encoding="utf-8-sig") as pgn:
        first_game = chess.pgn.read_game(pgn)
        for move in first_game.mainline_moves():
            board.push(move)
