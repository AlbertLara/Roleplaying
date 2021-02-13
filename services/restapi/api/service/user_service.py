from ..models import User,db


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    print(data)
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],

        )