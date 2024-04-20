# This module now contains the shared database access functions
from models.reddit_posts import SubredditPost
from sqlalchemy.exc import IntegrityError
from db.db import db

def update_post_replied_status(post_id, replied_status):
    try:
        post = SubredditPost.query.filter_by(post_id=post_id).first()
        if post:
            post.replied = replied_status
            db.session.commit()
            return True
    except Exception as e:
        db.session.rollback()
        return False

# Add other shared database functionalities if needed
