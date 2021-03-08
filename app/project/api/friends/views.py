from flask import redirect, url_for, abort, render_template
from flask_login import login_required
from .forms import *
from . import *
from ...services.service import *
from ...utils.models import *

@blueprint.route('/', methods=['GET','POST'])
@login_required
def index():
    form = NewFriend()
    friends = current_user.friends
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
    template = render_template('friends/index.html',title='Amigos',friends=friends, form=form)
    return template

@blueprint.route('/send',methods=['GET','POST'])
@login_required
def send_request():
    form = SendRequest()
    if form.validate_on_submit():
        friend_b = User.query.get(int(form.users.data))
        if friend_b.online:
            print(friend_b.__dict__)
        friends = Friends(friend_a_id=current_user.id,
                          friend_b_id=friend_b.id)
        friends.save_to_db()
        return redirect(url_for('friends.send_request'))
    users = [(user.id, user.username) for user in User.query.filter(User.id!=current_user.id).all() if user not in current_user.friends]
    form.users.choices = users
    template = render_template('friends/send.html',title='Amigos', form=form)
    return template