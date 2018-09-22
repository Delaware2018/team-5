'''from flask import Blueprint, render_template, flash, redirect, url_for
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
    View('Donate', '.index'),
    Subgroup(
        'Docs',
        Link('', '
'''
