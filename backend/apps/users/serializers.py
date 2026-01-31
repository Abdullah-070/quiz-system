from rest_framework import serializers
from .models import User, UserStats

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'avatar_url', 'created_at']

class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = ['total_questions_solved', 'total_quizzes_completed', 'overall_accuracy', 'last_practice_date']
