import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home1';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentView, setCurrentView] = useState('login');

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await axios.get('http://localhost:8000/auth/home/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (response.status === 200) {
          setIsAuthenticated(true);
        }
      } catch (err) {
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
    setCurrentView('home');
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsAuthenticated(false);
    setCurrentView('login');
  };

  return (
    <Router>
      <div>
        {isAuthenticated ? (
          <Home onLogout={handleLogout} />
        ) : (
          <div>
            {currentView === 'login' ? (
              <Login onLogin={handleLogin} />
            ) : (
              <Register onRegister={() => setCurrentView('login')} />
            )}
            <div>
              {currentView === 'login' ? (
                <p>
                  Don't have an account?{' '}
                  <button onClick={() => setCurrentView('register')}>Register</button>
                </p>
              ) : (
                <p>
                  Already have an account?{' '}
                  <button onClick={() => setCurrentView('login')}>Login</button>
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </Router>
  );
};

export default App;
