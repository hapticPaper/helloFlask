import flask
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_restful import reqparse
import pandas, os, requests

import string
digs = string.digits + "".join([s.upper() for s in string.ascii_letters])




def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)


app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/welcome/<name>')
def hello(name):
    return render_template('personalWelcome.html', name=name)

@app.route('/maths')
def maths():
    parser = reqparse.RequestParser()
    parser.add_argument('base', type=str, required=True, help="An number is required.", action='append')
    args = parser.parse_args()
    base = args['base'][0]
    
    if int(base)<=36:
        numbersdf = pandas.DataFrame([[n, int2base(n, int(base))] for n in range(30)], columns = ['int',f'base{base} int'])
        return render_template('maths.html',base=base, numbers=numbersdf.to_html(index=False))
    else:
        return "Please choose a base below 37"


@app.route('/num2base/<base>')
def num2base(base):
    parser = reqparse.RequestParser()
    parser.add_argument('num', type=str, required=True, help="An number is required.", action='append')
    args = parser.parse_args()
    num = args['num'][0]
    try:
        return int2base(int(num),int(base))
    except:
        return "Try a better number."

@app.route('/numception')
def numception():
    parser = reqparse.RequestParser()
    parser.add_argument('base', type=str, required=True, help="An base is required.", action='append')
    parser.add_argument('num', type=str, required=True, help="An number is required.", action='append')
    args = parser.parse_args()
    base = args['base'][0]
    num = args['num'][0]
    try:
        return requests.session().get(f'http://localhost:5000/json?base={base}').json()[num]
    except:
        return "Try a number < 1000"

@app.route('/json')
def jsonmath():
    parser = reqparse.RequestParser()
    parser.add_argument('base', type=str, required=True, help="An number is required.", action='append')
    args = parser.parse_args()
    base = args['base'][0]
    if int(base)<=36:
        return jsonify({n: int2base(n, int(base)) for n in range(1000)})
    else:
        return "Please choose a base below 37"


if __name__ == '__main__':
    app.run(threaded=True, debug=True)