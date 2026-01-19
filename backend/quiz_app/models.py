from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    CATEGORY_CHOICES = [
        ('arrays', 'Arrays'),
        ('strings', 'Strings'),
        ('linked_lists', 'Linked Lists'),
        ('trees', 'Trees'),
        ('graphs', 'Graphs'),
        ('dynamic_programming', 'Dynamic Programming'),
        ('sorting', 'Sorting'),
        ('hash_tables', 'Hash Tables'),
        ('heap', 'Heap'),
        ('queue_stack', 'Queue/Stack'),
        ('databases', 'Database Systems'),
        ('oop', 'OOP'),
        ('system_design', 'System Design'),
        ('bit_manipulation', 'Bit Manipulation'),
        ('math', 'Math'),
    ]
    
    TOPIC_CHOICES = [
        ('dsa', 'Data Structures & Algorithms'),
        ('oop', 'Object-Oriented Programming'),
        ('pf', 'Programming Fundamentals'),
        ('database', 'Database Systems'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    
    # Code related fields
    template_code = models.TextField(help_text="Starter code template")
    solution_code = models.TextField(help_text="Complete solution")
    explanation = models.TextField(help_text="Solution explanation")
    video_url = models.URLField(blank=True, null=True, help_text="Video explanation link")
    
    # Test cases as JSON
    test_cases = models.JSONField(default=list)
    
    # Metadata
    solved_count = models.IntegerField(default=0)
    avg_difficulty_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['difficulty', 'category']),
            models.Index(fields=['topic']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"


class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('practice', 'Practice'),
        ('timed', 'Timed'),
        ('mock', 'Mock Interview'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPE_CHOICES)
    
    # Questions in this quiz
    questions = models.ManyToManyField(Question, through='QuizQuestion')
    
    # Time limit in minutes (0 = no limit for practice mode)
    time_limit = models.IntegerField(default=30, validators=[MinValueValidator(0)])
    
    # Difficulty level
    difficulty = models.CharField(max_length=10, choices=Question.DIFFICULTY_CHOICES)
    
    # Category/Topic filtering
    category = models.CharField(max_length=50, choices=Question.CATEGORY_CHOICES, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()
    
    class Meta:
        ordering = ['order']
        unique_together = ('quiz', 'question')
    
    def __str__(self):
        return f"{self.quiz.name} - Q{self.order}"


class QuizSession(models.Model):
    SESSION_STATUS_CHOICES = [
        ('started', 'Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_sessions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, default='started')
    
    # Score and stats
    total_score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0.0)
    
    # Time tracking
    time_started = models.DateTimeField(auto_now_add=True)
    time_ended = models.DateTimeField(null=True, blank=True)
    time_spent = models.IntegerField(default=0, help_text="Time spent in seconds")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.name}"


class Answer(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    user_code = models.TextField()
    is_correct = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    
    feedback = models.TextField(blank=True)
    test_results = models.JSONField(default=dict)
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['submitted_at']
    
    def __str__(self):
        return f"Answer to {self.question.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Stats
    total_questions_solved = models.IntegerField(default=0)
    total_quizzes_completed = models.IntegerField(default=0)
    total_correct_answers = models.IntegerField(default=0)
    overall_accuracy = models.FloatField(default=0.0)
    
    # Strengths and weaknesses
    weak_areas = models.JSONField(default=dict, help_text="Categories with low accuracy")
    strong_areas = models.JSONField(default=dict, help_text="Categories with high accuracy")
    
    # Preferences
    preferred_difficulty = models.CharField(
        max_length=10, 
        choices=Question.DIFFICULTY_CHOICES,
        default='medium'
    )
    preferred_topic = models.CharField(
        max_length=20, 
        choices=Question.TOPIC_CHOICES,
        default='dsa'
    )
    
    # Last activity
    last_practice_date = models.DateTimeField(null=True, blank=True)
    notification_enabled = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile: {self.user.username}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bookmarked_by')
    
    notes = models.TextField(blank=True)
    is_solved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'question')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.title}"


class Leaderboard(models.Model):
    PERIOD_CHOICES = [
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('all_time', 'All Time'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    
    rank = models.IntegerField()
    score = models.IntegerField()
    questions_solved = models.IntegerField()
    accuracy = models.FloatField()
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['rank']
        unique_together = ('user', 'period')
    
    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} ({self.period})"
