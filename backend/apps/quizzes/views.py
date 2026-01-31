from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import QuizSession, QuizAnswer, Leaderboard
from .serializers import QuizSessionSerializer, QuizAnswerSerializer, LeaderboardSerializer

class QuizSessionViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSessionSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return QuizSession.objects.filter(user_id=user_id)
        return QuizSession.objects.all()

    @action(detail=False, methods=['post'])
    def create_session(self, request):
        """Create new quiz session"""
        user_id = request.data.get('user_id')
        quiz_type = request.data.get('quiz_type')
        category = request.data.get('category')
        difficulty = request.data.get('difficulty')
        time_limit = request.data.get('time_limit')
        questions = request.data.get('questions', [])

        session = QuizSession.objects.create(
            user_id=user_id,
            quiz_type=quiz_type,
            category=category,
            difficulty=difficulty,
            time_limit=time_limit,
            total_questions=len(questions)
        )

        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        """Submit answer for a question"""
        session = self.get_object()
        question_id = request.data.get('question_id')
        user_answer = request.data.get('user_answer')
        is_correct = request.data.get('is_correct')
        time_spent = request.data.get('time_spent', 0)

        answer = QuizAnswer.objects.create(
            session=session,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            time_spent=time_spent
        )

        if is_correct:
            session.correct_answers += 1
        
        serializer = QuizAnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete quiz session and calculate results"""
        session = self.get_object()
        session.is_completed = True
        session.completed_at = timezone.now()
        
        if session.total_questions > 0:
            accuracy = (session.correct_answers / session.total_questions) * 100
            session.accuracy = accuracy
        
        session.save()

        # Update user stats
        from apps.users.models import UserStats
        stats, created = UserStats.objects.get_or_create(user=session.user)
        stats.total_quizzes_completed += 1
        stats.total_questions_solved += session.total_questions
        stats.last_practice_date = timezone.now()
        stats.save()

        serializer = self.get_serializer(session)
        return Response(serializer.data)

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaderboardSerializer
    
    def get_queryset(self):
        week_start = self.request.query_params.get('week_start')
        if week_start:
            return Leaderboard.objects.filter(week_start=week_start).order_by('rank')
        return Leaderboard.objects.all().order_by('rank')
