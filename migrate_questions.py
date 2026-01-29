#!/usr/bin/env python3
"""
Migrate questions from Django API to Firestore
Usage: python migrate_questions.py
"""

import json
import sys
from datetime import datetime

try:
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore
except ImportError:
    print("❌ Firebase Admin SDK not installed")
    print("Install with: pip install firebase-admin")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("❌ Requests library not installed")
    print("Install with: pip install requests")
    sys.exit(1)


# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized")
except Exception as e:
    print(f"❌ Error initializing Firebase: {e}")
    print("Make sure serviceAccountKey.json exists in current directory")
    sys.exit(1)


def fetch_questions_from_api():
    """Fetch all questions from Django API"""
    api_url = "https://quiz-system-backend-oiq0.onrender.com/api/questions/"
    
    print(f"\n📥 Fetching questions from {api_url}...")
    
    try:
        response = requests.get(api_url, params={'page_size': 2000})
        response.raise_for_status()
        
        data = response.json()
        
        # Handle pagination
        if isinstance(data, dict) and 'results' in data:
            questions = data['results']
        else:
            questions = data if isinstance(data, list) else []
        
        print(f"✅ Fetched {len(questions)} questions")
        return questions
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching questions: {e}")
        return []


def migrate_to_firestore(questions):
    """Migrate questions to Firestore"""
    
    if not questions:
        print("❌ No questions to migrate")
        return False
    
    print(f"\n📤 Migrating {len(questions)} questions to Firestore...")
    
    batch = db.batch()
    success_count = 0
    error_count = 0
    
    for idx, question in enumerate(questions, 1):
        try:
            question_id = str(question.get('id', idx))
            question_ref = db.collection('questions').document(question_id)
            
            # Prepare question data
            question_data = {
                'id': question.get('id', idx),
                'title': question.get('title', ''),
                'description': question.get('description', ''),
                'difficulty': question.get('difficulty', 'medium'),
                'category': question.get('category', 'general'),
                'topic': question.get('topic', 'general'),
                'options': question.get('options', []),
                'correctAnswer': question.get('correct_answer') or question.get('correctAnswer', ''),
                'explanation': question.get('explanation', ''),
                'createdAt': datetime.now(),
                'updatedAt': datetime.now(),
            }
            
            batch.set(question_ref, question_data)
            success_count += 1
            
            # Firestore batch limit is 500
            if idx % 500 == 0:
                print(f"  Committing batch {idx // 500} ({idx} total)...")
                batch.commit()
                batch = db.batch()
        
        except Exception as e:
            print(f"  ❌ Error migrating question {idx}: {e}")
            error_count += 1
    
    # Commit remaining
    if success_count % 500 != 0:
        print(f"  Committing final batch ({success_count} total)...")
        batch.commit()
    
    print(f"\n✅ Successfully migrated {success_count} questions")
    if error_count > 0:
        print(f"⚠️  {error_count} questions failed to migrate")
    
    return True


def verify_migration():
    """Verify questions were migrated"""
    try:
        count = 0
        for doc in db.collection('questions').limit(1).stream():
            count += 1
        
        # Get actual count
        docs = db.collection('questions').stream()
        count = sum(1 for _ in docs)
        
        print(f"\n📊 Verification: {count} questions in Firestore")
        return count > 0
    
    except Exception as e:
        print(f"⚠️  Could not verify: {e}")
        return False


def main():
    print("=" * 60)
    print("🚀 Firestore Migration Script")
    print("=" * 60)
    
    # Step 1: Fetch questions from API
    questions = fetch_questions_from_api()
    
    if not questions:
        print("❌ Migration cancelled: No questions fetched")
        return False
    
    # Step 2: Migrate to Firestore
    success = migrate_to_firestore(questions)
    
    if not success:
        print("❌ Migration failed")
        return False
    
    # Step 3: Verify
    if verify_migration():
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Check Firestore Console: https://console.firebase.google.com")
        print("2. Deploy frontend: https://quiz-system-78263.web.app")
        print("3. Test taking a quiz")
        return True
    else:
        print("⚠️  Migration completed but verification inconclusive")
        return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
