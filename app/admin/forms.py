from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField



class SistemaForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired()])
    sKey = StringField('Clave',validators=[DataRequired()])
    submit = SubmitField("Crear Sistema")
    pass