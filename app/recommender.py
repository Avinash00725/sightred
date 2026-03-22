import praw
import os
from flask import session
from flask_login import current_user
from datetime import datetime
from functools import lru_cache

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    read_only=True  # Read-only mode for faster API calls
)

def simple_string_similarity(str1, str2):
    """
    Simple string similarity based on common words.
    Returns a score between 0 and 1.
    """
    words1 = set(str1.lower().split())
    words2 = set(str2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    return intersection / union if union > 0 else 0.0


def recommend_posts():
    """
    Recommend posts based on user's complete search history.
    Returns:
    - past_search_posts: Posts from previous searches (historical recommendations)
    - new_posts: Fresh posts from recent searches
    - trending_posts: Trending posts if needed to fill
    Total limit: 15 posts
    """
    from app.models import Search
    from app import db
    
    # Get all unique keywords from user's search history
    all_searches = Search.query.filter_by(user_id=current_user.id)\
                               .order_by(Search.timestamp.desc()).all()
    
    all_keywords = [s.keyword for s in all_searches]
    unique_keywords = list(dict.fromkeys(all_keywords))  # Remove duplicates, preserve order
    
    if not all_keywords:
        # No search history, return trending posts
        trending_posts = []
        try:
            for post in reddit.subreddit("all").hot(limit=15):
                trending_posts.append({
                    "title": post.title,
                    "url": post.url,
                    "subreddit": post.subreddit.display_name,
                    "score": post.score,
                    "author": str(post.author)
                })
        except Exception as e:
            print(f"Error fetching trending posts: {e}")
        
        return {
            "past_search_posts": [],
            "new_posts": [],
            "trending_posts": trending_posts
        }

    # --- Collect REST from Past Searches (older keywords) ---
    past_search_posts = []
    seen_urls = set()
    
    # Get posts from first 5-7 older searches for diversity
    older_keywords = unique_keywords[min(3, len(unique_keywords)):]  # Skip the most recent 3
    
    for kw in older_keywords[:5]:  # Fetch from up to 5 older keywords
        try:
            for post in reddit.subreddit("all").search(kw, limit=2, sort="top"):
                if post.url not in seen_urls:
                    past_search_posts.append({
                        "title": post.title,
                        "url": post.url,
                        "subreddit": post.subreddit.display_name,
                        "score": post.score,
                        "author": str(post.author)
                    })
                    seen_urls.add(post.url)
                    
                    if len(past_search_posts) >= 7:
                        break
        except Exception as e:
            print(f"Error searching for past keyword '{kw}': {e}")
        
        if len(past_search_posts) >= 7:
            break

    # --- Collect NEW Posts from Recent Searches ---
    new_posts = []
    
    # Get most recent keywords
    recent_keywords = unique_keywords[:3]
    
    # Use simple string similarity to rank which keywords are most relevant
    if len(unique_keywords) > 1:
        try:
            last_keyword = unique_keywords[-1]
            similarities = []
            
            for i, kw in enumerate(unique_keywords[:-1]):
                sim = simple_string_similarity(last_keyword, kw)
                if sim > 0.2:  # Only consider keywords with at least 20% similarity
                    similarities.append((i, sim, kw))
            
            # Sort by similarity descending
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Add top 2 similar keywords
            for _, _, kw in similarities[:2]:
                if kw not in recent_keywords:
                    recent_keywords.append(kw)
        except Exception as e:
            print(f"Error calculating similarity: {e}")
    
    recent_keywords = list(dict.fromkeys(recent_keywords))  # Remove duplicates
    
    for kw in recent_keywords[:3]:
        try:
            for post in reddit.subreddit("all").search(kw, limit=5, sort="relevance"):
                if post.url not in seen_urls:
                    new_posts.append({
                        "title": post.title,
                        "url": post.url,
                        "subreddit": post.subreddit.display_name,
                        "score": post.score,
                        "author": str(post.author)
                    })
                    seen_urls.add(post.url)
                    
                    if len(new_posts) >= 8:
                        break
        except Exception as e:
            print(f"Error searching for recent keyword '{kw}': {e}")
        
        if len(new_posts) >= 8:
            break

    # --- Fill remaining with trending posts if needed ---
    REQUIRED_LIMIT = 15
    trending_posts = None
    total_posts = len(past_search_posts) + len(new_posts)
    
    if total_posts < REQUIRED_LIMIT:
        needed = REQUIRED_LIMIT - total_posts
        trending_posts = []
        try:
            for post in reddit.subreddit("all").top(time_filter="week", limit=needed + 5):
                if post.url not in seen_urls:
                    trending_posts.append({
                        "title": post.title,
                        "url": post.url,
                        "subreddit": post.subreddit.display_name,
                        "score": post.score,
                        "author": str(post.author)
                    })
                    seen_urls.add(post.url)
                    
                    if len(trending_posts) >= needed:
                        break
        except Exception as e:
            print(f"Error fetching trending posts: {e}")

    return {
        "past_search_posts": past_search_posts,
        "new_posts": new_posts,
        "trending_posts": trending_posts
    }
