# 🚀 Railway Deployment Quick Guide

## The Error You Got

```
mise ERROR Failed to install core:python@3.13.12: Python installation is missing a `lib` directory
```

**Solution:** Railway's automatic Python detection failed. The `runtime.txt` file we added fixes this.

---

## ✅ What We Fixed

Added `runtime.txt` with:
```
python-3.10.13
```

This tells Railway exactly which Python version to use (compatible with your app).

---

## 🚀 Next Steps

### Step 1: **Railway Will Auto-Redeploy**

Since we pushed the `runtime.txt` fix, Railway will automatically rebuild:
- Go to Railway Dashboard
- Your Project → Deployments
- Wait for the new deployment to complete (you'll see "building" → "success")

### Step 2: **Check the Logs**

```
Deployments → Latest → View Logs

Look for:
✅ Python 3.10.13 installed
✅ Dependencies installed  
✅ Gunicorn started
✅ Database connected
```

### Step 3: **If Still Issues**

Common next fixes:
1. **DATABASE not set**: Add `DATABASE_URL` in Variables (Railway auto-sets this for PostgreSQL)
2. **SECRET_KEY missing**: Add in Variables (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
3. **App won't start**: Check logs for specific error

---

## 📋 Environment Variables to Set in Railway

Go to: **Project → Web Service → Variables**

| Name | Value |
|------|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Generate one (see Step 3) |
| `REDDIT_CLIENT_ID` | Your Reddit app ID |
| `REDDIT_CLIENT_SECRET` | Your Reddit app secret |
| `REDDIT_USER_AGENT` | `SightRed/1.0 by your_username` |

⚠️ **Don't set `DATABASE_URL`** - Railway automatically sets it when you add PostgreSQL service!

---

## 🔧 If Deploy Still Fails

**Option 1: Check Error in Logs**
```
Dashboard → Deployments → Latest → View Logs
Copy the error and Google it
```

**Option 2: Restart Service**
```
Project → Web Service → Reboot
Try deploying again
```

**Option 3: Check Python Version Compatibility**
- Your app was built with Python 3.10
- Railway's `runtime.txt` now specifies Python 3.10.13
- Should work perfectly

---

## ✅ Expected Success Message

When deployment completes, you'll see in logs:
```
[2024-03-21] Starting gunicorn
[2024-03-21] Listening on port 5000
[2024-03-21] Connection to PostgreSQL established
```

Then visit your Railway URL and test!

---

## 📞 Still Stuck?

Check these files for full deployment guides:
- **DEPLOYMENT.md** - Complete deployment guide (all platforms)
- **GITHUB_TO_RAILWAY.md** - Detailed Railway walkthrough

---

**The runtime.txt fix is usually all that's needed! 🎉**
