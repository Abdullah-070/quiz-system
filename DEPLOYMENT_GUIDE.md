# Backend Deployment Guide - Render

## Quick Deployment Steps:

### 1. Push Code to Git (GitHub, GitLab, or Gitea)

```bash
cd e:\UNIVERSITY\Side Projects\Interview Quiz
git init
git add .
git commit -m "Prepare for Render deployment"
git remote add origin https://github.com/YOUR_USERNAME/interview-quiz.git
git branch -M main
git push -u origin main
```

### 2. Create Render Account
- Go to https://render.com
- Sign up with GitHub account

### 3. Deploy Backend

**Option A: Using render.yaml (Recommended)**
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml` and configure everything
5. Click Deploy

**Option B: Manual Setup**
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Select the `backend` folder in "Root Directory"
5. Set Environment:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
6. Add Environment Variables:
   ```
   DEBUG=False
   SECRET_KEY=[auto-generated]
   ALLOWED_HOSTS=.onrender.com,quiz-system-78263.web.app
   ```
7. Click Deploy

### 4. Wait for Deployment
- Check logs for any errors
- Once deployed, you'll get a URL like: `https://quiz-system-backend-xxxx.onrender.com`

### 5. Update Frontend API URL

In `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-render-url.onrender.com/api';
```

Or set in `.env`:
```
REACT_APP_API_URL=https://your-render-url.onrender.com/api
```

### 6. Rebuild and Deploy Frontend

```bash
cd frontend
npm run build
firebase deploy
```

---

## What Gets Deployed:
- ✅ Django backend with all dependencies
- ✅ Database (PostgreSQL on free tier)
- ✅ Static files (managed by WhiteNoise)
- ✅ All API endpoints

## Important Notes:
- **First deployment takes 5-10 minutes**
- **Free tier may go to sleep after 15 min of inactivity** - wake it up by visiting the URL
- **To wake from sleep**: Add a simple cron job or uptime monitor
- **Database persists** even if dyno sleeps

---

## Troubleshooting:

**Connection refused errors?**
- Check Render URL is correct in frontend API_BASE_URL
- Ensure CORS is configured: ✅ Already done

**Database migration errors?**
- SSH into Render: `render run python manage.py migrate --noinput`

**Static files not loading?**
- WhiteNoise handles this automatically ✅

---

## Alternative Services (if Render doesn't work):

1. **Railway.app** - Similar to Render, easy deployment
2. **PythonAnywhere** - Specialized for Python/Django
3. **Heroku** - More expensive but reliable (paid only now)
4. **Fly.io** - Good performance, generous free tier
