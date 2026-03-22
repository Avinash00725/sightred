# app/nlp_utils.py

from textblob import TextBlob

# Note: spaCy removed to reduce deployment size
# Core app functionality doesn't require NLP features

# Analyze sentiment using TextBlob
def analyze_sentiment(text):
    """Analyze sentiment of text using TextBlob"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "Neutral"

# Extract entities - simplified version without spaCy
def extract_entities(text):
    """
    Extract entities from text.
    Simplified version without spaCy to reduce deployment size.
    Returns empty list as placeholder.
    """
    # For now, returns empty list
    # Can be enhanced with regex-based entity extraction if needed
    return []

