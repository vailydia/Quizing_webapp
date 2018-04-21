from flask import Flask, current_app, jsonify, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, emit, send, leave_room, close_room, rooms, disconnect


app = Flask(__name__)
app.config['SECRET_KEY']='xiweiling'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index3.html')


@socketio.on('connect', namespace='/connect')
def test_connect():
    emit('server response', {'data': 'Server Connected'})


@socketio.on('join', namespace='/connect')
def on_join(data):
    username = data['username']
    emit('joined-room', username + ' has connected.')


if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1',debug=True)
