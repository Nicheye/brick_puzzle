import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
  const [email, setEmail] = useState('');

  const submit = async e => {
    e.preventDefault();

    const user = {
      email: email
    };

    try {
      // Register the user
      await fetch('http://localhost:8000/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(user)
      });

      // Auto-login the user
      const config = {
        headers: {
          'Content-Type': 'application/json'
        },
        withCredentials: true
      };

      const { data } = await axios.post('http://localhost:8000/auth/login/', user, config);
      localStorage.clear();
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${data['access']}`;
      window.location.href = '/';
    } catch (error) {
      console.error('Registration or login failed', error);
    }
  };

  return (
    <div className="Auth-form-container">
      <form className="Auth-form" onSubmit={submit}>
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign Up</h3>
          <div className="form-group mt-3">
            <label>Email</label>
            <input
              name='email'
              type="email"
              className="form-control mt-1"
              placeholder="Enter email"
              value={email}
              required
              onChange={e => setEmail(e.target.value)}
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">Submit</button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default Register;