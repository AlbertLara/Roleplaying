from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, ValidationError, SelectField, Label, FormField
from wtforms.fields.html5 import IntegerField, IntegerRangeField
from wtforms.validators import DataRequired
from wtforms.widgets.html5 import NumberInput
from ..models import Games, Sistema


class CreateGameForm(Form):
    title = StringField('Titulo',validators=[DataRequired()])
    max_players = IntegerField('Numero jugadores',default=2,widget=NumberInput(step=1,min=2,max=7),validators=[DataRequired()])
    Sistema = SelectField('Sistema',coerce=int)
    submit = SubmitField('Crear')

    def validate_game(self,field):
        if Games.query.filter_by(title=field.data).first():
            raise ValidationError('Ya hay una partida con ese nombre.')

