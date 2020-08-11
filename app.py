from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_socketio import SocketIO
from random import randrange
from models import *
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", default="5f352379324c22463451387a0aec5d2f")


socketio = SocketIO(app)
usersOnlineDisplayNames = []
usersOnlineAvatars = []


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{username}:{password}@{host}:{port}/chatbot".format(
    username="postgres",#os.environ.get("PG_USER", default="postgres"),
    password="postgres",#os.environ.get("PG_PWD", default="postgres"),
    host="localhost",#os.environ.get("PG_HOST", default="localhost"),
    port="5432")#os.environ.get("PG_PORT", default="5432"))





db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    currDisplayName = session.get('displayName')
    # if user is not logged in and are coming to the page for the first time, return login page
    if request.referrer is None:
        return render_template('login.html')

    # if user is already logged in, return home page
    if currDisplayName in usersOnlineDisplayNames:
        connectionEvent()
        return render_template('home.html')

    previousPage = request.referrer.replace(request.url_root, '')

    # registration logic
    if previousPage == "register" and request.method == "POST":
        return runRegisterAction()

    # login logic
    if (previousPage == "" or previousPage == "/login") and request.method == "POST":
        return runLoginAction()

    else:
        return render_template('home.html') #"Hello"


@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template('register.html')


@socketio.on('connection event')
def connectionEvent():
    newUserDisplayName = session.get('displayName')
    newUseravatar = session.get('avatar')
    socketio.emit('someone connected', (newUserDisplayName, newUseravatar,  usersOnlineDisplayNames, usersOnlineAvatars))


@socketio.on('disconnect')
def disconnect():
    displayName = session.get("displayName")
    indexOfUser = usersOnlineDisplayNames.index(session.get("displayName"))
    usersOnlineDisplayNames.pop(indexOfUser)
    usersOnlineAvatars.pop(indexOfUser)
    session.pop('vnkdjnfjknfl1232#', None)
    session.clear()
    socketio.emit('disconnect event', displayName)

@socketio.on('message')
def handleMessage(msg):
    messageAuthor = session.get("displayName")
    userAvatar = session.get('avatar')
    print('Received message: ' + str(msg))
    socketio.emit("incoming message", (msg, messageAuthor, userAvatar))


# helper methods
def runRegisterAction():
    # check username and displayname uniqueness. if they are not unique, send them back to registration page
    username = request.form.get("username").lower()
    displayName = request.form.get("displayName").lower()

    if not checkUsernameUniqueness(username):
        return render_template('register.html', error="That username already exists. Please choose again.")

    if not checkDisplayNameUniqueness(displayName):
        return render_template('register.html', error="That display name already exists. Please choose again.")

    # if they are unique, add them to database, add sessionID, and return home.html
    password = request.form.get("password")
    newUser = User(username=username, password=password, display_name=displayName, avatar=randrange(1, 15))
    db.session.add(newUser)
    db.session.commit()
    updateSession(user=newUser)
    return render_template('home.html')


def runLoginAction():
    username = request.form.get("username").lower()
    password = request.form.get("password").lower()
    user = User.query.filter_by(username=username).first()
    if user is None or user.password != password:
        return render_template('login.html', error="Incorrect credentials. Please try again.")
    else:
        updateSession(user=user)
        return render_template('home.html')


def checkUsernameUniqueness(username):
    # check if username or display name is already in database
    usersWithUsername = User.query.filter_by(username=username).count()
    if usersWithUsername > 0:
        return False
    else:
        return True


def checkDisplayNameUniqueness(displayName):
    # check if username or display name is already in database
    usersWithDisplayName = User.query.filter_by(display_name=displayName).count()
    if usersWithDisplayName > 0:
        return False
    else:
        return True


def updateSession(user):
    session['displayName'] = user.display_name.title()
    session['username'] = user.username
    session['userid'] = user.user_id
    session['avatar'] = user.avatar
    usersOnlineDisplayNames.append(user.display_name.title())
    usersOnlineAvatars.append(user.avatar)


if __name__ == '__main__':
    socketio.run(app)
