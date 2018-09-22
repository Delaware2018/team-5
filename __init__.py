from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig

from front_end import frontend
from nav import nav

app = Flask(__name__)

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
    return render_template("home.html")


if __name__ == "__main__":
    app.debug = True
    app.run()

