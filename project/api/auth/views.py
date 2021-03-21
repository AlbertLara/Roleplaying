from flask import flash, redirect, url_for, render_template, session
from flask_login import login_required, login_user, logout_user, current_user
from rq import Queue, Connection
import redis
from . import *
from .forms import *
from ...utils.models import *
from ...utils.token import generate_confirmation_token, confirm_token
from ...utils.email import send_email
from datetime import datetime
import os
endpoint = os.environ.get('ENDPOINT')



@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        confirmed=False)
            user.save_to_db()
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            html = render_template('auth/activate.html', confirm_url=confirm_url)
            subject = "Confirma tu email"
            redis_url = current_app.config['REDIS_URL']
            with Connection(redis.from_url(redis_url)):
                q = Queue()
                q.enqueue(send_email, user.email, subject, html)
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash('Sorry. That email already exists.', 'danger')

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
            if user.active:
                user.save_to_db()

                login_user(user, remember=False,fresh=False)

                return redirect(url_for('home.homepage'))
            else:
                flash('Cuenta no activada. Por favor, dirigite a tu correo para activarla', 'danger')
        else:
            flash('Usuario o contraseña erróneos.', 'danger')
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


@blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Cuenta ya activada', 'success')
    else:
        user.confirmed = True
        user.active = True
        user.save_to_db()
    login_user(user)
    return redirect(url_for('home.homepage'))

@blueprint.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html',title='Perfil')