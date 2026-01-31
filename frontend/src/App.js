import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { auth } from './services/firebase';
import { onAuthStateChanged } from 'firebase/auth';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import QuizPage from './pages/QuizPage';
import Leaderboard from './pages/Leaderboard';

// Components
import Navbar from './components/Navbar';

import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        {user && <Navbar user={user} />}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          {user && (
            <>
              <Route path="/dashboard" element={<Dashboard user={user} />} />
              <Route path="/quiz" element={<QuizPage user={user} />} />
              <Route path="/leaderboard" element={<Leaderboard />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
