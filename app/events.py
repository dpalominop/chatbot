from flask import session, Blueprint
from flask_login import current_user, logout_user
from flask_socketio import emit, join_room, leave_room
from . import socketio

# Blueprint Configuration
events_bp = Blueprint(
    'events_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@socketio.on('message')
def parser(msg, methods=('GET', 'POST')):
    print('Received message: ' + str(msg))
    socketio.emit('response', {'username': current_user.name, 'message': msg['message']})


@socketio.on('connect')
def test_connect():
    emit('login-out', {'data': f"{current_user.name} is connected"}, broadcast=True, include_self=False)

@socketio.on('disconnect')
def test_disconnect():
    emit('login-out', {'data': f"{current_user.name} is disconnected"}, broadcast=True, include_self=False)