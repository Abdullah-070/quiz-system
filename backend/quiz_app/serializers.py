from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import (
    Question, Quiz, QuizSession, Answer, UserProfile, 
    Bookmark, Leaderboard, QuizQuestion
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists.')
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already registered.')
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user found with this email.')
        return value


class PasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data


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
    quiz_name = serializers.SerializerMethodField()
    questions = QuestionDetailSerializer(many=True, read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuizSession
        fields = [
            'id', 'quiz', 'quiz_name', 'title', 'quiz_type', 'time_limit',
            'status', 'total_score', 'total_questions', 'correct_answers', 
            'wrong_answers', 'accuracy', 'time_spent', 'time_started', 
            'time_ended', 'questions', 'answers'
        ]
    
    def get_quiz_name(self, obj):
        # Use title for custom quizzes or quiz.name for predefined quizzes
        if obj.title:
            return obj.title
        return obj.quiz.name if obj.quiz else 'Quiz'


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
