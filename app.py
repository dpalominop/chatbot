from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def parser(json, methods=('GET', 'POST')):
    print('Received message: ' + str(json))
    socketio.emit('response', json)


if __name__ == '__main__':
    socketio.run(app)
