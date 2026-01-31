import React, { useState, useEffect } from 'react';
import { usersAPI } from '../services/api';
import './Dashboard.css';

function Dashboard({ user }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // In a real app, you'd fetch user stats from the API
        // For now, we'll show placeholder data
        setStats({
          total_questions_solved: 45,
          total_quizzes_completed: 12,
          overall_accuracy: 78.5,
          last_practice_date: new Date().toLocaleDateString(),
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [user]);

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="dashboard">
      <div className="container">
        <h1>Welcome, {user?.email}! 👋</h1>
        
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Questions Solved</h3>
            <p className="stat-value">{stats?.total_questions_solved}</p>
          </div>
          <div className="stat-card">
            <h3>Quizzes Completed</h3>
            <p className="stat-value">{stats?.total_quizzes_completed}</p>
          </div>
          <div className="stat-card">
            <h3>Overall Accuracy</h3>
            <p className="stat-value">{stats?.overall_accuracy}%</p>
          </div>
          <div className="stat-card">
            <h3>Last Practice</h3>
            <p className="stat-value">{stats?.last_practice_date}</p>
          </div>
        </div>

        <div className="quick-actions">
          <h2>Quick Actions</h2>
          <div className="action-buttons">
            <button className="action-btn practice">
              📝 Start Practice
            </button>
            <button className="action-btn timed">
              ⏱️ Timed Quiz (30 min)
            </button>
            <button className="action-btn mock">
              🎯 Mock Interview
            </button>
            <button className="action-btn custom">
              ⚙️ Custom Quiz
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
