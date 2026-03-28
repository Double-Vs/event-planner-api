from flask import Blueprint, jsonify
from ..models import Tweet

bp = Blueprint('tweets', __name__, url_prefix='/tweets')

@bp.get('/')
def index():
    tweets = Tweet.query.all()
    return jsonify([
        {
            "id": tweet.id,
            "content": tweet.content,
            "user_id": tweet.user_id
        }

        for tweet in tweets
    ])

