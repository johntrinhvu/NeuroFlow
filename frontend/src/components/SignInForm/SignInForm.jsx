import { useState } from 'react';
import './SignInForm.css';

export default function SignInForm({ setUser }) {
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
  }

  return (
    <>
      <div className="title-wrapper">
        <h1 className="title font-semibold">Welcome back</h1>
      </div>
      <div className="login-container">
        <form autoComplete="off" onSubmit={handleSubmit} className="input-wrapper">
          <input type="email" placeholder="Email address" className="login-input-box" name="email" value={credentials.email} onChange={handleChange} required />
          <input type="password" placeholder="Password" className="login-input-box" name="password" value={credentials.password} onChange={handleChange} required />
          <button type="submit" className="continue-btn">Continue</button>
        </form>
      </div>
      <p className="error-message">&nbsp;{error}</p>
    </>
  );
}