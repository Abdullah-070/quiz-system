from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'quizzes', views.QuizViewSet, basename='quiz')
router.register(r'sessions', views.QuizSessionViewSet, basename='session')
router.register(r'profile', views.UserProfileViewSet, basename='profile')
router.register(r'bookmarks', views.BookmarkViewSet, basename='bookmark')
router.register(r'leaderboard', views.LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/current-user/', views.current_user, name='current-user'),
    path('auth/password-reset-request/', views.password_reset_request, name='password-reset-request'),
    path('auth/password-reset-confirm/', views.password_reset_confirm, name='password-reset-confirm'),
    # API routes
    path('', include(router.urls)),
]
