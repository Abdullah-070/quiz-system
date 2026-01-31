import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.questions.models import Question

# Sample questions data
SAMPLE_QUESTIONS = [
    {
        'title': 'Two Sum',
        'description': 'Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target.',
        'difficulty': 'Easy',
        'question_type': 'DSA',
        'category': 'Arrays',
        'code_template': 'def twoSum(nums, target):\n    pass',
        'expected_output': '[0, 1]',
        'source': 'LeetCode'
    },
    {
        'title': 'Binary Tree Level Order Traversal',
        'description': 'Given the root of a binary tree, return the level order traversal of its nodes values.',
        'difficulty': 'Medium',
        'question_type': 'DSA',
        'category': 'Trees',
        'code_template': 'def levelOrder(root):\n    pass',
        'expected_output': '[[3],[9,20],[15,7]]',
        'source': 'LeetCode'
    },
    {
        'title': 'Implement a Stack',
        'description': 'Implement a stack with push, pop, and peek operations.',
        'difficulty': 'Easy',
        'question_type': 'DSA',
        'category': 'Stack',
        'code_template': 'class Stack:\n    def __init__(self):\n        pass',
        'expected_output': 'Stack operations work correctly',
        'source': 'GeeksforGeeks'
    },
    {
        'title': 'What is Inheritance?',
        'description': 'Explain inheritance in object-oriented programming and provide an example.',
        'difficulty': 'Easy',
        'question_type': 'OOP',
        'category': 'Inheritance',
        'code_template': 'class Animal:\n    pass\n\nclass Dog(Animal):\n    pass',
        'expected_output': 'Proper inheritance implementation',
        'source': 'Internal'
    },
    {
        'title': 'Design Patterns - Singleton',
        'description': 'Implement the Singleton design pattern.',
        'difficulty': 'Medium',
        'question_type': 'OOP',
        'category': 'Design Patterns',
        'code_template': 'class Singleton:\n    _instance = None',
        'expected_output': 'Single instance maintained',
        'source': 'Internal'
    },
    {
        'title': 'SQL JOIN Operations',
        'description': 'Explain different types of JOIN operations in SQL.',
        'difficulty': 'Medium',
        'question_type': 'DB',
        'category': 'Joins',
        'code_template': 'SELECT * FROM table1\nJOIN table2 ON ...',
        'expected_output': 'Correct JOIN result',
        'source': 'Internal'
    },
    {
        'title': 'Database Normalization',
        'description': 'What are the different normal forms in database design?',
        'difficulty': 'Hard',
        'question_type': 'DB',
        'category': 'Normalization',
        'code_template': '',
        'expected_output': '1NF, 2NF, 3NF explanation',
        'source': 'Internal'
    },
    {
        'title': 'Design a URL Shortener',
        'description': 'Design a system that converts long URLs into short unique IDs.',
        'difficulty': 'Hard',
        'question_type': 'PF',
        'category': 'System Design',
        'code_template': 'class URLShortener:\n    pass',
        'expected_output': 'Functional URL shortener',
        'source': 'Internal'
    },
]

def seed_questions():
    """Seed the database with sample questions"""
    print("Seeding questions...")
    
    for q in SAMPLE_QUESTIONS:
        question, created = Question.objects.get_or_create(
            title=q['title'],
            defaults={
                'description': q['description'],
                'difficulty': q['difficulty'],
                'question_type': q['question_type'],
                'category': q['category'],
                'code_template': q['code_template'],
                'expected_output': q['expected_output'],
                'source': q['source'],
            }
        )
        
        if created:
            print(f"✓ Created: {question.title}")
        else:
            print(f"- Already exists: {question.title}")
    
    print(f"\nTotal questions in database: {Question.objects.count()}")

if __name__ == '__main__':
    seed_questions()
