from django.contrib import admin
from .models import QuizSession, QuizAnswer, Leaderboard

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz_type', 'total_questions', 'correct_answers', 'is_completed']
    list_filter = ['quiz_type', 'is_completed', 'started_at']

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['session', 'question', 'is_correct']

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['username', 'rank', 'accuracy', 'week_start']
    list_filter = ['week_start']
