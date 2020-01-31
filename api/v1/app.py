#!/usr/bin/python3
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


#@app.teardown_appcontext
#def teardown_db(x):
#    """close storage after session"""
#    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """error handler for 404 not found"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
