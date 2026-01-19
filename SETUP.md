# Interview Prep Quiz Platform - Installation & Setup Guide

## 🚀 Quick Start (15 minutes)

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL (optional, SQLite works for development)
- Git

### Backend Setup

```bash
cd backend

# 1. Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment variables
cp .env.example .env

# Edit .env with your settings (or just use defaults for development)

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (for Django admin)
python manage.py createsuperuser
# Enter username, email, password when prompted

# 6. Seed sample questions
python manage.py seed_questions

# 7. Start development server
python manage.py runserver
```

✅ Backend is now running at `http://localhost:8000`
- API: `http://localhost:8000/api/`
- Admin: `http://localhost:8000/admin/`

### Frontend Setup

In a new terminal:

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Setup environment variables
cp .env.example .env

# Edit .env with your Google OAuth Client ID (optional for now)

# 3. Start development server
npm start
```

✅ Frontend is now running at `http://localhost:3000`

## 📋 Setting Up Google OAuth (Optional)

To enable Google login:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials (Web application)
5. Add `http://localhost:3000` to Authorized origins
6. Copy your Client ID

Then update:
- Frontend `.env`: `REACT_APP_GOOGLE_CLIENT_ID=your-client-id`
- Backend `.env`: `GOOGLE_OAUTH_CLIENT_ID=your-client-id`, `GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret`

## 🗄️ Database Setup

### Using PostgreSQL (Recommended for production)

1. Install PostgreSQL
2. Create database:
```bash
createdb interview_quiz
```

3. Update backend `.env`:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=interview_quiz
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

4. Run migrations:
```bash
python manage.py migrate
```

### Using SQLite (Default for development)

SQLite is already configured by default. No additional setup needed.

## 📊 Seeding Questions

The platform comes with a sample questions seeding script. To add custom questions:

1. Create a `questions.json` file with your questions
2. Modify `backend/quiz_app/management/commands/seed_questions.py`
3. Run: `python manage.py seed_questions`

Or use Django admin to add questions manually at `/admin/`

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔍 Project File Structure Explained

### Backend (`/backend`)
```
config/           # Django configuration
├── settings.py   # Main settings
├── urls.py       # URL routing
├── wsgi.py       # WSGI app for deployment
└── celery.py     # Task scheduling

quiz_app/         # Main app
├── models.py     # Database models (Question, Quiz, etc.)
├── views.py      # API endpoints
├── serializers.py # Data serialization
├── admin.py      # Django admin config
├── signals.py    # Auto-create user profiles
└── management/
    └── commands/
        └── seed_questions.py  # Populate initial data

requirements.txt  # Python dependencies
manage.py         # Django management script
Procfile          # Deployment configuration
```

### Frontend (`/frontend`)
```
src/
├── components/    # Reusable React components
│   ├── QuestionCard.js
│   ├── StatsCard.js
│   ├── Timer.js
│   ├── Navigation.js
│   └── ...
├── pages/         # Page components
│   ├── Home.js
│   ├── Dashboard.js
│   ├── QuizInterface.js
│   ├── Leaderboard.js
│   └── ...
├── services/      # API integration
│   └── api.js     # Axios instance and API calls
├── context/       # React Context
│   └── AuthContext.js  # Authentication state
├── App.js         # Main app component
└── index.js       # Entry point

public/
└── index.html     # HTML template

package.json      # npm dependencies
tailwind.config.js # Tailwind CSS config
.env              # Environment variables
```

## 🌐 API Quick Reference

### Questions
```
GET  /api/questions/                 # List all
GET  /api/questions/{id}/            # Get one
GET  /api/questions/by_category/     # Group by category
GET  /api/questions/by_difficulty/   # Group by difficulty
```

### Quizzes
```
GET  /api/quizzes/                   # List all
GET  /api/quizzes/{id}/              # Get with questions
POST /api/quizzes/{id}/start/        # Start new session
GET  /api/quizzes/by_type/?type=practice
```

### Sessions (Quiz Attempts)
```
GET  /api/sessions/                  # User's sessions
GET  /api/sessions/{id}/             # Session details
POST /api/sessions/{id}/submit_answer/ # Submit answer
POST /api/sessions/{id}/finish/      # Complete quiz
```

### User
```
GET  /api/profile/me/                # User profile
GET  /api/bookmarks/                 # Saved questions
POST /api/bookmarks/                 # Save/unsave question
GET  /api/leaderboard/               # Rankings
```

## 🐛 Common Issues & Solutions

### Port Already in Use
```bash
# Backend (change port)
python manage.py runserver 8001

# Frontend (change port)
PORT=3001 npm start
```

### Database Errors
```bash
# Reset database
python manage.py flush
python manage.py migrate
python manage.py seed_questions
```

### CORS Issues
- Frontend running on wrong port?
- Check `CORS_ALLOWED_ORIGINS` in backend `settings.py`
- Add your frontend URL if needed

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## 🚀 Deployment

### Deploy Backend to Render

1. Create `Procfile` (already included)
2. Create account at [render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repository
5. Set environment variables in Render dashboard
6. Deploy

### Deploy Frontend to Vercel

1. Create account at [vercel.com](https://vercel.com)
2. Connect GitHub repository
3. Set environment variables
4. Deploy (auto-deploys on push)

## 📚 Learn More

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [REST API Guide](https://restfulapi.net/)
- [Tailwind CSS](https://tailwindcss.com/)

## ✅ Checklist

- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] Database migrations applied
- [ ] Sample questions seeded
- [ ] Google OAuth configured (optional)
- [ ] Environment variables set
- [ ] Created superuser account

## 🎯 Next Steps

1. Login to Django admin (`/admin`) to create quizzes
2. Browse questions at `/questions`
3. Start a quiz at `/quizzes`
4. Check dashboard for progress at `/dashboard`
5. View leaderboard at `/leaderboard`

---

Happy coding! 🚀
