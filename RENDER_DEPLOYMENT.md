# 🚀 Render Deployment Guide (GitHub → Render)

## Why Render? (vs Railway)

| Feature | Render | Railway |
|---------|--------|---------|
| Python Support | ✅ Perfect | ✅ Perfect |
| Free PostgreSQL | ✅ Yes (free tier) | ⚠️ Paid |
| Setup Time | ⚡ 10 min | ⚡ 5 min |
| Cold starts | ❌ Have free tier | ✅ None |
| Cost | 💰 Free tier generous | 💰 Slightly cheaper |
| Reliability | ✅ Excellent | ✅ Excellent |

**Render is great!** Slightly slower free tier, but free PostgreSQL!

---

## Stage 1: Verify GitHub is Ready

Your GitHub repo should have all files. Check:

```bash
# Verify your repo
ls -la
# Should show:
# ✅ wsgi.py
# ✅ Procfile
# ✅ requirements.txt
# ✅ runtime.txt
# ✅ app/ folder
# ❌ .env (NOT there)
# ✅ .env.example (there)
```

---

## Stage 2: Create Render Account

### Step 2.1: Sign Up

```
1. Go to https://render.com
2. Click "Get Started"
3. Click "Sign up with GitHub"
4. Authorize render.com
5. Create account
```

### Step 2.2: Connect GitHub

```
1. Dashboard → "GPU/CPU/Disk" selector (top)
2. Select your account
3. Go to "GitHub integration" tab
4. Click "Connect GitHub repository"
5. Search for "sightred"
6. Click to connect
```

---

## Stage 3: Create Web Service

### Step 3.1: Create New Web Service

```
1. Dashboard → "New +"
2. Select "Web Service"
3. Select your GitHub repo "sightred"
4. Click "Connect"
```

### Step 3.2: Configure Web Service

Fill in these fields:

```
Name: sightred
Region: Choose closest (US East, EU West, etc)
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
```

### Step 3.3: Create Service

```
Plan: Free (we'll add paid PostgreSQL if needed)
Click "Create Web Service"
```

Render will now **start building automatically**!

---

## Stage 4: Add PostgreSQL Database

### Step 4.1: Create PostgreSQL Instance

```
1. Dashboard → "New +"
2. Select "PostgreSQL"
3. Select "Free" plan
4. Name: sightred-db
5. Click "Create Database"
```

Render creates the database (takes 1-2 minutes).

### Step 4.2: Note Connection Details

When PostgreSQL is created, Render shows:
```
Host: your-db-host.render.com
Port: 5432
Database: sightred_db
User: your_user
Password: your_password
```

