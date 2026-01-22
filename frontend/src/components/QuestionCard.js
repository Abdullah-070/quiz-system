import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const QuestionCard = ({ question }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const difficultyColor = {
    easy: 'text-green-600 bg-green-100',
    medium: 'text-yellow-600 bg-yellow-100',
    hard: 'text-red-600 bg-red-100',
  };

  const handleClick = () => {
    // Pass current filter state to QuestionDetail
    navigate(`/question/${question.id}`, { 
      state: { from: '/questions', filters: location.state?.filters } 
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow cursor-pointer"
         onClick={handleClick}>
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-bold">{question.title}</h3>
        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${difficultyColor[question.difficulty]}`}>
          {question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1)}
        </span>
      </div>
      <p className="text-gray-600 text-sm mb-3 line-clamp-2">{question.description}</p>
      <div className="flex justify-between items-center text-sm text-gray-500">
        <span className="bg-gray-100 px-3 py-1 rounded-full">{question.category}</span>
        <span>{question.solved_count} solved</span>
      </div>
    </div>
  );
};

export default QuestionCard;
