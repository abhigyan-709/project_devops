import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Assuming you have your CSS here

function App() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    city: '',
    username: '',
    email: '',
    password: '',
  });
  const [errorMessage, setErrorMessage] = useState('');
  const [isLogin, setIsLogin] = useState(true); // Toggle between Login and Register
  const [token, setToken] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isLogin) {
        // Handle login
        const response = await axios.post('http://13.201.83.111:30960/token', {
          username: formData.username,
          password: formData.password,
        });
        setToken(response.data.access_token);
        setErrorMessage('');
      } else {
        // Handle registration
        const response = await axios.post('http://13.201.83.111:30960/register/', {
          username: formData.username,
          password: formData.password,
          email: formData.email,
          first_name: formData.first_name,
          last_name: formData.last_name,
          city: formData.city,
        });
        setErrorMessage('');
        alert('Registration successful!');
      }
    } catch (error) {
      // Handle Axios error
      if (error.response && error.response.data) {
        // Extract the error message from the response
        const errorMsg = error.response.data.detail || 'Something went wrong!';
        setErrorMessage(errorMsg);
      } else {
        setErrorMessage('Network error or server not reachable.');
      }
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>{isLogin ? 'Login' : 'Register'}</h1>
        <form className="form" onSubmit={handleSubmit}>
          {/* Conditional rendering for different form fields */}
          {!isLogin && (
            <>
              <div className="form-group">
                <label htmlFor="first_name">First Name</label>
                <input
                  type="text"
                  id="first_name"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleInputChange}
                  placeholder="Enter your first name"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="last_name">Last Name</label>
                <input
                  type="text"
                  id="last_name"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleInputChange}
                  placeholder="Enter your last name"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="city">City</label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={formData.city}
                  onChange={handleInputChange}
                  placeholder="Enter your city"
                  required
                />
              </div>
            </>
          )}
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              placeholder="Enter your username"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="Enter your email"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              placeholder="Enter your password"
              required
            />
          </div>
          <div className="form-group">
            <button type="submit" className="btn-submit">
              {isLogin ? 'Login' : 'Register'}
            </button>
          </div>
        </form>

        {/* Toggle between Login and Register */}
        <button onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? 'Need an account? Register here' : 'Already have an account? Login here'}
        </button>

        {/* Display error message */}
        {errorMessage && <div className="error-message">{errorMessage}</div>}
      </header>
    </div>
  );
}

export default App;
