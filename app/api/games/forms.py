from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField

from wtforms.fields.html5 import IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from wtforms.widgets.html5 import NumberInput
from app.models import Games, Sistema

class NewGame(FlaskForm):
    submit = SubmitField('CREAR NUEVA PARTIDA',validators=None)
    pass

class AdminForm(FlaskForm):
    send_request = SubmitField('Enviar invitaciones')
    view_request = SubmitField('Ver peticiones')

class ViewGamesForm(FlaskForm):
    sistema = QuerySelectField('Sistema',query_factory=lambda: Sistema.query.filter_by(status='a').all(),
                               get_label="nombre")
    submit = SubmitField('Buscar partidas')

class CreateGameForm(FlaskForm):
    title = StringField('Titulo',validators=[DataRequired()])
    max_players = IntegerField('Numero jugadores',default=2,widget=NumberInput(step=1,min=2,max=7),validators=[DataRequired()])
    is_public = SelectField('Tipo de partida', choices=[(True,'Publica'),(False,'Privada')])
    Sistema = SelectField('Sistema',coerce=int)
    submit = SubmitField('Crear')

    def validate_title(self,field):
        if len(field.data) < 10:
            raise ValidationError('El título de la partida debe contener mas de 10 carácteres')
        if len(field.data) > 40:
            raise ValidationError('El título de la partida debe contener menos de 50 carácteres')
        if Games.query.filter_by(title=field.data).first():
            raise ValidationError('Ya hay una partida con ese nombre.')