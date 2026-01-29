# Manual Setup for quiz-system-e9cfb

## Step 1: Get Your Firebase Config

### For firebaseConfig.js:

1. Go to: https://console.firebase.google.com/project/quiz-system-e9cfb/settings/general
2. Scroll down to "Your apps"
3. Click on your web app (or create one if missing)
4. Copy the firebaseConfig object
5. Replace values in `frontend/src/firebaseConfig.js`

### Example what you'll copy:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyD...",
  authDomain: "quiz-system-e9cfb.firebaseapp.com",
  projectId: "quiz-system-e9cfb",
  storageBucket: "quiz-system-e9cfb.firebasestorage.app",
  messagingSenderId: "123456...",
  appId: "1:123456:web:abcd...",
  measurementId: "G-XXXXX"
};
```

Paste your actual values here in firebaseConfig.js

---

## Step 2: Get Service Account Key

1. Go to: https://console.firebase.google.com/project/quiz-system-e9cfb/settings/serviceaccounts/adminsdk
2. Click "Generate New Private Key" (blue button)
3. File downloads as JSON
4. Save as: `quiz-system/serviceAccountKey.json`

---

## Step 3: Update Frontend Config

Edit: `frontend/src/firebaseConfig.js`

Replace the firebaseConfig object with your actual credentials from Step 1

---

## Step 4: Run Migration

```bash
cd "e:\UNIVERSITY\Side Projects\Interview Quiz"
pip install firebase-admin requests
python migrate_questions.py
```

---

## Step 5: Deploy Frontend

```bash
cd frontend
npm run build
npx firebase deploy
```

---

Done! App will be live at: https://quiz-system-e9cfb.web.app
