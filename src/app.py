from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the SQLAlchemy part
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your model
class SubredditPost(db.Model):
    __tablename__ = 'subreddit_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    selftext = db.Column(db.Text)
    url = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text)
    subreddit = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Text, nullable=False, unique=True)
    created_utc = db.Column(db.DateTime, nullable=False)

@app.route('/save_post', methods=['POST'])
def save_post():
    data = request.json
    try:
        # Create a new SubredditPost object
        new_post = SubredditPost(
            title=data['title'],
            selftext=data['selftext'],
            url=data['url'],
            author=data['author'],
            subreddit=data['subreddit'],
            post_id=data['post_id'],
            created_utc=data['created_utc']
        )
        
        db.session.add(new_post)  # Add the new object to the session
        db.session.commit()  # Commit the session to the database
        
        return jsonify({"message": "Post saved successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Roll back the session in case of error
        return jsonify({"error": str(e)}), 500
