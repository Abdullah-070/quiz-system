from django.contrib import admin
from .models import (
    Question, Quiz, QuizSession, Answer, UserProfile,
    Bookmark, Leaderboard, QuizQuestion
)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'category', 'topic', 'solved_count')
    list_filter = ('difficulty', 'category', 'topic', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'quiz_type', 'difficulty', 'is_active')
    list_filter = ('quiz_type', 'difficulty', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'status', 'correct_answers', 'accuracy', 'time_started')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'quiz__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'is_correct', 'score', 'submitted_at')
    list_filter = ('is_correct', 'submitted_at')
    search_fields = ('question__title', 'session__user__username')
    readonly_fields = ('submitted_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_questions_solved', 'overall_accuracy', 'last_practice_date')
    list_filter = ('created_at', 'last_practice_date')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_solved', 'created_at')
    list_filter = ('is_solved', 'created_at')
    search_fields = ('user__username', 'question__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank', 'score', 'period')
    list_filter = ('period',)
    search_fields = ('user__username',)
    readonly_fields = ('updated_at',)


admin.site.register(QuizQuestion)
