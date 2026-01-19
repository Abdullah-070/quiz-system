import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleGoogleSuccess = (credentialResponse) => {
    // Send token to backend
    login(credentialResponse.credential);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-blue-800">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-center mb-6">InterviewQuiz</h1>
        <p className="text-gray-600 text-center mb-8">Master your coding interviews</p>
        
        <div className="flex justify-center mb-6">
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => console.log('Login Failed')}
          />
        </div>

        <p className="text-center text-sm text-gray-600">
          Sign in to start practicing and tracking your progress
        </p>
      </div>
    </div>
  );
};

export default Login;
