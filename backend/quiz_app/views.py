from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    Question, Quiz, QuizSession, Answer, UserProfile,
    Bookmark, Leaderboard
)
from .serializers import (
    QuestionSerializer, QuestionDetailSerializer, QuizSerializer,
    QuizDetailSerializer, QuizSessionSerializer, AnswerSerializer,
    UserProfileSerializer, BookmarkSerializer, LeaderboardSerializer,
    UserRegistrationSerializer, PasswordResetRequestSerializer,
    PasswordResetSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuestionDetailSerializer
        return QuestionSerializer
    
    def get_queryset(self):
        queryset = Question.objects.all()
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by topic
        topic = self.request.query_params.get('topic')
        if topic:
            queryset = queryset.filter(topic=topic)
        
        # Search by title/description
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get questions grouped by category"""
        categories = Question.CATEGORY_CHOICES
        result = {}
        for cat_val, cat_name in categories:
            count = Question.objects.filter(category=cat_val).count()
            result[cat_val] = {'name': cat_name, 'count': count}
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get question count by difficulty"""
        difficulties = Question.DIFFICULTY_CHOICES
        result = {}
        for diff_val, diff_name in difficulties:
            count = Question.objects.filter(difficulty=diff_val).count()
            result[diff_val] = {'name': diff_name, 'count': count}
        return Response(result)


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.filter(is_active=True)
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizDetailSerializer
        return QuizSerializer
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a new quiz session"""
        quiz = self.get_object()
        
        session = QuizSession.objects.create(
            user=request.user,
            quiz=quiz,
            total_questions=quiz.questions.count()
        )
        
        serializer = QuizSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get quizzes by type"""
        quiz_type = request.query_params.get('type')
        if quiz_type:
            quizzes = Quiz.objects.filter(quiz_type=quiz_type, is_active=True)
            serializer = self.get_serializer(quizzes, many=True)
            return Response(serializer.data)
        return Response({'error': 'type parameter required'}, status=400)


class QuizSessionViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return QuizSession.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_custom(self, request):
        """Create a custom quiz session with selected questions"""
        question_ids = request.data.get('questions', [])
        quiz_type = request.data.get('quiz_type', 'practice')
        time_limit = request.data.get('time_limit', 0)
        title = request.data.get('title', 'Custom Quiz')
        
        if not question_ids:
            return Response(
                {'error': 'At least one question is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get questions
        questions = Question.objects.filter(id__in=question_ids)
        if not questions.exists():
            return Response(
                {'error': 'No valid questions found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create quiz session
        session = QuizSession.objects.create(
            user=request.user,
            title=title,
            quiz_type=quiz_type,
            time_limit=time_limit,
            total_questions=len(question_ids),
            status='in_progress'
        )
        
        # Attach questions to session
        session.questions.set(questions)
        
        # Return session with questions
        serializer = QuizSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        """Submit an answer to a question in the session"""
        session = self.get_object()
        
        if session.status == 'completed':
            return Response(
                {'error': 'Quiz session already completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question_id = request.data.get('question_id')
        user_code = request.data.get('code')
        
        if not question_id or not user_code:
            return Response(
                {'error': 'question_id and code required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        question = get_object_or_404(Question, id=question_id)
        
        # Create answer record
        answer = Answer.objects.create(
            session=session,
            question=question,
            user_code=user_code,
            is_correct=True,  # Simplified - implement actual test execution
            score=10  # Simplified scoring
        )
        
        session.correct_answers += 1
        session.total_score += answer.score
        session.accuracy = (session.correct_answers / session.total_questions) * 100 if session.total_questions > 0 else 0
        session.save()
        
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def finish(self, request, pk=None):
        """Mark quiz session as completed"""
        session = self.get_object()
        session.status = 'completed'
        session.time_ended = timezone.now()
        session.save()
        
        # Update user profile
        profile = request.user.profile
        profile.total_quizzes_completed += 1
        profile.last_practice_date = timezone.now()
        profile.save()
        
        serializer = QuizSessionSerializer(session)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)
    
    def create(self, request):
        """Create or toggle bookmark"""
        question_id = request.data.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            question=question
        )
        
        if not created:
            bookmark.delete()
            return Response({'deleted': True})
        
        serializer = self.get_serializer(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def is_bookmarked(self, request):
        """Check if question is bookmarked"""
        question_id = request.query_params.get('question_id')
        if not question_id:
            return Response({'error': 'question_id required'}, status=400)
        
        is_bookmarked = Bookmark.objects.filter(
            user=request.user,
            question_id=question_id
        ).exists()
        
        return Response({'is_bookmarked': is_bookmarked})


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        period = self.request.query_params.get('period', 'week')
        return Leaderboard.objects.filter(period=period).order_by('rank')
    
    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top 10 performers"""
        period = request.query_params.get('period', 'week')
        leaders = Leaderboard.objects.filter(
            period=period
        ).order_by('rank')[:10]
        serializer = self.get_serializer(leaders, many=True)
        return Response(serializer.data)


# Authentication Endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration with email and password"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """User login with email/username and password"""
    username_or_email = request.data.get('username')
    password = request.data.get('password')
    
    if not username_or_email or not password:
        return Response(
            {'error': 'Username/email and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Try to find user by username or email
    try:
        user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid username/email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Check password
    if not user.check_password(password):
        return Response(
            {'error': 'Invalid username/email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        },
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """Request password reset email"""
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        # In production, send email with reset link
        # For now, return token (frontend will use this)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return Response({
            'message': 'Password reset token generated',
            'uid': uid,
            'token': token,
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """Confirm password reset with token"""
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        try:
            uid = urlsafe_base64_decode(serializer.validated_data['uid']).decode()
            user = User.objects.get(pk=uid)
            token = serializer.validated_data['token']
            
            if default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({'message': 'Password reset successful'})
            else:
                return Response(
                    {'error': 'Invalid token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (User.DoesNotExist, ValueError):
            return Response(
                {'error': 'Invalid user'},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current authenticated user"""
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })
