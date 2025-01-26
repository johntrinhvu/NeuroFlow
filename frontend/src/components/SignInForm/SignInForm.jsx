import { useState } from 'react';
import { useNavigate } from "react-router-dom";
import './SignInForm.css';

export default function SignInForm() {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');

  function handleChange(evt) {
    setCredentials({ ...credentials, [evt.target.name]: evt.target.value });
    setError('');
  }

  async function handleSubmit(evt) {
    // Prevent form from being submitted to the server
    evt.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials)
      });

      if (!response.ok) {
        throw new Error('Invalid email or password');
      }

      const data = await response.json();
      localStorage.setItem('token', data.access_token)
      navigate('/');

    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <>
      <div className="title-wrapper">
        <h1 className="title font-semibold">Welcome back</h1>
      </div>
      <div className="login-container">
        <form autoComplete="off" onSubmit={handleSubmit} className="input-wrapper">
          <input type="email" placeholder="Email Address" className="login-input-box" name="email" value={credentials.email} onChange={handleChange} required />
          <input type="password" placeholder="Password" className="login-input-box" name="password" value={credentials.password} onChange={handleChange} required />
          <button type="submit" className="continue-btn">Continue</button>
        </form>
      </div>
      <p className="error-message">&nbsp;{error}</p>
    </>
  );
}