from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets.html5 import NumberInput


class SistemaForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired()])
    sKey = StringField('Clave',validators=[DataRequired()])
    submit = SubmitField("Crear Sistema")
    pass

