import React from 'react';
import { useNavigate } from 'react-router-dom';

const RecentQuizzes = ({ sessions }) => {
  const navigate = useNavigate();

  if (!sessions || sessions.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4">Recent Quizzes</h2>
        <p className="text-gray-600">No quizzes completed yet. <a href="/quizzes" className="text-blue-600 hover:underline">Start a quiz!</a></p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">Recent Quizzes</h2>
      <div className="space-y-3">
        {sessions.slice(0, 5).map(session => (
          <div 
            key={session.id} 
            className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition-colors"
            onClick={() => navigate(`/quiz-review/${session.id}`)}
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-bold">{session.quiz_name}</h3>
              <span className="text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                {session.accuracy.toFixed(1)}%
              </span>
            </div>
            <p className="text-sm text-gray-600">
              {session.correct_answers}/{session.total_questions} correct • Score: {session.total_score}
            </p>
            <p className="text-xs text-gray-400 mt-1">
              {new Date(session.time_started).toLocaleDateString()}
            </p>
            <p className="text-xs text-blue-600 mt-2 hover:underline">Click to review answers →</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentQuizzes;
