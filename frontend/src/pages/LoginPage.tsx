import React, { useState } from 'react';
import axios from 'axios';
import SignupModal from '../components/SignupModal';
import '../assets/LoginPage.css';

const LoginPage = () => {
  const [isSignupOpen, setSignupOpen] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const openSignupModal = () => setSignupOpen(true);
  const closeSignupModal = () => setSignupOpen(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', { username, password });
      const { access_token } = response.data;

      // Save token to localStorage (or cookies if preferred)
      localStorage.setItem('token', access_token);
      setIsLoggedIn(true);
      setErrorMessage('');
    } catch (error) {
      console.error('Login failed:', error);
      setErrorMessage('Invalid username or password. Please try again.');
    }
  };

  const handleSignup = async (signupData: { username: string; password: string }) => {
    try {
      await axios.post('http://localhost:5000/signup', signupData);
      alert('Signup successful! Please log in.');
      closeSignupModal();
    } catch (error) {
      console.error('Signup failed:', error);
      alert('Signup failed. Please try again.');
    }
  };

  return (
    <div className="login">
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
          {errorMessage && <p className="error-message">{errorMessage}</p>}
          <div>
            <a href="#" onClick={openSignupModal}>
              Don't have an account? Sign up now!
            </a>
          </div>
        </form>
      )}

      <SignupModal
        isOpen={isSignupOpen}
        onClose={closeSignupModal}
        onSignup={handleSignup}
      />
    </div>
  );
};

export default LoginPage;
