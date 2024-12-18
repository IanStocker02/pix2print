import React, { useState } from 'react';
import SignupModal from '../components/SignupModal';

const LoginPage = () => {
  const [isSignupOpen, setSignupOpen] = useState(false);

  const openSignupModal = () => setSignupOpen(true);
  const closeSignupModal = () => setSignupOpen(false);

  return (
    <div>
      <h1>Login</h1>
      <form>
        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />
        <button>Login</button>
        <div>
          <a href="#" onClick={openSignupModal}>Don't have an account? Sign up now!</a>
        </div>
      </form>
      <SignupModal isOpen={isSignupOpen} onClose={closeSignupModal} />
    </div>
  );
};

export default LoginPage;