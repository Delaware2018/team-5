from flask import Flask, render_template, redirect, request
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
app.config.from_object(Config)

login_data_list = list()


with open("static/database.json") as data:
    login_data_list = json.loads(data.read())


def set_login_false():
    open('is_logged_in.txt', 'w').write('False')

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

#/signup?phoneNumberInput=7602126042&firstNameInput=Alexander&lastNameInput=Tuchler&emailInput=awt2124%40columbia.edu&ageInput=19&occupationInput=Student&phoneNumberInput=100000
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
    print(input_data)
    print(request.full_path)
    print(account_data)
    with open('account_data.json', 'w') as outfile:
        json.dump(account_data, outfile)
    print(len(account_data))
    if len(account_data) < 8:
        return render_template('survey.html', title = 'Signup', form=form)
    set_login_false()
    return redirect('/')
    '''if form.validate_on_submit():
        print("YAY")
        flash("Login requested for user {}, remember_me = {}", format(form.phoneNumberInput, form.firstNameInput, form.lastNameInput, form.emailInput, form.ageInput, form.occupationInput, form.incomeInput))
        return redirect('/')
    return render_template('survey.html', title = 'Signup', form=form)'''


if __name__ == "__main__":
    login_data_list = list()
    is_logged_in = True
    app.debug = True
    app.run()
