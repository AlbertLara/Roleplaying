from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager, ma



class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True,nullable=False)
    username = db.Column(db.String(60), index=True, unique=True,nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('La contraseña no es un atributo legible')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Games(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    title = db.Column(db.String(60), index=True, unique=True,nullable=False)
    key = db.Column(db.String(4),unique=True)
    max_players = db.Column(db.Integer,nullable=False)
    players = db.Column(db.Integer,nullable=False)
    masterId = db.Column(db.Integer,nullable=False)
    Sistema = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return '<Games: {}>'.format(self.title)

class Sistema(db.Model):
    __tablename__ = 'Sistemas'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(50), unique=True,nullable=False)
    sKey = db.Column(db.String(10), unique=True,nullable=False)
    status = db.Column(db.String(1),nullable=False)

    def get_list(self):
        return (self.id,self.nombre)

class Players(db.Model):
    __tablename__='Players'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    userId = db.Column(db.Integer,nullable=False)
    gameId = db.Column(db.Integer,nullable=False)
    gameUser = db.Column(db.String(11),nullable=False)

class Atributos(db.Model):
    __tablename__='Atributos'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    Atributo = db.Column(db.String(3),nullable=False)
    dices = db.Column(db.String(4),nullable=False)

class Razas(db.Model):
    __tablename__ = 'Razas'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(255),nullable=False)
    atributos = db.Column(db.String(4),nullable=False)

class Groups(db.Model):
    __tablename__='Groups'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_name = db.Column(db.String(40),nullable=False)

class Members(db.Model):
    __tablename__='Members'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_id = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    group_name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(60),nullable=False)