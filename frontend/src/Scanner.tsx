import React, { useState, useEffect } from 'react';
import './assets/Scanner.css'; // Add necessary styles

const Scanner: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div className="scanner-container">
      <div
        className="scan-beam"
        style={{
          top: `${mousePosition.y}px`,
        }}
      ></div>
      {children}
    </div>
  );
};

export default Scanner;
