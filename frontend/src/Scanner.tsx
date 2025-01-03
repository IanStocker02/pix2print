// Import React and necessary hooks
// import React, { useState, useEffect } from 'react';
// Import styles for the Scanner component
// import './assets/Scanner.css'; // Add necessary styles

// Define the Scanner component with a React functional component
// const Scanner: React.FC<{ children: React.ReactNode }> = ({ children }) => {
//   // State to track the mouse position
//   const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

//   // Effect to add and clean up mousemove event listener
//   useEffect(() => {
//     const handleMouseMove = (e: MouseEvent) => {
//       // Update the mouse position state
//       setMousePosition({ x: e.clientX, y: e.clientY });
//     };

//     // Add mousemove event listener
//     window.addEventListener('mousemove', handleMouseMove);

//     // Cleanup the event listener on component unmount
//     return () => {
//       window.removeEventListener('mousemove', handleMouseMove);
//     };
//   }, []);

//   // Return the Scanner component JSX
//   return (
//     <div className="scanner-container">
//       <div
//         className="scan-beam"
//         style={{
//           top: `${mousePosition.y}px`,
//         }}
//       ></div>
//       {children}
//     </div>
//   );
// };

// Export the Scanner component
// export default Scanner;
