# 🚀 Deployment Guide for SightRed (Reddit Recommender)

## Table of Contents
1. [Before Deployment](#before-deployment)
2. [Environment Variables Setup](#environment-variables-setup)
3. [Database Management](#database-management)
4. [Deployment Options](#deployment-options)
5. [Post-Deployment](#post-deployment)

---

## Before Deployment

### ✅ Checklist
- [ ] All secrets are in `.env` file (NOT in code)
- [ ] `.gitignore` includes `.env` and `*.db`
- [ ] `requirements.txt` is up to date
- [ ] Reddit API credentials obtained
- [ ] Secret key is strong and unique
- [ ] Code is tested locally

---

## Environment Variables Setup

### 1. **Local Development Setup**

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:
```bash
# .env (LOCAL - NEVER COMMIT THIS!)
FLASK_ENV=development
SECRET_KEY=your_super_secret_key_here
DATABASE_URL=sqlite:///reddit_app.db

REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=SightRed/1.0 by your_username
```

### 2. **How to Get Reddit API Credentials**

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create application" or "Create another app"
3. Fill in the form:
   - **name**: SightRed
   - **app type**: Web app
   - **redirect uri**: `http://localhost:5000/callback` (for local)
   - **redirect uri**: `https://yourdomain.com/callback` (for production)
4. Copy the **client ID** and **client secret**
5. Store them in `.env`

### 3. **Generate a Strong Secret Key**

```python
# In Python terminal
import secrets
print(secrets.token_urlsafe(32))
```

Use this for your `SECRET_KEY` in production.

---

## Database Management

### **Important: SQLite vs PostgreSQL**

#### Development (SQLite)
```
DATABASE_URL=sqlite:///reddit_app.db
```
- File-based database
- Simple, no setup needed
- Not suitable for production

#### Production (PostgreSQL)
```
DATABASE_URL=postgresql://user:password@hostname:5432/dbname
```
- Robust, multi-user access
- Better for scaling
- Required for most cloud platforms

### **Creating/Migrating Database**

#### Option 1: Using Flask-Migrate (Recommended)
```bash
# Initialize migrations (one time)
flask db init

# Create migration for new schema changes
flask db migrate -m "Initial migration"

# Apply migrations to database
flask db upgrade
```

#### Option 2: Manual (Simpler for first deployment)
The `wsgi.py` file automatically creates tables:
```python
with app.app_context():
    db.create_all()  # Creates tables if they don't exist
```

### **Local Database Access**

View your local SQLite database:
```bash
# Using Python
python
>>> from app.models import User, Search
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
>>>     users = User.query.all()
>>>     searches = Search.query.all()
```

Or use DB viewer tools:
- **SQLite3 CLI**: `sqlite3 reddit_app.db`
- **DB Browser for SQLite**: GUI tool
- **DBeaver**: Universal database tool

---

## Deployment Options

### **Option 1: Heroku (Easiest for Beginners)**

#### Step 1: Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Login to Heroku
```bash
heroku login
```

#### Step 3: Create Heroku App
```bash
heroku create your-app-name
```

#### Step 4: Add Database
```bash
# Free database option (limited)
heroku addons:create heroku-postgresql:hobby-dev
```

#### Step 5: Set Environment Variables
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your_generated_secret_key
heroku config:set REDDIT_CLIENT_ID=your_client_id
heroku config:set REDDIT_CLIENT_SECRET=your_client_secret
heroku config:set REDDIT_USER_AGENT="SightRed/1.0 by your_username"
```

Verify:
```bash
heroku config
```

#### Step 6: Deploy
```bash
git push heroku main  # or master
```

#### Step 7: Run Database Migrations
```bash
heroku run python wsgi.py
```

#### Step 8: Check Logs
```bash
heroku logs --tail
```

#### Step 9: Open App
```bash
heroku open
```

---

### **Option 2: Railway.app (Modern & Simple)**

#### Step 1: Create Account
Go to https://railway.app and sign up with GitHub

#### Step 2: Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Select your GitHub repository

#### Step 3: Add PostgreSQL Database
- Click "Add Service" → "PostgreSQL"
- Railway automatically sets `DATABASE_URL`

#### Step 4: Set Environment Variables
In Railway dashboard → Variables:
```
FLASK_ENV=production
SECRET_KEY=your_secret_key
REDDIT_CLIENT_ID=xxx
REDDIT_CLIENT_SECRET=xxx
REDDIT_USER_AGENT=SightRed/1.0 by your_username
```

#### Step 5: Deploy
- Railways auto-deploys on GitHub push
- Or manually deploy in dashboard

#### Step 6: Check Logs
Dashboard → Deployments → View logs

---

### **Option 3: Render.com**

#### Step 1: Create Account
Go to https://render.com and sign up

#### Step 2: Connect GitHub Repository
- New → Web Service
- Select your GitHub repo
- Select branch (main/master)

#### Step 3: Configure Service
- **Name**: sightred
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app`

#### Step 4: Add Database
- New → PostgreSQL
- Note the internal database URL

#### Step 5: Set Environment Variables
- In Web Service settings → Environment
```
FLASK_ENV=production
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://...  (from PostgreSQL service)
REDDIT_CLIENT_ID=xxx
REDDIT_CLIENT_SECRET=xxx
REDDIT_USER_AGENT=SightRed/1.0 by your_username
```

#### Step 6: Deploy
- Click "Create Web Service"
- Render auto-deploys

---

### **Option 4: Self-Hosted (AWS, DigitalOcean, VPS)**

#### Using Docker (Recommended)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/sightred
      - SECRET_KEY=${SECRET_KEY}
      - REDDIT_CLIENT_ID=${REDDIT_CLIENT_ID}
      - REDDIT_CLIENT_SECRET=${REDDIT_CLIENT_SECRET}
      - REDDIT_USER_AGENT=SightRed/1.0 by your_username
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=secure_password
      - POSTGRES_DB=sightred
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Deploy:
```bash
docker-compose up -d
```

---

## Post-Deployment

### **1. Verify Database is Created**

#### Heroku
```bash
heroku pg:info
heroku pg:psql  # Access database
```

#### Railway/Render
- Check in dashboard → Database section

### **2. Test the App**

```bash
# Visit your deployed URL
https://your-app-name.herokuapp.com

# Or if using custom domain
https://yourdomain.com
```

### **3. View Logs**

#### Heroku
```bash
heroku logs --tail
```

#### Railway
Dashboard → Deployments → View Logs

#### Render
Dashboard → Web Service → Logs

### **4. Access Database in Production**

#### Heroku PostgreSQL
```bash
heroku pg:psql
```

#### Railway/Render
- Use their web dashboard GUI
- Or use database connection string with local tools:
```bash
psql postgresql://user:password@hostname/dbname
```

### **5. Backup Database (Important!)**

#### Heroku
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

#### Railway/Render
- Manual backups in dashboard
- Or use `pg_dump`:
```bash
pg_dump your_database_url > backup.sql
```

---

## ⚠️ Security Best Practices

### **DO ✅**
- [x] Use `.env` for ALL secrets
- [x] Add `.env` to `.gitignore`
- [x] Use strong SECRET_KEY (32+ characters)
- [x] Use PostgreSQL in production (not SQLite)
- [x] Enable HTTPS on your domain
- [x] Rotate API credentials regularly
- [x] Use environment variables for all sensitive data

### **DON'T ❌**
- [ ] Never commit `.env` file
- [ ] Never hardcode secrets in code
- [ ] Never use weak secret keys
- [ ] Never use SQLite for production
- [ ] Never expose database credentials
- [ ] Never display error messages with secrets
- [ ] Never use default Reddit API credentials

---

## Troubleshooting

### **App Crashes on Deployment**

**Check logs:**
```bash
# Heroku
heroku logs --tail

# Railway
Dashboard → Logs

# Render
Dashboard → Web Service → Logs
```

**Common Issues:**
1. **ModuleNotFoundError**: Missing package in `requirements.txt`
   - Add to `requirements.txt` and redeploy

2. **DATABASE_URL not set**
   - Verify environment variables are set correctly

3. **Reddit API credentials invalid**
   - Double-check credentials in `.env`

4. **Port binding error**: Change to port 5000 in config

### **Database Issues**

1. **Tables not created**
   - Run: `heroku run python -c "from wsgi import app; from app import db; app.app_context().push(); db.create_all()"`

2. **Can't connect to database**
   - Verify `DATABASE_URL` is correct
   - Check PostgreSQL is running

3. **Migrations failed**
   - Run: `heroku run flask db upgrade`

---

## Quick Reference Commands

```bash
# Local testing
python main.py

# Create database locally
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Heroku deployment
git push heroku main
heroku logs --tail
heroku config
heroku pg:reset DATABASE_URL  # Warning: Deletes all data!

# Railway/Render
git push origin main  # Auto-deploys
```

---

## Next Steps

1. ✅ Setup local environment variables
2. ✅ Verify app works locally
3. ✅ Choose a hosting platform
4. ✅ Deploy following the platform guide
5. ✅ Test all features on live app
6. ✅ Setup monitoring and alerts
7. ✅ Configure custom domain (optional)
8. ✅ Setup regular backups

---

**Happy Deploying! 🚀**
