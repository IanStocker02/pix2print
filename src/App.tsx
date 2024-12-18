import { Outlet } from 'react-router-dom';

const App = () => {
  return (
    <div>
      <div id="top-bar">
        <h1>pix2print</h1>
        <nav>
          <a href="/">Home</a>
          <a href="/start">start</a>
          <a href="/login">login</a>
        </nav>
      </div>
      <Outlet />
    </div>
  );
};

export default App;