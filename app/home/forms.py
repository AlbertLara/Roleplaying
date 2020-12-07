from flask_wtf import FlaskForm, Form
from wtforms import PasswordField, StringField, SubmitField, Label

class NewGame(FlaskForm):
    submit = SubmitField('CREAR NUEVA PARTIDA',validators=None)
    pass


class GameLayout(Form):
    title = Label(text='',field_id="title")
    players = Label(text='/',field_id='players')
    master = Label(field_id='master',text='')