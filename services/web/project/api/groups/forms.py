from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.widgets import TextArea
from ...services.service import GameService
from wtforms.fields.html5 import IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length
from wtforms.widgets.html5 import NumberInput
from ...models import Group
import re

class NewGroup(FlaskForm):
    submit = SubmitField('Crear Grupo', validators=None)



