import { Outlet, useLocation } from 'react-router-dom';

const App = () => {
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';

  return (
    <div>
      <header id="top-bar">
        <div className="container">
          <h1 className="logo">Pix2Print</h1>
          <nav>
            <a href="/" className="nav-link">Home</a>
            <a href="/about" className="nav-link">About</a>
            <a href="/login" className="nav-link">Login</a>
          </nav>
        </div>
      </header>

      {!isLoginPage && (
        <main>
          <section id="hero">
            <div className="container">
              <h2>Convert 3D Models Effortlessly</h2>
              <p>
                Transform your 3D models into various formats in seconds. Upload your file
                and get started!
              </p>
              <a href="/start" className="cta-button">Start Converting</a>
            </div>
          </section>

          <section id="features">
            <div className="container">
              <h3>Key Features</h3>
              <div className="features-grid">
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
                  <p>
                    Ensure your models look great after conversion with our advanced
                    technology.
                  </p>
                </div>
              </div>
            </div>
          </section>
        </main>
      )}

      {!isLoginPage && (
        <footer id="footer">
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
