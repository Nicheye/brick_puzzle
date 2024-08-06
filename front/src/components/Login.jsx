import React, { useState } from 'react';
import axios from 'axios';
import land_img from '../assets/land_img.png'

const Login = () => {
  const [email, setEmail] = useState('');

  const submit = async e => {
    e.preventDefault();

    const user = {
      email: email
    };

    const config = {
      headers: {
        'Content-Type': 'application/json'
      },
      withCredentials: true
    };

    try {
      const { data } = await axios.post('http://localhost:8000/auth/login/', user, config);
      localStorage.clear();
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      axios.defaults.headers.common['Authorization'] = `Bearer ${data['access']}`;
      window.location.href = '/';
    } catch (error) {
      console.error('Login failed:', error.response ? error.response.data : error.message);
      
      try {
        const registerResponse = await fetch('http://localhost:8000/auth/register/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(user)
        });

        if (registerResponse.ok) {
          const { data } = await axios.post('http://localhost:8000/auth/login/', user, config);
          localStorage.clear();
          localStorage.setItem('access_token', data.access);
          localStorage.setItem('refresh_token', data.refresh);
          axios.defaults.headers.common['Authorization'] = `Bearer ${data['access']}`;
          window.location.href = '/';
        } else {
          const errorData = await registerResponse.json();
          console.error('Registration failed:', errorData);
        }
      } catch (registerError) {
        console.error('Registration and login failed:', registerError);
      }
    }
  };

  return (
    <>
    <div className="p-3">
    <div class="flex items-center justify-center mt-10">
        <img class="h-auto max-w-full rounded-lg" src={land_img} alt="image description"/>
    </div>


    <div href="#" className="block max-w-sm p-6 bg-black border border-gray-800 rounded-lg shadow hover:bg-gray-900 auth_form">
      <h1 className="mb-4 text-2xl font-bold leading-snug tracking-tight text-gray-100 md:text-3xl lg:text-4xl">
        Contribute <mark className="px-2 text-white bg-blue-600 rounded dark:bg-blue-500">your part</mark> into collective art
      </h1>
      <h5 class="text-xl font-bold dark:text-white">Login or Register</h5>
      <form className="max-w-sm mx-auto auth_form_form" onSubmit={submit}>
        <label htmlFor="email-address-icon" className="block mb-2 text-sm font-medium text-gray-100">Your Email</label>
        <div className="relative">
          <div className="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
            <svg className="w-4 h-4 text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 16">
              <path d="m10.036 8.278 9.258-7.79A1.979 1.979 0 0 0 18 0H2A1.987 1.987 0 0 0 .641.541l9.395 7.737Z"/>
              <path d="M11.241 9.817c-.36.275-.801.425-1.255.427-.428 0-.845-.138-1.187-.395L0 2.6V14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2.5l-8.759 7.317Z"/>
            </svg>
          </div>
          <input type="email" value={email} required onChange={e => setEmail(e.target.value)} id="email-address-icon" className="bg-gray-800 border border-gray-700 text-gray-100 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 placeholder-gray-500" placeholder="name@flowbite.com"/>
        </div>
        <button type="submit" className="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-ml px-5 py-2.5 text-center mb-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 submit-btn">submit</button>
      </form>
    </div>
    </div>
    </>
  );
};

export default Login;
