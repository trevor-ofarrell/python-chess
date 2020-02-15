#!/usr/bin/python3
from flask import Flask, jsonify, render_template
from PGNBuddy.views import app_views

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    """error handler for 404 not found"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)
