#!/usr/bin/python3
from flask import *
from PGNBuddy.views import app_views
import pyrebase

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

config = {
    #Fire base config info here
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
#email = input('enter email')
#password = input('enter password')
#user = auth.create_user_with_email_and_password(email, password)
#user = auth.sign_in_with_email_and_password(email, password)
#auth.send_email_verification(user['idToken'])
#print(auth.get_account_info(user['idToken']))

@app.route('/', methods=['GET', 'POST'])
def login():
    succesful = "Login succesful"
    unsuccesful = 'incorrect email or password'
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('index.html', s=succesful)
        except:
            return render_template('index.html', us=unsuccesful)
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    """error handler for 404 not found"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)
