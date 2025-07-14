# app/recommender.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models import Search
from flask_login import current_user

def recommend_keywords():
    # Get all past search keywords of the current user
    searches = Search.query.filter_by(user_id=current_user.id).all()
    keywords = [s.keyword for s in searches]

    # Not enough data for recommendation
    if len(set(keywords)) < 2:
        return []

    # Convert keywords into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(keywords)

    # Compute cosine similarity between the most recent keyword and the rest
    sim_matrix = cosine_similarity(tfidf_matrix)
    last_idx = len(keywords) - 1  # Most recent keyword
    similarity_scores = list(enumerate(sim_matrix[last_idx]))

    # Sort by similarity score, skip the last entry itself (self match)
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    sorted_scores = [score for score in sorted_scores if score[0] != last_idx]

    # Get top 5 recommendations, excluding duplicates
    recommended = []
    seen = set()
    for idx, _ in sorted_scores:
        keyword = keywords[idx]
        if keyword not in seen:
            recommended.append(keyword)
            seen.add(keyword)
        if len(recommended) == 5:
            break

    return recommended
