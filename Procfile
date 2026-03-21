web: gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
release: python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
