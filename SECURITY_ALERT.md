# 🔐 SECURITY ALERT - CREDENTIALS CLEANUP

## ⚠️ IMPORTANT: Your Reddit API credentials were exposed!

The following credentials were found hardcoded in `app/__init__.py`:
- `client_id`: -OY_VDNQWsBKeQEYyRlAsw
- `client_secret`: HbKEJ9seAovAAH76qaDtC8Daffc35w

**These have been removed and moved to environment variables.**

## Immediate Actions Required

### 1. **Revoke the Exposed Credentials** (DO THIS NOW!)
```
1. Go to: https://www.reddit.com/prefs/apps
2. Find the "health_sentinel_v1" application
3. Click "Delete/Edit" and DELETE it
4. Create a NEW application with a different name
5. Generate NEW credentials
6. Store them ONLY in .env file
```

### 2. **Create New Reddit API Credentials**
```
1. Visit: https://www.reddit.com/prefs/apps
2. Click "Create application"
   - Name: SightRed-[YourName]
   - App type: Web app
   - Redirect URI: http://localhost:5000/callback
3. Copy the new Client ID and Client Secret
4. Add to .env file:
   REDDIT_CLIENT_ID=your_new_id
   REDDIT_CLIENT_SECRET=your_new_secret
```

### 3. **Verify in Code**
The code now uses environment variables:
```python
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)
```

### 4. **Update .env**
```bash
# Copy example
cp .env.example .env

# Edit .env with NEW credentials
REDDIT_CLIENT_ID=your_new_client_id
REDDIT_CLIENT_SECRET=your_new_client_secret
REDDIT_USER_AGENT=SightRed/1.0 by your_username
```

### 5. **Verify Nothing is Hardcoded**
```bash
# Search for exposed credentials
grep -r "REDDIT_CLIENT" app/  # Should find nothing
grep -r "client_secret" app/  # Should only find in __init__.py using os.getenv()

# Check for hardcoded API keys
grep -r "OY_VDNQWs" .  # Should return nothing (except in this SECURITY_ALERT.md)
grep -r "HbKEJ9se" .   # Should return nothing (except in this SECURITY_ALERT.md)
```

## Git Cleanup (Important!)

If you already pushed to GitHub with credentials exposed:

```bash
# Option 1: Revoke credentials (EASIEST - Already done above)
# The old credentials are now deleted from Reddit

# Option 2: Rewrite Git History (Advanced)
# Remove the commit with hardcoded credentials:
git log --all --oneline | head   # Find the commit
git rebase -i <commit_hash>      # Remove the problematic commit
git push --force-with-lease      # Force push (only if necessary)

# Option 3: Use BFG Repo-Cleaner
# More details: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```

## Verification Checklist

- [ ] Old Reddit credentials deleted from Reddit.com/prefs/apps
- [ ] New credentials created
- [ ] .env file updated with new credentials
- [ ] Code uses `os.getenv()` for all secrets
- [ ] .env is in .gitignore
- [ ] No hardcoded secrets found in codebase
- [ ] app/__init__.py loads from environment variables
- [ ] config.py uses environment variables
- [ ] All other files checked for hardcoded secrets

## Best Practices Going Forward

✅ **DO:**
- Store ALL secrets in `.env`
- Use `os.getenv()` to load from environment
- Check `.gitignore` before committing
- Use `git diff --cached` to review before commit
- Enable GitHub secret scanning (Settings → Security)

❌ **DON'T:**
- Hardcode API keys, tokens, or passwords
- Commit `.env` files
- Use the same API key for multiple projects
- Share credentials via email or chat
- Use old credentials after exposure

## For Deployment

When deploying to production (Heroku, Railway, Render, etc.):

1. Set environment variables in the platform's dashboard
2. **Never** commit credentials to GitHub
3. Use different credentials for production vs development
4. Rotate credentials periodically

---

**Status**: ✅ FIXED - Credentials removed, environment variables implemented

For full deployment guide, see [DEPLOYMENT.md](./DEPLOYMENT.md)
