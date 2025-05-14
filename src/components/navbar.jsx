import React from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : undefined}>
        Home
      </NavLink>
      <NavLink to="/rent" className={({ isActive }) => isActive ? 'active' : undefined}>
        Rent
      </NavLink>
      <NavLink to="/payment" className={({ isActive }) => isActive ? 'active' : undefined}>
        Payment
      </NavLink>
      <NavLink to="/Confirmation" className={({ isActive }) => isActive ? 'active' : undefined}>
        Confirmation
      </NavLink>
    </nav>
  );
};

export default Navbar;
