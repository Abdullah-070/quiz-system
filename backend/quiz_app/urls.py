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
    path('', include(router.urls)),
]
