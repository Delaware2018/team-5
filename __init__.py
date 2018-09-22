from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask import g

from front_end import frontend
from nav import nav
from login_data import login_data

import json


app = Flask(__name__)
login_data_list = list()


with open("static/database.json") as data:
    login_data_list = json.loads(data.read())


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
        return render_template("home.html")


if __name__ == "__main__":
    login_data_list = list()
    is_logged_in = False
    app.debug = True
    app.run()
