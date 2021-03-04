from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField

class NewGroup(FlaskForm):
    submit = SubmitField('Crear Grupo', validators=None)



