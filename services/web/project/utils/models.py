from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

class User(UserMixin,db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True,nullable=False)
    username = db.Column(db.String(60), index=True, unique=True,nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    online = db.Column(db.Boolean, nullable=False, default=False)
    members = db.relationship('Members',backref='User',lazy=True,uselist=True)
    a_friends = db.relationship('Friends',primaryjoin=lambda: User.id == Friends.friend_a_id)
    b_friends = db.relationship('Friends',primaryjoin=lambda: User.id == Friends.friend_b_id)

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

    @property
    def password(self):
        raise AttributeError('La contraseña no es un atributo legible')

    @property
    def friends(self):
        my_friends = User.query.join(Friends,Friends.friend_b_id==User.id).filter(Friends.friend_a_id==self.id).with_entities(User, Friends.accepted).all()
        im_their_friend = User.query.join(Friends,Friends.friend_a_id==User.id).filter(Friends.friend_b_id==self.id).with_entities(User,Friends.accepted).all()
        all_friends = list(my_friends+im_their_friend)
        friends = [{'user':friend[0],'accepted':friend[1]} for friend in all_friends]
        return friends

    @property
    def friend_requests(self):
        data = Friends.query.filter_by(friend_b_id=self.id).all()
        users = [user.friend_a for user in data]
        return []

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_user(cls,username,email):
        return cls.query.filter((cls.username==username) | (cls.email==email)).first()

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

class Friends(db.Model):
    __tablename__='Friends'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    friend_a_id = db.Column(db.ForeignKey('User.id'),nullable=False)
    friend_b_id = db.Column(db.ForeignKey('User.id'),nullable=False)
    accepted = db.Column(db.Boolean)

    @property
    def my_friend(self):
        is_my_friend = self.friend_a_id == current_user.id
        return is_my_friend

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



class Group(db.Model):
    __tablename__ = 'Group'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    title = db.Column(db.String(40), index=True, unique=True,nullable=False)
    group_key = db.Column(db.String(255),unique=True)
    members = db.relationship('Members',backref='group_member',lazy=True,uselist=True)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Members(db.Model):
    __tablename__='Members'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('Group.id'), nullable=False)
    group = db.relationship("Group",backref="Group",uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship("User",backref="User",uselist=False)
    approved = db.Column(db.Boolean)
    role = db.Column(db.String(6),default='Viewer')
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()