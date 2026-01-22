import React from 'react';
import { useNavigate } from 'react-router-dom';

const QuizzesPage = () => {
  const navigate = useNavigate();

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8">Create & Take Quizzes</h1>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Create Custom Quiz */}
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg p-8 text-white">
          <div className="text-4xl mb-4">🎯</div>
          <h2 className="text-2xl font-bold mb-3">Create Custom Quiz</h2>
          <p className="text-blue-100 mb-6">
            Build your own quiz by selecting questions from any category. Choose difficulty levels, number of questions, and quiz type.
          </p>
          <button
            onClick={() => navigate('/create-quiz')}
            className="w-full bg-white text-blue-600 py-3 rounded-lg font-bold hover:bg-blue-50 transition-all"
          >
            Create Quiz
          </button>
        </div>

        {/* Practice Mode Info */}
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow-lg p-8 text-white">
          <div className="text-4xl mb-4">📚</div>
          <h2 className="text-2xl font-bold mb-3">Browse Questions</h2>
          <p className="text-green-100 mb-6">
            Explore our question bank with 2000+ interview questions across DSA, OOP, Database & SQL, and Functional Programming.
          </p>
          <button
            onClick={() => navigate('/questions')}
            className="w-full bg-white text-green-600 py-3 rounded-lg font-bold hover:bg-green-50 transition-all"
          >
            Question Bank
          </button>
        </div>
      </div>

      {/* How It Works */}
      <div className="mt-12 bg-white rounded-lg shadow-md p-8">
        <h3 className="text-2xl font-bold mb-6">How to Get Started</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-4xl mb-3">1️⃣</div>
            <h4 className="font-bold mb-2">Select Options</h4>
            <p className="text-gray-600">Choose category, difficulty, number of questions, and quiz type</p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-3">2️⃣</div>
            <h4 className="font-bold mb-2">Pick Questions</h4>
            <p className="text-gray-600">Select specific questions or use random selection from your category</p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-3">3️⃣</div>
            <h4 className="font-bold mb-2">Attempt Quiz</h4>
            <p className="text-gray-600">Write code in the editor and submit your answers. Track your progress!</p>
          </div>
        </div>
      </div>

      {/* Quiz Types */}
      <div className="mt-12 bg-gray-50 rounded-lg shadow-md p-8">
        <h3 className="text-2xl font-bold mb-6">Quiz Types</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg p-6 border-2 border-gray-200">
            <h4 className="text-xl font-bold mb-3">🏆 Practice Mode</h4>
            <p className="text-gray-600">
              Learn at your own pace with no time limit. Perfect for understanding concepts and practicing solutions.
            </p>
          </div>
          <div className="bg-white rounded-lg p-6 border-2 border-orange-200">
            <h4 className="text-xl font-bold mb-3">⏱️ Timed Quiz</h4>
            <p className="text-gray-600">
              Challenge yourself with a time limit. Build speed and accuracy for real interviews.
            </p>
          </div>
          <div className="bg-white rounded-lg p-6 border-2 border-red-200">
            <h4 className="text-xl font-bold mb-3">🎓 Mock Test</h4>
            <p className="text-gray-600">
              Simulate a real interview experience with realistic conditions and comprehensive assessment.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizzesPage;
