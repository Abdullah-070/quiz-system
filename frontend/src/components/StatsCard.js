import React from 'react';

const StatsCard = ({ label, value, icon }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow">
      <div className="text-4xl mb-2">{icon}</div>
      <p className="text-gray-600 text-sm mb-2">{label}</p>
      <p className="text-3xl font-bold text-blue-600">{value}</p>
    </div>
  );
};

export default StatsCard;
