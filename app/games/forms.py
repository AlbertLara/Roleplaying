from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, ValidationError, SelectField, Label, FormField
from wtforms.fields.html5 import IntegerField, IntegerRangeField
from wtforms.validators import DataRequired
from wtforms.widgets.html5 import NumberInput
from ..models import Games, Sistema


class CreateGameForm(Form):
    title = StringField('Titulo',validators=[DataRequired()])
    key = StringField('Clave',validators=[DataRequired()])
    max_players = IntegerField('Numero jugadores',default=2,widget=NumberInput(step=1,min=2,max=7),validators=[DataRequired()])
    Sistema = SelectField('Sistema',coerce=int)
    submit = SubmitField('Crear')

    def validate_title(self,field):
        if len(field.data) < 10:
            raise ValidationError('El título de la partida debe contener mas de 10 carácteres')
        if Games.query.filter_by(title=field.data).first():
            raise ValidationError('Ya hay una partida con ese nombre.')

    def validate_key(self,field):
        if len(field.data) >4:
            raise ValidationError('Largo máximo clave: 4')
        if Games.query.filter_by(key=field.data).first():
            raise ValidationError('Ya hay una partida con ese nombre.')
