from django.db import models
import uuid

class QuizSession(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('Timed', 'Timed'),
        ('Practice', 'Practice'),
        ('Mock', 'Mock Interview'),
        ('Custom', 'Custom'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='quiz_sessions')
    quiz_type = models.CharField(max_length=50, choices=QUIZ_TYPE_CHOICES)
    category = models.CharField(max_length=100, blank=True, null=True)
    difficulty = models.CharField(max_length=20, blank=True, null=True)
    time_limit = models.IntegerField(null=True, blank=True)  # in minutes
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_completed']),
            models.Index(fields=['started_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.quiz_type}"

class QuizAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.BooleanField()
    time_spent = models.IntegerField(default=0)  # in seconds
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.user.username} - {self.question.title}"

class Leaderboard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    quizzes_completed = models.IntegerField(default=0)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    week_start = models.DateField()
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['week_start', 'rank']),
        ]

    def __str__(self):
        return f"{self.username} - Week {self.week_start}"
