import datetime
import uuid
from functools import wraps

import jwt
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.py')
print(app.config)
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

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            current_user = Users.query.filter_by(
                public_id=data['public_id'],
            ).first()
            print(current_user)
        except Exception:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


@app.route('/farbophon/register', methods=['POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(
        public_id=str(uuid.uuid4()),
        name=data['name'], password=hashed_password, admin=False,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@app.route('/farbophon/login', methods=['POST'])
def login_user():

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            'could not verify',
            401,
            {'WWW.Authentication': 'Basic realm: "login required"'},
        )

    user = Users.query.filter_by(name=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                'public_id': user.public_id,
                'exp': datetime.datetime.utcnow() +
                datetime.timedelta(minutes=30),
            },
            app.config['SECRET_KEY'],
        )
        return jsonify({'token': token.decode('UTF-8')})

    return make_response(
        'could not verify',
        401,
        {'WWW.Authentication': 'Basic realm: "login required"'},
    )


@app.route('/farbophon/addScore', methods=['POST'])
@token_required
def addScore(current_user):
    try:
        data = request.get_json()

        new_score = Scores(name=data['name'], score=data['score'])
        db.session.add(new_score)
        db.session.commit()

        return jsonify({'status': 'success'})
    except Exception:
        return jsonify({'status': 'failure'})


@app.route('/farbophon/getHighscore', methods=['POST', 'GET'])
def get_highscore():

    highscores = Scores.query.all().order_by(Scores.score.desc()).limit(5)
    print(highscores)

    output = []
    for score in highscores:

        score_data = {}
        score_data['name'] = score.name
        score_data['score'] = score.score
        output.append(score_data)

    return jsonify({'highscore': output})


if __name__ == '__main__':
    app.run(debug=True)
