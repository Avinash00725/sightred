# 🚀 Deployment Quick Reference

## Step 1: Setup Local Environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your values
nano .env  # or edit in your editor

# Should contain:
# FLASK_ENV=production
# SECRET_KEY=<your_generated_secret_key>
# DATABASE_URL=sqlite:///reddit_app.db (or PostgreSQL for production)
# REDDIT_CLIENT_ID=<your_new_id>
# REDDIT_CLIENT_SECRET=<your_new_secret>
# REDDIT_USER_AGENT=SightRed/1.0 by your_username
```

## Step 2: Initialize Database

```bash
# Option A: Python (Works on Windows/Mac/Linux)
python init_db.py

# Option B: Bash (Mac/Linux only)
bash init_db.sh

# Verify
python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
>>>     print(db.engine.table_names())  # Should show ['users', 'searches']
```

## Step 3: Test Locally

```bash
python main.py
# Visit http://localhost:5000
```

## Step 4: Choose Your Hosting

### 🟪 **Heroku** (Easiest)
```bash
# Install Heroku CLI, then:
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=<your_secret>
heroku config:set REDDIT_CLIENT_ID=<your_id>
heroku config:set REDDIT_CLIENT_SECRET=<your_secret>
heroku config:set REDDIT_USER_AGENT=SightRed/1.0
git push heroku main
heroku logs --tail
heroku open
```

### 🟦 **Railway** (Modern)
```bash
# 1. Go to railway.app
# 2. Connect GitHub repo
# 3. Add PostgreSQL service
# 4. Set environment variables in dashboard
# 5. Auto-deploys on git push
```

### 🟩 **Render** (Free option)
```bash
# 1. Go to render.com
# 2. New → Web Service
# 3. Connect GitHub repo
# 4. Set build/start commands:
#    Build: pip install -r requirements.txt
#    Start: gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
# 5. Add PostgreSQL service
# 6. Set environment variables
```

## Step 5: Verify Deployment

```bash
# Test the live app
curl https://your-app-name.herokuapp.com

# Check logs
heroku logs --tail  # Heroku
# Dashboard → Logs  # Railway/Render

# Check database
heroku pg:psql     # Heroku PostgreSQL
psql <connection_string>  # Local PostgreSQL client
```

## Step 6: Monitor

```bash
# Heroku monitoring
heroku metrics
heroku logs --tail

# Set up alerts (check platform documentation)
```

---

## 🔄 Updating Your App

```bash
# Make changes locally
git add .
git commit -m "Your changes"

# Deploy (auto-deploys on git push)
git push heroku main        # Heroku
git push origin main        # Railway (auto)
git push origin main        # Render (auto)
```

---

## 🗄️ Database Management

### View Data
```bash
# Heroku PostgreSQL
heroku pg:psql
sightred=# SELECT * FROM users;

# Local SQLite
sqlite3 reddit_app.db
sqlite> SELECT * FROM users;
```

### Backup Database
```bash
# Heroku
heroku pg:backups:capture
heroku pg:backups:download

# PostgreSQL
pg_dump postgresql://user:pass@host:5432/db > backup.sql
```

### Reset Database
```bash
# ⚠️ WARNING: Deletes all data!
heroku pg:reset DATABASE_URL
heroku run python -c "from wsgi import app; from app import db; app.app_context().push(); db.create_all()"
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| App won't start | Check logs: `heroku logs --tail` |
| Database not created | Run: `heroku run python init_db.py` |
| Invalid credentials | Verify `.env` vars: `heroku config` |
| Port binding error | Check Procfile has correct port |
| Can't connect to DB | Verify DATABASE_URL is set correctly |

---

## 📋 Environment Variables (Checklist)

Before deployment, verify all are set:

```bash
# For development
echo $FLASK_ENV                # should be "development"
echo $SECRET_KEY              # should not be empty
echo $DATABASE_URL            # should be sqlite:///reddit_app.db or postgresql://...
echo $REDDIT_CLIENT_ID        # should not be empty
echo $REDDIT_CLIENT_SECRET    # should not be empty
echo $REDDIT_USER_AGENT       # should be SightRed/1.0 by your_username

# For production (via platform dashboard)
# All same vars, but SECRET_KEY should be long random string
```

---

## ⚠️ Security Checklist

- [ ] .env NOT committed to git
- [ ] .env in .gitignore
- [ ] No hardcoded secrets in code
- [ ] Reddit credentials revoked if exposed
- [ ] NEW Reddit credentials created
- [ ] Strong SECRET_KEY generated
- [ ] Production uses PostgreSQL (not SQLite)
- [ ] HTTPS enabled (automatic on most platforms)

---

## 💾 First-time Files

Files you need for deployment:
- ✅ `Procfile` - Server configuration
- ✅ `wsgi.py` - Entry point for production
- ✅ `.env.example` - Environment variables template
- ✅ `requirements.txt` - Dependencies
- ✅ `.gitignore` - Ignore .env and secrets
- ✅ `DEPLOYMENT.md` - Full guide (this file)

---

## 📞 Support

### Heroku Issues?
```bash
heroku help
heroku status
heroku ps  # Check if app is running
```

### PostgreSQL Issues?
```bash
# Test connection
psql postgresql://user:password@host:5432/dbname

# Check usage
heroku pg:info
```

### Need to rollback deployment?
```bash
# Heroku
git revert <commit_hash>
git push heroku main
```

---

**Your app is ready to deploy! 🚀**

Full guide: [DEPLOYMENT.md](./DEPLOYMENT.md)

Security info: [SECURITY_ALERT.md](./SECURITY_ALERT.md)
