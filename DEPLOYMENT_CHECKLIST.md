# Quiz System - Backend Deployment Checklist

## Pre-Deployment ✅

- [x] Backend dependencies in `requirements.txt`
- [x] Production settings in `config/settings.py`
- [x] `render.yaml` created for auto-deployment
- [x] CORS configured for Firebase domain
- [x] Database migration ready
- [x] Static files configuration (WhiteNoise)
- [x] Environment variables documented

## GitHub Setup 📦

- [ ] Create GitHub account (https://github.com/signup)
- [ ] Create new repository named `interview-quiz`
- [ ] Push code to GitHub
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git remote add origin https://github.com/YOUR_USERNAME/interview-quiz.git
  git push -u origin main
  ```

## Render Deployment 🚀

### Account Setup
- [ ] Create Render account at https://render.com
- [ ] Sign up with GitHub

### Web Service Creation
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Select branch: `main`
- [ ] Set Root Directory: `backend`
- [ ] Runtime: `Python 3`
- [ ] Build Command: `pip install -r requirements.txt && python manage.py migrate`
- [ ] Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

### Environment Variables
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY=` (let Render auto-generate)
- [ ] `ALLOWED_HOSTS=.onrender.com,quiz-system-78263.web.app`
- [ ] `FRONTEND_URL=https://quiz-system-78263.web.app`

### Deploy
- [ ] Click "Deploy" button
- [ ] Wait 5-10 minutes
- [ ] Check Render dashboard for URL
- [ ] Copy URL (e.g., `https://quiz-system-backend-xxxx.onrender.com`)

## Frontend Update 🔄

- [ ] Note your Render backend URL
- [ ] Edit `frontend/.env.production`
- [ ] Update: `REACT_APP_API_URL=https://your-render-url.onrender.com/api`
- [ ] Run `npm run build`
- [ ] Run `npx firebase deploy`

## Testing ✅

### Local Testing (Before Deployment)
- [ ] Backend runs: `python manage.py runserver`
- [ ] Frontend runs: `npm start`
- [ ] Sign up works
- [ ] Google sign-in works
- [ ] Password reset works
- [ ] Quiz creation works
- [ ] Quiz solving works

### Production Testing (After Deployment)
- [ ] Visit https://quiz-system-78263.web.app
- [ ] Test sign up
- [ ] Test Google sign-in
- [ ] Test password reset
- [ ] Test quiz functionality
- [ ] Check Render logs for errors

## Troubleshooting 🔧

If deployment fails:
- [ ] Check Render logs: Dashboard → Logs tab
- [ ] Verify GitHub credentials
- [ ] Ensure `render.yaml` is in backend folder
- [ ] Check environment variables are set
- [ ] Verify requirements.txt is valid

If frontend can't connect:
- [ ] Check browser console (F12)
- [ ] Verify `REACT_APP_API_URL` in `.env.production`
- [ ] Ensure backend URL matches exactly
- [ ] Wait for backend to wake up (if on free tier)

If database issues:
- [ ] SSH into Render service: `python manage.py migrate --noinput`
- [ ] Check migration files exist
- [ ] Verify database user permissions

## Post-Deployment 🎉

- [ ] Share URL with friends: https://quiz-system-78263.web.app
- [ ] Monitor Render dashboard for performance
- [ ] Set up Render alerts (optional)
- [ ] Keep GitHub synced with code changes
- [ ] Document any custom domain setup

## Important Notes 📌

- **Free Tier Sleep**: Render free services sleep after 15 min inactivity
  - Solution: Visit the URL to wake it up
  - Or upgrade to paid tier ($7/month)

- **Database**: Render provides free PostgreSQL
  - Automatic backups
  - 1GB storage on free tier

- **Domains**:
  - Frontend: `quiz-system-78263.web.app` (Firebase free)
  - Backend: `quiz-system-backend-xxxx.onrender.com` (Render free)
  - Custom domains available (upgrade needed)

- **Support**:
  - Render: https://render.com/docs
  - Firebase: https://firebase.google.com/docs
  - Django: https://www.djangoproject.com/

---

## Quick Copy-Paste Commands

### Git Push
```bash
cd "e:\UNIVERSITY\Side Projects\Interview Quiz"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/interview-quiz.git
git branch -M main
git push -u origin main
```

### Build Frontend
```bash
cd frontend
npm run build
npx firebase deploy
```

### Local Testing
```bash
# Terminal 1
cd backend
python manage.py runserver

# Terminal 2
cd frontend
npm start
```

---

**Status**: ✅ Backend ready for Render deployment
**Next**: Push to GitHub and deploy on Render
**ETA**: 15 minutes total deployment time
