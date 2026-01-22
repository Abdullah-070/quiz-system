import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { sessionsAPI } from '../services/api';

const QuizReview = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  const fetchQuizReview = useCallback(async () => {
    try {
      setLoading(true);
      const response = await sessionsAPI.review(sessionId);
      setSession(response.data);
    } catch (error) {
      console.error('Error fetching quiz review:', error);
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  useEffect(() => {
    fetchQuizReview();
  }, [fetchQuizReview]);

  if (loading) {
    return <div className="max-w-6xl mx-auto p-6">Loading quiz details...</div>;
  }

  if (!session) {
    return <div className="max-w-6xl mx-auto p-6">Quiz not found</div>;
  }

  const correctPercentage = session.total_questions > 0 
    ? ((session.correct_answers / session.total_questions) * 100).toFixed(1)
    : 0;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <button
        onClick={() => navigate('/dashboard')}
        className="mb-6 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg flex items-center gap-2"
      >
        ← Back to Dashboard
      </button>

      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h1 className="text-3xl font-bold mb-4">{session.quiz_name || session.title}</h1>
        
        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-gray-600 text-sm">Accuracy</p>
            <p className="text-2xl font-bold text-blue-600">{correctPercentage}%</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-gray-600 text-sm">Correct</p>
            <p className="text-2xl font-bold text-green-600">{session.correct_answers}/{session.total_questions}</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-gray-600 text-sm">Score</p>
            <p className="text-2xl font-bold text-purple-600">{session.total_score}</p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-gray-600 text-sm">Quiz Type</p>
            <p className="text-2xl font-bold text-gray-600 capitalize">{session.quiz_type}</p>
          </div>
        </div>

        <div className="text-sm text-gray-500 mb-6">
          Attempted on: {new Date(session.time_started).toLocaleString()}
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="border-b border-gray-200">
          <div className="flex gap-4 p-6">
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                activeTab === 'overview'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab('answers')}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                activeTab === 'answers'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              Review Answers
            </button>
          </div>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="p-6">
            <div className="space-y-4">
              <div>
                <h3 className="font-bold mb-2">Quiz Details</h3>
                <p className="text-gray-600"><strong>Total Questions:</strong> {session.total_questions}</p>
                <p className="text-gray-600"><strong>Questions Answered:</strong> {session.answers?.length || 0}</p>
                <p className="text-gray-600"><strong>Correct Answers:</strong> {session.correct_answers}</p>
                <p className="text-gray-600"><strong>Wrong Answers:</strong> {session.wrong_answers}</p>
                <p className="text-gray-600"><strong>Total Score:</strong> {session.total_score}</p>
              </div>
            </div>
          </div>
        )}

        {/* Answers Tab */}
        {activeTab === 'answers' && (
          <div className="p-6">
            <div className="space-y-6">
              {session.answers && session.answers.length > 0 ? (
                session.answers.map((answer, index) => (
                  <div key={answer.id} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h4 className="font-bold text-lg mb-1">
                          Question {index + 1}: {answer.question?.title}
                        </h4>
                        <span
                          className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                            answer.is_correct
                              ? 'bg-green-100 text-green-700'
                              : 'bg-red-100 text-red-700'
                          }`}
                        >
                          {answer.is_correct ? '✓ Correct' : '✗ Incorrect'}
                        </span>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-bold">{answer.score} pts</p>
                      </div>
                    </div>

                    {/* Question Description */}
                    <div className="mb-4 bg-gray-50 p-3 rounded">
                      <p className="text-gray-700">{answer.question?.description}</p>
                    </div>

                    {/* Your Answer */}
                    <details className="mb-3">
                      <summary className="cursor-pointer font-semibold text-blue-600 hover:text-blue-700">
                        Your Answer
                      </summary>
                      <pre className="mt-2 bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto text-sm">
                        {answer.user_code}
                      </pre>
                    </details>

                    {/* Correct Solution */}
                    <details className="mb-3">
                      <summary className="cursor-pointer font-semibold text-green-600 hover:text-green-700">
                        Correct Solution
                      </summary>
                      <pre className="mt-2 bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto text-sm">
                        {answer.question?.solution_code}
                      </pre>
                    </details>

                    {/* Explanation */}
                    {answer.question?.explanation && (
                      <details>
                        <summary className="cursor-pointer font-semibold text-purple-600 hover:text-purple-700">
                          Explanation
                        </summary>
                        <div className="mt-2 bg-blue-50 p-3 rounded text-gray-700">
                          {answer.question.explanation}
                        </div>
                      </details>
                    )}
                  </div>
                ))
              ) : (
                <p className="text-gray-600">No answers submitted</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default QuizReview;
