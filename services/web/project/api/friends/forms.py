from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired, Length
from ...models import *
from flask_login import current_user

class AddUser(FlaskForm):
    submit = SubmitField('Enviar Solicitud', validators=None)


class SendRequest(FlaskForm):
    users = SelectField('Usuario',coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enviar', validators=None)


