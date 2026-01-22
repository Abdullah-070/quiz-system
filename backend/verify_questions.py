import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz_app.models import Question

print("\n" + "="*80)
print("SAMPLE QUESTIONS FROM EACH CATEGORY - VERIFICATION")
print("="*80)

# Get sample questions from each category
categories = ['dsa', 'oop', 'dbs', 'pf']
for cat in categories:
    print(f"\n📚 {cat.upper()} - Sample Questions:")
    print("-" * 80)
    questions = Question.objects.filter(topic=cat)[:2]
    for q in questions:
        print(f"\nTitle: {q.title}")
        print(f"Description: {q.description[:120]}...")
        print(f"Solution Snippet: {q.solution_code[:120]}...")

print("\n" + "="*80)
total = Question.objects.count()
print(f"✓ Total Questions: {total}")
for cat in categories:
    count = Question.objects.filter(topic=cat).count()
    print(f"✓ {cat.upper()}: {count}")
print("="*80 + "\n")
