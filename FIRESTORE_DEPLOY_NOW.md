# Firestore Deployment Step-by-Step

## 🎯 Your Mission (5 Simple Steps)

### STEP 1: Download Service Account Key (2 min)

1. Open: https://console.firebase.google.com/project/quiz-system-78263/settings/serviceaccounts/adminsdk
2. Click blue button: **Generate New Private Key**
3. File downloads (looks like: `quiz-system-78263-xxxxx.json`)
4. Move it to: `quiz-system/serviceAccountKey.json`
   - **Location**: Root folder (same level as `backend/` and `frontend/`)

### STEP 2: Run Question Migration (5 min)

**Windows PowerShell:**
```powershell
cd "e:\UNIVERSITY\Side Projects\Interview Quiz"

# Install Python dependencies
pip install firebase-admin requests

# Run migration
python migrate_questions.py
```

**Expected Result:** See "✅ MIGRATION COMPLETE!" message

### STEP 3: Deploy Frontend (5 min)

Go to: https://console.firebase.google.com/project/quiz-system-78263

**Option A (Easiest):**
1. Click **Hosting** (left menu)
2. Find folder: `e:\UNIVERSITY\Side Projects\Interview Quiz\frontend\build`
3. Drag & drop into upload area
4. Wait for "Deploy Complete"

**Option B (If drag-drop fails):**
1. Click **Hosting** → **Connect Repository**
2. Select: `Abdullah-070/quiz-system`
3. Click **Deploy**

### STEP 4: Test the App (5 min)

Visit: https://quiz-system-78263.web.app

**Test these:**
- [ ] Sign up with email
- [ ] Log in
- [ ] Click "Create Quiz"
- [ ] See 2000 questions load
- [ ] Answer a question
- [ ] See score
- [ ] Check leaderboard

### STEP 5: Security Rules (2 min)

1. Go to Firebase Console
2. Click **Firestore Database**
3. Click **Rules** tab
4. Replace all with:

```firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /questions/{document=**} {
      allow read: if request.auth != null;
    }
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
    match /sessions/{sessionId} {
      allow read, write: if request.auth.uid == resource.data.userId;
      allow create: if request.auth.uid == request.resource.data.userId;
    }
    match /bookmarks/{document=**} {
      allow read, write: if request.auth.uid == resource.data.userId;
    }
  }
}
```

5. Click **Publish**

---

## ⚡ Quick Commands

```bash
# If migration fails, try this
cd "e:\UNIVERSITY\Side Projects\Interview Quiz"
python migrate_questions.py

# Or use Node.js version
npm install firebase-admin axios
node migrate-questions.js
```

---

## ✅ Verification Checklist

After all 5 steps:

- [ ] Firestore has 2000 questions (check Console → Firestore → questions collection)
- [ ] Frontend deployed (app loads at https://quiz-system-78263.web.app)
- [ ] Can sign up and log in
- [ ] Quiz questions load correctly
- [ ] Score calculation works
- [ ] No red errors in browser console (F12)

---

## 🆘 Common Issues

### Issue: "serviceAccountKey.json not found"
**Fix:** Download it again, make sure it's in `quiz-system/` folder

### Issue: "Django API returned 404"
**Fix:** Django backend might be sleeping. Visit it first:
https://quiz-system-backend-oiq0.onrender.com/api/questions/

### Issue: "Firebase upload stuck"
**Fix:** Try Google Chrome instead of other browsers. Drag & drop might not work in Firefox.

### Issue: "Questions don't load in quiz"
**Fix:** Check browser console (F12). Look for Firestore errors. Make sure user is logged in.

### Issue: "Firestore rules error"
**Fix:** Temporarily set rules to `allow read, write: if true;` for testing, then apply security rules.

---

## 📊 What You're Getting

✅ **Zero Backend Server** - No more Render errors!
✅ **2000 Questions** - All loaded from Firestore
✅ **Free Hosting** - Firebase free tier (generous limits)
✅ **Real-time Database** - Scalable to millions of users
✅ **Mobile Ready** - Works on phones/tablets
✅ **Automatic Backups** - No manual database maintenance

---

## 💰 Cost

- **Before:** $7-15/month (Render backend)
- **After:** $0-5/month (Firestore + Hosting)
- **Savings:** ~$10/month

---

**That's it! You're migrating to serverless! 🚀**

Questions? Check the FIRESTORE_MIGRATION_GUIDE.md for more details.
