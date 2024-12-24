import React from 'react';
import { Helmet } from 'react-helmet';
import '../assets/AboutUs.css';

const teamMembers = [
  {
    name: 'Elliot Stocker',
    role: 'Full-Stack Developer',
    description: 'Elliot specializes in creating beautiful, responsive user interfaces with React and CSS.',
    imgSrc: 'https://via.placeholder.com/150',
  },
  {
    name: 'Joey Vedder',
    role: 'Full-Stack Developer',
    description: 'Joey is a master at building scalable APIs and managing databases effectively.',
    imgSrc: 'https://via.placeholder.com/150',
  },
  {
    name: 'Ian Stocker',
    role: 'Full-Stack Developer',
    description: 'Ian bridges the gap between front-end and back-end development with versatile skills.',
    imgSrc: 'https://via.placeholder.com/150',
  },
];

const AboutUs = () => {
  return (
    <div className="about-us">
      <Helmet>
        <title>About Us - Pix2Print</title>
        <meta name="description" content="Learn about Pix2Print and meet our dedicated team of developers." />
        <link
          href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap"
          rel="stylesheet"
        />
      </Helmet>
      <header className="about-header">
        <h1>About Us</h1>
        <p>
          At Pix2Print, we are dedicated to simplifying 3D model conversions with cutting-edge tools and a user-first approach.
        </p>
      </header>
      <section className="mission">
        <h2>Our Mission</h2>
        <p>
          Empower creators and developers with seamless 3D model conversion solutions, ensuring quality, speed, and ease of use.
        </p>
      </section>
      <section className="team">
        <h2>Meet the Team</h2>
        <div className="team-grid">
          {teamMembers.map((member, index) => (
            <div key={index} className="team-card">
              <img src={member.imgSrc} alt={`${member.name}'s profile`} className="team-photo" />
              <h3>{member.name}</h3>
              <p className="team-role">{member.role}</p>
              <p className="team-description">{member.description}</p>
            </div>
          ))}
        </div>
      </section>
      <footer>
        <p>&copy; {new Date().getFullYear()} Pix2Print. All Rights Reserved.</p>
      </footer>
    </div>
  );
};

export default AboutUs;
