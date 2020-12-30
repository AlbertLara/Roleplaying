from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, BadData
from . import app

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=60):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    data = {'email':'','expired':False}
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )

    except BadSignature as e:
        if e.payload is not None:
            try:
                email = serializer.load_payload(e.payload)
            except BadData as e:
                pass
        data['expired'] = True
    data['email'] = email
    return data