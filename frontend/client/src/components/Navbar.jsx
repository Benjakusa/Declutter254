import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1rem 2rem',
    backgroundColor: '#2c3e50',
    color: 'white',
    borderBottom: '1px solid #dee2e6'
  };

  const linksStyle = {
    display: 'flex',
    gap: '20px',
    alignItems: 'center'
  };

  const linkStyle = {
    color: 'white',
    textDecoration: 'none',
    fontWeight: '500'
  };

  return (
    <nav style={navStyle}>
      <Link to="/" style={{ ...linkStyle, fontSize: '1.5rem', fontWeight: 'bold' }}>
        Declutter254
      </Link>

      <div style={linksStyle}>
        <Link style={linkStyle} to="/">Home</Link>
        {user && (
          <>
            <Link style={linkStyle} to="/post-item">Post Item</Link>
            <Link style={linkStyle} to="/requests">Requests</Link>
            <Link style={linkStyle} to="/profile">Profile</Link>
          </>
        )}
        {user ? (
          <>
            <span style={{ marginRight: '10px' }}>Hello, {user.name}</span>
            <button
              onClick={handleLogout}
              style={{
                padding: '5px 15px',
                cursor: 'pointer',
                backgroundColor: '#e74c3c',
                color: 'white',
                border: 'none',
                borderRadius: '4px'
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link style={linkStyle} to="/login">Login</Link>
            <Link style={linkStyle} to="/signup">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;