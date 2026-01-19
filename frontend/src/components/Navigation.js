import React from 'react';
import { useAuth } from '../context/AuthContext';

const Navigation = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-8">
          <a href="/" className="text-2xl font-bold text-blue-600">InterviewQuiz</a>
          {user && (
            <ul className="flex gap-6">
              <li><a href="/dashboard" className="hover:text-blue-600">Dashboard</a></li>
              <li><a href="/questions" className="hover:text-blue-600">Questions</a></li>
              <li><a href="/quizzes" className="hover:text-blue-600">Quizzes</a></li>
              <li><a href="/leaderboard" className="hover:text-blue-600">Leaderboard</a></li>
            </ul>
          )}
        </div>
        <div className="flex items-center gap-4">
          {user ? (
            <>
              <span className="text-sm text-gray-600">{user.email || user.username}</span>
              <button
                onClick={logout}
                className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <a href="/login" className="text-blue-600 hover:text-blue-700 font-medium">
                Login
              </a>
              <a href="/signup" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                Sign Up
              </a>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
