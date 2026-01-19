# Interview Prep Quiz Platform - Backend

Django REST Framework backend for the Interview Prep Quiz Platform.

## Features

- RESTful API for questions, quizzes, and user sessions
- User authentication with Google OAuth
- Question bank with DSA, OOP, PF, and Database topics
- Quiz management with multiple modes (practice, timed, mock)
- User progress tracking and analytics
- Leaderboard system with time periods
- Bookmark system for saved questions
- Signal-based user profile creation

## Setup

### Prerequisites
- Python 3.9+
- PostgreSQL (optional, SQLite for development)
- Redis (for Celery tasks, optional)

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Update `.env` with your settings:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.postgresql
DB_NAME=interview_quiz
DB_USER=postgres
DB_PASSWORD=your_password
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

5. Apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Seed initial questions:
```bash
python manage.py seed_questions
```

8. Run development server:
```bash
python manage.py runserver
```

Server runs at `http://localhost:8000`

## API Endpoints

### Questions
- `GET /api/questions/` - List all questions
- `GET /api/questions/{id}/` - Get question details
- `GET /api/questions/by_category/` - Questions grouped by category
- `GET /api/questions/by_difficulty/` - Questions grouped by difficulty

### Quizzes
- `GET /api/quizzes/` - List all quizzes
- `GET /api/quizzes/{id}/` - Get quiz details with questions
- `POST /api/quizzes/{id}/start/` - Start a new quiz session
- `GET /api/quizzes/by_type/?type=practice` - Get quizzes by type

### Sessions
- `GET /api/sessions/` - User's quiz sessions
- `GET /api/sessions/{id}/` - Session details with answers
- `POST /api/sessions/{id}/submit_answer/` - Submit answer to question
- `POST /api/sessions/{id}/finish/` - Complete quiz session

### Profile
- `GET /api/profile/me/` - Current user profile
- `PUT /api/profile/` - Update profile

### Bookmarks
- `GET /api/bookmarks/` - User's bookmarks
- `POST /api/bookmarks/` - Create/toggle bookmark
- `GET /api/bookmarks/is_bookmarked/?question_id=123` - Check if bookmarked

### Leaderboard
- `GET /api/leaderboard/?period=week` - Leaderboard by period
- `GET /api/leaderboard/top_performers/?period=week` - Top 10 performers

## Models

- **Question**: Stores coding questions with solutions
- **Quiz**: Collections of questions with settings
- **QuizSession**: User's quiz attempt with results
- **Answer**: Individual answer submissions
- **UserProfile**: User statistics and preferences
- **Bookmark**: Saved questions for later
- **Leaderboard**: Rankings by period

## Authentication

Uses Django Allauth with Google OAuth provider. Frontend receives Google token and exchanges it at `/auth/google/`.

## Seeding Questions

To import questions from JSON file:

```python
# In seed_questions.py management command
import json
with open('questions.json') as f:
    questions_data = json.load(f)
```

## Admin Panel

Access at `/admin/` with superuser credentials. Manage:
- Questions
- Quizzes
- User profiles
- Bookmarks
- Leaderboard

## Deployment

### Using Render:

1. Create `Procfile`:
```
web: gunicorn config.wsgi --log-file -
release: python manage.py migrate
```

2. Set environment variables in Render dashboard

3. Deploy from GitHub

### Using Heroku:

```bash
heroku create your-app-name
heroku config:set DJANGO_SETTINGS_MODULE=config.settings
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py seed_questions
```

## Database Schema

```
User (Django Auth)
├── UserProfile (one-to-one)
├── QuizSession (one-to-many)
│   ├── Answer (one-to-many)
│   └── Quiz (foreign key)
├── Bookmark (one-to-many)
│   └── Question (foreign key)
└── Leaderboard (one-to-many)

Question
├── QuizQuestion (through table)
└── Bookmark (many-to-many via Bookmark)

Quiz
├── QuizQuestion (one-to-many)
└── QuizSession (one-to-many)
```

## Testing

Run tests:
```bash
python manage.py test
```

## Future Improvements

- Code execution and test case validation
- Email notifications for inactivity
- Celery tasks for async operations
- Solution video integration
- Advanced analytics dashboard
- Discussion forum
