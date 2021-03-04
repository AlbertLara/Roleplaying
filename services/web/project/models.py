from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .rest_db import db, login_manager


class Sistema(db.Model):
    __tablename__ = 'Sistemas'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(50), unique=True,nullable=False)
    skey = db.Column(db.String(10), unique=True,nullable=False)
    status = db.Column(db.String(1),nullable=False)
    games = db.relationship('Games',lazy=True,uselist=True)

    def get_list(self):
        return tuple([self.id,self.nombre])



class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True,nullable=False)
    username = db.Column(db.String(60), index=True, unique=True,nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    members = db.relationship('Members',backref='User',lazy=True,uselist=True)

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

class Games(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    title = db.Column(db.String(40), index=True, unique=True,nullable=False)
    game_key = db.Column(db.String(255),unique=True)
    max_players = db.Column(db.Integer,nullable=False)
    masterid = db.Column(db.Integer, nullable=False)
    sistema_Id = db.Column(db.Integer, db.ForeignKey('Sistemas.id'))
    sistema = db.relationship("Sistema", lazy=True,uselist=False)
    is_public = db.Column(db.Boolean, default=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime, nullable=False)
    members = db.relationship('Members',backref='game_member',lazy=True,uselist=True)

    @property
    def users(self):
        for member in self.members:
            print(member.user.username)
        return []

    @property
    def players(self):
        players = list(filter(lambda member: member.user_id != self.master_Id and member.approved, list(self.members)))
        return len(players)

    @property
    def master(self):
        return User.query.filter(User.id==self.master_Id).first().username

    @property
    def is_player(self):
        users = [member.user for member in self.members]
        return current_user in users

    def __repr__(self):
        return '<Games: {}>'.format(self.title)




class Members(db.Model):
    __tablename__='Members'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('Games.id'), nullable=False)
    game = db.relationship("Games",backref="Game",uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship("User",backref="User",uselist=False)
    approved = db.Column(db.Boolean)

class Razas(db.Model):
    __tablename__ = 'Razas'
    __table_args__ = {"schema":"sw"}
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(255),nullable=False)
    atributos = db.Column(db.String(4),nullable=False)


class RazasAtributos(db.Model):
    __tablename__ = 'RazasAtributos'
    __table_args__ = {"schema":"sw"}
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    raza_id = db.Column(db.Integer, nullable=False)
    atributo = db.Column(db.String(3), nullable=False)
    val_min = db.Column(db.String(3),nullable=False)
    val_max = db.Column(db.String(3),nullable=False)

class ListAtributos(db.Model):
    __tablename__ = 'ListAtributos'
    __table_args__ = {"schema":"sw"}
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(30),unique=True,nullable=False)
    short_name = db.Column(db.String(3),unique=True,nullable=False)