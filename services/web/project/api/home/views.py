# api/home/views.py
from flask import redirect, render_template, url_for, request
from . import *


@blueprint.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html',path='home', title="Welcome")