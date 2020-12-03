#!/usr/bin/env python3.6
import json
import sqlite3

from flask import Flask
from flask import g
from flask import request


app = Flask(__name__)
DATABASE = 'db/highscore.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/farbophon", methods=['POST', 'GET'])
def getData():
    if request.method == "POST":
        # return error when request.json not in correct schema
        highScoreList = addDataToDB(request.json)
        return json.dumps(highScoreList)
    elif request.method == "GET":
        songTable = list(request.json.keys())[0]
        return json.dumps(
            query_db(
                'SELECT * FROM '+songTable+' ORDER BY score DESC LIMIT 5',
            ),
        )


def addDataToDB(data):
    songTable = list(data.keys())[0]
    tableExists = query_db(
        'SELECT name FROM sqlite_master WHERE type="table" AND name=?',
        [songTable],
        one=True,
    )
    if not tableExists:
        query_db(
            'CREATE TABLE '+songTable+' (\
                  id INTEGER PRIMARY KEY AUTOINCREMENT,\
                  name TEXT NOT NULL,\
                  score INTEGER NOT NULL)',
        )
    for item in data[songTable]:
        playerName = item["name"]
        playerScore = item["score"]
        query = 'INSERT INTO '+songTable+' (name,score) VALUES (?,?)'
        query_db(query, [playerName, playerScore])
        # sqlcall insert unto
    get_db().commit()

    return query_db('SELECT * FROM '+songTable+' ORDER BY score DESC LIMIT 5')
    # return sqlcall get ordered list


@app.after_request  # blueprint can also be app~~
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5253)
