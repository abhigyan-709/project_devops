// src/index.js
import React from 'react';
import { createRoot } from 'react-dom/client'; // Import createRoot instead of render
import './index.css';
import App from './App';
import { ThemeProvider } from './context/ThemeContext';

// Create a root
const root = createRoot(document.getElementById('root'));

// Render your app
root.render(
  <React.StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </React.StrictMode>
);