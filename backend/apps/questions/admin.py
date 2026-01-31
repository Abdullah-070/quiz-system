from django.contrib import admin
from .models import Question, Bookmark

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'question_type', 'difficulty', 'category']
    list_filter = ['question_type', 'difficulty', 'category']
    search_fields = ['title', 'description']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'created_at']
    list_filter = ['created_at']
