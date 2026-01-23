# Render Deployment - Form Values

## Copy-Paste These Exact Values into Render Dashboard

### 1. Create Web Service
```
Repository: interview-quiz (your repo)
Branch: main
```

### 2. Service Configuration

**Name:**
```
quiz-system-backend
```

**Root Directory:**
```
backend
```

**Runtime:**
```
Python 3
```

**Build Command:**
```
pip install -r requirements.txt && python manage.py migrate
```

**Start Command:**
```
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

### 3. Environment Variables (Add these)

Click "Add Environment Variable" for each:

**1. DEBUG**
```
Key: DEBUG
Value: False
```

**2. SECRET_KEY**
```
Key: SECRET_KEY
Value: elc2t@v7**09*zyeibknrh_$d8dl^lc@%*j7h)u7y1(*2$o6vs
```

**3. ALLOWED_HOSTS**
```
Key: ALLOWED_HOSTS
Value: .onrender.com,quiz-system-78263.web.app
```

**4. FRONTEND_URL**
```
Key: FRONTEND_URL
Value: https://quiz-system-78263.web.app
```

### 4. Click Deploy
- Status will show "Building"
- Then "Deploying"
- Finally "Live" (takes ~5-10 min)
- Your URL appears in the logs

---

## After Getting Render URL

### Update Frontend

**File:** `frontend/.env.production`

Replace this:
```
REACT_APP_API_URL=https://quiz-system-backend.onrender.com/api
```

With your actual URL from Render:
```
REACT_APP_API_URL=https://quiz-system-backend-xxxx.onrender.com/api
```

(Replace `xxxx` with the random ID from your Render URL)

---

## Deploy Frontend

```bash
cd frontend
npm run build
npx firebase deploy
```

Done! ✅

---

## Render URL Format

Your URL will look like:
```
https://quiz-system-backend-abcd1234.onrender.com
```

The API endpoint will be:
```
https://quiz-system-backend-abcd1234.onrender.com/api
```

Use this in `REACT_APP_API_URL`

---

## Test the Deployment

### Check Backend is Working
Visit in browser:
```
https://quiz-system-backend-xxxx.onrender.com/api/auth/current-user/
```

Should show:
```json
{"detail": "Authentication credentials were not provided."}
```

✅ If you see this, backend is working!

### Check Frontend Works
Visit:
```
https://quiz-system-78263.web.app
```

✅ Should load the login page

---

## Database Setup

Render handles this automatically! ✅
- Creates PostgreSQL database
- Runs migrations
- Sets `DATABASE_URL` environment variable
- You don't need to do anything

---

## Logs

If anything goes wrong:
1. Go to render.com/dashboard
2. Click your service name
3. Click "Logs" tab
4. See all errors in real-time
5. Scroll up to see build logs

---

## Common Issues & Fixes

**"Build failed"**
- Check build command is exactly: `pip install -r requirements.txt && python manage.py migrate`
- Ensure `requirements.txt` exists in backend folder

**"Service crashed"**
- Check logs for error messages
- Usually missing environment variables
- Try redeploying from Render dashboard

**"503 Service Unavailable"**
- Backend might be sleeping (free tier)
- Visit URL once to wake it up
- Wait 30 seconds and refresh

---

That's it! You're ready to deploy! 🚀
