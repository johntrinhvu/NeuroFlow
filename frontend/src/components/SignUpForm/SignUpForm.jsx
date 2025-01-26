import { Component } from 'react';
import { Navigate } from "react-router-dom";

export default class SignUpForm extends Component {
  state = {
    username: '',
    email: '',
    password: '',
    confirm: '',
    error: ''
  };

  handleChange = (evt) => {
    this.setState({
      [evt.target.name]: evt.target.value,
      error: ''
    });
  };

  handleSubmit = async (evt) => {
    evt.preventDefault();

    const { username, email, password } = this.state;

    try {
      const response = await fetch("http://localhost:8000/users/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to sign up");
      }

      // redirect
      this.setState({ redirect: true });
    } catch (error) {
      this.setState({ error: error.message });
    }
  };

  render() {
    const disable = this.state.password !== this.state.confirm;

    if (this.state.redirect) {
      return <Navigate to="/" />;
    }

    return (
      <>
        <div className="title-wrapper">
            <h1 className="title font-semibold">Create an account</h1>
        </div>
        <div className="login-container">
          <form autoComplete="off" onSubmit={this.handleSubmit} className="input-wrapper">
            <input type="text" className="login-input-box" placeholder="Username" name="username" value={this.state.username} onChange={this.handleChange} required />
            <input type="email" className="login-input-box" placeholder="Email" name="email" value={this.state.email} onChange={this.handleChange} required />
            <input type="password" className="login-input-box" placeholder="Password" name="password" value={this.state.password} onChange={this.handleChange} required />
            <input type="password" className="login-input-box" placeholder="Confirm Password" name="confirm" value={this.state.confirm} onChange={this.handleChange} required />
            <button type="submit" disabled={disable} className="continue-btn">Sign Up</button>
          </form>
        </div>
        <p className="error-message">&nbsp;{this.state.error}</p>
      </>
    );
  }
}