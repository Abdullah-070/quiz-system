from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, BookmarkViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
]
