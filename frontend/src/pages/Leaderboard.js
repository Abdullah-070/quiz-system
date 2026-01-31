import React, { useState, useEffect } from 'react';
import { leaderboardAPI } from '../services/api';
import './Leaderboard.css';

function Leaderboard() {
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const weekStart = new Date();
        weekStart.setDate(weekStart.getDate() - weekStart.getDay());
        
        // In a real app, fetch from API
        // For now, show placeholder data
        setLeaders([
          { rank: 1, username: 'CodeMaster', quizzes_completed: 45, accuracy: 92.5 },
          { rank: 2, username: 'AlgoWhiz', quizzes_completed: 42, accuracy: 90.2 },
          { rank: 3, username: 'DataGeek', quizzes_completed: 40, accuracy: 88.7 },
          { rank: 4, username: 'JavaNinja', quizzes_completed: 38, accuracy: 87.3 },
          { rank: 5, username: 'PythonPro', quizzes_completed: 35, accuracy: 85.9 },
        ]);
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) return <div className="loading">Loading leaderboard...</div>;

  return (
    <div className="leaderboard">
      <div className="container">
        <h1>🏆 Weekly Leaderboard</h1>
        
        <div className="leaderboard-table">
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>Quizzes Completed</th>
                <th>Accuracy</th>
              </tr>
            </thead>
            <tbody>
              {leaders.map((leader) => (
                <tr key={leader.rank} className={`rank-${leader.rank}`}>
                  <td className="rank-cell">
                    {leader.rank === 1 ? '🥇' : leader.rank === 2 ? '🥈' : leader.rank === 3 ? '🥉' : leader.rank}
                  </td>
                  <td>{leader.username}</td>
                  <td>{leader.quizzes_completed}</td>
                  <td>
                    <span className="accuracy-badge">{leader.accuracy}%</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;
