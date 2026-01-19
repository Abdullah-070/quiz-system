import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AuthProvider } from './context/AuthContext';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import QuestionBrowser from './pages/QuestionBrowser';
import QuizzesPage from './pages/Quizzes';
import QuizInterface from './pages/QuizInterface';
import Leaderboard from './pages/Leaderboard';

// Components
import Navigation from './components/Navigation';
import PrivateRoute from './components/PrivateRoute';

function App() {
  const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID || '';

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <Router>
        <AuthProvider>
          <Navigation />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/questions" element={<QuestionBrowser />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            
            <Route 
              path="/dashboard" 
              element={<PrivateRoute><Dashboard /></PrivateRoute>} 
            />
            <Route 
              path="/quizzes" 
              element={<PrivateRoute><QuizzesPage /></PrivateRoute>} 
            />
            <Route 
              path="/quiz/:quizId" 
              element={<PrivateRoute><QuizInterface /></PrivateRoute>} 
            />
          </Routes>
        </AuthProvider>
      </Router>
    </GoogleOAuthProvider>
  );
}

export default App;
