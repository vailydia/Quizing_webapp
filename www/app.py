from operator import itemgetter
import heapq
import json
from flask import Flask, current_app, jsonify, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, emit, send, leave_room, close_room, rooms, disconnect
import random
from pymongo import MongoClient
import eventlet
# eventlet.monkey_patch()
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None


app = Flask(__name__)
app.config['SECRET_KEY'] = 'xiweiling_quiz_webapp'
socketio = SocketIO(app, engineio_logger=True, async_mode=async_mode)


# database access
client = MongoClient('localhost', 27017)
db = client['mydb']  # my own database in mongodb
# collections
questions_collection = db['questions']
users_collection = db['users']


ROOMS = {}  # dict to track active rooms
# ROOMS = {
#     'roomname': {
#                'inrooms': inrooms,
#                'questionset': questionset,
#                'roommessages': list(),
#            }
# }
#

active_users = {}
# active_users = {
#     'username': user,
# }
#

waiting_users = {}
# waiting_users = {
#        wait_username : {
#                 'username': username,
#                 'sid': request.sid,
#                 'room': room,
#             }
# }
#

# user = {
#     'username': 'default-user',
#     'score': 0,
#     'winRate': 0,
#     'mode': 'default-room',
#     'sid': sid,
#     'questionset': questionset,
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


# list the toppest 6 users
@app.route('/ranking')
def ranking():
    users_dic = {}
    for user in users_collection.find():
        users_dic[user['username']] = user['winRate']

    sorted_list = heapq.nlargest(6, users_dic.items(), key=itemgetter(1))
    return render_template('ranking.html', users=sorted_list)


@app.route('/login', methods=['GET'])
def login():
    # mode = request.form.get("mode")
    mode = request.args['mode']
    username = request.args["username"]

    data = {
        'username': username,
        'mode': mode,
        'relocate': '/main',
        'status': 302,
        'room': 'none'
    }
    return jsonify(data)


@app.route('/main', methods=['GET'])
def main_single():
    username = request.args['username']
    mode = request.args['mode']
    if users_collection.find_one({'username': username}) is not None:
        current_user = users_collection.find_one({'username': username})
        current_user['_id'] = ''
        current_user['score'] = 0

    else:
        current_user = {
            'username': username,
            'score': 0,
            'winRate': 0,
            'mode': mode,
        }
        result = users_collection.insert_one(current_user)
        current_user['_id'] = ''

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

    current_user['questionset'] = questionSet
    current_user['mode'] = mode

    active_users[username] = current_user
    waiting_usernames = [user.get('username') for user in waiting_users.values()]

    return render_template('main.html', username=username, mode=current_user['mode'],
                           score=current_user['score'], winRate=current_user['winRate'],
                           waiting_users=map(json.dumps, waiting_usernames),
                           )


# for battle users:
@socketio.on('join room')
def join_room(data):
    username = data['username']
    active_users[username]['sid'] = request.sid
    waiting_user = {
        'username': username,
        'sid': request.sid,
        'room': 'noneyet',
    }
    waiting_users[username] = waiting_user
    waiting_usernames = [user['username'] for user in waiting_users.values()]
    emit('handle wait userlists', waiting_usernames, broadcast=True)


@socketio.on('start quiz')
def pre_start(data):
    mode = data['mode']

    if mode == 'single':
        quiz_loop_single(data)
    elif mode == 'battle':
        quiz_loop_battle(data)


