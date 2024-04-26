# src/reddit_utils.py
import random
import string
import os
import requests
import time
import random
import re
from dotenv import load_dotenv
import praw
from datetime import datetime
from functools import lru_cache
from scripts.read_posts import fetch_unreplied_posts_sorted
from scripts.database_operations import update_post_replied_status
from src.gspread_utils import fetch_column_from_sheet, init_keywords_worksheet, gsheet
from tag_generation_openai.main import generate_response
from concurrent.futures import ThreadPoolExecutor
from aws.upload_to_s3 import upload_image_to_s3
from db.db import create_app

load_dotenv()

app = create_app()

REDDIT_CREDENTIALS = [
    {
        'CLIENT_ID': os.getenv('CLIENT_ID'),
        'CLIENT_SECRET': os.getenv('CLIENT_SECRET'),
        'USER_AGENT': os.getenv('USER_AGENT'),
        'USERNAME': os.getenv('USERNAME'),
        'PASSWORD': os.getenv('PASSWORD'),
        'PROXY_URL': 'http://proxy1.example.com:8080'  # Proxy for this account
    },
    # Add more accounts as needed
]



def load_reddit_instance(creds):
    # session = requests.Session()
    # session.proxies = {
    #     'http': creds['PROXY_URL'],
    #     'https': creds['PROXY_URL']
    # }
    return praw.Reddit(
        client_id=creds['CLIENT_ID'],
        client_secret=creds['CLIENT_SECRET'],
        user_agent=creds['USER_AGENT'],
        username=creds['USERNAME'],
        password=creds['PASSWORD'],
        ratelimit_seconds=600
        # requestor_kwargs={'session': session}
    )

def fetch_and_save_posts(save_data_to_db, creds=REDDIT_CREDENTIALS[0]):
    reddit = load_reddit_instance(creds)
    subreddit_names = fetch_subreddits()
    subreddit = reddit.subreddit(subreddit_names)
    for submission in subreddit.stream.submissions():
        try:
            username = str(submission.author)
            prompt_dict = {"title": submission.title,
                           "content": submission.selftext,
                           "username": username,
                           "comments": submission.num_comments,
                           "upvotes": submission.score,
                           "created_utc": datetime.fromtimestamp(submission.created_utc).isoformat()}
            
            response_dict = generate_response(prompt_dict)
            
            # Check for required keys in response_dict
            if not all(key in response_dict for key in ['title', 'content', 'quote', 'bg_color', 'color', 'reply']):
                raise KeyError("Missing one or more required keys in response_dict")

            id_of_content = format_title(response_dict['title'])
            from image_generation.image import create_decorated_image
            image = create_decorated_image(response_dict['title'], response_dict['content'], response_dict['quote'], response_dict['bg_color'], response_dict['color'])
            from image_generation.image import create_title_image
            og_image = create_title_image(response_dict['title'], response_dict['bg_color'], response_dict['color'])
            upload_image_to_s3(image, id_of_content, "reddit-calmclove")
            upload_image_to_s3(og_image, id_of_content+"-og", "reddit-calmclove")
            
            reply = format_content_link_in_reply(response_dict["reply"], id_of_content, response_dict["title"])

            request_payload = {
                "title": response_dict['title'],
                "content": response_dict['content'],
                "bg_color": response_dict['bg_color'],
                "color": response_dict['color'],
                "quote": response_dict['quote'],
                "reply": reply,
                "content_id": id_of_content
            }
            api_endpoint = "https://api.rejoying.com/api/content_posts/"
            # # parsed_data should have the URL, title, desc, and quote.
            response = requests.post(api_endpoint, json=request_payload)
            if response.status_code == 201:
                print("Data successfully sent to API endpoint.")
            else:
                print("Failed to send data to API endpoint.")
            
            post_data = {
                "title": submission.title,
                "content": submission.selftext,
                "username": username,
                "comments": submission.num_comments,
                "upvotes": submission.score,
                "created_utc": datetime.fromtimestamp(submission.created_utc).isoformat(),
                "url": submission.url,
                "author": str(submission.author),
                "subreddit": submission.subreddit.display_name,
                "post_id": submission.id,
                "reply": reply,
                "s3_content_name": id_of_content
            }
            save_data_to_db(post_data)  # Save each post individually

        except Exception as e:
            print(f"Error processing submission: {e}")
            continue  # Continue with the next submission


