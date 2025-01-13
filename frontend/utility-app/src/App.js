import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import { FaSun, FaMoon } from "react-icons/fa";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    city: "",
    username: "",
    email: "",
    password: "",
  });
  const [errorMessage, setErrorMessage] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [token, setToken] = useState("");
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      setIsDarkMode(true);
    }
  }, []);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    const newTheme = !isDarkMode ? "dark" : "light";
    localStorage.setItem("theme", newTheme);
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
        const response = await axios.post(
          "http://13.201.83.111:30960/token",
          new URLSearchParams({
            username: formData.username,
            password: formData.password,
          }),
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
          }
        );
        setToken(response.data.access_token);
        setErrorMessage("");
        alert("Login successful!");
      } else {
        const response = await axios.post("http://13.201.83.111:30960/register/", {
          username: formData.username,
          password: formData.password,
          email: formData.email,
          first_name: formData.first_name,
          last_name: formData.last_name,
          city: formData.city,
        });
        setErrorMessage("");
        alert("Registration successful! Please log in.");
        setIsLogin(true); // Switch to login form after successful registration
      }
    } catch (error) {
      if (error.response && error.response.data) {
        const errorMsg = error.response.data.detail || "Something went wrong!";
        setErrorMessage(errorMsg);
      } else {
        setErrorMessage("Network error or server not reachable.");
      }
    }
  };

  const handleLogout = () => {
    setToken("");
    alert("You have been logged out.");
  };

  return (
    <div className={`App ${isDarkMode ? "dark-theme" : "light-theme"}`}>
      {/* Header */}
      <header className="app-header">
      <nav className="navbar">
  <h1 className="navbar-brand">Utility App</h1>
  <div className="nav-buttons">
    <button className="nav-btn">Utilities</button>
    <button className="nav-btn">Downloaders</button>
    <button className="nav-btn">Job Portal</button>
    <button className="nav-btn">About Us</button>
    <button className="nav-btn">Contact Us</button>
    {!token ? (
      <>
        <button
          className={`nav-btn ${isLogin ? "active" : ""}`}
          onClick={() => setIsLogin(true)}
        >
          Login
        </button>
        <button
          className={`nav-btn ${!isLogin ? "active" : ""}`}
          onClick={() => setIsLogin(false)}
        >
          Register
        </button>
      </>
    ) : (
      <button className="nav-logout-btn" onClick={handleLogout}>
        Logout
      </button>
    )}
    {/* Add the theme toggle button here */}
    <button className="theme-toggle-btn" onClick={toggleTheme}>
      {isDarkMode ? <FaSun className="sun-icon" /> : <FaMoon className="moon-icon" />}
    </button>
  </div>
</nav>

      </header>

      {/* Main Content */}
      <main className="main-content">
        {token ? (
          <div className="logout-container">
            <h2>Welcome, {formData.username}!</h2>
            <button className="btn-logout" onClick={handleLogout}>
              Logout
            </button>
          </div>
        ) : (
          <div className="form-container">
            <h2>{isLogin ? "Login" : "Register"}</h2>
            <form onSubmit={handleSubmit}>
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
                  required
                />
              </div>
              <button type="submit" className="btn-submit">
                {isLogin ? "Login" : "Register"}
              </button>
            </form>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>© 2025 Utility App. All Rights Reserved.</p>
      </footer>
    </div>
  );
}

export default App;
