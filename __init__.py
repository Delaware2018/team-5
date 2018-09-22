from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask import g

from front_end import frontend
from nav import nav
from login_data import login_data

import json


app = Flask(__name__)
#global login_data_list
#global is_logged_in


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
<<<<<<< HEAD
    if is_logged_in == False:
        is_logged_in = True
        return render_template("login.html")
    else:
        is_logged_in = True
        return render_template("home.html")
=======
<<<<<<< HEAD
    return render_template("home.html")
=======
    return render_template("main.html")

@app.route('
>>>>>>> a749b9e23a3f48574ff39bfcd9847bb133e5d3a1
>>>>>>> 7d3544f92406d0a5419d074b9f15cfd563bca428


if __name__ == "__main__":
    login_data_list = list()
    is_logged_in = False
    app.debug = True
    app.run()
