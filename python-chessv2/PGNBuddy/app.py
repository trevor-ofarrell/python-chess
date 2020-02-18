#!/usr/bin/python3
from flask import *
from PGNBuddy.views import app_views
import pyrebase

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

config = {
    "apiKey": "AIzaSyAnbMzMdPQqXMKGRVLAZQJq3-yMRYn9DzY",
    "authDomain": "pgnbuddy.firebaseapp.com",
    "databaseURL": "https://pgnbuddy.firebaseio.com",
    "projectId": "pgnbuddy",
    "storageBucket": "pgnbuddy.appspot.com",
    "messagingSenderId": "207583183616",
    "appId": "1:207583183616:web:20b5e65cb049f905fca9e5",
    "measurementId": "G-LBG9Z3TJ5H"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
#email = input('enter email')
#password = input('enter password')
#user = auth.create_user_with_email_and_password(email, password)
#user = auth.sign_in_with_email_and_password(email, password)
#auth.send_email_verification(user['idToken'])
#print(auth.get_account_info(user['idToken']))

main = Blueprint('main', __name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('webindex.html')


@app.route('/profile')
def profile():
    return 'Profile'


@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.errorhandler(404)
def page_not_found(error):
    """error handler for 404 not found"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)
