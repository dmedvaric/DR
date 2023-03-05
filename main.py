from flask import Flask, render_template



app = Flask(__name__)


@app.route("/")  # how to handle requests
def home():
    return render_template('index.html')


from handlers.refresh_all_settings import *
from handlers.refresh_user_settings import *
from handlers.get_user_settings import *
from handlers.registration_user import *
from handlers.login_user import *
from handlers.mail_sender import * 

if __name__ == "__main__":
    app.run(debug=True)

