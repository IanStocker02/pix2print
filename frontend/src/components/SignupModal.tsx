import React from 'react';
import '../assets/SignupModal.css';

const SignupModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Sign Up</h2>
        <form>
          <input type="text" placeholder="Username" />
          <input type="password" placeholder="Password" />
          <button>Sign Up</button>
        </form>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default SignupModal;