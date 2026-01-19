from django.core.management.base import BaseCommand
import json
from quiz_app.models import Question


class Command(BaseCommand):
    help = 'Seed database with initial questions'
    
    def handle(self, *args, **options):
        # Sample data structure - you can import from JSON file
        sample_questions = [
            {
                'title': 'Two Sum',
                'description': 'Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'easy',
                'template_code': 'def twoSum(nums, target):\n    pass',
                'solution_code': 'def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen:\n            return [seen[target - num], i]\n        seen[num] = i\n    return []',
                'explanation': 'Use a hash map to store numbers we\'ve seen. For each number, check if target - num exists in the hash map.',
                'test_cases': [
                    {'input': {'nums': [2, 7, 11, 15], 'target': 9}, 'output': [0, 1]},
                    {'input': {'nums': [3, 2, 4], 'target': 6}, 'output': [1, 2]},
                ]
            },
            {
                'title': 'Valid Parentheses',
                'description': 'Given a string s containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid.',
                'topic': 'dsa',
                'category': 'queue_stack',
                'difficulty': 'easy',
                'template_code': 'def isValid(s):\n    pass',
                'solution_code': 'def isValid(s):\n    stack = []\n    mapping = {\')\': \'(\', \'}\': \'{\', \']\': \'[\'}\n    for char in s:\n        if char in mapping:\n            if not stack or stack[-1] != mapping[char]:\n                return False\n            stack.pop()\n        else:\n            stack.append(char)\n    return not stack',
                'explanation': 'Use a stack to keep track of opening brackets. When you encounter a closing bracket, check if it matches the most recent opening bracket.',
                'test_cases': [
                    {'input': {'s': '()'}, 'output': True},
                    {'input': {'s': '()[]{}'}, 'output': True},
                    {'input': {'s': '(]'}, 'output': False},
                ]
            },
        ]
        
        for q_data in sample_questions:
            question, created = Question.objects.get_or_create(
                title=q_data['title'],
                defaults=q_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {question.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Already exists: {question.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database')
        )
