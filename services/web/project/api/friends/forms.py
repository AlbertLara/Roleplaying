from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField

class AddUser(FlaskForm):
    submit = SubmitField('Enviar Solicitud', validators=None)


class SendRequest(FlaskForm):
    users = SelectField('Usuario', coerce=int, validate_choice=False)
    submit = SubmitField('Enviar')

class NewFriend(FlaskForm):
    submit = SubmitField('Enviar solicitud',validators=None)


