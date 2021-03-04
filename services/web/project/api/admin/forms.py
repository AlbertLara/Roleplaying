from flask_wtf import FlaskForm, Form
from wtforms.widgets import TableWidget, CheckboxInput
from wtforms import StringField, SubmitField, Label, BooleanField
from wtforms.validators import DataRequired
from marshmallow import Schema, fields

class SistemaForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired()])
    sKey = StringField('Clave',validators=[DataRequired()])
    submit = SubmitField("Crear Sistema")

class UsersForm(FlaskForm):
    username = StringField('Nombre',render_kw={'readonly': True})
    email = StringField('Correo',render_kw={'readonly': True})
    is_admin = BooleanField('Admin')
    active = BooleanField('Activo')
    online = BooleanField('Online')
    submit = SubmitField('Guardar',render_kw={'disabled': True})

class UserSchema(Schema):
    username = fields.String()
    is_admin = fields.Boolean()
    active = fields.Boolean()

class SendTask(FlaskForm):
    submit = SubmitField('Crear Tarea')