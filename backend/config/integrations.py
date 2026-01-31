"""
Integration utilities for Supabase and Firebase.
These functions help with authentication and database operations.
"""

import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from decouple import config
from supabase import create_client, Client
import json

# ==================== FIREBASE SETUP ====================

class FirebaseManager:
    """Manages Firebase authentication and verification"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
            cls._instance._init_firebase()
        return cls._instance
    
    def _init_firebase(self):
        """Initialize Firebase admin SDK"""
        try:
            # Try to initialize Firebase
            firebase_admin.get_app()
        except ValueError:
            # App not initialized yet
            # Note: In production, use a service account JSON file
            # For now, we'll configure this in Django settings
            pass
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify Firebase ID token and return user info.
        
        Args:
            token: Firebase ID token from frontend
            
        Returns:
            Dictionary with user info {uid, email, email_verified, etc.}
            
        Raises:
            firebase_admin.auth.InvalidIdTokenError: If token is invalid
        """
        try:
            decoded_token = firebase_auth.verify_id_token(token)
            return decoded_token
        except firebase_auth.InvalidIdTokenError as e:
            print(f"Invalid Firebase token: {e}")
            raise
    
    @staticmethod
    def get_user(uid: str) -> dict:
        """Get Firebase user by UID"""
        try:
            user = firebase_auth.get_user(uid)
            return {
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name,
                'photo_url': user.photo_url,
                'email_verified': user.email_verified,
            }
        except Exception as e:
            print(f"Error getting Firebase user: {e}")
            return None


# ==================== SUPABASE SETUP ====================

