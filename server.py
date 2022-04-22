from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import auth

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    app.register_blueprint(auth.auth)
    return app


app = create_app()
socket = SocketIO(app)


@app.route("/")
def index():
    return render_template('client.html')


@socket.on('connect')
def connect():
    print("[CLIENT CONNECTED]:", request.sid)


@socket.on('disconnect')
def connect():
    print("[CLIENT DISCONNECTED]:", request.sid)


@socket.on('notify')
def notify(user):
    print(user)
    emit('notify', user, broadcast=True, skip_sid=request.sid)


@socket.on('data')
def emitback(data):
    print(data)
    emit('returndata', data, broadcast=True)


if __name__ == "__main__":
    socket.run(app)
