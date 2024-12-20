// AboutUs.tsx
import React from 'react';
import '../assets/AboutUs.css'; // Optional: import a specific CSS file for this page

const AboutUs = () => {
  return (
    <div className="about-us">
      <h1>About Us</h1>
      <p>We are a team of three developers working to bring this site to life.</p>

      <h2>Meet the Team:</h2>

      {/* Developer 1 */}
      <div className="developer">
        <h3>Developer 1: Elliot Stocker</h3>
        <p><strong>Role:</strong> Full Stack Developer</p>
        <p><strong>Skills:</strong> React, TypeScript, CSS, HTML</p>
        <p><strong>Bio:</strong> John is passionate about building intuitive and responsive web applications. He loves working with modern JavaScript frameworks like React and ensuring a seamless user experience.</p>
      </div>

      {/* Developer 2 */}
      <div className="developer">
        <h3>Developer 2: Joey Vedder</h3>
        <p><strong>Role:</strong> Full Stack Developer</p>
        <p><strong>Skills:</strong> Node.js, Express, MongoDB, APIs</p>
        <p><strong>Bio:</strong> Jane is focused on server-side development, building robust and scalable backend systems. She enjoys working with databases and creating secure, efficient APIs.</p>
      </div>

      {/* Developer 3 */}
      <div className="developer">
        <h3>Developer 3: Ian Stocker</h3>
        <p><strong>Role:</strong> Full Stack Developer</p>
        <p><strong>Skills:</strong> React, Node.js, JavaScript, SQL</p>
        <p><strong>Bio:</strong> Alex bridges the gap between frontend and backend, creating end-to-end solutions. With a deep understanding of both technologies, Alex enjoys building feature-rich, full-stack applications.</p>
      </div>
    </div>
  );
};

export default AboutUs;
