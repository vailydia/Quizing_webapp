import json
from flask import Flask, current_app, jsonify, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, emit, send, leave_room, close_room, rooms, disconnect
import random
from pymongo import MongoClient


app = Flask(__name__)
app.config['SECRET_KEY'] = 'xiweiling_quiz_webapp'
socketio = SocketIO(app)
client = MongoClient('localhost', 27017)
db = client['mydb']  # my own database in mongodb
# collections
questions_collection = db['questions']
users_collection = db['users']

ROOMS = {}  # dict to track active rooms

# user = {
#     'username': 'default-user',
#     'score': 0,
#     'winRate': 0,
#     'room': 'default-room',
# }
#
# question = {
#     'qid': 9,
#     'question': 'What is the largest city in Great Britain by size?',
#     'answer': [
#         'A. Belfast',
#         'B. Glasgow',
#         'C. London',
#         'D. Edinburgh'
#     ],
#     'ans': 'C',
# }


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/main', methods=['POST', 'GET'])
def show_main():
    # create a room
    room = request.form.get("userRoom")
    # join_room(room)
    username = request.form.get("userName")
    if users_collection.find_one({'username': username}) is not None:
        current_user = users_collection.find_one({'username': username})
        current_user['_id'] = ''
    else:
        current_user = {
            'username': username,
            'room': room,
            'score': 0,
            'winRate': 1,
        }

    session['user'] = current_user
    if ROOMS.get(room):
        ROOMS[room].append(current_user)
    else:
        inrooms = list()
        inrooms.append(current_user)
        ROOMS[room] = inrooms

    # random choose a questions set!
    randomList = set()
    questionSet = []
    while len(randomList) < 5:
        choosen_qid = random.randrange(10)
        randomList.add(choosen_qid)
    for id in randomList:
        question = questions_collection.find_one({'qid': id})
        question['_id'] = ''
        questionSet.append(question)

    session['questionset'] = questionSet
    return render_template('main.html', username=username, room=room, score=current_user['score'], winRate=current_user['winRate'])


@socketio.on('join', namespace='/connect')
def on_join(data):
    user = session.get('user')
    questionset = session.get('questionset')

    if user is not None:
        room = user['room']
        id = 0
        process = data['data']
        if process == 'start quiz':
            question = questionset[id]
            question_send = {
                'qid': question['qid'],
                'question': question['question'],
                'answer': question['answer'],
            }
            emit('joined-room', {'user': user, 'question': question_send, 'id': 0})

        else:
            id = data['id']
            ans = data['ans']
            if check_answer(id, ans):
                user['score'] = user['score'] + 20

            if id+1 < len(questionset):
                question = questionset[id+1]
                question_send = {
                    'qid': question['qid'],
                    'question': question['question'],
                    'answer': question['answer'],
                }
                emit('joined-room', {'user': user, 'question': question_send, 'id': id+1})
            else:
                # compute new winRate
                newRate = (float(user['score']) / 100 + float(user['winRate'])) / 2
                user['winRate'] = round(newRate, 1)

                # handle the game over!
                emit('game-over', {'user': user, 'room': ROOMS[room]})

    else:
        # handle no user exist situation
        pass


def check_answer(id, ans):
    questionset = session.get('questionset')
    if ans == questionset[id]['ans']:
        print('Question ' + str(id) + ' is true.')
        return True
    else:
        print('Question ' + str(id) + ' is false.')
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
    socketio.run(app, host='127.0.0.1', port=50000, debug=True)
