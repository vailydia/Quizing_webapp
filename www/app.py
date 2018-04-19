import sys
import nltk
from flask import Flask, current_app, jsonify, request, render_template, redirect, url_for
from time import gmtime, strftime
from operator import itemgetter
import jinja2

# python3 server.py 5000
port_number = int(sys.argv[1])

app = Flask(__name__)

QUESTIONS = {
    'q1': {
        'question': 'What is your favoriate color?',
        'answer': ['red','blue','yellow','black'],
    },
    'q2': {
        'question': 'What is your favoriate color222?',
        'answer': ['red', 'blue', 'yellow', 'black'],
    },
}

PRODUCTS = {
    'iphone': {
        'name': 'iPhone 5S',
        'category': 'Phones',
        'price': 699,
    },
    'galaxy': {
        'name': 'Samsung Galaxy 5',
        'category': 'Phones',
        'price': 649,
    },
    'ipad-air': {
        'name': 'iPad Air',
        'category': 'Tablets',
        'price': 649,
    },
    'ipad-mini': {
        'name': 'iPad Mini',
        'category': 'Tablets',
        'price': 549
    }
}

userNames = ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    _name = request.form['userName']
    userNames = _name
    print("post success: %s" % (userNames))
    # return redirect(url_for('start'))
    return redirect(url_for('start'))


@app.route('/start', methods=['GET'])
def start():
    print("start quizing.")
    return render_template('main.html', questions=QUESTIONS, userNames = userNames)


@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html', products=PRODUCTS)


@app.route('/showMsg', methods=['GET'])
def search():
    return 'Please finish login process!!!!!!!.'


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=port_number)
