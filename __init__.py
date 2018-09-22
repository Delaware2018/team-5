from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig

from front_end import frontend
from nav import nav
from login_data import login_data


app = Flask(__name__)
login_data_list = list()

with open('\static\database.json', encoding = 'utf-8') as data:
    login_data_list = json.loads(data.read())


def create_app(configfile = None):
    #app = Flask(__name__)
    AppConfig(app)
    Bootstrap(app)
    app.register_blueprint(frontend)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    nav.init_app(app)
    return app


@app.route('/login/')
def index():
    return render_template("main.html")

@app.route('


if __name__ == "__main__":
    app.debug = True
    app.run()

