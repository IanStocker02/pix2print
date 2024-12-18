import React, { useState } from 'react';
import SignupModal from '../components/SignupModal';
import '../assets/SignupModal.css'

const LoginPage = () => {
  const [isSignupOpen, setSignupOpen] = useState(false);
  const [username, setUsername] = useState(''); 
  const [password, setPassword] = useState(''); 
  const [isLoggedIn, setIsLoggedIn] = useState(false); 

  const openSignupModal = () => setSignupOpen(true);
  const closeSignupModal = () => setSignupOpen(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (username && password) {
      setIsLoggedIn(true);
    }
  };

  return (
    <div>
      <h1>Login</h1>

      {isLoggedIn ? (
        <div>
          <h2>Hello, {username}!</h2>
          <p>Welcome back to Pix2Print.</p>
        </div>
      ) : (
        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit">Login</button>
          <div>
            <a href="#" onClick={openSignupModal}>Don't have an account? Sign up now!</a>
          </div>
        </form>
      )}

      <SignupModal isOpen={isSignupOpen} onClose={closeSignupModal} />
    </div>
  );
};

export default LoginPage;