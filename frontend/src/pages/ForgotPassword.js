import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { sendPasswordResetEmail, confirmPasswordReset, getAuth } from 'firebase/auth';
import app from '../firebaseConfig';
import './Auth.css';

const ForgotPassword = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: request, 2: confirm
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleRequestSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!email.trim()) {
      setError('Email is required');
      return;
    }

    if (!validateEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }

    setLoading(true);
    try {
      const auth = getAuth(app);
      await sendPasswordResetEmail(auth, email);
      setSuccess('Password reset email sent! Check your inbox for the reset link.');
      setStep(2);
    } catch (err) {
      if (err.code === 'auth/user-not-found') {
        setError('No account found with this email address');
      } else if (err.code === 'auth/invalid-email') {
        setError('Invalid email address');
      } else {
        setError(err.message || 'Failed to send password reset email');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Reset Password</h2>
        <p className="auth-subtitle">Enter your email to receive a password reset link</p>

        {error && <div className="error-message">{error}</div>}
        {success && <div style={{
          padding: '12px 16px',
          backgroundColor: '#d4edda',
          border: '1px solid #c3e6cb',
          borderRadius: '8px',
          color: '#155724',
          marginBottom: '20px',
          fontSize: '14px'
        }}>{success}</div>}

        {step === 1 ? (
          <form onSubmit={handleRequestSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setError('');
                }}
                placeholder="your@email.com"
                disabled={loading}
                autoFocus
              />
            </div>

            <button type="submit" className="auth-button" disabled={loading}>
              {loading ? 'Sending...' : 'Send Reset Link'}
            </button>
          </form>
        ) : (
          <div style={{
            padding: '16px',
            backgroundColor: '#e7f3ff',
            border: '1px solid #b3d9ff',
            borderRadius: '8px',
            color: '#004085'
          }}>
            <h3 style={{ marginTop: 0 }}>✓ Email Sent</h3>
            <p>We've sent a password reset link to <strong>{email}</strong>.</p>
            <p>Click the link in the email to reset your password.</p>
            <p style={{ fontSize: '13px', marginBottom: 0 }}>
              <em>If you don't see the email, check your spam folder.</em>
            </p>
          </div>
        )}

        <div className="auth-links">
          <p><Link to="/login" className="link">← Back to Login</Link></p>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
