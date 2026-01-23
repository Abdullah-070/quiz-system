import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginWithEmailPassword, registerUser, fetchCurrentUser, googleAuthLogin, requestPasswordReset, confirmPasswordReset } from '../services/api';
import { getAuth, sendPasswordResetEmail } from 'firebase/auth';
import app from '../firebaseConfig';

// Simple auth context
export const AuthContext = React.createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token');
    if (token) {
      // Fetch current user info
      fetchCurrentUser()
        .then(response => {
          setUser(response.data);
        })
        .catch(err => {
          localStorage.removeItem('access_token');
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = (token, userData) => {
    localStorage.setItem('access_token', token);
    setUser(userData);
    setError(null);
    navigate('/dashboard');
  };

  const emailPasswordLogin = async (username, password) => {
    try {
      setError(null);
      const response = await loginWithEmailPassword(username, password);
      login(response.data.access, response.data.user);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Login failed';
      setError(errorMsg);
      throw err;
    }
  };

  const googleSignIn = async (idToken, firebaseUser) => {
    try {
      setError(null);
      const response = await googleAuthLogin(idToken, firebaseUser.email, firebaseUser.displayName || '');
      login(response.data.access, response.data.user);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Google sign-in failed';
      setError(errorMsg);
      throw err;
    }
  };

  const signup = async (userData) => {
    try {
      setError(null);
      const response = await registerUser(userData);
      login(response.data.access, response.data.user);
    } catch (err) {
      const errorMsg = err.response?.data?.email?.[0] || err.response?.data?.username?.[0] || 'Registration failed';
      setError(errorMsg);
      throw err;
    }
  };

  const resetPassword = async (email) => {
    try {
      setError(null);
      const auth = getAuth(app);
      await sendPasswordResetEmail(auth, email);
      setError(null);
      return { success: true, message: 'Password reset email sent. Check your inbox.' };
    } catch (err) {
      const errorMsg = err.message || 'Password reset failed';
      setError(errorMsg);
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    setError(null);
    navigate('/');
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, login: emailPasswordLogin, googleLogin: googleSignIn, signup, logout, resetPassword }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
