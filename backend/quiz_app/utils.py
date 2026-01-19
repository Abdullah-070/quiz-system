from .models import (
    Question, Quiz, QuizSession, Answer, UserProfile,
    Bookmark, Leaderboard
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone


@api_view(['POST'])
def submit_code(request):
    """
    Execute user code against test cases.
    This is a placeholder - implement actual code execution
    """
    code = request.data.get('code')
    test_cases = request.data.get('test_cases', [])
    
    results = []
    for test_case in test_cases:
        # Placeholder for code execution
        results.append({
            'input': test_case.get('input'),
            'expected': test_case.get('output'),
            'passed': True,  # Simplified
            'output': None,
        })
    
    return Response({'results': results})


def calculate_user_stats(user):
    """Calculate and update user profile statistics"""
    sessions = QuizSession.objects.filter(user=user, status='completed')
    
    if not sessions.exists():
        return
    
    profile = user.profile
    total_answers = Answer.objects.filter(session__user=user)
    
    profile.total_questions_solved = total_answers.count()
    profile.total_quizzes_completed = sessions.count()
    profile.total_correct_answers = total_answers.filter(is_correct=True).count()
    
    if profile.total_questions_solved > 0:
        profile.overall_accuracy = (profile.total_correct_answers / profile.total_questions_solved) * 100
    
    # Calculate weak areas
    weak_areas = {}
    for category, _ in Question.CATEGORY_CHOICES:
        answers = total_answers.filter(question__category=category)
        if answers.exists():
            correct = answers.filter(is_correct=True).count()
            accuracy = (correct / answers.count()) * 100
            if accuracy < 70:
                weak_areas[category] = accuracy
    
    profile.weak_areas = weak_areas
    profile.save()


def update_leaderboard():
    """Update leaderboard rankings"""
    now = timezone.now()
    
    # Weekly leaderboard
    week_ago = now - timedelta(days=7)
    weekly_users = QuizSession.objects.filter(
        status='completed',
        time_ended__gte=week_ago
    ).values('user').distinct()
    
    for user_data in weekly_users:
        user_id = user_data['user']
        user = User.objects.get(id=user_id)
        
        sessions = QuizSession.objects.filter(
            user=user,
            status='completed',
            time_ended__gte=week_ago
        )
        
        score = sessions.aggregate(total=models.Sum('total_score'))['total'] or 0
        solved = Answer.objects.filter(
            session__user=user,
            session__status='completed',
            session__time_ended__gte=week_ago,
            is_correct=True
        ).count()
        
        if solved > 0:
            accuracy = (solved / Answer.objects.filter(
                session__user=user,
                session__time_ended__gte=week_ago
            ).count()) * 100
        else:
            accuracy = 0
        
        Leaderboard.objects.update_or_create(
            user=user,
            period='week',
            defaults={
                'score': score,
                'questions_solved': solved,
                'accuracy': accuracy,
                'rank': 0  # Will be set after all calculations
            }
        )
