from flask_mail import Message
from .db import mail
from flask import current_app as app
def send_email(to, subject, template):

    msg = Message(subject,
                  recipients=[to],
                  html=template,
                  sender=app.config['MAIL_USERNAME'])
    print(msg)
    mail.send(msg)