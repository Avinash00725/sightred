# # app/recommender.py

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from app.models import Search
# from flask_login import current_user

# def recommend_keywords():
#     # Get all past search keywords of the current user
#     searches = Search.query.filter_by(user_id=current_user.id).all()
#     keywords = [s.keyword for s in searches]

#     # Not enough data for recommendation
#     if len(set(keywords)) < 2:
#         return []

#     # Convert keywords into TF-IDF vectors
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(keywords)

#     # Compute cosine similarity between the most recent keyword and the rest
#     sim_matrix = cosine_similarity(tfidf_matrix)
#     last_idx = len(keywords) - 1  # Most recent keyword
#     similarity_scores = list(enumerate(sim_matrix[last_idx]))

#     # Sort by similarity score, skip the last entry itself (self match)
#     sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
#     sorted_scores = [score for score in sorted_scores if score[0] != last_idx]

#     # Get top 5 recommendations, excluding duplicates
#     recommended = []
#     seen = set()
#     for idx, _ in sorted_scores:
#         keyword = keywords[idx]
#         if keyword not in seen:
#             recommended.append(keyword)
#             seen.add(keyword)
#         if len(recommended) == 5:
#             break

#     return recommended


import praw
import os
import random
from flask import session

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
                    "subreddit": sub
                })

        return {"search_based_posts": None, "trending_posts": trending_posts}

    else:
        # Show posts for searched keywords
        search_based_posts = []
        for kw in searched_keywords[-3:]:  # limit to last 3 searches
            for post in reddit.subreddit("all").search(kw, limit=3):
                search_based_posts.append({
                    "title": post.title,
                    "url": post.url,
                    "subreddit": post.subreddit.display_name
                })

        return {"search_based_posts": search_based_posts, "trending_posts": None}

