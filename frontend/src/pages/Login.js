import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

function Login() {
  const navigate = useNavigate();

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Login</h1>
        <p>Firebase authentication is configured in the app. Sign in through the home page.</p>
        <button className="btn" onClick={() => navigate('/')}>
          Back to Home
        </button>
      </div>
    </div>
  );
}

export default Login;
