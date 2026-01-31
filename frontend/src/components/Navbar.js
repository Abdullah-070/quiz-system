import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { signOut } from 'firebase/auth';
import { auth } from '../services/firebase';
import './Navbar.css';

function Navbar({ user }) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="logo" onClick={() => navigate('/')}>
          📚 Interview Quiz
        </div>
        <div className="nav-links">
          <a href="/dashboard" className={location.pathname === '/dashboard' ? 'active' : ''}>
            Dashboard
          </a>
          <a href="/quiz" className={location.pathname === '/quiz' ? 'active' : ''}>
            Take Quiz
          </a>
          <a href="/leaderboard" className={location.pathname === '/leaderboard' ? 'active' : ''}>
            Leaderboard
          </a>
        </div>
        <div className="user-info">
          <span>{user?.email}</span>
          <button className="btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
