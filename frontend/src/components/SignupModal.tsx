import React, { useState } from 'react';
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

  const handleSignupSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password || !confirmPassword) {
      setErrorMessage('All fields are required.');
      return;
    }
    if (password !== confirmPassword) {
      setErrorMessage('Passwords do not match.');
      return;
    }
    onSignup({ username, password });
    setUsername('');
    setPassword('');
    setConfirmPassword('');
    setErrorMessage('');
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay visible">
      <div className="modal-content">
        <form onSubmit={handleSignupSubmit}>
          <h2>Sign Up</h2>
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
          <button onClick={onClose}>Close</button>
        </form>
      </div>
    </div>
  );
};

export default SignupModal;
