from django.contrib import admin
from .models import User, UserStats

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'created_at']
    search_fields = ['username', 'email']

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_questions_solved', 'overall_accuracy']
