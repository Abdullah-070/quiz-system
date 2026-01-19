from django.contrib.auth.models import User
from quiz_app.models import UserProfile


def create_or_update_user_from_google(user_data):
    """
    Create or update user from Google OAuth data
    """
    email = user_data.get('email')
    first_name = user_data.get('given_name', '')
    last_name = user_data.get('family_name', '')
    
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email.split('@')[0],
            'first_name': first_name,
            'last_name': last_name,
        }
    )
    
    if not created:
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    
    # Ensure profile exists
    UserProfile.objects.get_or_create(user=user)
    
    return user
