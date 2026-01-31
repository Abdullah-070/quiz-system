import React from 'react';
import { useNavigate } from 'react-router-dom';
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth } from '../services/firebase';
import './Home.css';

function Home() {
  const navigate = useNavigate();
  const googleProvider = new GoogleAuthProvider();

  const handleGoogleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      console.log('User logged in:', result.user);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <div className="home">
      <div className="home-container">
        <div className="hero">
          <h1>📚 Interview Prep Quiz Platform</h1>
          <p>Master coding interviews with 500+ DSA, OOP, PF, and Database questions</p>
          
          <div className="features">
            <div className="feature-card">
              <h3>📝 Practice Mode</h3>
              <p>Unlimited time to solve problems</p>
            </div>
            <div className="feature-card">
              <h3>⏱️ Timed Quizzes</h3>
              <p>30-minute timed quizzes</p>
            </div>
            <div className="feature-card">
              <h3>🎯 Mock Interviews</h3>
              <p>Simulate real interview pace</p>
            </div>
            <div className="feature-card">
              <h3>🏆 Leaderboard</h3>
              <p>Compete with peers</p>
            </div>
          </div>

          <button className="btn-login" onClick={handleGoogleLogin}>
            🔐 Sign in with Google
          </button>
        </div>
      </div>
    </div>
  );
}

export default Home;
