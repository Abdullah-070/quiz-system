# Interview Prep Quiz Platform

A comprehensive online platform for CS students to practice coding interview questions, take timed quizzes, and compete with peers.

## 🎯 Project Overview

InterviewQuiz provides:
- **500+ Questions** across DSA, OOP, Databases, and more
- **Multiple Quiz Modes**: Practice (unlimited time), Timed (30 min), Mock Interviews
- **Difficulty Levels**: Easy, Medium, Hard
- **Progress Tracking**: Dashboard with stats, accuracy rates, and weak areas
- **Competition**: Weekly/monthly leaderboards
- **Learning**: Video explanations and detailed solutions
- **Bookmarks**: Save questions for later

## 📁 Project Structure

```
Interview Quiz/
├── backend/               # Django REST API
│   ├── quiz_app/
│   │   ├── models.py      # Database models
│   │   ├── views.py       # API endpoints
│   │   ├── serializers.py # Data serializers
│   │   └── urls.py        # URL routing
│   ├── config/
│   │   ├── settings.py    # Django settings
│   │   ├── urls.py        # Main URLs
│   │   └── celery.py      # Celery config
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/              # React Application
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API integration
│   │   ├── context/       # React context
│   │   ├── App.js         # Main app
│   │   └── index.js       # Entry point
│   ├── public/
│   ├── package.json
│   └── README.md
│
└── README.md             # This file
```

## 🚀 Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed sample questions
python manage.py seed_questions

# Start server
python manage.py runserver
```

Server runs at `http://localhost:8000`
Admin panel: `http://localhost:8000/admin/`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm start
```

App runs at `http://localhost:3000`

## 🔧 Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - RESTful API
- **PostgreSQL** - Database
- **Django Allauth** - Authentication
- **Google OAuth** - Social login
- **Celery** - Task queue
- **Redis** - Caching & message broker

### Frontend
- **React 18** - UI library
- **React Router** - Navigation
- **Axios** - HTTP client
- **Ace/Monaco** - Code editor
- **Tailwind CSS** - Styling
- **Google OAuth** - Authentication
- **Chart.js** - Analytics visualization

### Deployment
- **Render** - Backend hosting
- **Vercel/Netlify** - Frontend hosting
- **PostgreSQL Cloud** - Database
- **Redis Cloud** - Message broker

## 📊 Database Models

### Core Models
- **User**: Django authentication
- **Question**: Coding problems with solutions
- **Quiz**: Collections of questions
- **QuizSession**: User quiz attempts
- **Answer**: Individual question answers
- **UserProfile**: User stats and preferences
- **Bookmark**: Saved questions
- **Leaderboard**: Rankings by period

## 🔐 Authentication

- Google OAuth 2.0 for signup/login
- JWT tokens for API authentication
- Protected endpoints for authenticated users

## 📝 API Endpoints

### Questions
- `GET /api/questions/` - List questions (filterable)
- `GET /api/questions/{id}/` - Question details
- `GET /api/questions/by_category/` - Questions by category
- `GET /api/questions/by_difficulty/` - Questions by difficulty

### Quizzes
- `GET /api/quizzes/` - List quizzes
- `GET /api/quizzes/{id}/` - Quiz details
- `POST /api/quizzes/{id}/start/` - Start quiz
- `GET /api/quizzes/by_type/` - Quizzes by type

### Sessions
- `GET /api/sessions/` - User's sessions
- `POST /api/sessions/{id}/submit_answer/` - Submit answer
- `POST /api/sessions/{id}/finish/` - Complete quiz

### User
- `GET /api/profile/me/` - User profile
- `GET /api/bookmarks/` - User's bookmarks
- `GET /api/leaderboard/` - Leaderboard

## 🎮 Features

### For Users
- Browse 500+ questions by difficulty and category
- Practice with unlimited time or timed quizzes
- Get instant feedback on submissions
- Track progress on dashboard
- Save questions for later
- View detailed solutions and video explanations
- Compare performance on leaderboard

### For Admins
- Django admin panel for content management
- Import questions from JSON
- Monitor user progress
- Manage quiz configurations
- View leaderboard statistics

## 🛣️ Development Roadmap

- [ ] Code execution engine (Python, JavaScript, Java)
- [ ] Automated test case validation
- [ ] Email reminders for inactive users
- [ ] Premium features (solution videos, advanced analytics)
- [ ] Discussion forum for questions
- [ ] Study plans and learning paths
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration features

## 📦 Deployment

### Backend (Render)
```bash
# 1. Create Procfile
# 2. Set environment variables
# 3. Deploy from GitHub
```

### Frontend (Vercel)
```bash
# 1. Connect GitHub repository
# 2. Set environment variables
# 3. Auto-deploy on push
```

## 📚 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [REST API Best Practices](https://restfulapi.net/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👥 Team

- Built as an interview prep platform for CS students

## 📞 Support

For issues and feature requests, please create an issue in the repository.

## 🎉 Acknowledgments

- Inspired by LeetCode, HackerRank, and InterviewBit
- Uses open-source libraries and frameworks
- Community-driven content model

---

**Happy coding! 🚀**
