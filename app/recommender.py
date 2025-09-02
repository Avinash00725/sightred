import praw
import os
from flask import session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend_posts():
    searched_keywords = session.get("searched_keywords", [])

    if not searched_keywords:
        # No searches, just trending posts
        trending_posts = []
        for post in reddit.subreddit("all").hot(limit=10):
            trending_posts.append({
                "title": post.title,
                "url": post.url,
                "subreddit": post.subreddit.display_name,
                "score": post.score,
                "author": str(post.author)
            })
        return {"search_based_posts": [], "trending_posts": trending_posts}

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(searched_keywords)

    last_query_vec = tfidf_matrix[-1]
    similarities = cosine_similarity(last_query_vec, tfidf_matrix[:-1]).flatten()

    if similarities.size > 0:
        most_similar_idx = np.argmax(similarities)
        similar_keyword = searched_keywords[most_similar_idx]
    else:
        similar_keyword = searched_keywords[-1]

    search_based_posts = []
    for kw in [searched_keywords[-1], similar_keyword]:
        for post in reddit.subreddit("all").search(kw, limit=3):
            search_based_posts.append({
                "title": post.title,
                "url": post.url,
                "subreddit": post.subreddit.display_name,
                "score": post.score,
                "author": str(post.author)
            })
    REQUIRED_LIMIT = 6
    if len(search_based_posts) < REQUIRED_LIMIT:
        needed = REQUIRED_LIMIT - len(search_based_posts)
        trending_posts = []
        for post in reddit.subreddit("all").top(time_filter="day", limit=needed):
            trending_posts.append({
                "title": post.title,
                "url": post.url,
                "subreddit": post.subreddit.display_name,
                "score": post.score,
                "author": str(post.author)
            })
    else:
        trending_posts = None

    return {"search_based_posts": search_based_posts, "trending_posts": trending_posts}
