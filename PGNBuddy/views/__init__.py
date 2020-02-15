#!/usr/bin/python3
"""init file """
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix='/pgnviewer')
from PGNBuddy.views.index import *
