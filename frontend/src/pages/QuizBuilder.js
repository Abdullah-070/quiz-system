import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { questionsAPI, sessionsAPI } from '../services/api';

const QuizBuilder = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: Select options, 2: Select questions, 3: Review
  const [questions, setQuestions] = useState([]);
  const [selectedQuestions, setSelectedQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [quizConfig, setQuizConfig] = useState({
    numQuestions: 10,
    category: 'dsa',
    quizType: 'practice', // practice, timed, mock
    timeLimit: 60, // minutes for timed quizzes
    title: '',
  });

  const categories = ['dsa', 'oop', 'dbs', 'pf'];
  const quizTypes = [
    { value: 'practice', label: 'Practice Mode', description: 'No time limit, learn at your pace' },
    { value: 'timed', label: 'Timed Quiz', description: 'Complete within set time' },
    { value: 'mock', label: 'Mock Test', description: 'Realistic exam experience' },
  ];

  // Step 1: Configuration
  const handleConfigChange = (field, value) => {
    setQuizConfig(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const proceedToSelectQuestions = async () => {
    try {
      setLoading(true);
      // Fetch questions for selected category
      const response = await questionsAPI.getAll({
        category: quizConfig.category,
        limit: 100, // Get more to choose from
      });
      
      const allQuestions = Array.isArray(response.data) ? response.data : response.data.results || [];
      setQuestions(allQuestions);
      setStep(2);
    } catch (error) {
      console.error('Error fetching questions:', error);
      alert('Failed to load questions');
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Select questions
  const toggleQuestionSelection = (question) => {
    const isSelected = selectedQuestions.some(q => q.id === question.id);
    if (isSelected) {
      setSelectedQuestions(selectedQuestions.filter(q => q.id !== question.id));
    } else {
      if (selectedQuestions.length < quizConfig.numQuestions) {
        setSelectedQuestions([...selectedQuestions, question]);
      }
    }
  };

  const selectRandomQuestions = () => {
    const shuffled = [...questions].sort(() => 0.5 - Math.random());
    setSelectedQuestions(shuffled.slice(0, quizConfig.numQuestions));
  };

  const proceedToReview = () => {
    if (selectedQuestions.length < quizConfig.numQuestions) {
      alert(`Please select ${quizConfig.numQuestions} questions`);
      return;
    }
    setQuizConfig(prev => ({
      ...prev,
      title: `${quizConfig.category.toUpperCase()} Quiz - ${new Date().toLocaleDateString()}`,
    }));
    setStep(3);
  };

  // Step 3: Start quiz
  const startQuiz = async () => {
    try {
      setLoading(true);
      
      // Create a quiz session with selected questions
      const sessionRes = await sessionsAPI.createCustomSession({
        title: quizConfig.title,
        questions: selectedQuestions.map(q => q.id),
        quiz_type: quizConfig.quizType,
        time_limit: quizConfig.quizType === 'timed' ? quizConfig.timeLimit : 0,
        category: quizConfig.category,
      });
      
      setSession(sessionRes.data);
      navigate(`/attempt/${sessionRes.data.id}`);
    } catch (error) {
      console.error('Error creating quiz session:', error);
      alert('Failed to start quiz');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">Create a Quiz</h1>

        {/* Step Indicator */}
        <div className="flex gap-4 mb-8">
          {[1, 2, 3].map(s => (
            <div
              key={s}
              className={`flex-1 py-3 rounded-lg text-center font-medium transition-all ${
                step === s
                  ? 'bg-blue-600 text-white'
                  : step > s
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-300 text-gray-600'
              }`}
            >
              Step {s}
            </div>
          ))}
        </div>

        {/* Step 1: Configuration */}
        {step === 1 && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">Quiz Configuration</h2>
            
            <div className="space-y-6">
              {/* Number of Questions */}
              <div>
                <label className="block text-lg font-medium mb-2">Number of Questions</label>
                <input
                  type="number"
                  min="5"
                  max="100"
                  value={quizConfig.numQuestions}
                  onChange={(e) => handleConfigChange('numQuestions', parseInt(e.target.value))}
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                />
                <p className="text-gray-600 text-sm mt-1">Choose between 5 and 100 questions</p>
              </div>

              {/* Category Selection */}
              <div>
                <label className="block text-lg font-medium mb-3">Category</label>
                <div className="grid grid-cols-2 gap-3">
                  {categories.map(cat => (
                    <button
                      key={cat}
                      onClick={() => handleConfigChange('category', cat)}
                      className={`p-4 rounded-lg font-medium transition-all border-2 ${
                        quizConfig.category === cat
                          ? 'border-blue-600 bg-blue-50 text-blue-600'
                          : 'border-gray-300 bg-white hover:border-blue-600'
                      }`}
                    >
                      {cat.toUpperCase()}
                    </button>
                  ))}
                </div>
              </div>

              {/* Quiz Type Selection */}
              <div>
                <label className="block text-lg font-medium mb-3">Quiz Type</label>
                <div className="space-y-3">
                  {quizTypes.map(type => (
                    <button
                      key={type.value}
                      onClick={() => handleConfigChange('quizType', type.value)}
                      className={`w-full p-4 rounded-lg text-left transition-all border-2 ${
                        quizConfig.quizType === type.value
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-300 bg-white hover:border-blue-600'
                      }`}
                    >
                      <div className="font-medium text-lg">{type.label}</div>
                      <div className="text-gray-600 text-sm">{type.description}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Time Limit (for timed quizzes) */}
              {quizConfig.quizType === 'timed' && (
                <div>
                  <label className="block text-lg font-medium mb-2">Time Limit (minutes)</label>
                  <input
                    type="number"
                    min="5"
                    max="300"
                    value={quizConfig.timeLimit}
                    onChange={(e) => handleConfigChange('timeLimit', parseInt(e.target.value))}
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                  />
                </div>
              )}

              {/* Action Button */}
              <button
                onClick={proceedToSelectQuestions}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400"
              >
                {loading ? 'Loading...' : 'Select Questions'}
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Select Questions */}
        {step === 2 && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-2">Select Questions</h2>
            <p className="text-gray-600 mb-6">
              Choose {quizConfig.numQuestions} questions from {quizConfig.category.toUpperCase()}
            </p>

            {/* Quick Actions */}
            <div className="flex gap-2 mb-6">
              <button
                onClick={selectRandomQuestions}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium"
              >
                Select Randomly
              </button>
              <button
                onClick={() => setSelectedQuestions([])}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 font-medium"
              >
                Clear Selection
              </button>
            </div>

            {/* Question Counter */}
            <div className="mb-6 p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
              <p className="text-lg font-medium">
                Selected: {selectedQuestions.length} / {quizConfig.numQuestions} questions
              </p>
            </div>

            {/* Questions Grid */}
            <div className="space-y-3 max-h-96 overflow-y-auto mb-6">
              {questions.map(question => (
                <div
                  key={question.id}
                  onClick={() => toggleQuestionSelection(question)}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                    selectedQuestions.some(q => q.id === question.id)
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-300 bg-white hover:border-blue-400'
                  } ${selectedQuestions.length >= quizConfig.numQuestions && !selectedQuestions.some(q => q.id === question.id) ? 'opacity-50' : ''}`}
                >
                  <div className="flex gap-4">
                    <div className={`w-6 h-6 rounded border-2 flex items-center justify-center flex-shrink-0 ${
                      selectedQuestions.some(q => q.id === question.id)
                        ? 'bg-blue-600 border-blue-600'
                        : 'border-gray-400'
                    }`}>
                      {selectedQuestions.some(q => q.id === question.id) && (
                        <span className="text-white text-sm">✓</span>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-lg truncate">{question.title}</h4>
                      <div className="flex gap-2 mt-2">
                        <span className="text-xs bg-gray-200 px-2 py-1 rounded">
                          {question.difficulty}
                        </span>
                        <span className="text-xs bg-gray-200 px-2 py-1 rounded">
                          {question.category}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Navigation Buttons */}
            <div className="flex gap-4">
              <button
                onClick={() => setStep(1)}
                className="flex-1 px-6 py-3 border-2 border-gray-600 text-gray-600 rounded-lg font-medium hover:bg-gray-100"
              >
                Back
              </button>
              <button
                onClick={proceedToReview}
                disabled={selectedQuestions.length < quizConfig.numQuestions}
                className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400"
              >
                Review Quiz
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Review */}
        {step === 3 && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">Review Your Quiz</h2>

            <div className="space-y-4 mb-6">
              <div className="p-4 bg-gray-100 rounded-lg">
                <p className="text-gray-600">Category</p>
                <p className="text-xl font-medium">{quizConfig.category.toUpperCase()}</p>
              </div>
              <div className="p-4 bg-gray-100 rounded-lg">
                <p className="text-gray-600">Quiz Type</p>
                <p className="text-xl font-medium">
                  {quizTypes.find(t => t.value === quizConfig.quizType)?.label}
                </p>
              </div>
              <div className="p-4 bg-gray-100 rounded-lg">
                <p className="text-gray-600">Questions</p>
                <p className="text-xl font-medium">{selectedQuestions.length} questions</p>
              </div>
              {quizConfig.quizType === 'timed' && (
                <div className="p-4 bg-gray-100 rounded-lg">
                  <p className="text-gray-600">Time Limit</p>
                  <p className="text-xl font-medium">{quizConfig.timeLimit} minutes</p>
                </div>
              )}
            </div>

            <h3 className="text-lg font-bold mb-3">Selected Questions:</h3>
            <div className="space-y-2 max-h-64 overflow-y-auto mb-6 p-4 bg-gray-50 rounded-lg">
              {selectedQuestions.map((q, idx) => (
                <div key={q.id} className="flex gap-3 p-2">
                  <span className="font-medium text-gray-600 flex-shrink-0">{idx + 1}.</span>
                  <span className="text-gray-700">{q.title}</span>
                </div>
              ))}
            </div>

            {/* Final Actions */}
            <div className="flex gap-4">
              <button
                onClick={() => setStep(2)}
                className="flex-1 px-6 py-3 border-2 border-gray-600 text-gray-600 rounded-lg font-medium hover:bg-gray-100"
              >
                Back
              </button>
              <button
                onClick={startQuiz}
                disabled={loading}
                className="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 disabled:bg-gray-400 text-lg"
              >
                {loading ? 'Starting...' : 'Start Quiz'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default QuizBuilder;
