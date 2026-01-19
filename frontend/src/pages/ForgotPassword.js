import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { requestPasswordReset, confirmPasswordReset } from '../services/api';
import './Auth.css';

const ForgotPassword = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: request, 2: reset
  const [email, setEmail] = useState('');
  const [resetData, setResetData] = useState({
    password: '',
    password_confirm: '',
  });
  const [uid, setUid] = useState('');
  const [token, setToken] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRequestSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!email.trim()) {
      setError('Email is required');
      return;
    }

    setLoading(true);
    try {
      const response = await requestPasswordReset(email);
      setUid(response.data.uid);
      setToken(response.data.token);
      setSuccess('Password reset token sent! Check your email or use the token below.');
      setStep(2);
    } catch (err) {
      setError(err.response?.data?.email?.[0] || 'Failed to request password reset');
    } finally {
      setLoading(false);
    }
  };

  const handleResetSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (resetData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    if (resetData.password !== resetData.password_confirm) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    try {
      await confirmPasswordReset(uid, token, resetData.password, resetData.password_confirm);
      setSuccess('Password reset successfully! You can now login with your new password.');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Reset Password</h2>
        <p className="auth-subtitle">Get back into your account</p>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {step === 1 ? (
          <form onSubmit={handleRequestSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
          <form onSubmit={handleResetSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="password">New Password</label>
              <input
                id="password"
                type="password"
                value={resetData.password}
                onChange={(e) => setResetData({ ...resetData, password: e.target.value })}
                placeholder="Enter new password"
                disabled={loading}
                autoFocus
              />
            </div>

            <div className="form-group">
              <label htmlFor="password_confirm">Confirm Password</label>
              <input
                id="password_confirm"
                type="password"
                value={resetData.password_confirm}
                onChange={(e) => setResetData({ ...resetData, password_confirm: e.target.value })}
                placeholder="Confirm new password"
                disabled={loading}
              />
            </div>

            <button type="submit" className="auth-button" disabled={loading}>
              {loading ? 'Resetting...' : 'Reset Password'}
            </button>
          </form>
        )}

        <div className="auth-links">
          <p><Link to="/login">Back to Login</Link></p>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
