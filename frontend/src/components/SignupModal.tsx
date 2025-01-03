import React, { useState } from 'react';
import axios from 'axios';
import '../assets/SignupModal.css';

const SignupModal = ({ isOpen, onClose, onSignup }: { 
  isOpen: boolean; 
  onClose: () => void; 
  onSignup: (signupData: { username: string; password: string }) => void; 
}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSignupSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password || !confirmPassword) {
      setErrorMessage('All fields are required.');
      return;
    }
    if (password !== confirmPassword) {
      setErrorMessage('Passwords do not match.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/auth/signup', {
        username,
        password,
      });
      onSignup(response.data);
      onClose();
    } catch (error) {
      setErrorMessage(error.response?.data?.message || 'Signup failed. Please try again.');
    }
  };

  return (
    <div className={`modal-overlay ${isOpen ? 'visible' : ''}`}>
      <div className="modal-content">
        <h2>Sign Up</h2>
        <form onSubmit={handleSignupSubmit}>
          {errorMessage && <p className="error-message">{errorMessage}</p>}
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
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <button type="submit" className="signup-btn">Sign Up</button>
          <button type="button" onClick={onClose}>Close</button>
        </form>
      </div>
    </div>
  );
};

export default SignupModal;