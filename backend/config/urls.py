"""
URL configuration for interview_quiz project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Health check endpoint
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.questions.urls')),
    path('api/', include('apps.quizzes.urls')),
]
