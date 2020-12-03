#!/usr/bin/python3

import pandas as pd
from flask import Flask, request, jsonify
from models import *
from config import *
from errors import InvalidUsage

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def load_data(csv):
    rests = {}
    df = pd.read_csv(csv, index_col='id')
    for id, row in df.iterrows():
        if id not in rests:
            rests[id] = Restaurant(id, row['name'], row['city'])
        menuObj = Menu(row['menus.name'])
        rests[id].addMenu(menuObj)
    return rests

rests = load_data('data.csv')
print(rests)

@app.route('/')
def home():
    return '<h1>Restaurant API</h1>\
        <li><a href={}restaurants>Restaurants</a></li>'.format(request.url_root)

@app.route('/restaurants/', methods=['GET'])
def restaurants():
    city = request.args.get('city')
    menu = request.args.get('menu')
    print(city)
    print(menu)
    try:
        res = []
        for rest in rests.values():
            if city and rest.city != city: continue
            if menu and menu not in rest.menus: continue
            res.append(rest.toDict())
        return jsonify(res)
    except Exception as e:
        print(e)
        raise InvalidUsage('Invalid query string', status_code=410, payload={'payload': 'Please check the query string'})

@app.route('/restaurants/<id>', methods=['GET'])
def restaurant(id):
    if id in rests:
        rest = rests[id]
        res = rest.toDict()
        return jsonify(res)
    else:
        return jsonify({})

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
