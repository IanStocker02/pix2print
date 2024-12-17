import { Link } from 'react-router-dom';

const Nav = () => {
  return (
    <nav>
      <Link to="/path1">Link 1</Link>
      <Link to="/path2">Link 2</Link>
    </nav>
  );
};

export default Nav;