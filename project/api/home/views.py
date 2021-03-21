# api/home/views.py
from flask import render_template, request, jsonify, session
from . import *

@blueprint.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    print("Home")
    return render_template('home/index.html',path='home', title="Welcome")


@blueprint.route('/close')
def close():

    print(session.sid)
    print(request.args)
    print("Closing")
    return jsonify(result="Success")