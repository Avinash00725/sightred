# app/nlp_utils.py
# Pure Python NLP utilities without external dependencies

def analyze_sentiment(text):
    """
    Analyze sentiment of text using simple keyword-based approach.
    Returns: "Positive", "Negative", or "Neutral"
    """
    try:
        text_lower = text.lower()
        
        # Simple positive keywords
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'awesome', 'wonderful',
            'love', 'like', 'best', 'perfect', 'beautiful', 'fantastic',
            'nice', 'happy', 'glad', 'good', 'brilliant'
        }
        
        # Simple negative keywords
        negative_words = {
            'bad', 'terrible', 'awful', 'hate', 'dislike', 'worst',
            'ugly', 'poor', 'sad', 'angry', 'horrible', 'disgusting',
            'stupid', 'dumb', 'sucks', 'useless', 'waste'
        }
        
        words = text_lower.split()
        positive_count = sum(1 for w in words if w in positive_words)
        negative_count = sum(1 for w in words if w in negative_words)
        
        if positive_count > negative_count:
            return "Positive"
        elif negative_count > positive_count:
            return "Negative"
        else:
            return "Neutral"
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "Neutral"


def extract_entities(text):
    """
    Extract entities from text using simple pattern matching.
    Returns: List of potential entity candidates
    Simplified version without external NLP libraries.
    """
    try:
        # Simple extraction - just return capitalized words as entities
        words = text.split()
        entities = [
            w.strip('.,!?;:') for w in words 
            if w and w[0].isupper() and len(w) > 1
        ]
        return list(set(entities))  # Remove duplicates
    except Exception as e:
        print(f"Error in entity extraction: {e}")
        return []


