from flask import session, Blueprint
from flask_login import current_user, logout_user
from flask_socketio import emit, join_room, leave_room
from . import socketio
from .models import db, Post, User
from datetime import datetime

# Blueprint Configuration
events_bp = Blueprint(
    'events_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': current_user.name + ' has entered the room.'}, room=room, broadcast=True, include_self=False)

    emit('clean', {}, room=room, broadcast=False)
    data = [{'user': User.query.get(post.user_id).name, 'msg': post.text} for post in Post.get_posts(5)]
    emit('message', data[::-1], room=room, broadcast=False)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""

    post = Post(
            user_id=current_user.id,
            text=message['msg'],
            created_on=datetime.now()
            )
    db.session.add(post)
    db.session.commit()  # Create new post

    room = session.get('room')
    emit('message', [{'user': current_user.name,  'msg': message['msg']}], room=room, broadcast=True)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': current_user.name + ' has left the room.'}, room=room, broadcast=True, include_self=False)


@socketio.on('disconnect')
def test_disconnect():
    socketio.emit('status', {'msg': f"{current_user.name} is disconnected"}, broadcast=True, include_self=False)

