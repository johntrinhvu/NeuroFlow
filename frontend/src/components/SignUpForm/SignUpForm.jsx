import { Component } from 'react';

export default class SignUpForm extends Component {
  state = {
    name: '',
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
  };

  render() {
    const disable = this.state.password !== this.state.confirm;
    return (
      <>
        <div className="title-wrapper">
            <h1 className="title font-semibold">Create an account</h1>
        </div>
        <div className="login-container">
          <form autoComplete="off" onSubmit={this.handleSubmit} className="input-wrapper">
            <input type="text" className="login-input-box" placeholder="Full Name" name="name" value={this.state.name} onChange={this.handleChange} required />
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