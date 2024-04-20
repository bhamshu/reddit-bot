# read_posts.py
from models.reddit_posts import SubredditPost
from db.db import create_app

app = create_app()

def fetch_posts_from_db():
    with app.app_context():
        # Retrieve all posts from the database
        posts = SubredditPost.query.all()
        # You can also filter, order, or limit the query as per your needs
        return posts

def fetch_post_by_post_id(post_id):
    with app.app_context():
        try:
            # Retrieve a single post by post_id from the database
            post = SubredditPost.query.filter_by(id=post_id).first()
            return post
        except Exception as e:
            print(f"An error occurred while fetching the post: {e}")
            return None

def fetch_unreplied_posts_sorted():
    with app.app_context():
        try:
            # Fetch posts from the database that haven't been replied to, sorted by upvotes and comments
            posts = SubredditPost.query.filter_by(replied=False).order_by(SubredditPost.upvotes.desc(), SubredditPost.comments.desc()).all()
            return posts
        except Exception as e:
            print(f"An error occurred while fetching unreplied posts: {e}")
            return None


def print_posts(posts):
    for post in posts:
        print(f"Reply: {post.reply}")

if __name__ == '__main__':
    posts = fetch_posts_from_db()
    print_posts(posts)
