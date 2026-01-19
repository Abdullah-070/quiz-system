import React, { useState, useEffect, useCallback } from 'react';
import { questionsAPI } from '../services/api';
import QuestionCard from '../components/QuestionCard';

const QuestionBrowser = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(10);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [filters, setFilters] = useState({
    difficulty: '',
    topic: '',
    search: '',
  });

  const fetchQuestions = useCallback(async () => {
    try {
      setLoading(true);
      const offset = (currentPage - 1) * itemsPerPage;
      const params = {
        ...filters,
        limit: itemsPerPage,
        offset: offset,
      };
      const response = await questionsAPI.getAll(params);
      setQuestions(response.data.results || response.data);
      setTotalQuestions(response.data.count || response.data.length);
    } catch (error) {
      console.error('Error fetching questions:', error);
    } finally {
      setLoading(false);
    }
  }, [currentPage, itemsPerPage, filters]);

  useEffect(() => {
    setCurrentPage(1);
  }, [filters, itemsPerPage]);

  useEffect(() => {
    fetchQuestions();
  }, [fetchQuestions]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleItemsPerPageChange = (e) => {
    setItemsPerPage(parseInt(e.target.value));
  };

  const totalPages = Math.ceil(totalQuestions / itemsPerPage);
  const displayedQuestions = questions.slice(0, itemsPerPage);

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8">Question Bank</h1>
      
      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="grid grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Search</label>
            <input
              type="text"
              name="search"
              value={filters.search}
              onChange={handleFilterChange}
              placeholder="Search questions..."
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Category</label>
            <select
              name="topic"
              value={filters.topic}
              onChange={handleFilterChange}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="">All Categories</option>
              <option value="dsa">DSA (Data Structures)</option>
              <option value="oop">OOP (Object-Oriented)</option>
              <option value="dbs">DBS (Database & SQL)</option>
              <option value="pf">PF (Functional Programming)</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Difficulty</label>
            <select
              name="difficulty"
              value={filters.difficulty}
              onChange={handleFilterChange}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="">All Levels</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Per Page</label>
            <select
              value={itemsPerPage}
              onChange={handleItemsPerPageChange}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="5">5 Questions</option>
              <option value="10">10 Questions</option>
              <option value="20">20 Questions</option>
              <option value="50">50 Questions</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Info */}
      <div className="text-sm text-gray-600 mb-4">
        Showing {((currentPage - 1) * itemsPerPage) + 1} - {Math.min(currentPage * itemsPerPage, totalQuestions)} of {totalQuestions} questions
      </div>

      {/* Questions List */}
      <div className="space-y-4">
        {loading ? (
          <div className="text-center py-8">Loading...</div>
        ) : displayedQuestions.length === 0 ? (
          <div className="text-center py-8">No questions found</div>
        ) : (
          displayedQuestions.map(question => (
            <QuestionCard key={question.id} question={question} />
          ))
        )}
      </div>

      {/* Pagination */}
      <div className="flex justify-between items-center mt-8 pt-6 border-t">
        <button
          onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
          disabled={currentPage === 1}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg disabled:bg-gray-400 hover:bg-blue-700"
        >
          ← Previous
        </button>
        
        <div className="flex items-center gap-2">
          <span className="text-gray-600">
            Page <span className="font-bold">{currentPage}</span> of <span className="font-bold">{totalPages || 1}</span>
          </span>
        </div>
        
        <button
          onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
          disabled={currentPage >= totalPages}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg disabled:bg-gray-400 hover:bg-blue-700"
        >
          Next →
        </button>
      </div>
    </div>
  );
};

export default QuestionBrowser;
