# models.py
from db.db import db

class SubredditPost(db.Model):
    __tablename__ = 'reddit_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    username = db.Column(db.String)
    url = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    subreddit = db.Column(db.String, nullable=False)
    upvotes =  db.Column(db.Integer)
    comments =  db.Column(db.Integer)
    post_id = db.Column(db.String, nullable=False, unique=True)
    replied = db.Column(db.Boolean, default=False)
    created_utc = db.Column(db.DateTime, nullable=False)
    reply = db.Column(db.String)
    s3_content_name = db.Column(db.String)

def get_all_posts():
    return SubredditPost.query.all()