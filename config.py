import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Use environment variable for secret key in production
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')

    # SQLite for development; can be overridden in production
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'reddit_app.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
