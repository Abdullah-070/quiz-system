import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { quizzesAPI } from '../services/api';

const QuizzesPage = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [quizType, setQuizType] = useState('practice');
  const navigate = useNavigate();

  useEffect(() => {
    fetchQuizzes();
  }, [quizType]);

  const fetchQuizzes = async () => {
    try {
      setLoading(true);
      const response = await quizzesAPI.byType(quizType);
      setQuizzes(response.data);
    } catch (error) {
      console.error('Error fetching quizzes:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8">Quizzes</h1>

      {/* Type Selector */}
      <div className="flex gap-4 mb-8">
        {['practice', 'timed', 'mock'].map(type => (
          <button
            key={type}
            onClick={() => setQuizType(type)}
            className={`px-6 py-2 rounded-lg font-medium ${
              quizType === type
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}
      </div>

      {/* Quizzes Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : quizzes.length === 0 ? (
          <div className="text-center py-8">No quizzes available</div>
        ) : (
          quizzes.map(quiz => (
            <div key={quiz.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg">
              <h3 className="text-2xl font-bold mb-2">{quiz.name}</h3>
              <p className="text-gray-600 mb-4">{quiz.description}</p>
              
              <div className="flex gap-2 mb-4">
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                  {quiz.questions_count} questions
                </span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                  {quiz.difficulty}
                </span>
                {quiz.time_limit > 0 && (
                  <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm">
                    {quiz.time_limit} min
                  </span>
                )}
              </div>

              <button
                onClick={() => navigate(`/quiz/${quiz.id}`)}
                className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 font-medium"
              >
                Start Quiz
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default QuizzesPage;
