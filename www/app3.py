from pymongo import MongoClient
import json


def handle_mongodb():
    client = MongoClient('localhost', 27017)
    db = client['mydb']  # my own database
    questions = db['questions']  # collections
    users = db['users']

    # # document(schema)
    # question = {
    #     'qid': 0,
    #     'question': 'How many kilometers is there for the official distance of full marathon? ',
    #     'answer': [
    #         'A.  5 kilometers',
    #         'B.  10 kilometers',
    #         'C.  40 kilometers',
    #         'D.  60 kilometers'
    #     ],
    #     'ans': 'C',
    # }
    # questions.insert_one(question)
    #
    # question = {
    #     'qid': 1,
    #     'question': '桃园三结义”中没有以下哪位',
    #     'answer': [
    #         'A. 刘备',
    #         'B. 关羽',
    #         'C. 诸葛亮',
    #         'D. 张飞'
    #     ],
    #     'ans': 'C',
    # }
    # questions.insert_one(question)
    #
    # question = {
    #     'qid': 2,
    #     'question': 'Which of the following is the longest river? ',
    #     'answer': [
    #         'A. Yangtze River',
    #         'B. Yellow River',
    #         'C. Amazon River',
    #         'D. Nile River'
    #     ],
    #     'ans': 'C',
    # }
    # questions.insert_one(question)
    #
    # question = {
    #     'qid': 3,
    #     'question': 'When was the computer invented?',
    #     'answer': [
    #         'A. 1935',
    #         'B. 1946',
    #         'C. 1951',
    #         'D. 1962'
    #     ],
    #     'ans': 'B',
    # }
    # questions.insert_one(question)
    #
    # question = {
    #     'qid': 4,
    #     'question': 'What kind of harmful gas will be emitted when using the copier?',
    #     'answer': [
    #         'A. Carbon monoxide',
    #         'B. Sulphur dioxide',
    #         'C. Ozone',
    #         'D. Nitrogen'
    #     ],
    #     'ans': 'C',
    # }
    # questions.insert_one(question)
    #
    # question = {
    #     'qid': 5,
    #     'question': 'Which planet is the hottest?',
    #     'answer': [
    #         'A. Jupiter',
    #         'B. Mars',
    #         'C. Mercury',
    #         'D. Venus'
    #     ],
    #     'ans': 'D',
    # }
    # questions.insert_one(question)
    #
    # question = {
    #     'qid': 6,
    #     'question': 'How many stepsisters does Cinderella have?',
    #     'answer': [
    #         'A. One',
    #         'B. Two',
    #         'C. Three',
    #         'D. Four'
    #     ],
    #     'ans': 'B',
    # }
    # questions.insert_one(question)
    #
    # question = {
    #     'qid': 7,
    #     'question': 'How many roses and of which colour is the traditional romantic gift?',
    #     'answer': [
    #         'A. Three, Yellow',
    #         'B. Nine, White',
    #         'C. Seven, Pink ',
    #         'D. Twelve, Red'
    #     ],
    #     'ans': 'D',
    # }
    # questions.insert_one(question)
    #
    # question = {
    #     'qid': 8,
    #     'question': '2018年《我是歌手》总冠军是谁？',
    #     'answer': [
    #         'A. 汪峰',
    #         'B. Jessie J',
    #         'C. 张韶涵',
    #         'D. 腾格尔'
    #     ],
    #     'ans': 'B',
    # }
    # questions.insert_one(question)
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
    # questions.insert_one(question)
    #
    #
    #
    #
    # user = {
    #     'username': 'default-user',
    #     'score': 0,
    #     'winRate': 0,
    #     'room': 'default-room',
    # }
    #
    # users.insert_one(user)


    print('-------------------------')

    username = 'default-user'

    if users.find({'username': username}) is not None:
        current_user = users.find_one({'username': username})

        print(current_user)

        print(current_user['score'])
        print(current_user['winRate'])
    else:
        print('yes')

    print('-------------------------')

    for q in questions.find():
        print(q)

    for u in users.find():
        print(u)





if __name__ == "__main__":

    from threading import Thread
    from time import sleep


    def print_hello(n):
        print("enter to Thread %d!" % n)
        sleep(10)
        print("END to Thread %d!" % n)

    # Create 5 threads
    threads = []
    for i in range(5):
        t = Thread(target=print_hello, args=(i,))
        t.start()
        threads.append(t)
    # Wait until all threads are finished
    for t in threads:
        t.join()

    print("END test")

    # handle_mongodb()

