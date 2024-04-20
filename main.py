# src/main.py
def main():
    user_input = input("Enter 0 to initialize DB, 1 to save posts, 2 to read posts, 3 to start replying: ")
    
    if user_input == "0":
        from db.init_db import init_db
        init_db()
    elif user_input == "1":
        from scripts.save_posts import save_data_to_db
        from src.reddit_utils import fetch_and_save_posts
        fetch_and_save_posts(save_data_to_db)
    elif user_input == "2":
        from scripts.read_posts import fetch_posts_from_db, print_posts
        posts = fetch_posts_from_db()
        print_posts(posts)
    elif user_input == "3":
        from src.reddit_utils import reply_to_posts
        reply_to_posts()
    else:
        print("Invalid input. Please enter 0, 1, 2 or 3.")

if __name__ == "__main__":
    main()
