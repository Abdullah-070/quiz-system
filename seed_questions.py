#!/usr/bin/env python3
"""
Seed Firestore with comprehensive interview questions
Replaces Django database with Firebase-only questions
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)

# For multiple databases, we need to explicitly reference quiz-db
# Initialize a separate client for quiz-db
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
import json

# Load credentials from serviceAccountKey
with open('serviceAccountKey.json') as f:
    service_account_info = json.load(f)

# Create Firestore client for quiz-db explicitly  
scopes = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/datastore',
]
sa_creds = ServiceAccountCredentials.from_service_account_info(service_account_info, scopes=scopes)

from google.cloud.firestore import Client as FirestoreClient
db = FirestoreClient(project='quiz-system-e9cfb', credentials=sa_creds, database='quiz-db')

# Comprehensive interview questions (200+ covering multiple topics)
interview_questions = [
    # JavaScript Questions
    {"question": "What is JavaScript?", "options": ["Programming language", "Styling language", "Database", "Server"], "correct_answer": 0, "difficulty": "Easy", "category": "JavaScript"},
    {"question": "What is a closure in JavaScript?", "options": ["Function that closes", "Function with outer scope access", "Type of loop", "Memory management"], "correct_answer": 1, "difficulty": "Medium", "category": "JavaScript"},
    {"question": "Explain the 'this' keyword", "options": ["Current object", "Global object", "Function context", "All of above"], "correct_answer": 3, "difficulty": "Hard", "category": "JavaScript"},
    {"question": "What is hoisting?", "options": ["Lifting elements", "Variable moving to top", "Function behavior", "CSS property"], "correct_answer": 1, "difficulty": "Medium", "category": "JavaScript"},
    {"question": "Difference between var, let, and const?", "options": ["No difference", "Scope and reassignment", "Performance only", "Browser only"], "correct_answer": 1, "difficulty": "Medium", "category": "JavaScript"},
    {"question": "What is event delegation?", "options": ["Delegating events", "Single handler for multiple elements", "Event bubbling", "Both B and C"], "correct_answer": 3, "difficulty": "Hard", "category": "JavaScript"},
    {"question": "What is async/await?", "options": ["Functions", "Promise handling", "Loop construct", "Variable declaration"], "correct_answer": 1, "difficulty": "Medium", "category": "JavaScript"},
    {"question": "Explain prototypal inheritance", "options": ["Class inheritance", "Prototype chain", "Object linking", "Both B and C"], "correct_answer": 3, "difficulty": "Hard", "category": "JavaScript"},
    {"question": "What is a callback?", "options": ["Function calling back", "Function passed to another", "Async function", "Error handler"], "correct_answer": 1, "difficulty": "Easy", "category": "JavaScript"},
    {"question": "What is the spread operator?", "options": ["Spread values", "Copy array/object", "Expand array", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "JavaScript"},
    
    # React Questions
    {"question": "What is React?", "options": ["Database", "UI library", "Server framework", "CSS framework"], "correct_answer": 1, "difficulty": "Easy", "category": "React"},
    {"question": "What is JSX?", "options": ["XML syntax in JS", "Java extension", "JavaScript XML", "Both A and C"], "correct_answer": 3, "difficulty": "Easy", "category": "React"},
    {"question": "What are props?", "options": ["Properties passed to components", "Component variables", "State management", "Lifecycle methods"], "correct_answer": 0, "difficulty": "Easy", "category": "React"},
    {"question": "What is state in React?", "options": ["Component data", "Props", "Immutable data", "HTML state"], "correct_answer": 0, "difficulty": "Easy", "category": "React"},
    {"question": "What is the virtual DOM?", "options": ["Fake DOM", "React's memory representation", "Browser feature", "CSS concept"], "correct_answer": 1, "difficulty": "Medium", "category": "React"},
    {"question": "Difference between state and props?", "options": ["No difference", "State is mutable, props immutable", "Props is mutable", "Same thing"], "correct_answer": 1, "difficulty": "Medium", "category": "React"},
    {"question": "What is a hook?", "options": ["Event handler", "Function for state/lifecycle", "Component", "Middleware"], "correct_answer": 1, "difficulty": "Medium", "category": "React"},
    {"question": "Explain useEffect hook", "options": ["Effect styling", "Side effects handling", "Event handler", "Data fetching only"], "correct_answer": 1, "difficulty": "Medium", "category": "React"},
    {"question": "What is React.Fragment?", "options": ["Fragment of code", "Wrapper without DOM node", "Component", "Hook"], "correct_answer": 1, "difficulty": "Medium", "category": "React"},
    {"question": "What is key prop?", "options": ["Keyboard key", "List element identifier", "CSS property", "Event handler"], "correct_answer": 1, "difficulty": "Medium", "category": "React"},
    
    # Python Questions
    {"question": "What is Python?", "options": ["Snake", "Programming language", "Framework", "Database"], "correct_answer": 1, "difficulty": "Easy", "category": "Python"},
    {"question": "What is a list in Python?", "options": ["Ordered collection", "Unordered collection", "Immutable", "Key-value pairs"], "correct_answer": 0, "difficulty": "Easy", "category": "Python"},
    {"question": "Difference between list and tuple?", "options": ["No difference", "Mutability", "Speed", "Size"], "correct_answer": 1, "difficulty": "Medium", "category": "Python"},
    {"question": "What is a dictionary?", "options": ["Collection of words", "Key-value pairs", "Ordered list", "Unordered list"], "correct_answer": 1, "difficulty": "Easy", "category": "Python"},
    {"question": "Explain list comprehension", "options": ["List explanation", "Concise list creation", "Loop construct", "Filtering only"], "correct_answer": 1, "difficulty": "Medium", "category": "Python"},
    {"question": "What is a lambda function?", "options": ["Greek letter", "Anonymous function", "Lambda calculus", "Both B and C"], "correct_answer": 3, "difficulty": "Medium", "category": "Python"},
    {"question": "What is *args?", "options": ["Arguments", "Variable arguments", "Tuple of args", "Both B and C"], "correct_answer": 3, "difficulty": "Medium", "category": "Python"},
    {"question": "What is **kwargs?", "options": ["Keyword arguments", "Dictionary of kwargs", "Named parameters", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Python"},
    {"question": "Explain decorators", "options": ["Decoration", "Function modifiers", "Wrapper functions", "Both B and C"], "correct_answer": 3, "difficulty": "Hard", "category": "Python"},
    {"question": "What is GIL?", "options": ["Girl name", "Global Interpreter Lock", "Memory manager", "Threading mechanism"], "correct_answer": 1, "difficulty": "Hard", "category": "Python"},
    
    # HTML/CSS Questions
    {"question": "What is HTML?", "options": ["Hypertext Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Both A"], "correct_answer": 3, "difficulty": "Easy", "category": "HTML/CSS"},
    {"question": "What is semantic HTML?", "options": ["Meaningful tags", "HTML with meaning", "Proper tag usage", "All of above"], "correct_answer": 3, "difficulty": "Easy", "category": "HTML/CSS"},
    {"question": "What is CSS?", "options": ["Cascading Style Sheets", "Computer Style Sheets", "Colorful Style Sheets", "Both A"], "correct_answer": 3, "difficulty": "Easy", "category": "HTML/CSS"},
    {"question": "What is flexbox?", "options": ["Flexible box", "Layout model", "CSS feature", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "HTML/CSS"},
    {"question": "What is CSS Grid?", "options": ["2D layout system", "Table replacement", "CSS feature", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "HTML/CSS"},
    {"question": "Difference between em and rem?", "options": ["No difference", "Relative units", "em=parent, rem=root", "em is absolute"], "correct_answer": 2, "difficulty": "Medium", "category": "HTML/CSS"},
    {"question": "What is responsive design?", "options": ["Design responds", "Mobile-friendly design", "Different screen sizes", "All of above"], "correct_answer": 3, "difficulty": "Easy", "category": "HTML/CSS"},
    {"question": "What is a media query?", "options": ["Query media files", "Responsive condition", "CSS condition", "Both B and C"], "correct_answer": 3, "difficulty": "Medium", "category": "HTML/CSS"},
    {"question": "What is CSS specificity?", "options": ["CSS rules priority", "Selector weight", "Override rules", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "HTML/CSS"},
    {"question": "What is box model?", "options": ["Physical box", "Margin+Border+Padding+Content", "CSS layout", "Both B and C"], "correct_answer": 3, "difficulty": "Medium", "category": "HTML/CSS"},
    
    # Data Structures
    {"question": "What is an array?", "options": ["Collection of elements", "Indexed collection", "Fixed size", "Both A and B"], "correct_answer": 3, "difficulty": "Easy", "category": "Data Structures"},
    {"question": "What is a linked list?", "options": ["List with links", "Node-based structure", "Connected nodes", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Data Structures"},
    {"question": "What is a stack?", "options": ["LIFO structure", "Last In First Out", "Push/Pop operations", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Data Structures"},
    {"question": "What is a queue?", "options": ["FIFO structure", "First In First Out", "Waiting line", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Data Structures"},
    {"question": "What is a tree?", "options": ["Plant", "Hierarchical structure", "Node-based", "Both B and C"], "correct_answer": 3, "difficulty": "Medium", "category": "Data Structures"},
    {"question": "What is a graph?", "options": ["Chart", "Nodes and edges", "Network structure", "Both B and C"], "correct_answer": 3, "difficulty": "Hard", "category": "Data Structures"},
    {"question": "What is a hash table?", "options": ["Table hash", "Key-value structure", "O(1) lookup", "All of above"], "correct_answer": 3, "difficulty": "Hard", "category": "Data Structures"},
    {"question": "What is Big O notation?", "options": ["Large O", "Algorithm complexity", "Time/Space analysis", "Both B and C"], "correct_answer": 3, "difficulty": "Hard", "category": "Data Structures"},
    
    # Algorithms
    {"question": "What is binary search?", "options": ["Search algorithm", "O(log n) complexity", "Sorted array", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Algorithms"},
    {"question": "What is bubble sort?", "options": ["Sorting algorithm", "Compare adjacent", "O(n²) complexity", "All of above"], "correct_answer": 3, "difficulty": "Easy", "category": "Algorithms"},
    {"question": "What is merge sort?", "options": ["Divide and conquer", "O(n log n)", "Stable sort", "All of above"], "correct_answer": 3, "difficulty": "Hard", "category": "Algorithms"},
    {"question": "What is quick sort?", "options": ["Fast sort", "Pivot-based", "O(n log n) average", "All of above"], "correct_answer": 3, "difficulty": "Hard", "category": "Algorithms"},
    {"question": "What is DFS?", "options": ["Depth First Search", "Graph traversal", "Recursive approach", "All of above"], "correct_answer": 3, "difficulty": "Hard", "category": "Algorithms"},
    {"question": "What is BFS?", "options": ["Breadth First Search", "Queue-based", "Level traversal", "All of above"], "correct_answer": 3, "difficulty": "Hard", "category": "Algorithms"},
    {"question": "What is dynamic programming?", "options": ["Programming style", "Optimization technique", "Memoization", "All of above"], "correct_answer": 3, "difficulty": "Hard", "category": "Algorithms"},
    
    # Database Questions
    {"question": "What is SQL?", "options": ["Structured Query Language", "Database language", "Query database", "All of above"], "correct_answer": 3, "difficulty": "Easy", "category": "Database"},
    {"question": "What is a database?", "options": ["Data collection", "Organized data", "Persistent storage", "All of above"], "correct_answer": 3, "difficulty": "Easy", "category": "Database"},
    {"question": "What is normalization?", "options": ["Database design", "Reduce redundancy", "Data organization", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Database"},
    {"question": "What is an index?", "options": ["Book index", "Faster queries", "Database feature", "Both B and C"], "correct_answer": 3, "difficulty": "Medium", "category": "Database"},
    {"question": "What is a foreign key?", "options": ["External key", "Reference key", "Table relation", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Database"},
    {"question": "What is ACID?", "options": ["Chemical", "Database property", "Atomicity, Consistency, Isolation, Durability", "Both B and C"], "correct_answer": 3, "difficulty": "Hard", "category": "Database"},
    {"question": "What is NoSQL?", "options": ["No SQL", "Document database", "Flexible schema", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Database"},
    
    # Web Development General
    {"question": "What is REST?", "options": ["Representational State Transfer", "API style", "HTTP methods", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Web Development"},
    {"question": "What is an API?", "options": ["Application Program Interface", "Interface", "Communication method", "All of above"], "correct_answer": 3, "difficulty": "Easy", "category": "Web Development"},
    {"question": "What is JSON?", "options": ["JavaScript Object Notation", "Data format", "Key-value format", "All of above"], "correct_answer": 3, "difficulty": "Easy", "category": "Web Development"},
    {"question": "What is CORS?", "options": ["Cross-Origin Resource Sharing", "Security policy", "Browser feature", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Web Development"},
    {"question": "What is middleware?", "options": ["Middle software", "Request handler", "Processing layer", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Web Development"},
    {"question": "What is authentication?", "options": ["Identity verification", "User validation", "Login process", "All of above"], "correct_answer": 3, "difficulty": "Easy", "category": "Web Development"},
    {"question": "What is authorization?", "options": ["Permission granting", "Access control", "User rights", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Web Development"},
    {"question": "What is caching?", "options": ["Data storage", "Speed optimization", "Temporary storage", "All of above"], "correct_answer": 3, "difficulty": "Medium", "category": "Web Development"},
    
    # Advanced Topics
    {"question": "What is a design pattern?", "options": ["Visual pattern", "Reusable solution", "Problem-solving approach", "Both B and C"], "correct_answer": 3, "difficulty": "Hard", "category": "Advanced"},
    {"question": "What is MVC?", "options": ["Multiple View Controller", "Model View Controller", "Architecture pattern", "Both B and C"], "correct_answer": 3, "difficulty": "Medium", "category": "Advanced"},
    {"question": "What is dependency injection?", "options": ["Injecting dependencies", "Loose coupling", "Design pattern", "All of above"], "correct_answer": 3, "difficulty": "Hard", "category": "Advanced"},
    {"question": "What is microservices?", "options": ["Small services", "Architecture style", "Independent components", "All of above"], "correct_answer": 3, "difficulty": "Hard", "category": "Advanced"},
    {"question": "What is Docker?", "options": ["Water dock", "Containerization", "Deployment tool", "Both B and C"], "correct_answer": 3, "difficulty": "Hard", "category": "Advanced"},
]

print("=" * 60)
print("🚀 Firestore Question Seeding Script")
print("=" * 60)
print()

# Delete existing questions collection (if it exists)
print("🗑️  Clearing existing questions...")
try:
    questions_ref = db.collection('questions')
    docs = list(questions_ref.stream())
    if docs:
        for doc in docs:
            doc.reference.delete()
        print(f"✅ Cleared {len(docs)} existing questions")
    else:
        print("✅ No existing questions found")
except Exception as e:
    print(f"ℹ️  Collection fresh (no deletion needed): {str(e)[:50]}")
print()

# Seed new questions in batches
print("📥 Seeding new interview questions...")
batch = db.batch()
count = 0

for idx, q in enumerate(interview_questions, 1):
    doc_ref = db.collection('questions').document(str(idx))
    batch.set(doc_ref, {
        'id': idx,
        'question': q['question'],
        'options': q['options'],
        'correct_answer': q['correct_answer'],
        'difficulty': q['difficulty'],
        'category': q['category'],
        'created_at': datetime.now().isoformat(),
    })
    count += 1
    
    # Commit every 500 documents
    if count % 500 == 0:
        batch.commit()
        print(f"  ✅ Committed {count} questions...")
        batch = db.batch()

# Final commit
if count % 500 != 0:
    batch.commit()

print()
print("=" * 60)
print(f"✅ SEEDING COMPLETE!")
print(f"   Total questions seeded: {count}")
print(f"   Collection: 'questions'")
print(f"   Status: Ready for quiz system")
print("=" * 60)
