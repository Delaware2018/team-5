from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

from .forms import SignupForm
from .nav import nav

frontend = Blueprint('frontend', __name__)

nav.register_element('frontend_top', Navbar(
    View('Home', '.index'),
    View('Profile', '.index'),
    View('Statistics', '.example_form'),
    View('Find A Store', 'debug.debug_root'),
    View('Donate', '.index')
))

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/form/', methods = ('GET', 'POST'))
def signup_form():
    form = SignupForm()

    if form.validate_on_submit():
        flash("Thank you {} for signing up for the Goodwill of Delaware and Delaware County's Mobile Service!".format(escape(form.name.data)))
        return redirect(url_for('.index')) #warning: may need to change this redirect
    return render_template('signup.html', form = form) #file name here, make sure to check if name changes

