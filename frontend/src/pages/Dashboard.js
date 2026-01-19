import React, { useState, useEffect } from 'react';
import { profileAPI, sessionsAPI } from '../services/api';
import StatsCard from '../components/StatsCard';
import RecentQuizzes from '../components/RecentQuizzes';

const Dashboard = () => {
  const [profile, setProfile] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [profileRes, sessionsRes] = await Promise.all([
        profileAPI.getMe(),
        sessionsAPI.getAll(),
      ]);
      
      setProfile(profileRes.data);
      setSessions(sessionsRes.data.results || sessionsRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading dashboard...</div>;
  }

  if (!profile) {
    return <div className="text-center py-8">Error loading profile</div>;
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatsCard 
          label="Questions Solved"
          value={profile.total_questions_solved}
          icon="✓"
        />
        <StatsCard 
          label="Quizzes Completed"
          value={profile.total_quizzes_completed}
          icon="📋"
        />
        <StatsCard 
          label="Accuracy"
          value={`${profile.overall_accuracy.toFixed(1)}%`}
          icon="🎯"
        />
        <StatsCard 
          label="Last Practice"
          value={profile.last_practice_date ? new Date(profile.last_practice_date).toLocaleDateString() : 'Never'}
          icon="📅"
        />
      </div>

      {/* Weak Areas */}
      {profile.weak_areas && Object.keys(profile.weak_areas).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">Areas to Improve</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {Object.entries(profile.weak_areas).map(([area, accuracy]) => (
              <div key={area} className="bg-red-50 p-4 rounded-lg">
                <p className="font-medium capitalize">{area.replace('_', ' ')}</p>
                <p className="text-lg text-red-600">{accuracy.toFixed(1)}% accuracy</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Quizzes */}
      <RecentQuizzes sessions={sessions} />
    </div>
  );
};

export default Dashboard;
