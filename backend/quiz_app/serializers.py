from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Question, Quiz, QuizSession, Answer, UserProfile, 
    Bookmark, Leaderboard, QuizQuestion
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'title', 'description', 'topic', 'category', 'difficulty',
            'template_code', 'explanation', 'video_url', 'test_cases',
            'solved_count', 'avg_difficulty_rating'
        ]


class QuestionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuizQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'order']


class QuizSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'name', 'description', 'quiz_type', 'time_limit',
            'difficulty', 'category', 'is_active', 'questions_count'
        ]
    
    def get_questions_count(self, obj):
        return obj.questions.count()


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(source='quizquestion_set', many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id', 'question', 'user_code', 'is_correct', 'score',
            'feedback', 'test_results', 'submitted_at'
        ]


class QuizSessionSerializer(serializers.ModelSerializer):
    quiz_name = serializers.CharField(source='quiz.name', read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuizSession
        fields = [
            'id', 'quiz', 'quiz_name', 'status', 'total_score',
            'total_questions', 'correct_answers', 'wrong_answers',
            'accuracy', 'time_spent', 'time_started', 'time_ended', 'answers'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'total_questions_solved', 'total_quizzes_completed',
            'total_correct_answers', 'overall_accuracy', 'weak_areas',
            'strong_areas', 'preferred_difficulty', 'preferred_topic',
            'last_practice_date'
        ]


class BookmarkSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'question', 'notes', 'is_solved', 'created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'rank', 'score', 'questions_solved', 'accuracy', 'period']
