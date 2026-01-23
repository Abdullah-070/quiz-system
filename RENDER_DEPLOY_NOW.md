# 🚀 Render Deployment - Step by Step

## Status: ✅ Code Pushed to GitHub!

Your code is now on GitHub: https://github.com/Abdullah-070/quiz-system

---

## 📋 Deploy to Render (5-10 minutes)

### Step 1: Go to Render Dashboard
1. Open **https://render.com**
2. Sign up or log in (use GitHub account for easy connection)

### Step 2: Create Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**

### Step 3: Connect GitHub Repository
1. Click **"Connect a repository"**
2. Search for: `quiz-system`
3. Select **Abdullah-070/quiz-system**
4. Click **"Connect"**

### Step 4: Configure Web Service

Fill in the form with these values:

```
Name:                    quiz-system-backend
Environment:             Python 3
Region:                  (any, e.g., Oregon)
Branch:                  main
Root Directory:          backend
Build Command:           pip install -r requirements.txt && python manage.py migrate
Start Command:           gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

### Step 5: Add Environment Variables

Click **"Add Environment Variable"** for each:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | `elc2t@v7**09*zyeibknrh_$d8dl^lc@%*j7h)u7y1(*2$o6vs` |
| `ALLOWED_HOSTS` | `.onrender.com,quiz-system-78263.web.app` |
| `FRONTEND_URL` | `https://quiz-system-78263.web.app` |

### Step 6: Create Database (Optional but Recommended)

For production, you can add a free PostgreSQL database:

1. On the same Render page, scroll down
2. Check **"Add PostgreSQL Database"**
3. Name: `quiz-db`
4. Plan: **Free**
5. Render will auto-set `DATABASE_URL` environment variable

### Step 7: Deploy

1. Click **"Create Web Service"**
2. Wait for build and deployment (5-10 minutes)
3. Check the **Logs** tab to see progress

---

## ✅ When Deployment Completes

You'll see:
- Status: **"Live"** (green)
- URL: `https://quiz-system-backend-xxxx.onrender.com`
- Your backend API endpoint: `https://quiz-system-backend-xxxx.onrender.com/api`

**Copy this URL!** You'll need it in the next step.

---

## 🔄 Update Frontend with Backend URL

### Step 1: Get Backend URL
From Render dashboard, copy your URL:
```
https://quiz-system-backend-xxxx.onrender.com
```

### Step 2: Update Frontend Config

**File:** `frontend/.env.production`

Change:
```env
REACT_APP_API_URL=https://quiz-system-backend-xxxx.onrender.com/api
```

(Replace `xxxx` with your actual Render URL's random ID)

### Step 3: Build & Deploy Frontend

```bash
cd frontend
npm run build
npx firebase deploy
```

---

## 🎉 Testing

### Test Backend API
Visit in browser:
```
https://quiz-system-backend-xxxx.onrender.com/api/questions/?page=1
```

Should return JSON with question data ✅

### Test Frontend
Visit:
```
https://quiz-system-78263.web.app
```

Should load without connection errors ✅

### Test User Registration
1. Go to Sign Up page
2. Create new account
3. Should work without errors ✅

### Test All Features
- ✅ Sign up new user
- ✅ Google sign-in
- ✅ Forgot password
- ✅ Browse questions
- ✅ Create custom quiz
- ✅ Solve quiz
- ✅ View dashboard
- ✅ Check leaderboard

---

## 📊 What You Get

**Frontend (Firebase):**
- ✅ https://quiz-system-78263.web.app
- ✅ Real-time hosting
- ✅ SSL certificate (HTTPS)
- ✅ Firebase Authentication
- ✅ Free tier with generous limits

**Backend (Render):**
- ✅ https://quiz-system-backend-xxxx.onrender.com/api
- ✅ Django REST API
- ✅ PostgreSQL database
- ✅ SSL certificate (HTTPS)
- ✅ Auto-deployments from GitHub
- ✅ Free tier (may sleep after 15 min)

**Features:**
- ✅ 2000+ interview questions
- ✅ User authentication
- ✅ Google sign-in
- ✅ Password reset
- ✅ Quiz creation & solving
- ✅ Real-time scoring
- ✅ Leaderboard
- ✅ Quiz history
- ✅ Dashboard statistics

---

## ⚠️ Important Notes

### Free Tier Limitations
- **Render**: Services go to sleep after 15 minutes of inactivity
  - **First request takes 30-60 seconds** (cold start)
  - **Solution**: Visit daily or upgrade to paid ($7/month)

### Auto-Deployments
- Every push to GitHub → Auto-deploys to Render
- **No manual deploys needed after initial setup!**

### Database
- PostgreSQL database included (1GB free)
- Automatic backups
- Data persists even if service sleeps

---

## 🆘 Troubleshooting

### Deployment Failed?
1. Check **Logs** tab in Render dashboard
2. Common errors:
   - `ModuleNotFoundError` → Dependencies missing
   - `SyntaxError` → Code error
   - `OperationalError` → Database not ready

### Backend URL shows 502 error?
1. Check Logs in Render
2. Wait for build to complete (it may still be building)
3. Hard refresh browser (Ctrl+F5)

### Frontend can't connect to backend?
1. Check `REACT_APP_API_URL` in `frontend/.env.production`
2. Ensure URL is correct: `https://your-url.onrender.com/api`
3. Wait for both services to be "Live"
4. Check browser console for CORS errors

### Still having issues?
1. Check Render logs: Dashboard → Service → Logs tab
2. Restart service: Dashboard → Service → Settings → Manual Deploy
3. Check GitHub push: `git log --oneline`

---

## 📞 Render Support

- **Docs**: https://render.com/docs
- **Status**: https://status.render.com
- **Support**: https://render.com/support

---

## 🎯 Summary

| Step | Time | Status |
|------|------|--------|
| Push to GitHub | ✅ Done | Complete |
| Deploy to Render | ⏳ Next | 5-10 min |
| Update frontend | Then | 2 min |
| Test live app | Finally | 5 min |

**Total: ~20 minutes**

---

## ✨ You're Almost Done!

Your app will be **live on the internet** accessible from **anywhere in the world**!

### Next: Go to Render and deploy! 🚀

https://render.com
