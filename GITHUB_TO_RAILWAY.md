# 🚀 Railway Deployment Guide (GitHub → Railway)

## Stage 1: Prepare Your GitHub Repository

### Step 1.1: Initialize Git (if not already done)

```bash
# Check if git is initialized
cd /home/avinash/Personal/projects/pythonLearnings/sightred
git status

# If not initialized, initialize git
git init
```

### Step 1.2: Verify .gitignore

Your `.gitignore` should exclude `.env` and database files:

```bash
cat .gitignore
```

Should contain:
```
.env
.env.local
*.db
*.sqlite
__pycache__/
venv/
```

✅ **Verify:** `.env` file should NOT be tracked
```bash
git status | grep -i ".env"  # Should show nothing
```

### Step 1.3: Create GitHub Repository

**Option A: Online (GitHub Website)**
```
1. Go to https://github.com/new
2. Repository name: sightred
3. Description: Reddit Post Recommender with ML
4. Select: Public (or Private if you prefer)
5. Skip "Initialize with README" (we'll commit locally)
6. Click "Create repository"
7. Copy the URL (like git@github.com:your-username/sightred.git)
```

**Option B: Using GitHub CLI**
```bash
# Install GitHub CLI if needed
# macOS: brew install gh
# Linux: sudo apt install gh
# Windows: choco install gh

# Login
gh auth login

# Create repo
gh repo create sightred --public --source=. --remote=origin --push
```

### Step 1.4: Add Remote and First Commit

```bash
# Add GitHub as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/sightred.git

# Verify remote is added
git remote -v
# Should show:
# origin  https://github.com/YOUR_USERNAME/sightred.git (fetch)
# origin  https://github.com/YOUR_USERNAME/sightred.git (push)
```

### Step 1.5: Commit All Files

```bash
# Stage all files (but .env is ignored)
git add .

# Check what will be committed (VERIFY NO .env!)
git status

# Commit
git commit -m "Initial commit: SightRed project ready for deployment"

# Verify files
git log --oneline -1  # Should show your commit
```

### Step 1.6: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main

# Verify on GitHub
# Visit: https://github.com/YOUR_USERNAME/sightred
```

✅ **Verify Your GitHub Repo:**
- All files are present
- `.env` file is NOT there
- `.env.example` IS there

---

## Stage 2: Deploy to Railway from GitHub

### Step 2.1: Create Railway Account

```
1. Go to https://railway.app
2. Click "Login"
3. Click "Sign up with GitHub"
4. Authorize railway.app to access your GitHub
5. Create account
```

### Step 2.2: Create New Railway Project

```
1. Dashboard → "New Project"
2. Select "Deploy from GitHub repo"
3. Search for "sightred"
4. Click to connect
5. Select branch: main
6. Click "Deploy"
```

Railway will start building automatically.

### Step 2.3: Add PostgreSQL Database

**In Railway Dashboard:**
```
1. Your Project → "Add Service" (+ button)
2. Search "PostgreSQL"
3. Click "PostgreSQL"
4. Railway creates database automatically
```

✅ **Database Status:**
- Railway automatically sets `DATABASE_URL` environment variable
- Your app will use PostgreSQL in production

### Step 2.4: Set Environment Variables

**In Railway Dashboard:**
```
1. Your Web Service → "Variables"
2. Add each variable:
```

| Variable | Value | Where to Get |
|----------|-------|--------------|
| `FLASK_ENV` | `production` | Set it |
| `SECRET_KEY` | Generate new (see below) | Run command |
| `REDDIT_CLIENT_ID` | Your Reddit app ID | https://reddit.com/prefs/apps |
| `REDDIT_CLIENT_SECRET` | Your Reddit app secret | https://reddit.com/prefs/apps |
| `REDDIT_USER_AGENT` | `SightRed/1.0 by your_username` | Your choice |

**Generate Strong SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and paste as `SECRET_KEY` in Railway.

### Step 2.5: Get Reddit API Credentials

If you don't have them yet:

```
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create another app"
3. Fill in:
   - name: SightRed
   - app type: Web app
   - redirect uri: https://your-railway-url.up.railway.app/callback
4. Get Client ID (shown under app name)
5. Get Client Secret (shown below Client ID)
```

⚠️ **Don't have Railway URL yet?** Use `http://localhost:5000/callback` for now, we'll update it later.

