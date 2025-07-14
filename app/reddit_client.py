import praw
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os


reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_posts(subreddit_name, keyword, limit=10):
    """
    Fetch posts from a subreddit based on a keyword.
    
    Args:
        subreddit_name (str): Name of the subreddit (e.g., 'health').
        keyword (str): Search keyword.
        limit (int): Number of posts to retrieve.
    
    Returns:
        list: A list of dictionaries containing post title, URL, and creation time.
    """
    posts = []
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.search(keyword, limit=limit):
            posts.append({
                'title': post.title,
                'url': post.url,
                'created': datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            })
    except Exception as e:
        print(f"[Reddit Fetch Error] {e}")
    
    return posts
