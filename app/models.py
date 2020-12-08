from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager, ma


class Sistema(db.Model):
    __tablename__ = 'Sistemas'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(50), unique=True,nullable=False)
    sKey = db.Column(db.String(10), unique=True,nullable=False)
    status = db.Column(db.String(1),nullable=False)

    def get_list(self):
        return (self.id,self.nombre)


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
    permissions = db.relationship('GamePermission',backref='Games',lazy='dynamic')
    def __repr__(self):
        return '<Games: {}>'.format(self.title)

class GamePermission(db.Model):
    __tablename__ = 'GamePermission'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    game_id = db.Column(db.Integer,db.ForeignKey('Games.id'),nullable=False)
    group_id = db.Column(db.Integer,db.ForeignKey('Groups.id'),nullable=False)

class Groups(db.Model):
    __tablename__='Groups'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_name = db.Column(db.String(40),nullable=False)
    permissions = db.relationship('GamePermission', backref='Groups', lazy='dynamic')

class Members(db.Model):
    __tablename__='Members'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_id = db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

class Razas(db.Model):
    __tablename__ = 'Razas'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(255),nullable=False)
    atributos = db.Column(db.String(4),nullable=False)

