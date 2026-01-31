from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    firebase_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username

class UserStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_questions_solved = models.IntegerField(default=0)
    total_quizzes_completed = models.IntegerField(default=0)
    overall_accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    last_practice_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Stats"

    def __str__(self):
        return f"Stats for {self.user.username}"
