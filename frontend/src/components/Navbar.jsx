import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Navbar() {
  const location = useLocation();

  return (
    <nav className="glass-panel" style={{ 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center', 
      padding: '1rem 2rem',
      marginBottom: '2rem',
      borderRadius: '1rem'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <h2 style={{ margin: 0, fontSize: '1.5rem', background: 'linear-gradient(to right, #60a5fa, #34d399)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          JobCheq
        </h2>
      </div>
      
      <div style={{ display: 'flex', gap: '1.5rem' }}>
        <NavLink to="/" current={location.pathname}>Analyze</NavLink>
        <NavLink to="/report" current={location.pathname}>Report Scam</NavLink>
        <NavLink to="/awareness" current={location.pathname}>Safety Tips</NavLink>
      </div>
    </nav>
  );
}

function NavLink({ to, current, children }) {
  const isActive = current === to;
  return (
    <Link to={to} style={{ 
      textDecoration: 'none', 
      color: isActive ? '#fff' : '#94a3b8',
      fontWeight: isActive ? 600 : 400,
      transition: 'color 0.3s ease',
      borderBottom: isActive ? '2px solid #3b82f6' : '2px solid transparent'
    }}>
      {children}
    </Link>
  );
}

export default Navbar;
