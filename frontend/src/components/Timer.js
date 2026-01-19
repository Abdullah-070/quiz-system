import React, { useState, useEffect } from 'react';

const Timer = ({ timeLimit }) => {
  const [timeLeft, setTimeLeft] = useState(timeLimit * 60);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const isWarning = timeLeft < 300; // Less than 5 minutes

  return (
    <div className={`text-2xl font-bold ${isWarning ? 'text-red-600' : 'text-blue-600'}`}>
      ⏱️ {minutes}:{seconds.toString().padStart(2, '0')}
    </div>
  );
};

export default Timer;
