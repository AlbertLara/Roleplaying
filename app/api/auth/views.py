from flask import flash, redirect, url_for, render_template
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .forms import LoginForm, RegistrationForm
#Models
from ...models import *
from ...email import send_email
from ...token import *

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email',token=token,_external=True)
        html = render_template('auth/activate.html',confirm_url=confirm_url)
        subject = "Por favor, confirma tu correo"
        send_email(user.email,subject,html)
        # redirect to the login page
        return redirect(url_for('auth.unconfirmed'))
    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    data = confirm_token(token)
    email = data['email']
    expired = data['expired']
    user = User.query.filter_by(email=email).first_or_404()
    if not user.confirmed and not expired:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
    if expired:
        #<p></p>
    #<p><a href="{{ url_for('auth.resend_confirmation') }}">Reenviar</a>.</p>
        msg = [{'txt':'El enlace de confirmación no es válido o ha caducado.','re_send':False},
               {'txt':'','re_send':True}]
        return render_template('auth/expired.html',msg=msg, title='Expirado')
    else:
        return redirect(url_for('auth.login'))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('auth.login'))
    msg = [{
        'txt':'No ha confirmado su cuenta. '
              'Compruebe su bandeja de entrada (y su carpeta de correo no deseado). '
              'Debería haber recibido un correo electrónico con un enlace de confirmación.',
        're_send':False
    },
        {
            'txt':'¿No recibiste el correo electrónico? ',
            're_send':True
        }]
    return render_template('auth/expired.html',msg=msg,title='Confirmar')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = User.query.filter_by(username=form.username.data, confirmed=True).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the dashboard page after login
            return redirect(url_for('home.homepage'))
        # when login details are incorrect
        else:
            flash('Usuario o contraseña erróneos.')

    # load login template
    if not current_user.is_authenticated:
        return render_template('auth/login.html', form=form, title='Login')
    else:
        return redirect(url_for('home.homepage'))


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')
    # redirect to the login page
    return redirect(url_for('auth.login'))


@auth.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url)
    subject = "Por favor confirma tu email"
    send_email(current_user.email, subject, html)
    return redirect(url_for('auth.unconfirmed'))