import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { auth } from '../firebaseConfig';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import './Auth.css';

const SignUp = () => {
  const navigate = useNavigate();
  const { signup, googleLogin, error: authError } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    password_confirm: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.username.trim()) newErrors.username = 'Username is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) newErrors.email = 'Invalid email format';
    if (formData.password.length < 8) newErrors.password = 'Password must be at least 8 characters';
    if (formData.password !== formData.password_confirm) newErrors.password_confirm = 'Passwords do not match';
    
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    try {
      await signup({
        username: formData.username,
        email: formData.email,
        first_name: formData.first_name,
        last_name: formData.last_name,
        password: formData.password,
        password_confirm: formData.password_confirm,
      });
    } catch (err) {
      console.error('Signup failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignUp = async () => {
    try {
      setLoading(true);
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(auth, provider);
      const user = result.user;
      const idToken = await user.getIdToken();
      
      await googleLogin(idToken, user);
      navigate('/dashboard');
    } catch (err) {
      console.error('Google sign-up failed:', err);
      setErrors({ google: err.message || 'Google sign-up failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Create Account</h2>
        <p className="auth-subtitle">Sign up to get started</p>

        {authError && <div className="error-message">{authError}</div>}
        {errors.google && <div className="error-message">{errors.google}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Choose a username"
              disabled={loading}
            />
            {errors.username && <span className="field-error">{errors.username}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your@email.com"
              disabled={loading}
            />
            {errors.email && <span className="field-error">{errors.email}</span>}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="first_name">First Name</label>
              <input
                id="first_name"
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                placeholder="John"
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label htmlFor="last_name">Last Name</label>
              <input
                id="last_name"
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                placeholder="Doe"
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="At least 8 characters"
              disabled={loading}
            />
            {errors.password && <span className="field-error">{errors.password}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password_confirm">Confirm Password</label>
            <input
              id="password_confirm"
              type="password"
              name="password_confirm"
              value={formData.password_confirm}
              onChange={handleChange}
              placeholder="Confirm your password"
              disabled={loading}
            />
            {errors.password_confirm && <span className="field-error">{errors.password_confirm}</span>}
          </div>

          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <div className="auth-divider">or</div>

        <button
          type="button"
          className="google-button"
          onClick={handleGoogleSignUp}
          disabled={loading}
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19.6 10.23c0-.82-.3-1.42-.74-1.97V5.65h-2.7v2.26h-.46a2.18 2.18 0 00-1.97-1.08c-1.05 0-1.95.52-2.5 1.3-.3-.44-.77-1.04-2.55-1.04-2.2 0-4.08 1.53-4.08 3.85 0 2.05 1.53 3.76 3.97 3.76 1.1 0 1.87-.35 2.51-.89h.46v.7c0 .42-.04.82-.3 1.44H5.88c-.22-.4-.35-.82-.35-1.29 0-.95.42-1.64 1.24-1.64.37 0 .74.18.74.54 0 .38-.26.79-.74.79-.22 0-.38.04-.5.13v-.7c0-.38.04-.79.3-1.13.22-.3.58-.52 1.1-.52.95 0 1.58.89 1.58 1.76 0 .95-.42 1.76-1.48 1.76-.56 0-.99-.22-1.24-.56-.22-.3-.38-.74-.38-1.13 0-.38.04-.82.3-1.13.22-.3.54-.52 1.06-.52.99 0 1.58 1.04 1.58 2.08 0 1.44-.99 2.59-2.55 2.59-1.97 0-3.25-1.73-3.25-3.68 0-2.05 1.53-3.76 3.97-3.76 1.1 0 1.87.35 2.51.89h.46v-.7c0-.42.04-.82.3-1.44h2.59z" fill="currentColor"/>
          </svg>
          Sign up with Google
        </button>

        <div className="auth-divider">or</div>

        <div className="auth-links">
          <p>Already have an account? <Link to="/login">Login here</Link></p>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
