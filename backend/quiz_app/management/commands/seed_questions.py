from django.core.management.base import BaseCommand
import json
from quiz_app.models import Question


class Command(BaseCommand):
    help = 'Seed database with initial questions'
    
    def handle(self, *args, **options):
        # Sample data structure - comprehensive coding interview questions
        sample_questions = [
            # Arrays
            {
                'title': 'Two Sum',
                'description': 'Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'easy',
                'template_code': 'def twoSum(nums, target):\n    pass',
                'solution_code': 'def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen:\n            return [seen[target - num], i]\n        seen[num] = i\n    return []',
                'explanation': 'Use a hash map to store numbers we have seen. For each number, check if target - num exists in the hash map.',
                'test_cases': [
                    {'input': {'nums': [2, 7, 11, 15], 'target': 9}, 'output': [0, 1]},
                    {'input': {'nums': [3, 2, 4], 'target': 6}, 'output': [1, 2]},
                ]
            },
            {
                'title': 'Best Time to Buy and Sell Stock',
                'description': 'Given an array prices where prices[i] is the price of a given stock on the ith day, find the maximum profit you can achieve.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'easy',
                'template_code': 'def maxProfit(prices):\n    pass',
                'solution_code': 'def maxProfit(prices):\n    if not prices:\n        return 0\n    min_price = prices[0]\n    max_profit = 0\n    for price in prices[1:]:\n        max_profit = max(max_profit, price - min_price)\n        min_price = min(min_price, price)\n    return max_profit',
                'explanation': 'Track the minimum price seen so far and calculate profit at each price. Keep track of maximum profit.',
                'test_cases': [
                    {'input': {'prices': [7, 1, 5, 3, 6, 4]}, 'output': 5},
                    {'input': {'prices': [7, 6, 4, 3, 1]}, 'output': 0},
                ]
            },
            {
                'title': 'Contains Duplicate',
                'description': 'Given an integer array nums, return true if any value appears at least twice in the array.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'easy',
                'template_code': 'def containsDuplicate(nums):\n    pass',
                'solution_code': 'def containsDuplicate(nums):\n    return len(nums) != len(set(nums))',
                'explanation': 'Convert array to a set and compare lengths. If lengths differ, there are duplicates.',
                'test_cases': [
                    {'input': {'nums': [1, 2, 3, 1]}, 'output': True},
                    {'input': {'nums': [1, 2, 3, 4]}, 'output': False},
                ]
            },
            {
                'title': '3Sum',
                'description': 'Given an integer array nums, return all the triplets that sum to zero. The solution set must not contain duplicate triplets.',
                'topic': 'dsa',
                'category': 'arrays',
                'difficulty': 'medium',
                'template_code': 'def threeSum(nums):\n    pass',
                'solution_code': 'def threeSum(nums):\n    nums.sort()\n    result = []\n    n = len(nums)\n    for i in range(n-2):\n        if i > 0 and nums[i] == nums[i-1]:\n            continue\n        left, right = i+1, n-1\n        target = -nums[i]\n        while left < right:\n            s = nums[left] + nums[right]\n            if s == target:\n                result.append([nums[i], nums[left], nums[right]])\n                while left < right and nums[left] == nums[left+1]:\n                    left += 1\n                while left < right and nums[right] == nums[right-1]:\n                    right -= 1\n                left += 1\n                right -= 1\n            elif s < target:\n                left += 1\n            else:\n                right -= 1\n    return result',
                'explanation': 'Sort the array first. For each element, use two pointers to find two other elements that sum to zero.',
                'test_cases': [
                    {'input': {'nums': [-1, 0, 1, 2, -1, -4]}, 'output': [[-1, -1, 2], [-1, 0, 1]]},
                ]
            },
            # Strings
            {
                'title': 'Valid Palindrome',
                'description': 'Given a string s, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.',
                'topic': 'dsa',
                'category': 'strings',
                'difficulty': 'easy',
                'template_code': 'def isPalindrome(s):\n    pass',
                'solution_code': 'def isPalindrome(s):\n    cleaned = "".join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]',
                'explanation': 'Filter only alphanumeric characters, convert to lowercase, and check if it reads the same forwards and backwards.',
                'test_cases': [
                    {'input': {'s': "A man, a plan, a canal: Panama"}, 'output': True},
                    {'input': {'s': "race a car"}, 'output': False},
                ]
            },
            {
                'title': 'Longest Substring Without Repeating Characters',
                'description': 'Given a string s, find the length of the longest substring without repeating characters.',
                'topic': 'dsa',
                'category': 'strings',
                'difficulty': 'medium',
                'template_code': 'def lengthOfLongestSubstring(s):\n    pass',
                'solution_code': 'def lengthOfLongestSubstring(s):\n    char_map = {}\n    max_len = 0\n    start = 0\n    for i, char in enumerate(s):\n        if char in char_map and char_map[char] >= start:\n            start = char_map[char] + 1\n        char_map[char] = i\n        max_len = max(max_len, i - start + 1)\n    return max_len',
                'explanation': 'Use a sliding window approach with a hash map to track characters and their positions.',
                'test_cases': [
                    {'input': {'s': "abcabcbb"}, 'output': 3},
                    {'input': {'s': "bbbbb"}, 'output': 1},
                ]
            },
            # Stack/Queue
            {
                'title': 'Valid Parentheses',
                'description': 'Given a string s containing just the characters (), {}, [], determine if the input string is valid.',
                'topic': 'dsa',
                'category': 'queue_stack',
                'difficulty': 'easy',
                'template_code': 'def isValid(s):\n    pass',
                'solution_code': 'def isValid(s):\n    stack = []\n    mapping = {"): "(", "}": "{", "]": "["}\n    for char in s:\n        if char in mapping:\n            if not stack or stack[-1] != mapping[char]:\n                return False\n            stack.pop()\n        else:\n            stack.append(char)\n    return not stack',
                'explanation': 'Use a stack to keep track of opening brackets. When encountering closing bracket, check if it matches the most recent opening bracket.',
                'test_cases': [
                    {'input': {'s': '()'}, 'output': True},
                    {'input': {'s': '()[]{}'}, 'output': True},
                    {'input': {'s': '(]'}, 'output': False},
                ]
            },
            # Linked List
            {
                'title': 'Reverse Linked List',
                'description': 'Given the head of a singly linked list, reverse the list and return the reversed list.',
                'topic': 'dsa',
                'category': 'linked_lists',
                'difficulty': 'easy',
                'template_code': 'def reverseList(head):\n    pass',
                'solution_code': 'def reverseList(head):\n    prev = None\n    curr = head\n    while curr:\n        next_temp = curr.next\n        curr.next = prev\n        prev = curr\n        curr = next_temp\n    return prev',
                'explanation': 'Iterate through the list, reversing pointers as you go. Keep track of previous node.',
                'test_cases': [
                    {'input': {'head': [1, 2, 3]}, 'output': [3, 2, 1]},
                ]
            },
            # Binary Tree
            {
                'title': 'Maximum Depth of Binary Tree',
                'description': 'Given the root of a binary tree, return its maximum depth. Maximum depth is the number of nodes along the longest path.',
                'topic': 'dsa',
                'category': 'trees',
                'difficulty': 'easy',
                'template_code': 'def maxDepth(root):\n    pass',
                'solution_code': 'def maxDepth(root):\n    if not root:\n        return 0\n    return 1 + max(maxDepth(root.left), maxDepth(root.right))',
                'explanation': 'Use recursion. The depth is 1 plus the maximum depth of either subtree.',
                'test_cases': [
                    {'input': {'root': '[3, 9, 20, null, null, 15, 7]'}, 'output': 3},
                ]
            },
            # Dynamic Programming
            {
                'title': 'Climbing Stairs',
                'description': 'You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps. How many ways to climb to the top?',
                'topic': 'dsa',
                'category': 'dynamic_programming',
                'difficulty': 'easy',
                'template_code': 'def climbStairs(n):\n    pass',
                'solution_code': 'def climbStairs(n):\n    if n == 1:\n        return 1\n    if n == 2:\n        return 2\n    dp = [0] * (n + 1)\n    dp[1] = 1\n    dp[2] = 2\n    for i in range(3, n + 1):\n        dp[i] = dp[i-1] + dp[i-2]\n    return dp[n]',
                'explanation': 'Dynamic programming problem. To reach step n, you can come from step n-1 or n-2.',
                'test_cases': [
                    {'input': {'n': 2}, 'output': 2},
                    {'input': {'n': 3}, 'output': 3},
                ]
            },
            {
                'title': 'House Robber',
                'description': 'You are a professional robber. Given an array of non-negative integers representing amount of money in each house, determine maximum money you can rob.',
                'topic': 'dsa',
                'category': 'dynamic_programming',
                'difficulty': 'medium',
                'template_code': 'def rob(nums):\n    pass',
                'solution_code': 'def rob(nums):\n    if not nums:\n        return 0\n    if len(nums) == 1:\n        return nums[0]\n    dp = [0] * len(nums)\n    dp[0] = nums[0]\n    dp[1] = max(nums[0], nums[1])\n    for i in range(2, len(nums)):\n        dp[i] = max(dp[i-1], dp[i-2] + nums[i])\n    return dp[-1]',
                'explanation': 'DP where dp[i] is max money robbing houses up to i. Either rob current + max from i-2, or skip current.',
                'test_cases': [
                    {'input': {'nums': [1, 2, 3, 1]}, 'output': 4},
                    {'input': {'nums': [2, 7, 9, 3]}, 'output': 9},
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
            self.style.SUCCESS('Successfully seeded database with questions')
        )
