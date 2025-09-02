from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from datetime import datetime
from collections import Counter
import json
import praw
from dotenv import load_dotenv
load_dotenv()
import os

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

from app.models import Search
from app import db
from app.reddit_client import fetch_posts
from app.nlp_utils import analyze_sentiment, extract_entities
from app.recommender import recommend_posts

# Registering the blueprint
main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    """Landing page after login"""
    return render_template('home.html')


@main.route('/subreddit/<name>', methods=["GET", "POST"])
@login_required
def subreddit(name):
    keyword = request.args.get('keyword', '')
    posts = []

    print(f"Subreddit: {name}, Keyword: {keyword}")

    if keyword:
        subreddit = reddit.subreddit(name)
        try:
            posts = list(subreddit.search(keyword, limit=10))
            print(f"Found {len(posts)} posts")

            # Save search to DB
            new_search = Search(
                user_id=current_user.id,
                subreddit=name,
                keyword=keyword,
                timestamp=datetime.utcnow()
            )
            db.session.add(new_search)
            db.session.commit()

            # Save search to session
            if "searched_keywords" not in session:
                session["searched_keywords"] = []
            session["searched_keywords"].append(keyword)
            session.modified = True

        except Exception as e:
            print(f"Error during search: {e}")

    return render_template('subreddit.html', subreddit=name, keyword=keyword, posts=posts)


@main.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard to show recent searches and keyword frequency.
    """
    searches = Search.query.filter_by(user_id=current_user.id)\
                           .order_by(Search.timestamp.desc())\
                           .limit(10).all()

    all_keywords = [s.keyword for s in Search.query.filter_by(user_id=current_user.id).all()]
    keyword_counts = Counter(all_keywords)

    chart_data = {
        'labels': list(keyword_counts.keys()),
        'values': list(keyword_counts.values())
    }

    return render_template('dashboard.html', searches=searches, chart_data=json.dumps(chart_data))


@main.route('/recommendations')
@login_required
def recommendations():
    """
    Show recommended posts based on user searches or default trending posts.
    """
    recs = recommend_posts()

    # If user has searched before → show posts based on those keywords
    if recs.get("search_based_posts"):
        return render_template(
            'recommendations.html',
            search_based_posts=recs["search_based_posts"],
            trending_posts=None
        )
    else:
        # Otherwise show trending default posts
        return render_template(
            'recommendations.html',
            search_based_posts=None,
            trending_posts=recs["trending_posts"]
        )
