# 📊 Visual Deployment Flow

## Architecture After Deployment

```
┌─────────────────────────────────────────────────────┐
│                 USER BROWSER                         │
│            Your Quiz Application                     │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌──────────┐
    │Firebase│  │  React │  │ API Calls│
    │  Auth  │  │ Frontend│  │ to Django│
    └────────┘  └────────┘  └──────────┘
         │           │           │
         └───────────┼───────────┘
                     │
    ┌────────────────▼────────────────┐
    │   https://quiz-system-78263     │
    │        .web.app                 │
    │   (Firebase Hosting)            │
    │                                  │
    │  - React App                     │
    │  - User Interface                │
    │  - Static Files                  │
    └────────────────┬────────────────┘
                     │
                     │ HTTP Requests
                     │ (JSON APIs)
                     │
    ┌────────────────▼────────────────────────┐
    │  https://quiz-system-backend-xxxx       │
    │         .onrender.com/api                │
    │   (Render Web Service)                   │
    │                                          │
    │  - Django REST API                       │
    │  - Authentication Logic                  │
    │  - Quiz Management                       │
    │  - Scoring & Leaderboard                 │
    │  - Gunicorn Server                       │
    └────────────────┬────────────────────────┘
                     │
                     │ SQL Queries
                     │
    ┌────────────────▼────────────────┐
    │      PostgreSQL Database        │
    │      (Render Managed)           │
    │                                  │
    │  - Users                         │
    │  - Questions                     │
    │  - Quiz Sessions                 │
    │  - Answers & Scores              │
    │  - Leaderboard Data              │
    └─────────────────────────────────┘
```

---

## Deployment Timeline

```
┌─ Day 1: Setup ──────────────────────┐
│  ├─ Create GitHub account (5 min)   │
│  ├─ Push code to GitHub (5 min)     │
│  └─ Create Render account (2 min)   │
└─────────────────────────────────────┘
                │
                ▼
┌─ Day 1: Deploy Backend ─────────────┐
│  ├─ Connect GitHub to Render (1 min)│
│  ├─ Fill in Render form (2 min)     │
│  ├─ Click Deploy (1 click)          │
│  ├─ Wait for build (5-10 min)       │
│  └─ Get backend URL (1 min)         │
└─────────────────────────────────────┘
                │
                ▼
┌─ Day 1: Deploy Frontend ────────────┐
│  ├─ Update .env.production (1 min)  │
│  ├─ Build frontend (3 min)          │
│  ├─ Deploy to Firebase (3 min)      │
│  └─ Test live app (5 min)           │
└─────────────────────────────────────┘
                │
                ▼
         ✅ DONE! Live on Web!
```

---

## File Structure (What Gets Deployed)

### Backend (Render)
```
backend/
├── config/
│   ├── settings.py        ✅ Production ready
│   ├── urls.py            ✅ All routes
│   └── wsgi.py            ✅ Gunicorn config
├── quiz_app/
│   ├── models.py          ✅ Database models
│   ├── views.py           ✅ API endpoints
│   ├── serializers.py     ✅ Data serialization
│   └── urls.py            ✅ API routes
├── manage.py              ✅ Django manager
├── requirements.txt       ✅ Dependencies
└── render.yaml            ✅ Render config
```

### Frontend (Firebase)
```
frontend/
├── public/
│   └── index.html         ✅ Entry point
├── src/
│   ├── App.js             ✅ Main component
│   ├── pages/             ✅ Page components
│   ├── components/        ✅ UI components
│   ├── services/
│   │   └── api.js         ✅ API calls (points to backend)
│   ├── context/
│   │   └── AuthContext.js ✅ Authentication logic
│   └── firebaseConfig.js  ✅ Firebase config
├── package.json           ✅ Dependencies
├── .env.production        ✅ API URL for production
└── build/                 ✅ Production build (deployed)
```

---

## Data Flow Example: User Signs Up

```
User fills signup form
        │
        ▼
┌──────────────────┐
│ Frontend (React) │  Validates form
│ firebaseConfig   │
└────────────────┬─┘
                 │
                 │ POST /api/auth/register/
                 │ {username, email, password, ...}
                 ▼
        ┌─────────────────────┐
        │ Backend (Django)    │
        │ Django Auth         │
        │ UserProfile create  │
        └────────┬────────────┘
                 │
                 │ Generate JWT Token
                 │
                 ▼
        ┌──────────────────────┐
        │ Save to PostgreSQL   │
        │ - User created       │
        │ - Profile created    │
        └──────────┬───────────┘
                   │
                   │ Return JWT token
                   ▼
        ┌──────────────────────┐
        │ Frontend (React)     │
        │ - Store token        │
        │ - Navigate to home   │
        │ - User logged in ✓   │
        └──────────────────────┘
```

