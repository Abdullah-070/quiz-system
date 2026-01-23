# Render Deployment Form - Copy These Exact Values

## Quick Reference - Copy & Paste

### Repository Connection
```
Repository:   Abdullah-070/quiz-system
Branch:       main
```

### Service Configuration

#### Basic Settings
```
Service Name:             quiz-system-backend
Environment:              Python 3
Region:                   (Any - e.g., Oregon)
Root Directory:           backend
```

#### Build and Start Commands
```
Build Command:
pip install -r requirements.txt && python manage.py migrate

Start Command:
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

### Environment Variables (Add these)

**Add Variable 1:**
```
Key:   DEBUG
Value: False
```

**Add Variable 2:**
```
Key:   SECRET_KEY
Value: elc2t@v7**09*zyeibknrh_$d8dl^lc@%*j7h)u7y1(*2$o6vs
```

**Add Variable 3:**
```
Key:   ALLOWED_HOSTS
Value: .onrender.com,quiz-system-78263.web.app
```

**Add Variable 4:**
```
Key:   FRONTEND_URL
Value: https://quiz-system-78263.web.app
```

### Optional: Database Setup

On the same form, you can add a free PostgreSQL database:

```
✓ Add PostgreSQL Database

Database Name: quiz-db
Plan: Free
```

Render will automatically set `DATABASE_URL` environment variable.

---

## Step-by-Step Screenshots Guide

### 1. Create Web Service
- Click "New +" (top right)
- Select "Web Service"

### 2. Connect Repository
- Click "Connect a repository"
- Search for: `quiz-system`
- Click `Abdullah-070/quiz-system`
- Click "Connect"

### 3. Fill Service Settings
```
Name:                    quiz-system-backend
Environment:             Python 3
Region:                  Oregon (or any)
Branch:                  main
Root Directory:          backend
Build Command:           pip install -r requirements.txt && python manage.py migrate
Start Command:           gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

### 4. Add Environment Variables
- Click "Add Environment Variable"
- Add 4 variables (see above)

### 5. Deploy
- Scroll down, click "Create Web Service"
- Wait for build (5-10 minutes)
- Check "Logs" tab to see progress
- When done: Status shows "Live" ✅

---

## What to Expect During Deployment

```
Building...        [████░░░░░░] 30%   (2-3 min)
Deploying...       [████████░░] 60%   (3-5 min)
Initializing...    [██████████] 100%  
✓ Live             Status: Active ✅   (Total: 5-10 min)
```

---

## After Deployment

You'll see a green "Live" status and a URL like:
```
https://quiz-system-backend-xxxx.onrender.com
```

Where `xxxx` is a random ID.

### Copy this URL!
You need it for the next step.

---

## Test Your Backend

Visit this URL in browser:
```
https://quiz-system-backend-xxxx.onrender.com/api/questions/?page=1
```

Should return JSON with questions. ✅

---

## If Deployment Fails

Check the **Logs** tab:
- Look for red error messages
- Common fixes:
  - Ensure `backend/requirements.txt` exists
  - Ensure `render.yaml` is in backend folder
  - Check build command syntax
  - Verify environment variables

---

## Auto-Deployments

Every time you push to GitHub:
```
git push origin main
```

Render automatically:
1. Detects the change
2. Rebuilds the application
3. Deploys new version
4. Takes 2-3 minutes

**No manual deploys needed!**

---

## Dashboard Links

- **Render Dashboard**: https://render.com/dashboard
- **Your Service**: https://dashboard.render.com (after deployment)
- **GitHub Repo**: https://github.com/Abdullah-070/quiz-system

---

**Ready? Go to https://render.com and deploy!** 🚀