class SupabaseManager:
    """Manages Supabase database and authentication"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseManager, cls).__new__(cls)
            cls._instance._init_supabase()
        return cls._instance
    
    def _init_supabase(self):
        """Initialize Supabase client"""
        try:
            url = config('SUPABASE_URL', default='')
            key = config('SUPABASE_ANON_KEY', default='')
            
            if url and key:
                self.client = create_client(url, key)
            else:
                print("Warning: Supabase credentials not configured")
                self.client = None
        except Exception as e:
            print(f"Error initializing Supabase: {e}")
            self.client = None
    
    def get_client(self) -> Client:
        """Get Supabase client instance"""
        return self.client
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, email: str, username: str, firebase_uid: str = None, avatar_url: str = None) -> dict:
        """Create new user in Supabase"""
        try:
            data = {
                'email': email,
                'username': username,
                'firebase_uid': firebase_uid,
                'avatar_url': avatar_url,
            }
            response = self.client.table('users').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user(self, user_id: str) -> dict:
        """Get user by ID"""
        try:
            response = self.client.table('users').select('*').eq('id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> dict:
        """Get user by email"""
        try:
            response = self.client.table('users').select('*').eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    # ==================== QUESTION OPERATIONS ====================
    
    def get_questions(self, filters: dict = None, limit: int = 20, offset: int = 0) -> list:
        """Get questions with optional filters"""
        try:
            query = self.client.table('questions').select('*')
            
            if filters:
                if filters.get('difficulty'):
                    query = query.eq('difficulty', filters['difficulty'])
                if filters.get('question_type'):
                    query = query.eq('question_type', filters['question_type'])
                if filters.get('category'):
                    query = query.eq('category', filters['category'])
            
            response = query.range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            print(f"Error getting questions: {e}")
            return []
    
    def get_question(self, question_id: str) -> dict:
        """Get single question by ID"""
        try:
            response = self.client.table('questions').select('*').eq('id', question_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting question: {e}")
            return None
    
    # ==================== QUIZ OPERATIONS ====================
    
    def create_quiz_session(self, user_id: str, quiz_data: dict) -> dict:
        """Create new quiz session"""
        try:
            data = {
                'user_id': user_id,
                'quiz_type': quiz_data.get('quiz_type'),
                'category': quiz_data.get('category'),
                'difficulty': quiz_data.get('difficulty'),
                'time_limit': quiz_data.get('time_limit'),
                'total_questions': quiz_data.get('total_questions', 0),
                'correct_answers': 0,
                'is_completed': False,
            }
            response = self.client.table('quiz_sessions').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating quiz session: {e}")
            return None
    
    def submit_answer(self, session_id: str, answer_data: dict) -> dict:
        """Submit an answer for a question"""
        try:
            data = {
                'session_id': session_id,
                'question_id': answer_data.get('question_id'),
                'user_answer': answer_data.get('user_answer'),
                'is_correct': answer_data.get('is_correct'),
                'time_spent': answer_data.get('time_spent', 0),
            }
            response = self.client.table('quiz_answers').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error submitting answer: {e}")
            return None
    
    def complete_quiz_session(self, session_id: str, accuracy: float) -> dict:
        """Mark quiz session as complete and save accuracy"""
        try:
            data = {
                'is_completed': True,
                'completed_at': 'now()',  # Supabase function
                'accuracy': accuracy,
            }
            response = self.client.table('quiz_sessions').update(data).eq('id', session_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error completing quiz: {e}")
            return None
    
    # ==================== BOOKMARK OPERATIONS ====================
    
    def add_bookmark(self, user_id: str, question_id: str) -> dict:
        """Add bookmark for a question"""
        try:
            data = {
                'user_id': user_id,
                'question_id': question_id,
            }
            response = self.client.table('bookmarks').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding bookmark: {e}")
            return None
    
    def remove_bookmark(self, user_id: str, question_id: str) -> bool:
        """Remove bookmark"""
        try:
            response = self.client.table('bookmarks').delete().eq('user_id', user_id).eq('question_id', question_id).execute()
            return True
        except Exception as e:
            print(f"Error removing bookmark: {e}")
            return False
    
    def get_bookmarks(self, user_id: str) -> list:
        """Get all bookmarks for user"""
        try:
            response = self.client.table('bookmarks').select('question_id').eq('user_id', user_id).execute()
            return [b['question_id'] for b in response.data]
        except Exception as e:
            print(f"Error getting bookmarks: {e}")
            return []
    
    # ==================== STATS OPERATIONS ====================
    
    def update_user_stats(self, user_id: str, updates: dict) -> dict:
        """Update user statistics"""
        try:
            response = self.client.table('user_stats').update(updates).eq('user_id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating user stats: {e}")
            return None
    
    def get_user_stats(self, user_id: str) -> dict:
        """Get user statistics"""
        try:
            response = self.client.table('user_stats').select('*').eq('user_id', user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user stats: {e}")
            return None
    
    # ==================== LEADERBOARD OPERATIONS ====================
    
    def get_weekly_leaderboard(self, week_start: str, limit: int = 10) -> list:
        """Get weekly leaderboard"""
        try:
            response = self.client.table('leaderboard').select('*').eq('week_start', week_start).order('rank').limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []


# ==================== MIDDLEWARE ====================

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class FirebaseTokenAuthentication(TokenAuthentication):
    """
    Custom authentication using Firebase tokens.
    Usage: Add to REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] in settings.py
    """
    
    keyword = 'Bearer'
    
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if not auth or auth[0].lower() != self.keyword.lower():
            return None
        
        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header.')
        
        try:
            token = auth[1]
            firebase_manager = FirebaseManager()
            decoded_token = firebase_manager.verify_token(token)
            uid = decoded_token['uid']
            
            # Get or create user in Django
            from apps.users.models import User
            from django.contrib.auth.models import User as DjangoUser
            
            firebase_user = firebase_manager.get_user(uid)
            
            # This is a simplified version - implement as needed
            return (uid, None)
        except Exception as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')


# ==================== INITIALIZATION ====================

# Initialize managers as singletons
firebase_manager = FirebaseManager()
supabase_manager = SupabaseManager()

# Example usage:
# firebase_manager.verify_token(token)
# supabase_manager.get_questions(filters={'difficulty': 'Easy'})
