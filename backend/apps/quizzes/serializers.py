from rest_framework import serializers
from .models import QuizSession, QuizAnswer, Leaderboard

class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = ['id', 'question', 'user_answer', 'is_correct', 'time_spent']

class QuizSessionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = QuizSession
        fields = ['id', 'quiz_type', 'category', 'difficulty', 'time_limit', 'started_at', 'completed_at', 'total_questions', 'correct_answers', 'accuracy', 'is_completed', 'answers']

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['user', 'username', 'quizzes_completed', 'accuracy', 'rank', 'week_start']
