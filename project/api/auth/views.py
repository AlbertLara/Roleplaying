from flask import flash, redirect, url_for, render_template, session
from flask_login import login_required, login_user, logout_user, current_user
from . import *
from .forms import *
from ...utils.models import *
from datetime import datetime
import os
endpoint = os.environ.get('ENDPOINT')

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    created_on=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    active=False)
        user.save_to_db()
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            user.last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user.save_to_db()
            login_user(user)
            return redirect(url_for('home.homepage'))
    # load login template
        else:
            flash('Usuario o contraseña erróneos.')
    if not current_user.is_authenticated:
        return render_template('auth/login.html', form=form, title='Login')
    else:
        return redirect(url_for('home.homepage'))

@blueprint.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    user = User.query.get(int(current_user.id))
    user.online = False
    user.save_to_db()

    logout_user()
    flash('You have successfully been logged out.')
    # redirect to the login page
    return redirect(url_for('auth.login'))


@blueprint.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html',title='Perfil')