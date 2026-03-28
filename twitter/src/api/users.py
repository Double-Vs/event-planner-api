import sqlalchemy 
from flask import Blueprint, jsonify, abort, request
from ..models import User, Tweet, db, likes
import hashlib
import secrets

# Hide the password before saving it

def scramble(password: str):
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

# Create all /users routes

bp = Blueprint('users', __name__, url_prefix='/users')

# GET /users

# Get all users

@bp.route('', methods=['GET'])

def index():

    users = User.query.all()
    result = []


    for u in users:
        result.append(u.serialize())

    return jsonify(result)


# GET /users/<id>

# Get one user

@bp.route('/<int:id>', methods=['GET'])

def show(id):
    user = User.query.get(id)

    if not user:
        abort(404)
    return jsonify(user.serialize())

# POST /users

# Create a new user
@bp.route('', methods=['POST'])

def create():
    username = request.json['username']
    password = request.json['password']

    # Check username and password length

    if len(username) < 3 or len(password) < 8:

        abort(400)

    # Hide password before saving
    password = scramble(password)

    # Create user
    u = User(username=username, password=password)

    # Save to database
    db.session.add(u)
    db.session.commit()
    return jsonify(u.serialize())

# Delete 

@bp.route('/<int:id>', methods=['DELETE'])

def delete(id):
    user = User.query.get(id)
    if not user:
        return jsonify(False)

    try:

        db.session.delete(user)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
    

@bp.route('/<int:id>', methods=['PUT', 'PATCH'])

def update(id):
    u = User.query.get_or_404(id)

    username = request.json.get('username')
    password = request.json.get('password')

    # If nothing was sent, return 400

    if not username and not password:
        abort(400)

    # Update username if sent

    if username:
        if len(username) < 3:
            abort(400)
        u.username = username

    # Update password if sent

    if password:
        if len(password) < 8:
            abort(400)
        u.password = scramble(password)


    try:
        db.session.commit()
        return jsonify(u.serialize())

    except:
        return jsonify(False)

@bp.route('/<int:id>/liked_tweets', methods=['GET'])

def liked_tweets(id: int):
    u = User.query.get_or_404(id)

    result = []

    for t in u.liked_tweets:
        result.append(t.serialize())

    return jsonify(result)
    
@bp.route('/<int:id>/likes', methods=['POST'])
def like(id):
    if 'tweet_id' not in request.json:
        abort(400)

    User.query.get_or_404(id)
    Tweet.query.get_or_404(request.json['tweet_id'])

    stmt = sqlalchemy.insert(likes).values(
        user_id=id,
        tweet_id=request.json['tweet_id']
    )

    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)

