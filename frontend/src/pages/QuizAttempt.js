import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';
import { sessionsAPI } from '../services/api';

const QuizAttempt = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();

  const [session, setSession] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(null);

  useEffect(() => {
    loadSessionData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionId]);

  useEffect(() => {
    if (!timeLeft || timeLeft <= 0 || showResults) return;

    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          finishQuiz();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeLeft, showResults]);

  const loadSessionData = async () => {
    try {
      setLoading(true);
      const sessionRes = await sessionsAPI.getById(sessionId);
      setSession(sessionRes.data);

      // Initialize timer if timed quiz
      if (sessionRes.data.time_limit > 0) {
        setTimeLeft(sessionRes.data.time_limit * 60); // Convert to seconds
      }

      // Load all questions for this session
      if (sessionRes.data.questions && Array.isArray(sessionRes.data.questions)) {
        setQuestions(sessionRes.data.questions);
        if (sessionRes.data.questions.length > 0) {
          setCode(sessionRes.data.questions[0].template_code || '');
        }
      }
    } catch (error) {
      console.error('Error loading session:', error);
      alert('Failed to load quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const submitAnswer = async () => {
    if (!questions[currentIndex]) return;

    try {
      setSubmitting(true);
      const currentQuestion = questions[currentIndex];

      await sessionsAPI.submitAnswer(sessionId, {
        question_id: currentQuestion.id,
        code,
      });

      // Store answer
      setAnswers(prev => ({
        ...prev,
        [currentQuestion.id]: code,
      }));

      // Move to next question
      if (currentIndex < questions.length - 1) {
        setCurrentIndex(currentIndex + 1);
        setCode(questions[currentIndex + 1].template_code || '');
      } else {
        // Quiz completed
        await finishQuiz();
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Failed to submit answer');
    } finally {
      setSubmitting(false);
    }
  };

  const finishQuiz = async () => {
    try {
      setSubmitting(true);
      await sessionsAPI.finish(sessionId);
      setShowResults(true);
    } catch (error) {
      console.error('Error finishing quiz:', error);
      alert('Failed to complete quiz');
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (seconds) => {
    if (!seconds) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-4xl mb-4">Loading quiz...</div>
        </div>
      </div>
    );
  }

  if (!session || questions.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="text-2xl mb-4">Error loading quiz</div>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  if (showResults) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="text-5xl mb-4">✓</div>
            <h1 className="text-3xl font-bold mb-2">Quiz Completed!</h1>
            <p className="text-gray-600 text-lg mb-8">
              You have successfully submitted all answers.
            </p>
            
            <div className="bg-blue-50 rounded-lg p-6 mb-8">
              <p className="text-gray-600 text-sm mb-2">Questions Answered</p>
              <p className="text-4xl font-bold text-blue-600">{Object.keys(answers).length} / {questions.length}</p>
            </div>

            <div className="space-y-3">
              <button
                onClick={() => navigate('/dashboard')}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
              >
                Back to Dashboard
              </button>
              <button
                onClick={() => navigate('/quizzes')}
                className="w-full px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 font-medium"
              >
                Create Another Quiz
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-md p-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">{session.title || 'Quiz'}</h1>
            <p className="text-gray-600">Question {currentIndex + 1} of {questions.length}</p>
          </div>
          <div className="flex gap-8 items-center">
            {timeLeft !== null && (
              <div className={`text-center ${timeLeft < 300 ? 'text-red-600' : ''}`}>
                <p className="text-sm text-gray-600">Time Left</p>
                <p className="text-3xl font-bold">{formatTime(timeLeft)}</p>
              </div>
            )}
            <button
              onClick={() => {
                if (window.confirm('Are you sure you want to finish the quiz?')) {
                  finishQuiz();
                }
              }}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Finish Quiz
            </button>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mt-4 w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden flex">
        {/* Questions Panel */}
        <div className="w-1/2 bg-white border-r overflow-y-auto p-6">
          <div className="max-w-2xl">
            <h2 className="text-2xl font-bold mb-4">{currentQuestion.title}</h2>
            
            <div className="mb-4 flex gap-2">
              <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                {currentQuestion.difficulty}
              </span>
              <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                {currentQuestion.category}
              </span>
            </div>

            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h3 className="font-bold mb-2">Problem:</h3>
              <p className="text-gray-700 whitespace-pre-wrap">{currentQuestion.description}</p>
            </div>

            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h3 className="font-bold mb-2">Template Code:</h3>
              <pre className="text-sm overflow-x-auto bg-gray-800 text-gray-100 p-3 rounded">
                {currentQuestion.template_code}
              </pre>
            </div>

            {currentQuestion.explanation && (
              <div className="bg-yellow-50 rounded-lg p-4">
                <h3 className="font-bold mb-2">Hint:</h3>
                <p className="text-gray-700">{currentQuestion.explanation.substring(0, 200)}...</p>
              </div>
            )}
          </div>
        </div>

        {/* Code Editor Panel */}
        <div className="w-1/2 flex flex-col">
          <div className="flex-1 overflow-hidden p-4">
            <AceEditor
              mode="python"
              theme="monokai"
              value={code}
              onChange={handleCodeChange}
              name="code_editor"
              width="100%"
              height="100%"
              fontSize={14}
              showPrintMargin={true}
              showGutter={true}
              highlightActiveLine={true}
              setOptions={{
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
                enableSnippets: true,
                showLineNumbers: true,
                tabSize: 4,
              }}
            />
          </div>

          {/* Navigation Buttons */}
          <div className="bg-white border-t p-4 flex gap-3 max-w-full">
            <button
              onClick={() => {
                if (currentIndex > 0) {
                  setCurrentIndex(currentIndex - 1);
                  setCode(questions[currentIndex - 1].template_code || '');
                }
              }}
              disabled={currentIndex === 0}
              className="px-6 py-2 border-2 border-gray-600 text-gray-600 rounded hover:bg-gray-100 disabled:opacity-50"
            >
              ← Previous
            </button>
            <button
              onClick={submitAnswer}
              disabled={submitting}
              className="flex-1 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400 font-medium"
            >
              {submitting ? 'Submitting...' : currentIndex === questions.length - 1 ? 'Submit & Finish' : 'Submit & Next'}
            </button>
            <button
              onClick={() => {
                if (currentIndex < questions.length - 1) {
                  setCurrentIndex(currentIndex + 1);
                  setCode(questions[currentIndex + 1].template_code || '');
                }
              }}
              disabled={currentIndex === questions.length - 1}
              className="px-6 py-2 border-2 border-gray-600 text-gray-600 rounded hover:bg-gray-100 disabled:opacity-50"
            >
              Next →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizAttempt;
