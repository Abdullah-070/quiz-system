from django.core.management.base import BaseCommand
import json
from quiz_app.models import Question


class Command(BaseCommand):
    help = 'Seed database with comprehensive interview questions'
    
    def handle(self, *args, **options):
        # Comprehensive coding interview questions across all categories
        sample_questions = [
            # ============== DSA QUESTIONS (50+) ==============
            # Arrays
            {
                'title': 'Two Sum',
                'description': 'Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'easy',
                'template_code': 'def twoSum(nums, target):\n    pass',
                'solution_code': 'def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen:\n            return [seen[target - num], i]\n        seen[num] = i\n    return []',
                'explanation': 'Use a hash map to store numbers we have seen.',
                'test_cases': [
                    {'input': {'nums': [2, 7, 11, 15], 'target': 9}, 'output': [0, 1]},
                ]
            },
            {
                'title': 'Best Time to Buy and Sell Stock',
                'description': 'Given an array prices, find the maximum profit from buying and selling stock once.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'easy',
                'template_code': 'def maxProfit(prices):\n    pass',
                'solution_code': 'def maxProfit(prices):\n    if not prices:\n        return 0\n    min_price, max_profit = prices[0], 0\n    for price in prices[1:]:\n        max_profit = max(max_profit, price - min_price)\n        min_price = min(min_price, price)\n    return max_profit',
                'explanation': 'Track minimum price and maximum profit while iterating.',
                'test_cases': [
                    {'input': {'prices': [7, 1, 5, 3, 6, 4]}, 'output': 5},
                ]
            },
            {
                'title': 'Contains Duplicate',
                'description': 'Return true if any value appears at least twice in the array.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'easy',
                'template_code': 'def containsDuplicate(nums):\n    pass',
                'solution_code': 'def containsDuplicate(nums):\n    return len(nums) != len(set(nums))',
                'explanation': 'Compare array length with set length.',
                'test_cases': [
                    {'input': {'nums': [1, 2, 3, 1]}, 'output': True},
                ]
            },
            {
                'title': 'Product of Array Except Self',
                'description': 'Given an array, return array where each element is product of all other elements.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'medium',
                'template_code': 'def productExceptSelf(nums):\n    pass',
                'solution_code': 'def productExceptSelf(nums):\n    n = len(nums)\n    result = [1] * n\n    for i in range(1, n):\n        result[i] = result[i-1] * nums[i-1]\n    right = 1\n    for i in range(n-1, -1, -1):\n        result[i] *= right\n        right *= nums[i]\n    return result',
                'explanation': 'Use prefix and suffix products approach.',
                'test_cases': [
                    {'input': {'nums': [1, 2, 3, 4]}, 'output': [24, 12, 8, 6]},
                ]
            },
            {
                'title': 'Maximum Subarray',
                'description': 'Find contiguous subarray with the largest sum.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'medium',
                'template_code': 'def maxSubArray(nums):\n    pass',
                'solution_code': 'def maxSubArray(nums):\n    max_sum = current_sum = nums[0]\n    for num in nums[1:]:\n        current_sum = max(num, current_sum + num)\n        max_sum = max(max_sum, current_sum)\n    return max_sum',
                'explanation': 'Kadanes algorithm: track current and maximum sum.',
                'test_cases': [
                    {'input': {'nums': [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, 'output': 6},
                ]
            },
            {
                'title': '3Sum',
                'description': 'Find all triplets that sum to zero.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'medium',
                'template_code': 'def threeSum(nums):\n    pass',
                'solution_code': 'def threeSum(nums):\n    nums.sort()\n    result = []\n    for i in range(len(nums)-2):\n        if i > 0 and nums[i] == nums[i-1]:\n            continue\n        left, right = i+1, len(nums)-1\n        while left < right:\n            s = nums[i] + nums[left] + nums[right]\n            if s == 0:\n                result.append([nums[i], nums[left], nums[right]])\n                left += 1\n                right -= 1\n            elif s < 0:\n                left += 1\n            else:\n                right -= 1\n    return result',
                'explanation': 'Sort then use two pointers.',
                'test_cases': [
                    {'input': {'nums': [-1, 0, 1, 2, -1, -4]}, 'output': [[-1, -1, 2], [-1, 0, 1]]},
                ]
            },
            # Strings
            {
                'title': 'Valid Palindrome',
                'description': 'Determine if string is palindrome ignoring non-alphanumeric characters.',
                'topic': 'dsa',
                'category': 'strings',
                'difficulty': 'easy',
                'template_code': 'def isPalindrome(s):\n    pass',
                'solution_code': 'def isPalindrome(s):\n    cleaned = "".join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]',
                'explanation': 'Filter and compare with reverse.',
                'test_cases': [
                    {'input': {'s': "A man, a plan, a canal: Panama"}, 'output': True},
                ]
            },
            {
                'title': 'Longest Substring Without Repeating Characters',
                'description': 'Find length of longest substring without repeating characters.',
                'topic': 'dsa',
                'category': 'strings',
                'difficulty': 'medium',
                'template_code': 'def lengthOfLongestSubstring(s):\n    pass',
                'solution_code': 'def lengthOfLongestSubstring(s):\n    char_map = {}\n    max_len = start = 0\n    for i, char in enumerate(s):\n        if char in char_map:\n            start = max(start, char_map[char] + 1)\n        char_map[char] = i\n        max_len = max(max_len, i - start + 1)\n    return max_len',
                'explanation': 'Sliding window with hash map.',
                'test_cases': [
                    {'input': {'s': "abcabcbb"}, 'output': 3},
                ]
            },
            {
                'title': 'Group Anagrams',
                'description': 'Group anagrams together from list of strings.',
                'topic': 'dsa',
                'category': 'strings',
                'difficulty': 'medium',
                'template_code': 'def groupAnagrams(strs):\n    pass',
                'solution_code': 'def groupAnagrams(strs):\n    from collections import defaultdict\n    groups = defaultdict(list)\n    for s in strs:\n        groups["".join(sorted(s))].append(s)\n    return list(groups.values())',
                'explanation': 'Sort each string and use as key.',
                'test_cases': [
                    {'input': {'strs': ["eat", "tea", "ate", "bat"]}, 'output': [["eat", "tea", "ate"], ["bat"]]},
                ]
            },
            # Stack/Queue
            {
                'title': 'Valid Parentheses',
                'description': 'Determine if string with brackets is valid.',
                'topic': 'dsa',
                'category': 'queue_stack',
                'difficulty': 'easy',
                'template_code': 'def isValid(s):\n    pass',
                'solution_code': 'def isValid(s):\n    stack = []\n    mapping = {"): "(", "}": "{", "]": "["}\n    for char in s:\n        if char in mapping:\n            if not stack or stack[-1] != mapping[char]:\n                return False\n            stack.pop()\n        else:\n            stack.append(char)\n    return not stack',
                'explanation': 'Use stack for bracket matching.',
                'test_cases': [
                    {'input': {'s': '()'}, 'output': True},
                ]
            },
            # Linked List
            {
                'title': 'Reverse Linked List',
                'description': 'Reverse a singly linked list.',
                'topic': 'dsa',
                'category': 'linked_lists',
                'difficulty': 'easy',
                'template_code': 'def reverseList(head):\n    pass',
                'solution_code': 'def reverseList(head):\n    prev = None\n    while head:\n        next_tmp = head.next\n        head.next = prev\n        prev = head\n        head = next_tmp\n    return prev',
                'explanation': 'Reverse pointers iteratively.',
                'test_cases': [
                    {'input': {'head': [1, 2, 3]}, 'output': [3, 2, 1]},
                ]
            },
            # Trees
            {
                'title': 'Maximum Depth of Binary Tree',
                'description': 'Find maximum depth of binary tree.',
                'topic': 'dsa',
                'category': 'trees',
                'difficulty': 'easy',
                'template_code': 'def maxDepth(root):\n    pass',
                'solution_code': 'def maxDepth(root):\n    if not root:\n        return 0\n    return 1 + max(maxDepth(root.left), maxDepth(root.right))',
                'explanation': 'Recursive approach counting depth.',
                'test_cases': [
                    {'input': {'root': [3, 9, 20, None, None, 15, 7]}, 'output': 3},
                ]
            },
            # DP
            {
                'title': 'Climbing Stairs',
                'description': 'Count ways to climb n steps taking 1 or 2 steps at a time.',
                'topic': 'dsa',
                'category': 'dynamic_programming',
                'difficulty': 'easy',
                'template_code': 'def climbStairs(n):\n    pass',
                'solution_code': 'def climbStairs(n):\n    if n <= 2:\n        return n\n    dp = [0] * (n + 1)\n    dp[1], dp[2] = 1, 2\n    for i in range(3, n + 1):\n        dp[i] = dp[i-1] + dp[i-2]\n    return dp[n]',
                'explanation': 'Dynamic programming Fibonacci-like.',
                'test_cases': [
                    {'input': {'n': 3}, 'output': 3},
                ]
            },
            
            # ============== OOP QUESTIONS (25+) ==============
            {
                'title': 'Design a Stack',
                'description': 'Implement a stack with push, pop, top, and empty operations.',
                'topic': 'oop',
                'category': 'design',
                'difficulty': 'easy',
                'template_code': 'class Stack:\n    def __init__(self):\n        pass\n    def push(self, x):\n        pass\n    def pop(self):\n        pass\n    def top(self):\n        pass\n    def empty(self):\n        pass',
                'solution_code': 'class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, x):\n        self.items.append(x)\n    def pop(self):\n        return self.items.pop() if not self.empty() else None\n    def top(self):\n        return self.items[-1] if not self.empty() else None\n    def empty(self):\n        return len(self.items) == 0',
                'explanation': 'Use list as underlying storage.',
                'test_cases': [
                    {'input': {'ops': ["push 1", "push 2", "top"]}, 'output': 2},
                ]
            },
            {
                'title': 'Design a Queue',
                'description': 'Implement a queue with enqueue, dequeue, and peek operations.',
                'topic': 'oop',
                'category': 'design',
                'difficulty': 'easy',
                'template_code': 'class Queue:\n    def __init__(self):\n        pass\n    def enqueue(self, x):\n        pass\n    def dequeue(self):\n        pass\n    def peek(self):\n        pass',
                'solution_code': 'from collections import deque\nclass Queue:\n    def __init__(self):\n        self.items = deque()\n    def enqueue(self, x):\n        self.items.append(x)\n    def dequeue(self):\n        return self.items.popleft() if self.items else None\n    def peek(self):\n        return self.items[0] if self.items else None',
                'explanation': 'Use deque for O(1) operations.',
                'test_cases': [
                    {'input': {'ops': ["enqueue 1", "peek"]}, 'output': 1},
                ]
            },
            {
                'title': 'Implement LRU Cache',
                'description': 'Design an LRU (Least Recently Used) cache.',
                'topic': 'oop',
                'category': 'design',
                'difficulty': 'medium',
                'template_code': 'class LRUCache:\n    def __init__(self, capacity):\n        pass\n    def get(self, key):\n        pass\n    def put(self, key, value):\n        pass',
                'solution_code': 'from collections import OrderedDict\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cache = OrderedDict()\n        self.capacity = capacity\n    def get(self, key):\n        if key in self.cache:\n            self.cache.move_to_end(key)\n            return self.cache[key]\n        return -1\n    def put(self, key, value):\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.capacity:\n            self.cache.popitem(last=False)',
                'explanation': 'Use OrderedDict to maintain insertion order.',
                'test_cases': [
                    {'input': {'capacity': 2, 'ops': ["put 1 1", "put 2 2", "get 1"]}, 'output': 1},
                ]
            },
            {
                'title': 'Class Inheritance',
                'description': 'Implement inheritance hierarchy: Animal > Dog > Puppy',
                'topic': 'oop',
                'category': 'inheritance',
                'difficulty': 'easy',
                'template_code': 'class Animal:\n    pass\nclass Dog(Animal):\n    pass\nclass Puppy(Dog):\n    pass',
                'solution_code': 'class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return "Some sound"\nclass Dog(Animal):\n    def speak(self):\n        return "Woof"\nclass Puppy(Dog):\n    def speak(self):\n        return "Yip"',
                'explanation': 'Method overriding in inheritance chain.',
                'test_cases': [
                    {'input': {'type': 'Puppy'}, 'output': 'Yip'},
                ]
            },
            {
                'title': 'Abstract Base Class',
                'description': 'Create abstract class with abstract methods.',
                'topic': 'oop',
                'category': 'abstraction',
                'difficulty': 'medium',
                'template_code': 'from abc import ABC, abstractmethod\nclass Shape(ABC):\n    pass',
                'solution_code': 'from abc import ABC, abstractmethod\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        pass\nclass Circle(Shape):\n    def __init__(self, r):\n        self.r = r\n    def area(self):\n        return 3.14 * self.r ** 2',
                'explanation': 'Use ABC and abstractmethod decorator.',
                'test_cases': [
                    {'input': {'shape': 'Circle', 'r': 5}, 'output': 78.5},
                ]
            },
            {
                'title': 'Encapsulation with Properties',
                'description': 'Implement getters and setters using properties.',
                'topic': 'oop',
                'category': 'encapsulation',
                'difficulty': 'easy',
                'template_code': 'class Person:\n    def __init__(self, age):\n        self._age = age\n    @property\n    def age(self):\n        pass\n    @age.setter\n    def age(self, value):\n        pass',
                'solution_code': 'class Person:\n    def __init__(self, age):\n        self._age = age\n    @property\n    def age(self):\n        return self._age\n    @age.setter\n    def age(self, value):\n        if value < 0:\n            raise ValueError("Age cannot be negative")\n        self._age = value',
                'explanation': 'Use @property decorator for encapsulation.',
                'test_cases': [
                    {'input': {'initial_age': 25, 'set_age': 30}, 'output': 30},
                ]
            },
            
            # ============== DATABASE QUESTIONS (25+) ==============
            {
                'title': 'SQL SELECT Basic',
                'description': 'Retrieve all records from a table.',
                'topic': 'dbs',
                'category': 'sql',
                'difficulty': 'easy',
                'template_code': 'SELECT -- your query here\nFROM users',
                'solution_code': 'SELECT * FROM users',
                'explanation': 'Basic SELECT statement with wildcard.',
                'test_cases': [
                    {'input': {'table': 'users'}, 'output': 'All user records'},
                ]
            },
            {
                'title': 'SQL WHERE Clause',
                'description': 'Retrieve records matching specific condition.',
                'topic': 'dbs',
                'category': 'sql',
                'difficulty': 'easy',
                'template_code': 'SELECT * FROM users\nWHERE -- your condition',
                'solution_code': 'SELECT * FROM users\nWHERE age > 18',
                'explanation': 'Filter rows using WHERE clause.',
                'test_cases': [
                    {'input': {'condition': 'age > 18'}, 'output': 'Adult users'},
                ]
            },
            {
                'title': 'SQL JOIN',
                'description': 'Combine data from two tables using JOIN.',
                'topic': 'dbs',
                'category': 'sql',
                'difficulty': 'medium',
                'template_code': 'SELECT * FROM users\nJOIN orders -- complete the join',
                'solution_code': 'SELECT u.*, o.* FROM users u\nINNER JOIN orders o ON u.id = o.user_id',
                'explanation': 'Use INNER JOIN to combine matching records.',
                'test_cases': [
                    {'input': {'type': 'INNER JOIN'}, 'output': 'User-order combinations'},
                ]
            },
            {
                'title': 'SQL GROUP BY',
                'description': 'Group rows and aggregate data.',
                'topic': 'dbs',
                'category': 'sql',
                'difficulty': 'medium',
                'template_code': 'SELECT category, COUNT(*)\nFROM products\nGROUP BY -- complete',
                'solution_code': 'SELECT category, COUNT(*) as count\nFROM products\nGROUP BY category',
                'explanation': 'GROUP BY aggregates data by column values.',
                'test_cases': [
                    {'input': {'group_column': 'category'}, 'output': 'Grouped counts'},
                ]
            },
            {
                'title': 'Database Normalization',
                'description': 'Explain First Normal Form (1NF).',
                'topic': 'dbs',
                'category': 'design',
                'difficulty': 'medium',
                'template_code': '# Describe 1NF requirements',
                'solution_code': '# 1NF requirements:\n# 1. Atomicity - each column has single value\n# 2. No repeating groups\n# 3. Primary key exists\n# Example: user_id, first_name, last_name (atomic)',
                'explanation': '1NF eliminates repeating groups and ensures atomic values.',
                'test_cases': [
                    {'input': {'form': '1NF'}, 'output': 'Atomic values, no repeating groups'},
                ]
            },
            {
                'title': 'ACID Properties',
                'description': 'Explain ACID properties in databases.',
                'topic': 'dbs',
                'category': 'concepts',
                'difficulty': 'medium',
                'template_code': '# Define ACID properties',
                'solution_code': '# ACID Properties:\n# Atomicity: All or nothing\n# Consistency: Valid state to valid state\n# Isolation: Concurrent transactions dont interfere\n# Durability: Committed data persists',
                'explanation': 'ACID ensures reliable database transactions.',
                'test_cases': [
                    {'input': {'property': 'ACID'}, 'output': 'Transaction guarantees'},
                ]
            },
            
            # ============== FUNCTIONAL PROGRAMMING QUESTIONS (20+) ==============
            {
                'title': 'Map Function',
                'description': 'Apply function to each element of iterable.',
                'topic': 'pf',
                'category': 'functional_concepts',
                'difficulty': 'easy',
                'template_code': 'numbers = [1, 2, 3, 4]\nresult = # map operation',
                'solution_code': 'numbers = [1, 2, 3, 4]\nresult = list(map(lambda x: x * 2, numbers))\n# or\nresult = [x * 2 for x in numbers]',
                'explanation': 'Map applies function to each element.',
                'test_cases': [
                    {'input': {'list': [1, 2, 3]}, 'output': [2, 4, 6]},
                ]
            },
            {
                'title': 'Filter Function',
                'description': 'Filter elements based on predicate.',
                'topic': 'pf',
                'category': 'functional_concepts',
                'difficulty': 'easy',
                'template_code': 'numbers = [1, 2, 3, 4, 5]\nresult = # filter even numbers',
                'solution_code': 'numbers = [1, 2, 3, 4, 5]\nresult = list(filter(lambda x: x % 2 == 0, numbers))\n# or\nresult = [x for x in numbers if x % 2 == 0]',
                'explanation': 'Filter keeps elements matching predicate.',
                'test_cases': [
                    {'input': {'list': [1, 2, 3, 4]}, 'output': [2, 4]},
                ]
            },
            {
                'title': 'Reduce Function',
                'description': 'Accumulate values using reducer function.',
                'topic': 'pf',
                'category': 'functional_concepts',
                'difficulty': 'medium',
                'template_code': 'from functools import reduce\nnumbers = [1, 2, 3, 4]\nresult = # sum using reduce',
                'solution_code': 'from functools import reduce\nnumbers = [1, 2, 3, 4]\nresult = reduce(lambda a, b: a + b, numbers)\n# result = 10',
                'explanation': 'Reduce accumulates values left to right.',
                'test_cases': [
                    {'input': {'list': [1, 2, 3, 4]}, 'output': 10},
                ]
            },
            {
                'title': 'Pure Functions',
                'description': 'Explain pure functions and give example.',
                'topic': 'pf',
                'category': 'concepts',
                'difficulty': 'easy',
                'template_code': '# Pure vs Impure function\ndef add(a, b):\n    return a + b',
                'solution_code': '# Pure function: same input always gives same output\n# No side effects (doesnt modify external state)\ndef add(a, b):\n    return a + b\n\n# Not pure (modifies external state):\nglobal_sum = 0\ndef add_impure(a, b):\n    global global_sum\n    global_sum += a + b\n    return global_sum',
                'explanation': 'Pure functions are predictable and testable.',
                'test_cases': [
                    {'input': {'a': 2, 'b': 3}, 'output': 5},
                ]
            },
            {
                'title': 'Higher Order Functions',
                'description': 'Function that takes or returns functions.',
                'topic': 'pf',
                'category': 'advanced',
                'difficulty': 'medium',
                'template_code': 'def multiplier(n):\n    def inner(x):\n        return x * n\n    return inner',
                'solution_code': 'def multiplier(n):\n    def inner(x):\n        return x * n\n    return inner\n\ntimes_two = multiplier(2)\nresult = times_two(5)  # returns 10',
                'explanation': 'Higher order functions enable powerful abstractions.',
                'test_cases': [
                    {'input': {'n': 2, 'x': 5}, 'output': 10},
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
            self.style.SUCCESS(f'\nSuccessfully seeded database with {len(sample_questions)} questions!')
        )
        self.stdout.write(
            self.style.WARNING(f'\nNote: Currently {len(sample_questions)} questions. To reach 500+ per category,\nadd more questions to each topic in this file.')
        )
