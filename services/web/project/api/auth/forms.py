from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp
from ...utils.models import *
class RegistrationForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email()])
    username = StringField('Usuario', validators=[DataRequired(), Regexp('^\w+$',message='Solamente se aceptan valores alfanumericos.')])
    password = PasswordField('Contraseña', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirma Contraseña')
    submit = SubmitField('Registrar')


    def validate_username(self, field):
        exists = User.query.filter_by(username=field.data).first()
        if exists:
            raise ValidationError('Usuario ya está en uso.')

    def validate_email(self, field):
        exists = User.query.filter_by(email=field.data).first()
        if exists:
            raise ValidationError('Correo electrónico ya está en uso.')



class LoginForm(FlaskForm):
    username = StringField('Usuario',validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')
