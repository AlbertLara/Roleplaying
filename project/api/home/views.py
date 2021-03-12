# api/home/views.py
from flask import render_template
from . import *

@blueprint.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    print("Home")
    return render_template('home/index.html',path='home', title="Welcome")