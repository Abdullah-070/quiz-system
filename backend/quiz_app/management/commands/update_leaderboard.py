from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from quiz_app.models import Leaderboard, QuizSession


class Command(BaseCommand):
    help = 'Calculate and update leaderboard rankings'
    
    def handle(self, *args, **options):
        now = timezone.now()
        periods_data = {
            'week': now - timedelta(days=7),
            'month': now - timedelta(days=30),
            'all_time': None
        }
        
        for period, start_date in periods_data.items():
            self.stdout.write(f"\n📊 Calculating {period.upper()} leaderboard...")
            
            # Get all users with completed quizzes in this period
            if period == 'all_time':
                sessions = QuizSession.objects.filter(status='completed')
            else:
                sessions = QuizSession.objects.filter(
                    status='completed',
                    time_ended__gte=start_date
                )
            
            # Get unique users
            user_ids = sessions.values_list('user_id', flat=True).distinct()
            
            # Calculate stats for each user
            leaderboard_entries = []
            for user_id in user_ids:
                if period == 'all_time':
                    user_sessions = QuizSession.objects.filter(user_id=user_id, status='completed')
                else:
                    user_sessions = QuizSession.objects.filter(
                        user_id=user_id,
                        status='completed',
                        time_ended__gte=start_date
                    )
                
                total_score = sum(s.total_score for s in user_sessions)
                total_questions = sum(s.total_questions for s in user_sessions)
                total_correct = sum(s.correct_answers for s in user_sessions)
                accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
                
                leaderboard_entries.append({
                    'user_id': user_id,
                    'score': total_score,
                    'questions_solved': total_questions,
                    'accuracy': accuracy
                })
            
            # Sort by score (descending)
            leaderboard_entries.sort(key=lambda x: x['score'], reverse=True)
            
            # Assign ranks and update database
            for rank, entry in enumerate(leaderboard_entries, 1):
                leaderboard, created = Leaderboard.objects.get_or_create(
                    user_id=entry['user_id'],
                    period=period,
                    defaults={
                        'rank': rank,
                        'score': entry['score'],
                        'questions_solved': entry['questions_solved'],
                        'accuracy': entry['accuracy']
                    }
                )
                
                if not created:
                    leaderboard.rank = rank
                    leaderboard.score = entry['score']
                    leaderboard.questions_solved = entry['questions_solved']
                    leaderboard.accuracy = entry['accuracy']
                    leaderboard.save()
            
            self.stdout.write(self.style.SUCCESS(f"✓ Updated {len(leaderboard_entries)} entries for {period}"))
        
        self.stdout.write(self.style.SUCCESS("\n✅ Leaderboard rankings updated!"))
