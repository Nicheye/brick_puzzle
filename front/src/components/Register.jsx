// front/src/components/Register.jsx
import React, { useState } from 'react';

const Register = () => {
  const [email, setEmail] = useState('');

  const submit = async (e) => {
    e.preventDefault();

    await fetch('http://localhost:8000/register/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    window.location.href = '/login';
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
      <button type="submit">Register</button>
    </form>
  );
};

export default Register;