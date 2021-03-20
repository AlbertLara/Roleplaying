from flask import session
from flask_socketio import emit, leave_room
from .db import socket


@socket.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)