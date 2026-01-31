import React, { useState, useEffect } from 'react';
import { questionsAPI, quizAPI } from '../services/api';
import './QuizPage.css';

function QuizPage({ user }) {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [showQuiz, setShowQuiz] = useState(false);
  const [filters, setFilters] = useState({ question_type: '', difficulty: '', category: '' });
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await questionsAPI.getCategories();
        setCategories(response.data.categories || []);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    fetchCategories();
  }, []);

  const handleStartQuiz = async () => {
    try {
      const response = await questionsAPI.filter(filters);
      setQuestions(response.data.results || []);
      setCurrentQuestion(0);
      setShowQuiz(true);
    } catch (error) {
      console.error('Error fetching questions:', error);
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  if (!showQuiz) {
    return (
      <div className="quiz-setup">
        <div className="container">
          <h1>📝 Create a Quiz</h1>
          
          <div className="quiz-form">
            <div className="form-group">
              <label>Question Type</label>
              <select value={filters.question_type} onChange={(e) => setFilters({...filters, question_type: e.target.value})}>
                <option value="">All Types</option>
                <option value="DSA">Data Structures & Algorithms</option>
                <option value="OOP">Object-Oriented Programming</option>
                <option value="PF">Pattern Fundamentals</option>
                <option value="DB">Database Systems</option>
              </select>
            </div>

            <div className="form-group">
              <label>Difficulty</label>
              <select value={filters.difficulty} onChange={(e) => setFilters({...filters, difficulty: e.target.value})}>
                <option value="">All Levels</option>
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>

            <div className="form-group">
              <label>Category</label>
              <select value={filters.category} onChange={(e) => setFilters({...filters, category: e.target.value})}>
                <option value="">All Categories</option>
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <button className="btn-start" onClick={handleStartQuiz}>
              Start Quiz
            </button>
          </div>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];

  return (
    <div className="quiz-page">
      <div className="container">
        <div className="quiz-header">
          <h1>Question {currentQuestion + 1} of {questions.length}</h1>
          <div className="progress-bar">
            <div className="progress" style={{width: `${((currentQuestion + 1) / questions.length) * 100}%`}}></div>
          </div>
        </div>

        {question && (
          <div className="question-card">
            <div className="question-meta">
              <span className={`badge badge-${question.difficulty.toLowerCase()}`}>{question.difficulty}</span>
              <span className="category">{question.category}</span>
            </div>
            
            <h2>{question.title}</h2>
            <p className="description">{question.description}</p>

            {question.code_template && (
              <pre className="code-template">{question.code_template}</pre>
            )}

            <textarea className="answer-input" placeholder="Write your solution here..."></textarea>

            <div className="quiz-actions">
              <button className="btn btn-prev" onClick={handlePreviousQuestion} disabled={currentQuestion === 0}>
                ← Previous
              </button>
              <button className="btn btn-submit">
                Submit Answer
              </button>
              <button className="btn btn-next" onClick={handleNextQuestion} disabled={currentQuestion === questions.length - 1}>
                Next →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default QuizPage;
