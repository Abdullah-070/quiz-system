# Interview Prep Quiz Platform - Frontend

React-based frontend for the Interview Prep Quiz Platform.

## Features

- Interactive quiz interface with Ace/Monaco code editor
- Dashboard with user statistics and progress tracking
- Question browser with filtering and search
- Leaderboard with weekly, monthly, and all-time rankings
- Google OAuth authentication
- Real-time timer for timed quizzes
- Responsive design with Tailwind CSS

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file with your configuration:
```bash
cp .env.example .env
```

3. Update `.env` with your values:
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000/api)
- `REACT_APP_GOOGLE_CLIENT_ID`: Your Google OAuth Client ID

4. Start the development server:
```bash
npm start
```

The app will run on `http://localhost:3000`

## Building for Production

```bash
npm run build
```

## Key Components

- **QuizInterface**: Full-screen quiz with code editor and timer
- **Dashboard**: User stats, recent quizzes, and weak areas
- **QuestionBrowser**: Search and filter through all questions
- **Leaderboard**: Competitive rankings by period
- **Authentication**: Google OAuth integration

## API Integration

The frontend communicates with the Django backend via REST API:
- Questions: `/api/questions/`
- Quizzes: `/api/quizzes/`
- Sessions: `/api/sessions/`
- Profile: `/api/profile/`
- Leaderboard: `/api/leaderboard/`
