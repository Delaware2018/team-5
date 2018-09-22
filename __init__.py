from flask import Flask, render_template, redirect, request, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask import g

from front_end import frontend
from nav import nav
from login_data import login_data
from forms import SignupForm
from config import Config


import json


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config.from_object(Config)
user = None

with open("static/joe.json") as data:
    user = json.load(data)


def create_app(configfile = None):
    #app = Flask(__name__)
    AppConfig(app)
    Bootstrap(app)
    app.register_blueprint(frontend)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    nav.init_app(app)
    return app


@app.route('/')
def index():
    f = open('is_logged_in.txt', 'r').read().splitlines()
    is_logged_in = True if f[0] == "True" else False
    print(login_data_list)
    if is_logged_in == False:
        f[0] = "True"
        open('is_logged_in.txt', 'w').write('\n'.join(f))
        return render_template("login.html")
    else:
        is_logged_in = True
        return redirect("home")


@app.route('/home')
def main_page():
    return render_template('home.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      receipt_file = request.files['file']
      flash('Thanks for you receipt!')
      return redirect('home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    print(form.phoneNumberInput)
    if form.validate_on_submit():
        print('afasoksf')
        flash("Login requested for user {}, remember_me = {}", format(form.phoneNumberInput, form.firstNameInput, form.lastNameInput, form.emailInput, form.ageInput, form.occupationInput, form.incomeInput))
        return redirect('/')
    print('faijfsofioa')
    return render_template('survey.html', title = 'Signup', form=form)


if __name__ == "__main__":
    login_data_list = list()
    is_logged_in = True
    app.debug = True
    app.run()
