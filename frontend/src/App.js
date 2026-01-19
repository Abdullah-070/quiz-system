import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AuthProvider } from './context/AuthContext';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import ForgotPassword from './pages/ForgotPassword';
import Dashboard from './pages/Dashboard';
import QuestionBrowser from './pages/QuestionBrowser';
import QuestionDetail from './pages/QuestionDetail';
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
            <Route path="/signup" element={<SignUp />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/questions" element={<QuestionBrowser />} />
            <Route path="/question/:id" element={<QuestionDetail />} />
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
