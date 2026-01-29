# Complete Manual Deployment for quiz-system-e9cfb

## 📋 Your Checklist

```
PHASE 1: Get Credentials (5 min)
  ☐ Firebase Config from Project Settings
  ☐ Service Account Key

PHASE 2: Update Frontend (2 min)
  ☐ Update firebaseConfig.js with your credentials

PHASE 3: Migrate Questions (5 min)
  ☐ Run Python migration script

PHASE 4: Deploy Frontend (5 min)
  ☐ Build and deploy to Firebase Hosting

PHASE 5: Test (5 min)
  ☐ Sign up, create quiz, take quiz
```

---

## PHASE 1: Get Your Credentials (5 min)

### Step 1.1: Get Firebase Configuration

**Go to:**
```
https://console.firebase.google.com/project/quiz-system-e9cfb/settings/general
```

**Find "Your apps" section:**
- If no web app exists, click "Add app" → Select "Web"
- You'll see a config object

**Copy this config:**
```javascript
const firebaseConfig = {
  apiKey: "YOUR_VALUE_HERE",
  authDomain: "quiz-system-e9cfb.firebaseapp.com",
  projectId: "quiz-system-e9cfb",
  storageBucket: "quiz-system-e9cfb.firebasestorage.app",
  messagingSenderId: "YOUR_VALUE_HERE",
  appId: "YOUR_VALUE_HERE",
  measurementId: "YOUR_VALUE_HERE"
};
```

### Step 1.2: Get Service Account Key

**Go to:**
```
https://console.firebase.google.com/project/quiz-system-e9cfb/settings/serviceaccounts/adminsdk
```

**Click:** Generate New Private Key (blue button)

**Save as:** `quiz-system/serviceAccountKey.json`

⚠️ **IMPORTANT:** Add to `.gitignore` so you don't commit it!

```bash
echo "serviceAccountKey.json" >> .gitignore
```

---

## PHASE 2: Update Frontend Config (2 min)

**Edit file:** `frontend/src/firebaseConfig.js`

**Replace the firebaseConfig object with your actual values from Step 1.1**

```javascript
// BEFORE (placeholder)
const firebaseConfig = {
  apiKey: "AIzaSyBsxokS9iRLeqTVJrwwgplwohQA3JO8zow",
  authDomain: "quiz-system-78263.firebaseapp.com",
  ...
};

// AFTER (your actual credentials)
const firebaseConfig = {
  apiKey: "YOUR_ACTUAL_API_KEY_HERE",
  authDomain: "quiz-system-e9cfb.firebaseapp.com",
  projectId: "quiz-system-e9cfb",
  storageBucket: "quiz-system-e9cfb.firebasestorage.app",
  messagingSenderId: "YOUR_ACTUAL_SENDER_ID",
  appId: "YOUR_ACTUAL_APP_ID",
  measurementId: "YOUR_ACTUAL_MEASUREMENT_ID"
};
```

✅ Save the file

---

## PHASE 3: Migrate 2000 Questions (5 min)

**Open PowerShell and run:**

```powershell
cd "e:\UNIVERSITY\Side Projects\Interview Quiz"

# Install dependencies
pip install firebase-admin requests

# Run migration
python migrate_questions.py
```

**Wait for output:**
```
============================================================
🚀 Firestore Migration Script
============================================================

📥 Fetching questions from https://quiz-system-backend-oiq0.onrender.com/api/questions/...
✅ Fetched 2000 questions

📤 Migrating 2000 questions to Firestore...
  Committing batch 1 (500 total)...
  Committing batch 2 (1000 total)...
  Committing batch 3 (1500 total)...
  Committing batch 4 (2000 total)...

✅ Successfully migrated 2000 questions

📊 Verification: 2000 questions in Firestore

============================================================
✅ MIGRATION COMPLETE!
============================================================
```

✅ If you see this, all questions are in Firestore!

---

## PHASE 4: Deploy Frontend (5 min)

**Build the frontend:**

```powershell
cd "e:\UNIVERSITY\Side Projects\Interview Quiz\frontend"

npm run build
```

Wait for: `The build folder is ready to be deployed.`

**Deploy to Firebase:**

```powershell
npx firebase deploy
```

Wait for:
```
+  Deploy complete!
Hosting URL: https://quiz-system-e9cfb.web.app
```

✅ Your app is now live!

---

## PHASE 5: Test Your App (5 min)

**Visit:** https://quiz-system-e9cfb.web.app

**Test these features:**