**Save these!** (You'll see them in dashboard)

---

## Stage 5: Connect Web Service to Database

### Step 5.1: Get Database Internal URL

```
1. Go to your PostgreSQL service
2. Copy "Internal Database URL"
3. It looks like: 
   postgresql://user:password@hostname:5432/dbname
```

### Step 5.2: Add to Web Service

```
1. Go to Web Service (sightred)
2. Click "Environment" (left menu)
3. Add new environment variable:
   Name: DATABASE_URL
   Value: postgresql://user:password@hostname:5432/dbname
4. Click "Save"
```

---

## Stage 6: Set Environment Variables

In your Web Service → Environment, add all variables:

| Name | Value | Notes |
|------|-------|-------|
| `FLASK_ENV` | `production` | Set it |
| `SECRET_KEY` | Generate new | See below |
| `DATABASE_URL` | From PostgreSQL | Already added above |
| `REDDIT_CLIENT_ID` | Your Reddit ID | From reddit.com/prefs/apps |
| `REDDIT_CLIENT_SECRET` | Your Reddit secret | From reddit.com/prefs/apps |
| `REDDIT_USER_AGENT` | `SightRed/1.0 by your_username` | Your choice |

### Generate SECRET_KEY

```bash
# In your terminal
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and paste as `SECRET_KEY` in Render.

### Get Reddit Credentials

```
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create another app"
3. Fill form:
   - name: SightRed
   - app type: Web app
   - redirect uri: https://your-render-url.onrender.com/callback
4. Copy Client ID and Client Secret
5. Add to Render environment
```

⚠️ **Don't have Render URL yet?** Use `http://localhost:5000/callback` for now, update later.

---

## Stage 7: Monitor Deployment

### Step 7.1: Check Build Status

```
1. Web Service → "Logs" tab
2. Watch for messages like:
   - "Build started"
   - "Installing dependencies"
   - "Building application"
   - "Build completed successfully"
```

### Step 7.2: Troubleshoot if Build Fails

**Common issues:**

1. **Missing dependencies**
   ```
   Error: ModuleNotFoundError: No module named 'xxx'
   Fix: Add to requirements.txt and redeploy
   ```

2. **Python version wrong**
   ```
   Error: Python 3.13 not compatible
   Fix: Already fixed in runtime.txt (Python 3.10)
   ```

3. **Gunicorn failed to start**
   ```
   Error: failed to bind port
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
   ```

---

## Stage 8: Initialize Database

### Step 8.1: Get Your Render URL

```
Web Service → "Settings" → "Render URL"
Example: https://sightred-abc123.onrender.com
```

### Step 8.2: Initialize Tables

Method 1: **Visit health endpoint** (auto-creates tables)
```bash
# In browser, visit:
https://sightred-abc123.onrender.com/
# This triggers wsgi.py which creates tables
```

Method 2: **Manual initialization** (if needed)
```bash
# In Render Shell (if available):
cd /app
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### Step 8.3: Verify Database

```
1. PostgreSQL service → "Connect" tab
2. Copy connection string
3. Connect from your computer:
   psql postgresql://user:password@hostname:5432/dbname
   
   Then check:
   \dt  # Show tables
   SELECT * FROM users;  # Should be empty
```

---

## Stage 9: Test Your App

### Step 9.1: Visit Your App

```
Browser → https://your-render-url.onrender.com
Should see: Login page ✅
```

### Step 9.2: Test Features

```
1. Register new account
2. Go to home page
3. Search for a subreddit (e.g., Python)
4. Search for a keyword (e.g., tutorial)
5. Click "Recommendations"
6. Go to "Dashboard"
```

**All working?** ✅ Deployment successful!

---

## Stage 10: Update Reddit Redirect URI

After deployment, update your Reddit app:

```
1. Go to https://www.reddit.com/prefs/apps
2. Find your app
3. Edit → Change redirect uri:
   Old: http://localhost:5000/callback
   New: https://your-render-url.onrender.com/callback
4. Save
```

---

## Going Forward: Auto-Redeployment

Every time you push to GitHub, Render automatically redeploys:

```bash
# Make changes
nano app/routes.py

# Test locally
python main.py

# Commit and push
git add .
git commit -m "Add new feature"
git push origin main

# Render auto-deploys! (watch Logs tab)
```

---

## Troubleshooting

### ❌ App won't start

```
Check Logs:
1. Web Service → Logs
2. Look for:
   ❌ ModuleNotFoundError
   ❌ ImportError
   ❌ SyntaxError
   ❌ Missing environment variable
```

### ❌ Can't connect to database

```
Check DATABASE_URL:
1. Environment tab
2. Verify DATABASE_URL is set
3. Must start with: postgresql://
4. No typos in password

If still failing:
1. Restart Web Service (click "Restart")
2. Check PostgreSQL service is running
3. Verify connection string in psql locally
```

### ❌ Login fails

```
Check SECRET_KEY:
1. Environment tab
2. Verify SECRET_KEY is set (not empty)
3. Restart Web Service
```

### ❌ Recommendations page blank

```
Check database was initialized:
1. Visit app URL (triggers wsgi.py)
2. Check PostgreSQL → Connect → run:
   SELECT * FROM "user";
   SELECT * FROM searches;
3. If empty, tables might exist but no data

OR run init manually:
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### ❌ Build fails with Python 3.13

```
Fix: runtime.txt should have:
    python-3.10.13

If wrong, edit and push:
git add runtime.txt
git commit -m "Fix Python version"
git push origin main
Render auto-rebuilds
```

---

## Performance Tips

### Free Tier (Spin Down)
- Services sleep after 15 minutes of inactivity
- First request after sleep takes 30 seconds
- **Upgrade to "Starter" plan** to avoid this

### Production (Recommended)
- Use "Starter" plan ($7/month)
- No spin-down delays
- Better performance
- Free PostgreSQL still included

---

## Monitoring & Logs

### View Real-time Logs
```
Web Service → Logs → "Tail logs" button
See in real-time as users visit
```

### Check Deployments
```
Web Service → Deployments
See history of all deployments
Click any deployment → View logs
```

### Restart Service
```
Web Service → "Restart" button
Useful if something goes wrong
```

---

## Database Backups

### Manual Backup
```
PostgreSQL → "Connect" → Copy connection string

Use pgAdmin or local psql:
pg_dump postgresql://user:pass@host:5432/db > backup.sql

Upload backup somewhere safe (Google Drive, etc)
```

---

## Final Checklist

- [ ] GitHub repo has all files (wsgi.py, Procfile, requirements.txt, runtime.txt)
- [ ] Web Service created with correct build/start commands
- [ ] PostgreSQL database created
- [ ] DATABASE_URL environment variable set
- [ ] FLASK_ENV = production
- [ ] SECRET_KEY generated and set
- [ ] Reddit credentials set (CLIENT_ID, CLIENT_SECRET, USER_AGENT)
- [ ] Database tables initialized
- [ ] Can visit web app URL
- [ ] Can register/login
- [ ] Can search subreddits
- [ ] Recommendations work
- [ ] Dashboard works

---

## Comparison: Railway vs Render

| Aspect | Railway | Render |
|--------|---------|--------|
| Setup | ⚡ 5 min | ⚡ 10 min |
| Free tier | Limited | Better (includes free DB) |
| Cold starts | ✅ None | ❌ Free tier has 30s |
| Cost | Slightly cheaper | Slightly more |
| Support | Good docs | Excellent docs |
| **Best For** | **Quick start** | **Budget conscious** |

**Both are great! Render is better if you want free PostgreSQL.**

---

## Need Help?

### Render Documentation
- https://render.com/docs
- Community: https://render.com/discussions

### Common Commands
```bash
# View live logs
# (Use Render dashboard Logs tab)

# Trigger rebuild
git push origin main

# Check environment
# (Use Render dashboard Environment tab)
```

---

## 🎉 You're Ready!

You can now deploy on **Render instead of Railway!**

**Which platform?**
- **Railway** = Faster, prettier, slightly paid
- **Render** = Free PostgreSQL, budget-friendly

Both work great! Pick whichever you prefer! 🚀
