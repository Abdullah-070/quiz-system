import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  getAuth, 
  sendPasswordResetEmail,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
} from 'firebase/auth';
import app from '../firebaseConfig';
import { createUserProfile, getUserProfile } from '../services/firestore';

// Simple auth context
export const AuthContext = React.createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const auth = getAuth(app);

  useEffect(() => {
    // Listen for auth state changes
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        try {
          const userProfile = await getUserProfile(firebaseUser.uid);
          setUser({
            id: firebaseUser.uid,
            email: firebaseUser.email,
            ...userProfile,
          });
        } catch (err) {
          console.error('Error loading user profile:', err);
          setUser({
            id: firebaseUser.uid,
            email: firebaseUser.email,
          });
        }
      } else {
        setUser(null);
      }
      setLoading(false);
    });

    return unsubscribe;
  }, [auth]);

  const login = (userData) => {
    setUser(userData);
    setError(null);
    navigate('/dashboard');
  };

  const emailPasswordLogin = async (email, password) => {
    try {
      setError(null);
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const userProfile = await getUserProfile(userCredential.user.uid);
      login({
        id: userCredential.user.uid,
        email: userCredential.user.email,
        ...userProfile,
      });
    } catch (err) {
      const errorMsg = err.message || 'Login failed';
      setError(errorMsg);
      throw err;
    }
  };

  const googleSignIn = async (idToken, firebaseUser) => {
    try {
      setError(null);
      // Firebase handles Google sign-in
      // Just get or create user profile
      let userProfile = await getUserProfile(firebaseUser.uid);
      
      if (!userProfile) {
        // Create new profile
        await createUserProfile(firebaseUser.uid, {
          email: firebaseUser.email,
          firstName: firebaseUser.displayName?.split(' ')[0] || '',
          lastName: firebaseUser.displayName?.split(' ').slice(1).join(' ') || '',
        });
        userProfile = await getUserProfile(firebaseUser.uid);
      }

      login({
        id: firebaseUser.uid,
        email: firebaseUser.email,
        ...userProfile,
      });
    } catch (err) {
      const errorMsg = err.message || 'Google sign-in failed';
      setError(errorMsg);
      throw err;
    }
  };

  const signup = async (userData) => {
    try {
      setError(null);
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        userData.email,
        userData.password
      );

      // Create user profile in Firestore
      await createUserProfile(userCredential.user.uid, {
        email: userData.email,
        username: userData.username,
        firstName: userData.first_name || '',
        lastName: userData.last_name || '',
      });

      const userProfile = await getUserProfile(userCredential.user.uid);
      login({
        id: userCredential.user.uid,
        email: userCredential.user.email,
        ...userProfile,
      });
    } catch (err) {
      const errorMsg = err.message || 'Registration failed';
      setError(errorMsg);
      throw err;
    }
  };

  const resetPassword = async (email) => {
    try {
      setError(null);
      await sendPasswordResetEmail(auth, email);
      return { success: true, message: 'Password reset email sent. Check your inbox.' };
    } catch (err) {
      const errorMsg = err.message || 'Password reset failed';
      setError(errorMsg);
      throw err;
    }
  };

  const logout = async () => {
    try {
      await signOut(auth);
      setUser(null);
      setError(null);
      navigate('/');
    } catch (err) {
      console.error('Logout error:', err);
    }
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
