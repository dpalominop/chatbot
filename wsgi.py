"""App entry point."""
from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080)
    socketio.run(app, host='127.0.0.1', port=5000)
