import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Assuming you have your CSS here
import { FaSun, FaMoon } from 'react-icons/fa'; // React icons for sun and moon

// Header component


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
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Check for saved theme preference in localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDarkMode(true);
    }
  }, []);

  // Toggle theme
  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    const newTheme = !isDarkMode ? 'dark' : 'light';
    localStorage.setItem('theme', newTheme); // Save theme preference in localStorage
  };

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
        const response = await axios.post(
          'http://13.201.83.111:30960/token',
          new URLSearchParams({
            username: formData.username,
            password: formData.password,
          }),
          {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          }
        );

        // Save the token and show success message
        setToken(response.data.access_token);
        setErrorMessage('');
        alert('Login successful!'); // Show success popup
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
        alert('Registration successful!'); // Show success popup
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
    <div className={`App ${isDarkMode ? 'dark-theme' : 'light-theme'}`}>
    

      <div className="form-container">
        <h1>{isLogin ? 'Login' : 'Register'}</h1>
        <form className="form" onSubmit={handleSubmit}>
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
          {!isLogin && (
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
          )}
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

        <button onClick={() => setIsLogin(!isLogin)} type="submit" className="btn-submit">
          {isLogin ? 'Need an account? Register here' : 'Already have an account? Login here'}
        </button>

        {errorMessage && <div className="error-message">{errorMessage}</div>}
      </div>

      {/* Theme toggle button */}
      <button className="theme-toggle-btn" onClick={toggleTheme}>
        <FaSun className="sun-icon" />
        <FaMoon className="moon-icon" />
      </button>

      
    </div>
  );
}

export default App;