---

## API Request/Response Cycle

```
Frontend (JavaScript)              Backend (Django)           Database
─────────────────────              ────────────────           ────────

Request:
GET /api/questions/?page=1
    │
    ├─> CORS headers
    ├─> JWT token
    └──────────────────────────────────────────────→ Check origin
                                                    ↓
                                              Check authentication
                                                    ↓
                                              Query database
                                              (SELECT * FROM questions)
                                                    ↓
                                              Serialize response
                                                    ↓
Response:
                        ←────────────────────── {
                                                  "count": 2000,
                                                  "results": [...],
                                                  "next": "...",
                                              }

Parse JSON                     
    ↓
Update state
    ↓
Render UI
```

---

## Deployment Command Cheatsheet

```bash
# 1. Git Push (one time)
cd "e:\UNIVERSITY\Side Projects\Interview Quiz"
git init
git add .
git commit -m "Deployment"
git remote add origin https://github.com/USERNAME/interview-quiz.git
git push -u origin main

# 2. Frontend Build
cd frontend
npm run build        # Creates optimized production build
npm run build        # Re-run after updating .env.production

# 3. Frontend Deploy
npx firebase deploy  # Pushes to Firebase Hosting

# 4. Backend Deploy
# Use Render Dashboard (no command needed!)
# Or: git push (Render auto-deploys from GitHub)

# 5. Local Testing
cd backend && python manage.py runserver    # Terminal 1
cd frontend && npm start                     # Terminal 2
# Open http://localhost:3000
```

---

## Security Overview

```
🔒 What's Secure

Frontend (React):
  ✅ No sensitive data stored in code
  ✅ JWT tokens in localStorage
  ✅ CORS protection enabled
  ✅ Firebase Auth handles passwords

Backend (Django):
  ✅ SECRET_KEY auto-generated on Render
  ✅ JWT authentication for all API calls
  ✅ CORS whitelist configured
  ✅ Database credentials in environment variables
  ✅ SSL/HTTPS automatic on both platforms

Database (PostgreSQL):
  ✅ Credentials not in code
  ✅ Automatic backups by Render
  ✅ Encrypted connections
  ✅ No data exposed in frontend
```

---

## Monitoring & Logs

```
Component           Where to Check Logs
──────────────────────────────────────────────
Backend Errors      Render Dashboard → Service → Logs
Frontend Errors     Browser DevTools (F12) → Console
Auth Issues         Firebase Console → Authentication → Sign-in method
Database Issues     Render Dashboard → Database → Logs
Performance         Firebase Console → Hosting → Metrics
```

---

## Success Indicators ✅

After deployment, you should see:

```
✅ Frontend loads at https://quiz-system-78263.web.app
✅ Login page appears
✅ Can sign up new account
✅ Can sign in with Google
✅ Can create custom quiz
✅ Can solve questions
✅ Dashboard shows stats
✅ Leaderboard populated
✅ No CORS errors in console
✅ Backend API responds: https://your-url/api/auth/current-user/
```

---

## Troubleshooting Decision Tree

```
                      Error?
                        │
         ┌──────────────┼──────────────┐
         │              │              │
      Backend        Frontend        Auth
        │              │              │
        ├─ No logs     ├─ Blank page  ├─ Can't login
        ├─ 502 error   ├─ 404 error   ├─ Google fails
        ├─ Crash       ├─ CSS broken  └─ Reset fails
        └─ Slow        └─ API fails
           │              │              │
           → Check Render → Clear cache  → Check Firebase
             logs         Browser restart  Console
                          npm build
                          firebase deploy
```

---

## Total Deployment Time

| Task | Time |
|------|------|
| Push code | 5 min |
| Deploy backend | 10 min |
| Update frontend | 2 min |
| Build frontend | 3 min |
| Deploy frontend | 3 min |
| **Total** | **~25 min** |

**First request will be slow (cold start): 30-60 seconds**

---

Good luck deploying! 🚀

For detailed steps, see **[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)**
