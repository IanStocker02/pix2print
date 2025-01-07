import React from 'react';
import { Helmet } from 'react-helmet';
import '../assets/AboutUs.css';

const teamMembers = [
  {
    name: 'Elliot Stocker',
    role: 'Full-Stack Developer',
    description: 'Elliot bridges the gap between front-end and back-end development with versatile skills and database integration.',
    linkedin: 'https://www.linkedin.com/in/jacob-stocker-bb781a333/', 
    github: 'https://github.com/jelliots2', 
  },
  {
    name: 'Joey Vedder',
    role: 'Full-Stack Developer',
    description: 'Worked on the frontend, responsive design, local storage functionality, and resolving any issues to deliver a user-friendly experience.',
    linkedin: 'https://www.linkedin.com/in/joey-vedder-4b0a6a324/', 
    github: 'https://github.com/joeyvedder', 
  },
  {
    name: 'Ian Stocker',
    role: 'Full-Stack Developer',
    description: 'Ian is a master at building scalable APIs and managing back end processes.',
    linkedin: 'https://www.linkedin.com/in/ianstocker', // Replace with actual LinkedIn URL
    github: 'https://github.com/ianstocker', // Replace with actual GitHub URL
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
              <h3>{member.name}</h3>
              <p className="team-role">{member.role}</p>
              <p className="team-description">{member.description}</p>
              <div className="team-links">
                <a
                  href={member.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="team-link"
                >
                  LinkedIn
                </a>
                {' | '}
                <a
                  href={member.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="team-link"
                >
                  GitHub
                </a>
              </div>
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
