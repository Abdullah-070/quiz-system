from django.test import TestCase
from django.contrib.auth.models import User
from quiz_app.models import Question, Quiz, QuizSession


class QuestionModelTest(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            title='Test Question',
            description='Test Description',
            topic='dsa',
            category='arrays',
            difficulty='easy',
            template_code='def test(): pass',
            solution_code='def test(): pass',
            explanation='Test explanation'
        )
    
    def test_question_creation(self):
        self.assertEqual(self.question.title, 'Test Question')
        self.assertEqual(self.question.difficulty, 'easy')


class UserProfileSignalTest(TestCase):
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertTrue(hasattr(user, 'profile'))
