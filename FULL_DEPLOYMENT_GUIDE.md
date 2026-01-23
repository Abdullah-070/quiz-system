# Quiz System - Complete Deployment Guide

## Overview

Your app has **3 parts**:
1. **Backend (Django)** - API server
2. **Frontend (React)** - User interface
3. **Firebase** - Authentication & Hosting

## Current Status

✅ **Frontend**: Deployed on Firebase (https://quiz-system-78263.web.app)
✅ **Firebase Auth**: Google Sign-In & Password Reset configured
⏳ **Backend**: Ready to deploy (needs to be deployed to Render)

---

## Step 1: Initialize Git Repository

If you haven't already, set up Git:

```bash
cd e:\UNIVERSITY\Side Projects\Interview Quiz
git init
git config user.email "your-email@example.com"
git config user.name "Your Name"
git add .
git commit -m "Initial commit - ready for deployment"
```

## Step 2: Create GitHub Account & Push Code

1. Go to https://github.com/signup
2. Create account & verify email
3. Create a new repository (call it `interview-quiz`)
4. In your project folder:

```bash
git remote add origin https://github.com/YOUR_USERNAME/interview-quiz.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy Backend to Render

### Option A: Using Render Dashboard (Easy)

1. Go to https://render.com and sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your `interview-quiz` repo
5. Fill in details:
   - **Name**: quiz-system-backend
   - **Root Directory**: backend
   - **Runtime**: Python 3
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py migrate
     ```
   - **Start Command**: 
     ```
     gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
     ```

6. **Environment Variables** (Add these):
   ```
   DEBUG=False
   SECRET_KEY=[Let Render generate]
   ALLOWED_HOSTS=.onrender.com,quiz-system-78263.web.app
   FRONTEND_URL=https://quiz-system-78263.web.app
   ```

7. Click **Deploy**
8. Wait 5-10 minutes for deployment
9. Get your URL: `https://quiz-system-backend-xxxx.onrender.com`

### Option B: Using render.yaml (Automated)

Render will auto-detect `render.yaml` in your backend folder and use those settings automatically.

---

## Step 4: Update Frontend API URL

After backend is deployed, update the frontend:

**File**: `frontend/.env.production`

```env
REACT_APP_API_URL=https://quiz-system-backend-xxxx.onrender.com/api
```

(Replace `xxxx` with your actual Render URL)

---

## Step 5: Rebuild & Redeploy Frontend

```bash
cd frontend

# Update environment file
# Edit .env.production with your actual Render backend URL

# Build and deploy
npm run build
npx firebase deploy
```

---

## Testing

### Local Testing (Before Deployment)
```bash
# Terminal 1: Backend
cd backend
python manage.py runserver

# Terminal 2: Frontend
cd frontend
npm start

# Open http://localhost:3000
```

### Production Testing (After Deployment)
1. Visit https://quiz-system-78263.web.app
2. Test Sign Up → Should work with new backend
3. Test Google Sign-In → Should work
4. Test Forgot Password → Should work

---

## Troubleshooting

### "Connection Refused" Error
- ❌ **Problem**: Frontend can't reach backend
- ✅ **Solution**: Check `REACT_APP_API_URL` in `.env.production` matches your Render URL

### CORS Errors
- ✅ **Already fixed** in `backend/config/settings.py`
- Allows `quiz-system-78263.web.app` and `*.firebaseapp.com`

### Backend Not Connecting
- Go to Render Dashboard → Select your service
- Check **Logs** tab for errors
- Ensure all environment variables are set
- Try visiting your backend URL directly: `https://your-url.onrender.com/api/auth/current-user/`

### Database Issues on Render
- Render provides PostgreSQL automatically
- Migrations run during build (`python manage.py migrate`)
- If issues: SSH into service and run `python manage.py migrate --noinput`

---

## Important Notes

### Free Tier Limitations
- **Render**: Service goes to sleep after 15 min inactivity
  - Solution: Visit URL to wake it up, or upgrade to paid
- **Firebase**: Full features available on free tier ✅
- **Database**: Free PostgreSQL on Render ✅

### Performance
- First deployment: 5-10 minutes
- Subsequent builds: 2-3 minutes
- Cold start (after sleep): 30 seconds

### Monitoring
- **Backend**: Render Dashboard → Logs tab
- **Frontend**: Firebase Console → Hosting tab
- **Auth**: Firebase Console → Authentication tab

---

## What's Already Configured

✅ **Backend**:
- Django REST Framework
- JWT Authentication
- Google OAuth integration (Firebase)
- Password reset (Firebase)
- CORS headers (allows Firebase domain)
- Database ready (SQLite locally, PostgreSQL on Render)
- Static files handling (WhiteNoise)

✅ **Frontend**:
- React with React Router
- Ace Editor for code questions
- Google Sign-In button
- Password reset form
- Firebase authentication
- Quiz builder & solver
- Dashboard with statistics
- Leaderboard

✅ **Firebase**:
- Authentication (Email/Password, Google)
- Hosting (deployed)
- Password reset emails
- Custom domain ready

---

## Quick Reference: URLs After Deployment

| Service | URL |
|---------|-----|
| Frontend | https://quiz-system-78263.web.app |
| Backend API | https://quiz-system-backend-xxxx.onrender.com/api |
| Render Dashboard | https://render.com/dashboard |
| Firebase Console | https://console.firebase.google.com/project/quiz-system-78263 |
| Django Admin | https://quiz-system-backend-xxxx.onrender.com/admin |

---

## Next Steps (Optional Improvements)

1. **Custom Domain**
   - Firebase: buy domain, set up custom domain
   - Render: add CNAME record to DNS

2. **SSL Certificate**
   - ✅ Automatic on Firebase
   - ✅ Automatic on Render

3. **Email Service**
   - Currently: Console backend (logs to terminal)
   - Upgrade: SendGrid, Mailgun, Gmail SMTP

4. **Monitoring & Analytics**
   - Firebase: Built-in analytics
   - Render: New Relic, Sentry available

5. **Backup Strategy**
   - Database: Render automatic backups
   - Files: GitHub serves as backup

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Firebase Docs**: https://firebase.google.com/docs
- **Django REST Framework**: https://www.django-rest-framework.org/
- **React Docs**: https://react.dev

---

**Questions or issues? Check the logs!**
- **Backend errors**: Render Dashboard → Logs
- **Frontend errors**: Browser DevTools → Console
- **Auth errors**: Firebase Console → Authentication → Logs
