from flask import session, current_app
from flask_login import logout_user, current_user
from flask_socketio import emit, leave_room
from .db import socket

@socket.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)

@socket.on('disconnect')
def disconnect_user():
    print("Disconnect")
    current_user.active = False
    logout_user()
    session.clear()
    pass