from django.db import models
import uuid

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    TYPE_CHOICES = [
        ('DSA', 'Data Structures & Algorithms'),
        ('OOP', 'Object-Oriented Programming'),
        ('PF', 'Pattern Fundamentals'),
        ('DB', 'Database Systems'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    question_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    category = models.CharField(max_length=100)  # e.g., "Arrays", "Trees", "Inheritance"
    code_template = models.TextField(blank=True, null=True)
    expected_output = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=100, blank=True, null=True)  # e.g., 'LeetCode'

    class Meta:
        indexes = [
            models.Index(fields=['question_type']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookmarks')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"
