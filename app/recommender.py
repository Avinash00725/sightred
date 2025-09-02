import praw
import os
import random
from flask import session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def recommend_posts():
    searched_keywords = session.get("searched_keywords", [])

    if not searched_keywords:
        # Default: trending posts
        default_subreddits = ["technology", "worldnews", "sports", "science"]
        trending_posts = []

        for sub in default_subreddits:
            subreddit = reddit.subreddit(sub)
            for post in subreddit.top(time_filter="week", limit=3):
                trending_posts.append({
                    "title": post.title,
                    "url": post.url,
                    "subreddit": sub,
                    "score": post.score,
                    "author": str(post.author),
                    "created": post.created_utc
                })

        return {"search_based_posts": None, "trending_posts": trending_posts}

    else:
        # Use TF-IDF on searched keywords
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(searched_keywords)

        # Compare last search with all previous
        last_query_vec = tfidf_matrix[-1]
        similarities = cosine_similarity(last_query_vec, tfidf_matrix[:-1]).flatten()

        if similarities.size > 0:
            most_similar_idx = np.argmax(similarities)
            similar_keyword = searched_keywords[most_similar_idx]
        else:
            similar_keyword = searched_keywords[-1]

        # Fetch posts for both latest keyword + similar one
        search_based_posts = []
        for kw in [searched_keywords[-1], similar_keyword]:
            for post in reddit.subreddit("all").search(kw, limit=3):
                search_based_posts.append({
                    "title": post.title,
                    "url": post.url,
                    "subreddit": post.subreddit.display_name,
                    "score": post.score,
                    "author": str(post.author),
                    "created": post.created_utc
                })

        return {"search_based_posts": search_based_posts, "trending_posts": None}
