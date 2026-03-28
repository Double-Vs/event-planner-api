from flask_sqlalchemy import SQLAlchemy
import datetime

# Initialize database

db = SQLAlchemy()

# Association table to connect users and tweets (many-to-many)

# This stores which user liked which tweet

likes = db.Table(

    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('tweet_id', db.Integer, db.ForeignKey('tweets.id'))

)

class User(db.Model):

    __tablename__ = "users"

    # Primary key

    id = db.Column(db.Integer, primary_key=True)

    # unique Username

    username = db.Column(db.String(128), unique=True, nullable=False)

    # Password 

    password = db.Column(db.String(128), nullable=False)

    # One user → many tweets

    tweets = db.relationship('Tweet', backref='user', cascade='all,delete')

    # Many-to-many: users ↔ liked tweets

    liked_tweets = db.relationship(
        'Tweet',
        secondary=likes,
        backref='liking_users'
    )

    def __init__(self, username, password):

        self.username = username
        self.password = password

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }

class Tweet(db.Model):
    __tablename__ = "tweets"

    # Primary key

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Tweet text 

    content = db.Column(db.String(280), nullable=False)

    # tweet timestamp

    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    # Foreign key links
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    # Return tweet data as JSON
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "created_at": self.created_at
        }
    