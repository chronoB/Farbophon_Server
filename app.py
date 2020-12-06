from functools import wraps

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
CORS(app)

app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    score = db.Column(db.Integer)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        if token != app.config['API_KEY']:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)
    return decorator


@app.route('/farbophon/addScore', methods=['POST'])
@token_required
def addScore():
    try:
        data = request.get_json()

        new_score = Scores(name=data['name'], score=data['score'])
        db.session.add(new_score)
        db.session.commit()

        return jsonify({'status': 'success'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'failure'})


@app.route('/farbophon/getHighscore', methods=['GET'])
def get_highscore():

    highscores = Scores.query.order_by(Scores.score.desc()).limit(5).all()

    output = []
    for score in highscores:

        score_data = {}
        score_data['name'] = score.name
        score_data['score'] = score.score
        output.append(score_data)

    return jsonify({'highscore': output})


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5253)
