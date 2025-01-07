
import React, { useState, useEffect } from 'react';
import { Outlet, useLocation, Link } from 'react-router-dom';

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(true);

  useEffect(() => {
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode === 'false') {
      setIsDarkMode(false);
      document.body.classList.add('light-mode');
    } else {
      setIsDarkMode(true);
      document.body.classList.add('dark-mode');
    }
  }, []);

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => {
      const newMode = !prevMode;
      localStorage.setItem('darkMode', newMode.toString());
      if (newMode) {
        document.body.classList.add('dark-mode');
        document.body.classList.remove('light-mode');
      } else {
        document.body.classList.add('light-mode');
        document.body.classList.remove('dark-mode');
      }
      return newMode;
    });
  };
  
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';
  const isHomePage = location.pathname === '/';

  const isLoggedIn = localStorage.getItem('token');  // Assuming a token means user is logged in

  return (
    <div>
      <header id="top-bar">
        <div className="header-container">
          <h1 className="header">Pix2Print</h1>
        </div>
        <nav>
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/about" className="nav-link">About</Link>
          <Link to="/start" className="nav-link">Start Converting</Link>
          <Link to="/billing" className="nav-link">Pricing</Link>
          {isLoggedIn ? (
            <Link to="/account" className="nav-link">My Account</Link>
          ) : (
            <Link to="/login" className="nav-link">Login</Link>
          )}
        </nav>
        <button onClick={toggleDarkMode} className="toggle-theme-btn">
          {isDarkMode ? '🤢' : '🙂‍↕️'}
        </button>
      </header>

      {isHomePage && !isLoginPage && <div className="scanAnimation"></div>}


      {/* Conditional content and footer rendering */}
      {isHomePage && !isLoginPage && (
        <main id="home-content">
          <section id="hero">
            <h2>Convert 3D Models Effortlessly</h2>
            <p>
              Transform your 3D models into various formats in seconds. Upload your file and get started!
            </p>
            <Link to="/start" className="cta-button">Start Converting</Link>
          </section>

          <section id="features">
            <h3>Key Features</h3>
            <div className="feature">
              <h4>Multiple Formats Supported</h4>
              <p>Supports a wide range of 3D file formats for easy conversion.</p>
            </div>
            <div className="feature">
              <h4>Fast and Easy</h4>
              <p>Convert your 3D models with just a few clicks and get instant results.</p>
            </div>
            <div className="feature">
              <h4>High-Quality Output</h4>
              <p>Ensure your models look great after conversion with our advanced technology.</p>
            </div>
          </section>
        </main>
      )}

      {isHomePage && !isLoginPage && (
        <footer id="footer">
          <div className="scan-effect"></div>
          <div className="container">
            <p>&copy; 2024 Pix2Print. All Rights Reserved.</p>
          </div>
        </footer>
      )}

      <Outlet />
    </div>
  );
};
export default App;
