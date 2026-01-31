from rest_framework import serializers
from .models import Question, Bookmark

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'difficulty', 'question_type', 'category', 'code_template', 'expected_output', 'source', 'created_at']

class BookmarkSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'question', 'created_at']
