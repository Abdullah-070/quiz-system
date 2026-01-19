import React, { useState, useEffect } from 'react';
import { leaderboardAPI } from '../services/api';

const Leaderboard = () => {
  const [leaders, setLeaders] = useState([]);
  const [period, setPeriod] = useState('week');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLeaderboard();
  }, [period]);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await leaderboardAPI.getAll(period);
      setLeaders(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8">Leaderboard</h1>

      {/* Period Selector */}
      <div className="flex gap-4 mb-8">
        {['week', 'month', 'all_time'].map(p => (
          <button
            key={p}
            onClick={() => setPeriod(p)}
            className={`px-4 py-2 rounded-lg font-medium ${
              period === p
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
            }`}
          >
            {p === 'week' ? 'This Week' : p === 'month' ? 'This Month' : 'All Time'}
          </button>
        ))}
      </div>

      {/* Leaderboard Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-100 border-b">
            <tr>
              <th className="text-left p-4 font-bold">Rank</th>
              <th className="text-left p-4 font-bold">User</th>
              <th className="text-left p-4 font-bold">Questions Solved</th>
              <th className="text-left p-4 font-bold">Accuracy</th>
              <th className="text-left p-4 font-bold">Score</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="5" className="text-center py-8">Loading...</td>
              </tr>
            ) : leaders.length === 0 ? (
              <tr>
                <td colSpan="5" className="text-center py-8">No leaderboard data yet</td>
              </tr>
            ) : (
              leaders.map(leader => (
                <tr key={leader.id} className="border-b hover:bg-gray-50">
                  <td className="p-4">
                    <span className="text-2xl">
                      {leader.rank === 1 ? '🥇' : leader.rank === 2 ? '🥈' : leader.rank === 3 ? '🥉' : leader.rank}
                    </span>
                  </td>
                  <td className="p-4">{leader.user.username}</td>
                  <td className="p-4">{leader.questions_solved}</td>
                  <td className="p-4">{leader.accuracy.toFixed(1)}%</td>
                  <td className="p-4 font-bold text-blue-600">{leader.score}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Leaderboard;
