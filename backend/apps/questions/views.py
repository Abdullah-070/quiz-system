from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Question, Bookmark
from .serializers import QuestionSerializer, BookmarkSerializer

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['difficulty', 'question_type', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'difficulty']

    @action(detail=False, methods=['get'])
    def random(self, request):
        """Get random question"""
        import random
        questions = self.get_queryset()
        if questions.exists():
            question = random.choice(questions)
            serializer = self.get_serializer(question)
            return Response(serializer.data)
        return Response({'error': 'No questions available'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all categories"""
        categories = self.get_queryset().values_list('category', flat=True).distinct()
        return Response({'categories': list(categories)})

class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Bookmark.objects.filter(user_id=user_id)
        return Bookmark.objects.all()

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle bookmark for a question"""
        user_id = request.data.get('user_id')
        question_id = request.data.get('question_id')
        
        bookmark = Bookmark.objects.filter(user_id=user_id, question_id=question_id).first()
        
        if bookmark:
            bookmark.delete()
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)
        else:
            bookmark = Bookmark.objects.create(user_id=user_id, question_id=question_id)
            serializer = self.get_serializer(bookmark)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
