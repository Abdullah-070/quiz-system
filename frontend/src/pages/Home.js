import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Home = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 text-white">
      {/* Navigation */}
      <nav className="flex justify-between items-center p-6 max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold">InterviewQuiz</h1>
        <div className="flex gap-4">
          {user ? (
            <button
              onClick={() => navigate('/dashboard')}
              className="bg-white text-blue-600 px-6 py-2 rounded-lg font-bold hover:bg-gray-100"
            >
              Dashboard
            </button>
          ) : (
            <button
              onClick={() => navigate('/login')}
              className="bg-white text-blue-600 px-6 py-2 rounded-lg font-bold hover:bg-gray-100"
            >
              Login
            </button>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-6xl mx-auto px-6 py-20 text-center">
        <h2 className="text-5xl font-bold mb-6">Master Your Coding Interviews</h2>
        <p className="text-xl mb-12 text-blue-100">
          Practice 500+ DSA, OOP, and Database questions. Track your progress and compete with peers.
        </p>
        
        <div className="flex gap-4 justify-center mb-16">
          {!user && (
            <>
              <button
                onClick={() => navigate('/login')}
                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-bold hover:bg-gray-100"
              >
                Get Started
              </button>
              <button
                onClick={() => navigate('/questions')}
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700"
              >
                Browse Questions
              </button>
            </>
          )}
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <div className="bg-blue-700 p-6 rounded-lg">
            <h3 className="text-2xl font-bold mb-2">500+ Questions</h3>
            <p className="text-blue-100">DSA, OOP, PF, and Database problems from easy to hard</p>
          </div>
          <div className="bg-blue-700 p-6 rounded-lg">
            <h3 className="text-2xl font-bold mb-2">Multiple Quiz Modes</h3>
            <p className="text-blue-100">Practice, Timed (30min), and Mock Interview modes</p>
          </div>
          <div className="bg-blue-700 p-6 rounded-lg">
            <h3 className="text-2xl font-bold mb-2">Track Progress</h3>
            <p className="text-blue-100">Dashboard with accuracy, weak areas, and analytics</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-blue-700 p-6 rounded-lg">
            <h3 className="text-2xl font-bold mb-2">Compete</h3>
            <p className="text-blue-100">Join the leaderboard and compete with peers weekly and monthly</p>
          </div>
          <div className="bg-blue-700 p-6 rounded-lg">
            <h3 className="text-2xl font-bold mb-2">Learn</h3>
            <p className="text-blue-100">Video explanations and detailed solutions for every question</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