def reply_to_posts(creds=REDDIT_CREDENTIALS[0]):
    """Generate and post replies to fetched posts from the database that haven't been replied to yet, with dynamic rate limiting."""
    with app.app_context():
        reddit = load_reddit_instance(creds)
        
        # Initial rate limit setup
        # base_delay = 120  # 2 minutes

        posts = fetch_unreplied_posts_sorted()
        
        for post in posts:
            if not post.replied:  # Double-checking the flag
                submission = reddit.submission(id=post.post_id)
                response_text = post.reply
                if response_text:
                    try:
                        submission.reply(response_text)
                        print(f"Replied to post {post.post_id} with {response_text}")

                        # Update Database
                        if update_post_replied_status(post.post_id, True):
                            print(f"Database updated for post {post.post_id}")

                    except Exception as e:
                        if "RATELIMIT" in str(e):
                            match = re.search(r'\b(\d+)\sminutes\b', str(e))
                            if match:
                                minutes = int(match.group(1))
                                # base_delay = minutes * 60
                                print(e)
                                print(f"Rate limit exceeded. Adjusting rate limit to {minutes} minutes.")
                            else:
                                # base_delay = 180  # Default to 9 minutes
                                print(e)
                                print("Rate limit exceeded. Adjusting rate limit to 3 minutes.")

                            # Randomize delay within a 0 to 120 seconds range for RATELIMIT error
                            random_variation = random.randint(0, 120)
                            delay =  random_variation
                            time.sleep(delay)
                            print(f"Waiting for {delay} seconds before retrying the same operation.")
                            continue  # Retry the same post after waiting
                            
                        else:
                            print(f"Failed to reply to post {post.post_id}: {e}")
                            continue  # Skip to the next post for all other types of exceptions

        # Restore the rate limit after about an hour of execution
        time.sleep(120)  # Wait for an hour
        # base_delay = 120  # Reset to 2 minutes
        print("Restored base delay to 2 minutes.")

@lru_cache(maxsize=128)
def fetch_subreddits():
    subreddits_and_keywords_worksheet = init_keywords_worksheet(gsheet, 1)
    subreddits_in_sheet = fetch_column_from_sheet(subreddits_and_keywords_worksheet, "subreddits")
    subreddit_names = '+'.join(subreddits_in_sheet)
    return subreddit_names

def fetch_and_save_reddit_posts_thread(fetch_and_save_posts, save_data_to_db):
    """Process fetching all subreddits using multiple Reddit credentials concurrently."""
    with ThreadPoolExecutor(max_workers=len(REDDIT_CREDENTIALS)) as executor:
        for creds in REDDIT_CREDENTIALS:
            executor.submit(fetch_and_save_posts, save_data_to_db, creds)

def post_reply_reddit_posts_thread(reply_to_posts):
    """Process replying to all subreddits using multiple Reddit credentials concurrently."""
    with ThreadPoolExecutor(max_workers=len(REDDIT_CREDENTIALS)) as executor:
        for creds in REDDIT_CREDENTIALS:
            executor.submit(reply_to_posts, creds)


def extract_specific_reply(response_text):
    # Split the response text by the '---' delimiter
    parts = response_text.split('---')
    # Select the last part which is the actual message intended for the user
    specific_reply = parts[-1].strip()  # Use strip() to remove any leading/trailing whitespace
    return specific_reply

def format_title(title):
    # Split the title by spaces and join by hyphens
    hyphenated_title = '-'.join(title.split())
    
    # Generate a random string of 7 alphanumeric characters
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    
    # Combine the hyphenated title with the random string
    final_title = f"{hyphenated_title}-{random_string}"
    
    return final_title.lower()

def format_content_link_in_reply(reply, content_id, link_text):
    # Define the URL pattern to insert
    url = f"https://calmclove.com/?choice=happy&content={content_id}.png"
    
    # Construct the Markdown link
    markdown_link = f"[{link_text}]({url})"
    
    # Check if the placeholder exists in the reply
    if "[LINK_FOR_THE_CONTENT]" in reply:
        # Replace the placeholder in the reply with the Markdown link
        formatted_reply = reply.replace("[LINK_FOR_THE_CONTENT]", markdown_link)
    else:
        # Append a new sentence with the Markdown link if the placeholder is not found
        formatted_reply = f"{reply} I found this piece of advice very uplifting; perhaps it could help you too - {markdown_link}"
    
    return formatted_reply
