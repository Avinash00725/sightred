# Keyword-Based Reddit Recommendation System

## 📘 Project Overview

This project is a personalized recommendation system built using **Flask**, **PRAW** (Python Reddit API Wrapper), **scikit-learn**, and **spaCy**. It enables users to:

- Search for keywords or topics of interest.
- Receive recommended keywords based on their search history.
- View the latest Reddit posts related to their queries.

## ⚙️ How It Works

1. **User Search**:
   - Users input a keyword, which is stored in a database for tracking search history.

2. **Recommendation Engine**:
   - Utilizes **TF-IDF vectorization** and **cosine similarity** to suggest keywords similar to the user's recent searches.

3. **Reddit Integration**:
   - Leverages the **PRAW API** to scrape and display the latest Reddit posts based on user queries and recommended keywords.

4. **Sentiment & Entity Analysis**:
   - Employs **spaCy** for extracting named entities from post titles.
   - Optionally uses **textblob** or **spaCy** for basic sentiment analysis of posts.

## 🚀 Usage

To run the project locally:
1. Clone the repository: `git clone <repository-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure Reddit API credentials in a `.env` file.
4. Run the Flask app: `python main.py`
5. Access the app at `http://localhost:5000`.