### Step 2.6: Database Initialization

After deployment, Railway needs to create tables:

```
1. Dashboard → Your Web Service → "Deployments"
2. Most recent deployment → "View Logs"
3. Look for any errors
```

**If tables aren't created automatically:**

```bash
# In Railway Dashboard → Terminal (if available)
# Or use this post-deployment command:
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Tables created!')"
```

---

## Stage 3: Verify Deployment

### Step 3.1: Get Your Railway URL

```
In Railway Dashboard:
1. Your Web Service → Overview
2. Look for "Domains" section
3. Your URL will be like: https://sightred-production-abc123.up.railway.app
```

### Step 3.2: Test Your App

```bash
# Visit in browser
https://your-railway-url.up.railway.app

# You should see the login page
```

### Step 3.3: Check Logs

```bash
# In Railway Dashboard
1. Deployments → Latest → View Logs
2. Should see:
   - Flask app starting
   - Connected to PostgreSQL
   - No error messages
```

### Step 3.4: Test Features

```
1. Register new account
2. Go to search page
3. Search for a subreddit and keyword
4. Check recommendations page
5. Check dashboard
```

✅ **All working?** Deployment successful!

---

## Stage 4: Quick Update Guide (Going Forward)

### Making Changes and Redeploying

```bash
# 1. Make your changes
nano app/routes.py  # example

# 2. Test locally
python main.py
# Visit http://localhost:5000

# 3. Commit and push
git add .
git commit -m "Add new feature X"
git push origin main

# 4. Watch Railway auto-deploy
# Dashboard → Deployments → Latest (should say "building")
```

**Railway auto-deploys on every push to main!**

---

## Troubleshooting

### ❌ App crashes immediately

```bash
# Check logs in Railway Dashboard
Deployments → Latest → View Logs

# Common issues:
1. Missing environment variable → Add it in Variables
2. Database not initialized → Run init commands
3. Python version mismatch → Check Railway Python version
```

### ❌ Can't connect to database

```bash
# Verify DATABASE_URL is set
1. Dashboard → Variables → Check DATABASE_URL exists
2. It should start with: postgresql://

# If still failing:
# Restart the service: Dashboard → "Reboot" button
```

### ❌ Login not working

```bash
# Check SECRET_KEY is set
1. Dashboard → Variables → Check SECRET_KEY exists
2. If not, add it: python -c "import secrets; print(secrets.token_urlsafe(32))"
3. Restart service
```

### ❌ Recommendations page blank

```bash
# Database tables might not exist
# Run in Railway Terminal (if available):
cd /app
python init_db.py

# Or create manually:
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## Optional: Update Reddit Redirect URI

After deployment, update your Reddit app settings:

```
1. Go to https://www.reddit.com/prefs/apps
2. Find your app
3. Edit to change redirect URI:
   - Update to: https://your-railway-url.up.railway.app/callback
   - Save
```

---

## Final Checklist

- [ ] GitHub repo created with all files
- [ ] `.env` NOT committed to GitHub
- [ ] `.env.example` IS in GitHub
- [ ] Railway project created
- [ ] PostgreSQL service added
- [ ] All environment variables set in Railway:
  - [ ] FLASK_ENV
  - [ ] SECRET_KEY
  - [ ] REDDIT_CLIENT_ID
  - [ ] REDDIT_CLIENT_SECRET
  - [ ] REDDIT_USER_AGENT
- [ ] App deployed successfully
- [ ] Can access your Railway URL
- [ ] Can login/register
- [ ] Can search and get recommendations
- [ ] Database is working (check logs)

---

## 🎉 You're Live!

Your app is now deployed on Railway and auto-updates whenever you push to GitHub!

**Next time you update:**
```bash
git add .
git commit -m "Your changes"
git push origin main
# Railway auto-deploys! ✨
```

---

## Need Help?

Check the logs:
```
Dashboard → Deployments → Latest → View Logs
```

Most issues show up in logs. If stuck:
1. Check environment variables are all set
2. Restart the service (Reboot button)
3. Check DATABASE_URL format is correct
4. Verify SECRET_KEY is generated properly

---

**Happy Deploying! 🚀**