1. **Sign Up**
   - Click "Sign up here"
   - Enter email, password, name
   - Click "Sign Up"
   - ✅ Should redirect to Dashboard

2. **Create Quiz**
   - Click "Create Quiz" or "New Quiz"
   - Select 10 questions
   - Click "Start Quiz"
   - ✅ Questions should load instantly

3. **Answer Questions**
   - Read question
   - Select answer
   - Click "Next" or "Submit"
   - ✅ Should move to next question

4. **Submit Quiz**
   - Click "Finish Quiz" or "Submit"
   - ✅ Should see score calculated
   - ✅ Should see stats updated

5. **Check Dashboard**
   - Click "Dashboard"
   - ✅ Should show your stats
   - ✅ Total quizzes, best score, average score

6. **Check Leaderboard**
   - Click "Leaderboard"
   - ✅ Should show users ranked by score

**If all ✅ pass, you're done!**

---

## Verification in Firebase Console

### Check Firestore Data

1. Go to: https://console.firebase.google.com/project/quiz-system-e9cfb
2. Click **Firestore Database** (left menu)
3. You should see these collections:
   - `questions/` → 2000 documents
   - `users/` → Your user account
   - `sessions/` → Your quiz attempt
   - `bookmarks/` → (empty until you bookmark)

### Check Hosting

1. Go to: https://console.firebase.google.com/project/quiz-system-e9cfb
2. Click **Hosting** (left menu)
3. You should see:
   - Status: ✅ Live
   - URL: https://quiz-system-e9cfb.web.app
   - Build: Latest deployment

---

## Setup Security Rules (Optional but Recommended)

**Go to:** https://console.firebase.google.com/project/quiz-system-e9cfb/firestore/rules

**Click Rules tab and replace all with:**

```firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow authenticated users to read questions
    match /questions/{document=**} {
      allow read: if request.auth != null;
    }
    
    // Users can read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
    
    // Users can read/write their own sessions
    match /sessions/{sessionId} {
      allow read, write: if request.auth.uid == resource.data.userId;
      allow create: if request.auth.uid == request.resource.data.userId;
    }
    
    // Users can manage their bookmarks
    match /bookmarks/{document=**} {
      allow read, write: if request.auth.uid == resource.data.userId;
    }
  }
}
```

**Click Publish**

---

## Troubleshooting

### Problem: Firebase config values are "YOUR_VALUE_HERE"
**Solution:** You didn't copy your actual config from Firebase Console. Go back to Step 1.1 and copy the real values.

### Problem: Migration script says "API 404"
**Solution:** Django backend might be asleep. Visit this first:
```
https://quiz-system-backend-oiq0.onrender.com/api/questions/
```
Wait 30 seconds and try again.

### Problem: "Permission denied" when migrating
**Solution:** 
- Check serviceAccountKey.json exists in quiz-system/ folder
- Make sure file isn't corrupted (open in text editor, should have JSON)

### Problem: Frontend deploys but shows blank page
**Solution:**
- Hard refresh: Ctrl+Shift+R
- Clear cache: Ctrl+Shift+Delete
- Check console (F12): Look for errors

### Problem: Can't sign up, "Database error"
**Solution:**
- Check Firestore Database status (should be green)
- Check Security Rules allow writes
- Try temporarily allowing all (rules: `allow read, write: if true;`)

### Problem: Questions don't appear in quiz
**Solution:**
- Go to Firebase Console → Firestore → questions collection
- Should show 2000 documents
- If empty, migration didn't work - run `python migrate_questions.py` again

---

## Success Indicators

After completing all phases:

```
✅ Frontend deployed at https://quiz-system-e9cfb.web.app
✅ Can sign up and create account
✅ Can create quiz with 2000 questions
✅ Can take quiz and answer questions
✅ Score calculated correctly
✅ Dashboard shows stats
✅ Leaderboard works
✅ Firestore has all data
✅ No console errors (F12)
```

---

## Next Steps

1. **Invite users** - Share URL
2. **Monitor usage** - Check Firebase Console
3. **Add features** - See FIRESTORE_MIGRATION_GUIDE.md

---

## Timeline

| Phase | Time | Status |
|-------|------|--------|
| Get Credentials | 5 min | |
| Update Frontend | 2 min | |
| Migrate Questions | 5 min | |
| Deploy Frontend | 5 min | |
| Test App | 5 min | |
| **TOTAL** | **~22 min** | |

---

**You're all set! Follow the phases above and your app will be live! 🚀**

Questions? Check the browser console (F12) for detailed error messages.