@socketio.on('battle quiz')
def quiz_loop_battle(data):
    username = data['username']
    user = active_users.get(username)
    battle_username = data['battle']
    battle_user = active_users.get(battle_username)

    if user is not None:
        id = 0
        process = data['data']
        if process == 'start quiz':
            # remove from waiting users list
            del waiting_users[username]
            del waiting_users[battle_username]

            # create room
            room = username + "&" + data['battle']
            print(user['sid'])
            print(battle_user['sid'])
            # join_room(room, sid=user['sid'])
            socketio.server.enter_room(user['sid'], room)
            # join_room(room, sid=battle_user['sid'])
            socketio.server.enter_room(battle_user['sid'], room)

            questionset = user.get('questionset')

            inrooms = list()
            inrooms.append(username)
            inrooms.append(battle_user['username'])
            ROOMS[room] = {
                'inrooms': inrooms,
                'questionset': questionset,
                'roommessages': list(),
            }

            del user['questionset']
            del battle_user['questionset']

            question = questionset[id]
            question_send = {
                'qid': question['qid'],
                'question': question['question'],
                'answer': question['answer'],
            }
            emit('joined-room', {
                'user': user,
                'battle_user': battle_user,
                'question': question_send,
                'id': 0,
                'room': room
            }, room=room)

        else:
            id = data['id']
            ans = data['ans']
            room = data['room']
            questionset = ROOMS[room]['questionset']

            # record the answers received
            ROOMS[room]['roommessages'].append(ans)

            if ans == questionset[id]['ans']:
                print('Question ' + str(id) + ' is true.')
                user['score'] = user['score'] + 20
            else:
                print('Question ' + str(id) + ' is false.')

            if id+1 < len(questionset):

                # determin whether two battler are answered or not: if yes, clear record and broadcast a new question.
                if len(ROOMS[room]['roommessages']) == 2:

                    ROOMS[room]['roommessages'] = list()

                    question = questionset[id+1]
                    question_send = {
                        'qid': question['qid'],
                        'question': question['question'],
                        'answer': question['answer'],
                    }

                    emit('joined-room', {
                        'user': user,
                        'battle_user': battle_user,
                        'question': question_send,
                        'id': id+1,
                        'room': room
                    }, room=room)
                else:
                    pass
                    # tell user to wait other to complete
                    # emit('server response', {'data': 'Please wait!'})

            else:
                if len(ROOMS[room]['roommessages']) == 2:

                    ROOMS[room]['roommessages'] = list()

                    # compute new winRate
                    newRate = (float(user['score']) / 100 + float(user['winRate'])) / 2
                    user['winRate'] = round(newRate, 2)

                    # update the database user info
                    users_collection.update_one(
                        {"username": user['username']},
                        {"$set": {"winRate": user['winRate']}},
                    )

                    # handle the game over!
                    emit('game-over', {
                        'user': user,
                        'battle_user': battle_user,
                        'room': room
                    }, room=room)

                    # leave room and delete room
                    leave_room(room)
                    ROOMS[room]['inrooms'].remove(username)
                    if len(ROOMS[room]['inrooms']) == 0:
                        del ROOMS[room]

                else:
                    pass


@socketio.on('single quiz')
def quiz_loop_single(data):
    username = data['username']
    user = active_users.get(username)
    questionset = user.get('questionset')

    if user is not None:
        id = 0
        process = data['data']
        if process == 'start quiz':
            question = questionset[id]
            question_send = {
                'qid': question['qid'],
                'question': question['question'],
                'answer': question['answer'],
            }
            emit('joined-room', {
                'user': user,
                'question': question_send,
                'id': 0
            })

        else:
            id = data['id']
            ans = data['ans']

            if ans == questionset[id]['ans']:
                print('Question ' + str(id) + ' is true.')
                user['score'] = user['score'] + 20
            else:
                print('Question ' + str(id) + ' is false.')

            if id+1 < len(questionset):
                question = questionset[id+1]
                question_send = {
                    'qid': question['qid'],
                    'question': question['question'],
                    'answer': question['answer'],
                }
                emit('joined-room', {
                    'user': user,
                    'question': question_send,
                    'id': id+1
                })
            else:
                # compute new winRate
                newRate = (float(user['score']) / 100 + float(user['winRate'])) / 2
                user['winRate'] = round(newRate, 2)

                # update the database user info
                users_collection.update_one(
                    {"username": user['username']},
                    {"$set": {"winRate": user['winRate']}},
                )

                # handle the game over!
                emit('game-over', {'user': user})

    else:
        # handle no user exist situation
        pass


# Listen to the connection status and error handling part!
@socketio.on('connect')
def connect():
    print("client: {} connected.".format(request.sid))


# disconnect as well as some clear action
@socketio.on('disconnect')
def disconnect():
    for user in active_users.values():
        if user['sid'] == request.sid:
            del waiting_users[user['username']]
            del active_users[user['username']]

    print('Client: {} disconnected'.format(request.sid))


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print('some error happened in:  ' + str(e))


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('handles all namespaces without an explicit error handler:  ' + str(e))


if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=8000, debug=True)
