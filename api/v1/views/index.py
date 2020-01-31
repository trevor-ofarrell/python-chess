#!/usr/bin/python3
"""index for file"""
from flask import jsonify
from api.v1.views import app_views
import json
import chess


@app_views.route('/status')
def status():
    """return status of app"""
    return jsonify({"status": "OK"})


@app_views.route('/')
def status():
    """render python-chess board"""
    board = chess.Board()
    
