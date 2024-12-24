import React from 'react';
import '../assets/SignupModal.css';

const SignupModal = ({ isOpen, onClose }) => {
  return (
    <div className={`modal-overlay ${isOpen ? 'visible' : ''}`}>
      <div className="modal-content">
        <form>
          <h2>Sign Up</h2>
          <input type="text" placeholder="Username" />
          <input type="password" placeholder="Password" />
          <button>Sign Up</button>
        <button onClick={onClose}>Close</button>
        </form>
      </div>
    </div>
  );
};

export default SignupModal;


