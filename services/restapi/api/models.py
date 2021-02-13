from werkzeug.security import generate_password_hash, check_password_hash
from .db import db
from passlib.hash import pbkdf2_sha256 as sha256
from itertools import groupby
import jwt
import os

class Sistema(db.Model):
    __tablename__ = 'Sistemas'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(50), unique=True,nullable=False)
    skey = db.Column(db.String(10), unique=True,nullable=False)
    status = db.Column(db.String(1),nullable=False)
    games = db.relationship('Games',lazy=True,uselist=True)

    @classmethod
    def get_by_status(cls,status):
        return cls.query.filter_by(status=status).all()

    def get_list(self):
        return tuple([self.id,self.nombre])



class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True,nullable=False)
    username = db.Column(db.String(60), index=True, unique=True,nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    members = db.relationship('Members',backref='User',lazy=True,uselist=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    def update(self,data:dict):
        if 'email' in data.keys():
            self.email = data.get('email')
        if 'username' in data.keys():
            self.username = data.get('username')
        if 'password' in data.keys():
            self.password_hash = self.generate_hash(data.get('password'))
        if 'is_admin' in data.keys():
            self.is_admin = str(data.get('is_admin')).upper() == 'TRUE'
        if 'active' in data.keys():
            self.active = str(data.get('active')).upper() == 'TRUE'
        db.session.commit()

    @classmethod
    def find_user(cls,username,email):
        return cls.query.filter((cls.username==username) | (cls.email==email)).first()

    @staticmethod
    def generate_hash(password):
        return jwt.encode({'password':password},os.environ.get('SECRET_KEY'),algorithm='HS256').decode('ascii')

    @staticmethod
    def verify_hash(password,hash_):
        return sha256.verify(password,hash_)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

class UserAtributes(db.Model):
    __tablename__ = 'UserAtributes'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    userid= db.Column(db.Integer, nullable=False)
    atribute_name = db.Column(db.String(60),unique=True)
    atribute_value = db.Column(db.String(60),unique=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Games(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    title = db.Column(db.String(40), index=True, unique=True,nullable=False)
    game_key = db.Column(db.String(255),unique=True)
    max_players = db.Column(db.Integer,nullable=False)
    masterid = db.Column(db.Integer, nullable=False)
    sistema_id = db.Column(db.Integer, db.ForeignKey('Sistemas.id'))
    sistema = db.relationship("Sistema", lazy=True,uselist=False)
    is_public = db.Column(db.Boolean, default=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    update_date  = db.Column(db.DateTime, nullable=False)
    members = db.relationship('Members',backref='game_member',lazy=True,uselist=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @property
    def players(self):
        players = list(filter(lambda member: member.user_id != self.masterid and member.approved, list(self.members)))
        return len(players)

    @property
    def master(self):
        return User.query.filter(User.id==self.masterid).first().username

    @property
    def users(self):
        members = []
        for member in self.members:
            obj = {'role':member.role,'username':member.user.username}
            if member.role != 'GM':
                obj['approved'] = member.approved
            members.append(obj)
        return members

    @classmethod
    def find_game_by_key(cls,key):
        return cls.query.filter_by(game_key=key).all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()


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
    role = db.Column(db.String(6),default='Viewer')
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Razas(db.Model):
    __tablename__ = 'Razas'
    __table_args__ = {"schema":"sw"}
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(255),nullable=False)
    atributos = db.Column(db.String(4),nullable=False)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class RazasAtributos(db.Model):
    __tablename__ = 'RazasAtributos'
    __table_args__ = {"schema":"sw"}
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    raza_id = db.Column(db.Integer, nullable=False)
    atributo = db.Column(db.String(3), nullable=False)
    val_min = db.Column(db.String(3),nullable=False)
    val_max = db.Column(db.String(3),nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class ListAtributos(db.Model):
    __tablename__ = 'ListAtributos'
    __table_args__ = {"schema":"sw"}
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    nombre = db.Column(db.String(30),unique=True,nullable=False)
    short_name = db.Column(db.String(3),unique=True,nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

