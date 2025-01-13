import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import { FaSun, FaMoon } from "react-icons/fa";
import { motion } from "framer-motion";
import { Carousel } from 'react-bootstrap';
import "bootstrap/dist/css/bootstrap.min.css";
import '@fortawesome/fontawesome-free/css/all.min.css';
import '@fontsource/poppins/300.css';
import '@fontsource/poppins/400.css';
import '@fontsource/poppins/500.css';
import '@fontsource/poppins/600.css';
import '@fontsource/poppins/700.css';

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
  const [showAuthModal, setShowAuthModal] = useState(false);

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
        setShowAuthModal(false);
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
        setIsLogin(true);
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
      {/* Enhanced Header */}
      <header className="app-header">
  <nav className="navbar">
    <div className="navbar-container">
      <div className="navbar-brand-section">
        <h1 className="navbar-brand">Utility App</h1>
        <div className="navbar-tagline">Your Ultimate Utility Solution</div>
      </div>
      
      <div className="nav-links">
        <ul className="nav-menu">
          <li className="nav-item">
            <a href="#utilities" className="nav-link">
              <i className="fas fa-tools"></i>
              Utilities
            </a>
          </li>
          <li className="nav-item">
            <a href="#downloaders" className="nav-link">
              <i className="fas fa-download"></i>
              Downloaders
            </a>
          </li>
          <li className="nav-item">
            <a href="#job-portal" className="nav-link">
              <i className="fas fa-briefcase"></i>
              Job Portal
            </a>
          </li>
          <li className="nav-item">
            <a href="#about" className="nav-link">
              <i className="fas fa-info-circle"></i>
              About Us
            </a>
          </li>
          <li className="nav-item">
            <a href="#contact" className="nav-link">
              <i className="fas fa-envelope"></i>
              Contact
            </a>
          </li>
        </ul>
      </div>

      <div className="navbar-actions">
        {!token ? (
          <>
            <button className="auth-btn login-btn" onClick={() => {
              setIsLogin(true);
              setShowAuthModal(true);
            }}>
              <i className="fas fa-sign-in-alt"></i>
              Login
            </button>
            <button className="auth-btn register-btn" onClick={() => {
              setIsLogin(false);
              setShowAuthModal(true);
            }}>
              <i className="fas fa-user-plus"></i>
              Register
            </button>
          </>
        ) : (
          <button className="auth-btn logout-btn" onClick={handleLogout}>
            <i className="fas fa-sign-out-alt"></i>
            Logout
          </button>
        )}
        <button className="theme-toggle-btn" onClick={toggleTheme}>
          {isDarkMode ? <FaSun className="sun-icon" /> : <FaMoon className="moon-icon" />}
        </button>
      </div>
    </div>
  </nav>
</header>

      <main>
        {/* Hero Section */}
        <section className="hero-section">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="hero-content"
          >
            <h1>Welcome to Utility App</h1>
            <p>Your one-stop solution for all utility needs</p>
            <button className="cta-button">Get Started</button>
          </motion.div>
        </section>

        {/* Features Section */}
        <section className="features-section">
          <h2>Our Features</h2>
          <div className="features-grid">
            {[
              {
                title: "Easy to Use",
                description: "Simple and intuitive interface for all users",
                icon: "🚀"
              },
              {
                title: "Secure",
                description: "Top-notch security for your peace of mind",
                icon: "🔒"
              },
              {
                title: "24/7 Support",
                description: "Round-the-clock support for all your needs",
                icon: "💬"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="feature-card"
                whileHover={{ scale: 1.05 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <div className="feature-icon">{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Carousel Section */}
        <section className="carousel-section">
          <Carousel>
            <Carousel.Item>
              <div className="carousel-content">
                <h3>Powerful Tools</h3>
                <p>Access a wide range of utility tools</p>
              </div>
            </Carousel.Item>
            <Carousel.Item>
              <div className="carousel-content">
                <h3>Smart Solutions</h3>
                <p>Innovative solutions for modern problems</p>
              </div>
            </Carousel.Item>
            <Carousel.Item>
              <div className="carousel-content">
                <h3>Global Community</h3>
                <p>Join our worldwide community of users</p>
              </div>
            </Carousel.Item>
          </Carousel>
        </section>

        {/* Statistics Section */}
        <section className="stats-section">
          <div className="stats-grid">
            {[
              { number: "1000+", label: "Active Users" },
              { number: "50+", label: "Features" },
              { number: "24/7", label: "Support" },
            ].map((stat, index) => (
              <motion.div
                key={index}
                className="stat-card"
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
              >
                <h2>{stat.number}</h2>
                <p>{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Auth Modal */}
        {showAuthModal && (
          <div className="auth-modal">
            <div className="modal-content">
              <button className="close-btn" onClick={() => setShowAuthModal(false)}>
                ×
              </button>
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
            </div>
          </div>
        )}
      </main>

      {/* Enhanced Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h3 className="footer-title">About Us</h3>
            <p className="footer-description">
              Utility App provides comprehensive solutions for all your utility needs.
              We're dedicated to making your life easier with our innovative tools.
            </p>
          </div>

          <div className="footer-section">
            <h3 className="footer-title">Quick Links</h3>
            <ul className="footer-links">
              <li><a href="#home">Home</a></li>
              <li><a href="#services">Services</a></li>
              <li><a href="#pricing">Pricing</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h3 className="footer-title">Contact Info</h3>
            <ul className="footer-contact">
              <li>
                <i className="fas fa-envelope"></i>
                <a href="mailto:contact@utilityapp.com">contact@utilityapp.com</a>
              </li>
              <li>
                <i className="fas fa-phone"></i>
                <a href="tel:+1234567890">+1 (234) 567-890</a>
              </li>
              <li>
                <i className="fas fa-map-marker-alt"></i>
                <span>123 Tech Street, Digital City</span>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h3 className="footer-title">Follow Us</h3>
            <div className="social-links">
              <a href="#" className="social-link"><i className="fab fa-facebook"></i></a>
              <a href="#" className="social-link"><i className="fab fa-twitter"></i></a>
              <a href="#" className="social-link"><i className="fab fa-linkedin"></i></a>
              <a href="#" className="social-link"><i className="fab fa-github"></i></a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <div className="footer-bottom-content">
            <p className="copyright">
              © {new Date().getFullYear()} Utility App. All Rights Reserved.
            </p>
            <div className="footer-bottom-links">
              <a href="#privacy">Privacy Policy</a>
              <a href="#terms">Terms of Service</a>
              <a href="#cookies">Cookie Policy</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;