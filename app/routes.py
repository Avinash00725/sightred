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


@main.route('/api/suggestions')
@login_required
def get_suggestions():
    """
    API endpoint for autocomplete suggestions.
    Returns subreddit or keyword suggestions based on user input.
    """
    query = request.args.get('q', '').strip().lower()
    suggestion_type = request.args.get('type', 'keyword')  # 'keyword' or 'subreddit'
    
    if not query or len(query) < 1:
        return json.dumps([])
    
    suggestions = []
    
    try:
        if suggestion_type == 'subreddit':
            # Get subreddit suggestions from Reddit
            try:
                for subreddit in reddit.subreddits.search(query, limit=5):
                    suggestions.append({
                        'name': subreddit.display_name,
                        'subscribers': subreddit.subscribers
                    })
            except Exception as e:
                print(f"Error fetching subreddit suggestions: {e}")
            
            # Also add user's previous subreddit searches
            previous_searches = Search.query.filter_by(user_id=current_user.id).all()
            previous_subreddits = list(set([s.subreddit for s in previous_searches 
                                           if query in s.subreddit.lower()]))
            for sub in previous_subreddits[:3]:
                if not any(s.get('name') == sub for s in suggestions):
                    suggestions.insert(0, {'name': sub, 'subscribers': 0})
        
        else:  # keyword suggestions
            # Get user's previous keyword searches
            previous_searches = Search.query.filter_by(user_id=current_user.id).all()
            previous_keywords = list(set([s.keyword for s in previous_searches 
                                         if query in s.keyword.lower()]))
            for kw in previous_keywords[:5]:
                suggestions.append({'keyword': kw})
            
            # Add trending keywords if needed
            if len(suggestions) < 5:
                try:
                    trending = reddit.subreddit("all").hot(limit=10)
                    for post in trending:
                        if query in post.title.lower():
                            suggestions.append({'keyword': query})
                            break
                except:
                    pass
    
    except Exception as e:
        print(f"Error in get_suggestions: {e}")
    
    return json.dumps(suggestions[:10])


@main.route('/recommendations')
@login_required
def recommendations():
    """
    Show recommended posts based on user's search history:
    - Posts from past searches (older keywords)
    - New posts from recent searches
    - Trending posts to fill remaining slots
    """
    recs = recommend_posts()

    return render_template(
        'recommendations.html',
        past_search_posts=recs.get("past_search_posts", []),
        new_posts=recs.get("new_posts", []),
        trending_posts=recs.get("trending_posts", [])
    )
