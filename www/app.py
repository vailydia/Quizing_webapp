import json
from flask import Flask, current_app, jsonify, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, emit, send, leave_room, close_room, rooms, disconnect
from time import gmtime, strftime
from operator import itemgetter
import random


app = Flask(__name__)
app.config['SECRET_KEY']='xiweiling'
socketio = SocketIO(app)
ROOMS = {} # dict to track active rooms

# data model: question, user,


QUESTIONS = [
    {
        'qid':0,
        'question': 'What is your favoriate color?',
        'answer': ['A.  red','B.  blue','C.  yellow','D.  black'],
        'ans': 'A',
    },
    {
        'qid':1,
        'question': 'What is your favoriate color222?',
        'answer': ['red', 'blue', 'yellow', 'black'],
        'ans': 'A',
    },
]

users = {
    'default': {
        'username': 'default',
        'score': 0,
        'rank': 1,
    }
}


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/main', methods=['POST', 'GET'])
def show_main():
    # choose a room and question set
    username = request.form.get("userName")
    room = request.form.get("userRoom")
    current_user = {'username': username, 'room': room, 'score': 10}
    session['user'] = current_user
    choosen_qid = random.randint(0,1) # random choose a questions set!
    # session['questionset'] = QUESTIONS[choosen_qid]
    session['questionset'] = QUESTIONS
    return render_template('main.html', username=username, room=room, score=10)


@socketio.on('join', namespace='/connect')
def on_join(data):
    user = session.get('user')
    questionset = session.get('questionset')
    if user is not None:
        room = user['room']
        ROOMS[room] = questionset
        join_room(room)

        process = data['data']
        if process == 'start quiz':
            question = questionset[0]
            question_send = {
                'qid': question['qid'],
                'question': question['question'],
                'answer': question['answer'],
            }
            emit('joined-room', {'user': user, 'question': question_send})
        else:
            qid = data['qid']
            ans = data['ans']
            if check_answer(qid, ans):
                user['score'] = user['score'] + 10

            if qid+1 < len(questionset):
                question = questionset[qid+1]
                question_send = {
                    'qid': question['qid'],
                    'question': question['question'],
                    'answer': question['answer'],
                }
                emit('joined-room', {'user': user, 'question': question_send})
            else:
                # handle the game over!
                emit('game-over', {'user': user})
    else:
        pass
        # handle no user exist situation


def check_answer(qid, ans):
    if ans == QUESTIONS[qid]['ans']:
        print('question' + str(qid) + 'is true.')
        return True
    else:
        print('question' + str(qid) + 'is false.')
        return False


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


@socketio.on('flip_card')
def on_flip_card(data):
    """flip card and rebroadcast game object"""
    room = data['room']
    card = data['card']
    ROOMS[room].flip_card(card)
    send(ROOMS[room].to_json(), room=room)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print('some error happened' + str(e))


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('handles all namespaces without an explicit error handler:  ' + str(e))


if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1',debug=True)
