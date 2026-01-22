import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { questionsAPI } from '../services/api';

const QuestionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showSolution, setShowSolution] = useState(false);
  const [activeTab, setActiveTab] = useState('description');

  const fetchQuestion = useCallback(async () => {
    try {
      setLoading(true);
      const response = await questionsAPI.getById(id);
      setQuestion(response.data);
    } catch (error) {
      console.error('Error fetching question:', error);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchQuestion();
  }, [fetchQuestion]);

  const handleBack = () => {
    // Reconstruct filter query params from URL and go back to questions
    const params = new URLSearchParams();
    const difficulty = searchParams.get('difficulty');
    const topic = searchParams.get('topic');
    const search = searchParams.get('search');
    
    if (difficulty) params.append('difficulty', difficulty);
    if (topic) params.append('topic', topic);
    if (search) params.append('search', search);
    
    const queryString = params.toString();
    navigate(`/questions${queryString ? '?' + queryString : ''}`);
  };

  if (loading) {
    return <div className="max-w-4xl mx-auto p-6">Loading...</div>;
  }

  if (!question) {
    return <div className="max-w-4xl mx-auto p-6">Question not found</div>;
  }

  const difficultyColor = {
    easy: 'text-green-600 bg-green-100',
    medium: 'text-yellow-600 bg-yellow-100',
    hard: 'text-red-600 bg-red-100',
  };

  const categoryLabel = {
    dsa: 'Data Structures & Algorithms',
    oop: 'Object-Oriented Programming',
    dbs: 'Database & SQL',
    pf: 'Functional Programming',
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <button
        onClick={handleBack}
        className="mb-6 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg flex items-center gap-2"
      >
        ← Back
      </button>

      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        {/* Header */}
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold mb-2">{question.title}</h1>
            <div className="flex gap-3 items-center">
              <span className={`px-4 py-1 rounded-full text-sm font-semibold ${difficultyColor[question.difficulty]}`}>
                {question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1)}
              </span>
              <span className="bg-blue-100 text-blue-700 px-4 py-1 rounded-full text-sm font-semibold">
                {categoryLabel[question.topic] || question.topic}
              </span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-6">
          <div className="flex gap-4">
            <button
              onClick={() => setActiveTab('description')}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                activeTab === 'description'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              Problem
            </button>
            <button
              onClick={() => setActiveTab('solution')}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                activeTab === 'solution'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              Solution
            </button>
            <button
              onClick={() => setActiveTab('testcases')}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                activeTab === 'testcases'
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900'
              }`}
            >
              Test Cases
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="space-y-4">
          {activeTab === 'description' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Problem Description</h2>
              <p className="text-gray-700 whitespace-pre-wrap mb-6">{question.description}</p>
              
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <h3 className="font-bold mb-3">Template Code</h3>
                <pre className="bg-gray-900 text-gray-100 p-4 rounded overflow-x-auto text-sm">
                  <code>{question.template_code}</code>
                </pre>
              </div>
            </div>
          )}

          {activeTab === 'solution' && (
            <div>
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">Solution Explanation</h2>
                <button
                  onClick={() => setShowSolution(!showSolution)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {showSolution ? 'Hide Solution' : 'Show Solution'}
                </button>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200 mb-6">
                <p className="text-gray-700">{question.explanation}</p>
              </div>

              {showSolution && (
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h3 className="font-bold mb-3">Complete Solution</h3>
                  <pre className="bg-gray-900 text-gray-100 p-4 rounded overflow-x-auto text-sm">
                    <code>{question.solution_code}</code>
                  </pre>
                </div>
              )}
            </div>
          )}

          {activeTab === 'testcases' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Test Cases</h2>
              <div className="space-y-4">
                {question.test_cases && question.test_cases.length > 0 ? (
                  question.test_cases.map((testCase, index) => (
                    <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                      <h3 className="font-bold mb-2">Test Case {index + 1}</h3>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <p className="text-sm text-gray-600 font-semibold">Input</p>
                          <pre className="bg-white p-2 rounded border border-gray-300 text-sm mt-1">
                            {JSON.stringify(testCase.input, null, 2)}
                          </pre>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600 font-semibold">Expected Output</p>
                          <pre className="bg-white p-2 rounded border border-gray-300 text-sm mt-1">
                            {JSON.stringify(testCase.output, null, 2)}
                          </pre>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-600">No test cases available</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuestionDetail;
