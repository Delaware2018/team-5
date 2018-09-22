from flask import Flask, render_template, redirect, request, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask import g

from front_end import frontend
from nav import nav
from login_data import login_data
from forms import SignupForm
from forms import LoginForm
from config import Config

import json

from receipt.data import User
from receipt.receipt_reader import read_receipt


app = Flask(__name__)
app.config.from_object(Config)
user = None


with open("static/joe.json") as data:
    entry_dict = json.load(data)
    user = User(entry_dict)


def set_login_state(state): #state should be either 'True' or 'False'
    open('is_logged_in.txt', 'w').write(state)


def create_app(configfile = None):
    #app = Flask(__name__)
    AppConfig(app)
    Bootstrap(app)
    app.register_blueprint(frontend)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    nav.init_app(app)
    return app


@app.route('/', methods=["GET", "POST"])
def index():
    data_fields = ["phone", "last_name"]
    form = LoginForm()
    f = open('is_logged_in.txt', 'r').read().splitlines()
    is_logged_in = True if f[0] == "True" else False
    account_data = {"phone":"","last_name":""}
    input_data = request.full_path[2:]
    chars = ""
    take_chars = False
    index = 0
    for c in input_data:
        if c == '&':
            account_data[data_fields[index]] = chars
            index += 1
            chars = ""
            take_chars = False
        if take_chars:
            chars += c
        if c == '=':
            take_chars = True
    account_data[data_fields[index]] = chars
    compare_data = None
    
    with open("account_data.json") as data:
        compare_data = json.load(data)
    
    if compare_data[data_fields[1]] == account_data[data_fields[1]] and compare_data[data_fields[0]] == account_data[data_fields[0]]:
        set_login_state("True")
        return redirect("home")
    else:
        return render_template("login.html", title = 'Signup', form=form)


@app.route('/home', methods=["GET", "POST"])
def main_page():
    user_data = None
    with open('account_data.json') as data:
        user_data = json.load(data)
    full_name = user_data['first_name'] + " " + user_data['last_name']
    return render_template('home.html')


@app.route('/upload')
def upload_page():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      receipt_file = request.files['file']
      items = read_receipt(receipt_file.filename)
      user['data']['history'].extend(items)

      flash('Thanks for you receipt!')
      print(user)
      return redirect('home')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    data_fields = ['phone', 'first_name', 'last_name', 'email', 'age', 'job', 'income', 'history']
    form = SignupForm()
    account_data = dict()
    input_data = request.full_path[8:]
    chars = ""
    take_chars = False
    index = 0
    for c in input_data:
        if c == '&':
            account_data[data_fields[index]] = chars
            index += 1
            chars = ""
            take_chars = False
        if take_chars:
            chars += c
        if c == '=':
            take_chars = True
    account_data[data_fields[index]] = chars
    index += 1
    account_data[data_fields[index]] = list()
    with open('account_data.json', 'w') as outfile:
        json.dump(account_data, outfile)
    if len(account_data) < 8:
        return render_template('survey.html', title = 'Signup', form=form)
    set_login_state('False')
    return redirect('/')

@app.route('/profile')
def profile_page():
    out_str = ''
    out_str += 'Name: %s %s<br />' % (user['first_name'], user['last_name'])
    out_str += 'History: <br />'
    
    for item in user['data']['history']:
        out_str += '\t%s<br />' % item

    out_str += '<br />%s<br />' % user

    return out_str



   
if __name__ == "__main__":
    login_data_list = list()
    is_logged_in = True
    app.debug = True
    app.run()
