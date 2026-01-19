import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-github';
import { quizzesAPI, sessionsAPI } from '../services/api';
import Timer from '../components/Timer';

const QuizInterface = () => {
  const { quizId } = useParams();
  const [quiz, setQuiz] = useState(null);
  const [session, setSession] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    initializeQuiz();
  }, [quizId]);

  const initializeQuiz = async () => {
    try {
      setLoading(true);
      // Fetch quiz details
      const quizRes = await quizzesAPI.getById(quizId);
      setQuiz(quizRes.data);

      // Start quiz session
      const sessionRes = await quizzesAPI.start(quizId);
      setSession(sessionRes.data);
      
      // Set initial code from first question
      if (quizRes.data.questions && quizRes.data.questions.length > 0) {
        setCode(quizRes.data.questions[0].question.template_code);
      }
    } catch (error) {
      console.error('Error initializing quiz:', error);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    try {
      setSubmitting(true);
      const currentQuestion = quiz.questions[currentQuestionIndex].question;
      
      await sessionsAPI.submitAnswer(session.id, {
        question_id: currentQuestion.id,
        code,
      });

      // Move to next question
      if (currentQuestionIndex < quiz.questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
        setCode(quiz.questions[currentQuestionIndex + 1].question.template_code);
      } else {
        // Quiz completed
        await sessionsAPI.finish(session.id);
        // Navigate to results page
      }
    } catch (error) {
      console.error('Error submitting answer:', error);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading quiz...</div>;
  }

  if (!quiz || !session) {
    return <div className="text-center py-8">Error loading quiz</div>;
  }

  const currentQuestion = quiz.questions[currentQuestionIndex].question;
  const progress = ((currentQuestionIndex + 1) / quiz.questions.length) * 100;

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-md p-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">{quiz.name}</h1>
          <p className="text-gray-600">Question {currentQuestionIndex + 1} of {quiz.questions.length}</p>
        </div>
        {quiz.time_limit > 0 && <Timer timeLimit={quiz.time_limit} />}
      </div>

      {/* Progress Bar */}
      <div className="bg-white border-b px-4 py-2">
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Problem Panel */}
        <div className="w-1/2 p-6 overflow-y-auto bg-white">
          <h2 className="text-3xl font-bold mb-4">{currentQuestion.title}</h2>
          <p className="text-gray-700 mb-6">{currentQuestion.description}</p>
          
          <div className="mb-6">
            <h3 className="font-bold text-lg mb-2">Examples:</h3>
            {currentQuestion.test_cases && currentQuestion.test_cases.slice(0, 2).map((test, idx) => (
              <div key={idx} className="bg-gray-100 p-4 rounded mb-2 text-sm">
                <p><strong>Input:</strong> {JSON.stringify(test.input)}</p>
                <p><strong>Output:</strong> {JSON.stringify(test.output)}</p>
              </div>
            ))}
          </div>

          {currentQuestion.explanation && (
            <div className="bg-blue-50 p-4 rounded">
              <h3 className="font-bold mb-2">Explanation:</h3>
              <p className="text-sm">{currentQuestion.explanation}</p>
            </div>
          )}
        </div>

        {/* Code Editor Panel */}
        <div className="w-1/2 p-6 bg-gray-50 flex flex-col">
          <h3 className="font-bold text-lg mb-4">Solution</h3>
          <div className="flex-1 border rounded-lg overflow-hidden mb-4">
            <AceEditor
              mode="python"
              theme="github"
              value={code}
              onChange={setCode}
              width="100%"
              height="100%"
              setOptions={{ tabSize: 2 }}
            />
          </div>

          <div className="flex gap-4">
            {currentQuestionIndex > 0 && (
              <button
                onClick={() => {
                  setCurrentQuestionIndex(currentQuestionIndex - 1);
                  setCode(quiz.questions[currentQuestionIndex - 1].question.template_code);
                }}
                className="flex-1 bg-gray-400 text-white py-2 rounded hover:bg-gray-500"
              >
                Previous
              </button>
            )}
            <button
              onClick={submitAnswer}
              disabled={submitting}
              className="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
            >
              {submitting ? 'Submitting...' : 'Submit & Next'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizInterface;
