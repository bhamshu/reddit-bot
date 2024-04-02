import os
from dotenv import load_dotenv
from openai_utils import generate_reply, generate_user_summary
import praw
from gspread_utils import gsheet, init_reviews_worksheet, append_to_sheet, init_keywords_worksheet, fetch_column_from_sheet
from datetime import datetime, timezone
import time
import random
import re

# Load environment variables from .env file
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USER_AGENT'),
    username=os.getenv('USERNAME'),
    password=os.getenv('PASSWORD')
)
def subreddit_reply_generator():
    # Initialize the Keywords Worksheet
    subreddits_and_keywords_worksheet = init_keywords_worksheet(gsheet, 1)
    subreddits_in_sheet = fetch_column_from_sheet(subreddits_and_keywords_worksheet, "subreddits")
    # Join the items with '+' and remove disallowed characters
    subreddit_string = '+'.join(subreddits_in_sheet)
    allowed_subreddit_string = re.sub(r'[^a-zA-Z0-9_+]', '', subreddit_string)

    keywords = fetch_column_from_sheet(subreddits_and_keywords_worksheet, "keywords")
    
    subreddit = reddit.subreddit(allowed_subreddit_string)
   
    # Initialize the Reviews Worksheet
    reviews_worksheet = init_reviews_worksheet(gsheet, 0)

    for submission in subreddit.stream.submissions():
        if any(keyword.lower() in submission.title.lower() for keyword in keywords):
            print(f"Found a post: {submission.title}")
          
            username = str(submission.author)
            user_summary = redditor_summary_generator(username)

            prompt_dict = {"title":submission.title, "content": submission.selftext, "username": username, "user_summary": user_summary}

            # Generate a reply for the post's content
            reply_text = generate_reply(prompt_dict)
                
            # Prepare the data row
            row_data = [submission.title, submission.url, username, submission.selftext, reply_text, user_summary]
            # Append the data to the Google Sheet
            append_to_sheet(reviews_worksheet, row_data)

            # Here, you reply to the post with the generated reply_text
            try:
                submission.reply(reply_text)
                print(f"Replied to {submission.title}")
            except Exception as e:
                print(f"Failed to reply to {submission.title}: {str(e)}")
            
            # Wait for 5 minutes (300 seconds) + a random number of seconds before processing the next post
            time_to_wait = 300 + random.randint(0, 200)
            print(f"Waiting for {time_to_wait} seconds...")
            time.sleep(time_to_wait)


def redditor_summary_generator(username): 
    user = reddit.redditor(username)

    user_posts = []

    for submission in user.submissions.new(limit=50):
        post_details = {
            "title": submission.title,
            "content": submission.selftext,
            "url": submission.url,
            "username": submission.author.name if submission.author else 'deleted',
            "date_of_post": datetime.fromtimestamp(submission.created_utc, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')  # Now using timezone-aware datetime
        }
        user_posts.append(post_details)

     # Check if the list is not empty before proceeding
    if not user_posts:
        print("No posts found for user.")
        return "No past posts for this user."
    else:
        print(f"Fetched {len(user_posts)} posts for user.")
        summary = generate_user_summary(user_posts)
        return summary
    