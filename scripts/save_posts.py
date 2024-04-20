# scripts/save_posts.py
from db.db import create_app, db
from models.reddit_posts import SubredditPost
from src.reddit_utils import fetch_and_save_posts
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = create_app()
app.app_context().push()

def save_data_to_db(post):
    with app.app_context():
        print(post)
        new_post = SubredditPost(
            title=post['title'],
            content=post.get('content', None),
            username=post['username'],
            comments=post["comments"],
            upvotes=post["upvotes"],
            created_utc=post['created_utc'],  # Make sure to handle timezone
            url=post['url'],
            author=post['author'],
            subreddit=post['subreddit'],
            post_id=post['post_id'],
            reply=post["reply"],
            s3_content_name=post["s3_content_name"]
            # tags=[""]  # Assuming you have logic to handle tags properly
        )
        db.session.add(new_post)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"Skipped duplicate post: {post['post_id']}")


if __name__ == '__main__':
    fetch_and_save_posts(save_data_to_db)
