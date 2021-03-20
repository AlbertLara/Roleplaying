from flask import redirect, url_for, abort, render_template, session, current_app
from flask_login import login_required
from .forms import *
from . import *
from ...services.service import *
from flask_socketio import emit, send
from ...utils.models import *
from ...utils.db import socket
@blueprint.route('/', methods=['GET','POST'])
@login_required
def index():
    form = NewFriend()
    friends = current_user.friends
    users = User.query.filter(User.id != current_user.id).all()
    user_friends = [friend['user'] for friend in friends]
    not_friends = []
    for user in users:
        if user not in user_friends:
            not_friends.append(user)
    for friend in friends:
        obj = {'class': ['fas', 'fa-lg'],
               'title': '',
               'color':'black'}
        if friend['accepted'] is None:
            icons = ['fa-sync-alt','fa-spin']
            obj['class'] = (obj['class']+icons)
            obj['title'] = 'Esperando respuesta'
        else:
            obj['color']= 'green' if friend['user'].online else 'gray'
        obj['class'] = " ".join(obj['class'])
        friend['icon'] = obj
    if form.validate_on_submit():
        return redirect(url_for('friends.send_request'))
    form = None if len(not_friends) == 0 else form
    template = render_template('friends/index.html',title='Amigos', friends=friends, form=form)
    return template

@blueprint.route('/send',methods=['GET','POST'])
@login_required
def send_request():
    form = SendRequest()
    if form.validate_on_submit():
        friend_b = User.query.get(int(form.users.data))
        socket.emit('my event', {'message':'Hello'})
        """friends = Friends(friend_a_id=current_user.id,
                          friend_b_id=friend_b.id)
        friends.save_to_db()"""
        return redirect(url_for('friends.send_request'))
    friends = current_user.friends
    user_friends = [friend['user'] for friend in friends]
    users = [(user.id, user.username) for user in User.query.filter(User.id != current_user.id).all() if user not in user_friends]
    form.users.choices = users
    template = render_template('friends/send.html',title='Amigos', form=form)
    return template