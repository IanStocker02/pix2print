import { Outlet } from 'react-router-dom';

const App = () => {
  return (
    <div>
      <div id="top-bar">
        <h1>Placeholder Title</h1>
        <nav>
          <a href="/">Home</a>
          <a href="/page1">Page 1</a>
          <a href="/page2">Page 2</a>
        </nav>
      </div>
      <Outlet />
    </div>
  );
};

export default App;