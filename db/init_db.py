# db/init_db.py
from db.db import create_app, db
from models.reddit_posts import SubredditPost

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created.")

if __name__ == '__main__':
    init_db()
