# Firestore Migration Guide

## Prerequisites

1. **Firebase Service Account Key**
   - Go to: https://console.firebase.google.com/project/quiz-system-78263/settings/serviceaccounts/adminsdk
   - Click **Generate New Private Key**
   - Save as `serviceAccountKey.json` in the root directory (same level as `backend/` and `frontend/`)
   - ⚠️ KEEP THIS FILE SECRET - Never commit to GitHub!

2. **Node.js Installation**
   ```bash
   node --version  # Should be v14+
   ```

## Setup

1. **Add to `.gitignore`** (protect sensitive key)
   ```
   serviceAccountKey.json
   ```

2. **Install Firebase Admin SDK**
   ```bash
   npm install firebase-admin axios --save
   ```

3. **Make sure Django backend is running**
   ```
   The migration script fetches questions from:
   https://quiz-system-backend-oiq0.onrender.com/api/questions/
   ```

## Run Migration

```bash
# From root directory (quiz-system/)
node migrate-questions.js
```

### Expected Output
```
Starting question migration...

Fetching questions from Django API...
Found 2000 questions
Committing batch of 500 (total: 500)...
Committing batch of 500 (total: 1000)...
Committing batch of 500 (total: 1500)...
Committing batch of 500 (total: 2000)...
✅ Successfully migrated 2000 questions to Firestore

✅ Migration complete!
```

## Verify Migration

1. Go to: https://console.firebase.google.com/project/quiz-system-78263
2. Click **Firestore Database** (left sidebar)
3. You should see `questions` collection with 2000 documents

## Manual Deployment (if Firebase CLI still has issues)

### Option A: Via Firebase Console
1. Go to https://console.firebase.google.com/project/quiz-system-78263
2. Click **Hosting**
3. Click **Connect repository** → Select `Abdullah-070/quiz-system`
4. Deploy

### Option B: Via Google Cloud Storage
1. Go to Cloud Console
2. Upload `frontend/build/` folder to Firebase Hosting bucket
3. Set as public

### Option C: Using `gcloud` CLI
```bash
# Install gcloud CLI
# Then deploy with:
gcloud app deploy --project quiz-system-78263
```

## Firestore Database Structure

After migration, you'll have:

```
Firestore Collections:
├── users/
│   └── {userId}
│       ├── email
│       ├── username
│       ├── totalQuizzes
│       └── bestScore
│
├── questions/
│   └── {questionId}  (2000 documents)
│       ├── title
│       ├── difficulty
│       ├── category
│       ├── options[]
│       └── correctAnswer
│
├── sessions/
│   └── {sessionId}
│       ├── userId
│       ├── score
│       └── answers[]
│
└── bookmarks/
    └── {userId_questionId}
```

## Troubleshooting

### "serviceAccountKey.json not found"
- Download from Firebase Console
- Place in root directory

### "API returned 404"
- Check if Django backend (Render) is running
- Try visiting: https://quiz-system-backend-oiq0.onrender.com/api/questions/

### "Permission denied" when writing to Firestore
- Go to Firestore Settings
- Update Security Rules to allow writes
- Temporary (for testing only):
  ```
  rules_version = '2';
  service cloud.firestore {
    match /databases/{database}/documents {
      match /{document=**} {
        allow read, write: if true;
      }
    }
  }
  ```

### "Batch limit exceeded"
- Script automatically handles batches of 500
- No action needed

## After Migration

1. ✅ Firestore has 2000 questions
2. ✅ Frontend deployed on Firebase Hosting
3. ✅ No more Django backend needed
4. ✅ All auth via Firebase Auth
5. ✅ Real-time updates via Firestore

## Next Steps

1. Test app at: https://quiz-system-78263.web.app
2. Try creating an account
3. Try taking a quiz (questions will load from Firestore)
4. Check leaderboard
5. Delete Render backend (optional - saves money)

---

**Questions?** Check frontend console (F12) for any Firestore errors.
