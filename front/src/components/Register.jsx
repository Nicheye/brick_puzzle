import React, { useState } from 'react';
import axios from 'axios';

const Register = ({ onRegister }) => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const submit = async (e) => {
    e.preventDefault();

    try {
      await fetch('http://localhost:8000/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const response = await axios.post('http://localhost:8000/auth/login/', {
        email,
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      });

      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      
    
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <form onSubmit={submit}>
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit">Register</button>
    </form>
  );
};

export default Register;