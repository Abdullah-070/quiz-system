from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz_app.models import QuizSession, Answer, UserProfile, Leaderboard


class Command(BaseCommand):
    help = 'Delete all user data and quiz attempts while keeping questions'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n⚠️  DELETING USER DATA AND QUIZ ATTEMPTS...'))
        
        # Count records before deletion
        users_count = User.objects.count()
        sessions_count = QuizSession.objects.count()
        answers_count = Answer.objects.count()
        profiles_count = UserProfile.objects.count()
        leaderboard_count = Leaderboard.objects.count()
        
        self.stdout.write(f'\n📊 Records to delete:')
        self.stdout.write(f'  • Users: {users_count}')
        self.stdout.write(f'  • Quiz Sessions: {sessions_count}')
        self.stdout.write(f'  • Answers: {answers_count}')
        self.stdout.write(f'  • User Profiles: {profiles_count}')
        self.stdout.write(f'  • Leaderboard Entries: {leaderboard_count}')
        
        # Confirm deletion
        confirm = input('\n⚠️  This will permanently delete all user and quiz data. Continue? (yes/no): ')
        
        if confirm.lower() != 'yes':
            self.stdout.write(self.style.ERROR('❌ Deletion cancelled'))
            return
        
        # Delete in correct order (respecting foreign keys)
        self.stdout.write('\n🗑️  Deleting data...')
        
        Answer.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('  ✓ Deleted all answers'))
        
        QuizSession.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('  ✓ Deleted all quiz sessions'))
        
        Leaderboard.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('  ✓ Deleted all leaderboard entries'))
        
        UserProfile.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('  ✓ Deleted all user profiles'))
        
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('  ✓ Deleted all users'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ All user and quiz attempt data deleted!'))
        self.stdout.write(self.style.WARNING('✓ Questions remain intact\n'))
