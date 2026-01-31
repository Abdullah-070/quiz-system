# Interview Quiz Platform - Complete Project

A full-stack web application for CS students to practice coding interview questions with features like timed quizzes, leaderboards, and progress tracking.

## 🎯 Features

### Quiz Modes
- **Practice Mode**: Unlimited time, no restrictions
- **Timed Quizzes**: 30-minute timed sessions
- **Mock Interviews**: Simulate real interview pace
- **Custom Quizzes**: Select difficulty, type, category

### Question Bank
- 500+ DSA (Data Structures & Algorithms)
- 500+ OOP (Object-Oriented Programming)  
- 500+ PF (Pattern Fundamentals)
- 500+ Database Systems questions

### Difficulty Levels
- Easy, Medium, Hard

### User Features
- 🔐 Google OAuth & Firebase authentication
- 📊 Dashboard with stats (questions solved, accuracy rate)
- 📌 Bookmarks for favorite questions
- 🏆 Weekly leaderboard
- 📧 Email notifications

## 🛠 Tech Stack

### Backend
- **Framework**: Django + Django REST Framework
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: Firebase
- **Deployment**: Railway/Render/Heroku

### Frontend
- **Framework**: React 18
- **Code Editor**: Ace Editor / Monaco
- **HTTP Client**: Axios
- **Database Client**: Supabase JS
- **Charting**: Recharts (for analytics)
- **Deployment**: Vercel/Netlify

### Infrastructure
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Firebase
- **Email**: Supabase (with Edge Functions)

## 📋 Project Structure

```
interview-quiz/
├── backend/                    # Django Backend
│   ├── config/                # Django settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/                  # Django apps
│   │   ├── users/            # User management
│   │   ├── questions/        # Question management
│   │   └── quizzes/          # Quiz logic
│   ├── manage.py
│   ├── requirements.txt
│   ├── seed_data.py          # Sample questions
│   └── .env.example
│
├── frontend/                   # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API & Firebase
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── .env.example
│
├── SETUP.md                   # Setup instructions
├── FIREBASE_SETUP.md         # Firebase guide
├── SUPABASE_SETUP.md         # Supabase guide
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL (via Supabase)
- Firebase Account
- GitHub (for deployment)

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env
# Edit .env with your credentials

# Run migrations
python manage.py migrate

# Seed sample data
python manage.py shell < seed_data.py

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Backend runs at: `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Copy and configure .env
cp .env.example .env
# Edit .env with your credentials

# Start development server
npm start
```

Frontend runs at: `http://localhost:3000`

## 📚 API Endpoints

### Users
- `POST /api/users/register/` - Register new user
- `GET /api/users/{id}/` - Get user profile
- `GET /api/users/{id}/stats/` - Get user statistics

### Questions
- `GET /api/questions/` - Get all questions (with filters)
- `GET /api/questions/{id}/` - Get single question
- `GET /api/questions/random/` - Get random question
- `GET /api/questions/categories/` - Get all categories

### Quizzes
- `POST /api/quiz-sessions/create_session/` - Create quiz session
- `GET /api/quiz-sessions/{id}/` - Get session details
- `POST /api/quiz-sessions/{id}/submit_answer/` - Submit answer
- `POST /api/quiz-sessions/{id}/complete/` - Complete quiz

### Bookmarks
- `GET /api/bookmarks/` - Get user bookmarks
- `POST /api/bookmarks/toggle/` - Toggle bookmark

### Leaderboard
- `GET /api/leaderboard/` - Get weekly leaderboard

## 🔧 Configuration

### Environment Variables (Backend)

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Firebase
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-auth-domain.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id

# CORS
FRONTEND_URL=http://localhost:3000
```

### Environment Variables (Frontend)

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_FIREBASE_API_KEY=your-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-auth-domain.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-storage-bucket.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
REACT_APP_FIREBASE_APP_ID=your-app-id
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key
```

## 🚢 Deployment

### Backend Deployment (Railway/Render)

**Railway:**
1. Push code to GitHub
2. Connect repository to Railway
3. Add environment variables
4. Deploy automatically

**Render:**
1. Create new Web Service
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn config.wsgi:application`

### Frontend Deployment (Vercel/Netlify)

**Vercel:**
```bash
npm install -g vercel
vercel
```

**Netlify:**
```bash
npm run build
# Drag & drop the build folder to Netlify
```

## 📊 Database Schema

### Tables
- **users** - User profiles
- **questions** - Quiz questions
- **quiz_sessions** - User quiz attempts
- **quiz_answers** - Individual question answers
- **bookmarks** - Saved questions
- **user_stats** - User statistics
- **leaderboard** - Weekly rankings

## 🔐 Authentication Flow

```
1. User clicks "Sign in with Google" on home page
2. Firebase handles OAuth with Google
3. User info stored in Firebase
4. Frontend makes authenticated API calls with Firebase token
5. Backend validates token with Firebase
6. User data synced with Django user model
```

## 📧 Email Notifications

Currently configured with Supabase. To enable:

1. Set up Supabase Email Templates
2. Create Edge Function to check for inactive users
3. Schedule function to run daily

Alternative: Use SendGrid or Resend for email service.

## 🧪 Testing

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
npm test
```

## 📝 Adding More Questions

Edit `backend/seed_data.py` and add questions to the `SAMPLE_QUESTIONS` list:

```python
{
    'title': 'Question Title',
    'description': 'Question description...',
    'difficulty': 'Easy',  # Easy, Medium, Hard
    'question_type': 'DSA',  # DSA, OOP, PF, DB
    'category': 'Arrays',
    'code_template': 'def solution():\n    pass',
    'expected_output': 'Expected result',
    'source': 'LeetCode'
}
```

Then run: `python manage.py shell < seed_data.py`

## 🐛 Troubleshooting

### CORS Issues
- Add frontend URL to `CORS_ALLOWED_ORIGINS` in Django settings
- Check Supabase CORS settings

### Firebase Not Working
- Verify credentials in .env
- Check authorized domains in Google Cloud Console
- Clear browser cache

### Database Connection Issues
- Test Supabase connection with provided credentials
- Check PostgreSQL is running
- Verify RLS policies aren't blocking access

## 📚 Resources

- [Django Docs](https://docs.djangoproject.com/)
- [React Docs](https://react.dev/)
- [Firebase Docs](https://firebase.google.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [DRF Docs](https://www.django-rest-framework.org/)

## 🎓 Learning Path

1. **Week 1**: Set up infrastructure, create basic CRUD
2. **Week 2**: Implement quiz logic, scoring system
3. **Week 3**: Add authentication, user dashboard
4. **Week 4**: Implement leaderboard, notifications
5. **Week 5**: Polish UI, add more features
6. **Week 6**: Deploy to production

## 💡 Future Features

- [ ] Video solutions for each question
- [ ] Discussion forums
- [ ] Code execution sandbox
- [ ] Mobile app (React Native)
- [ ] Premium features/subscription
- [ ] Live mock interviews with mentors
- [ ] Company-specific question sets
- [ ] Performance analytics with graphs

## 📄 License

MIT License - Feel free to use for personal projects

## 🤝 Contributing

Found a bug? Have an idea? Feel free to contribute!

---

**Happy coding! 🚀**
