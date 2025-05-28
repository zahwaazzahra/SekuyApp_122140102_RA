// components/navbar.jsx
import React from "react";
import { NavLink } from "react-router-dom";
import "../styles/navbar.css";
import { useAuth } from "../hooks/useAuth";

const Navbar = () => {
  const { isAuthenticated, logout, user, isAdmin } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <nav className="navbar">
      <NavLink
        to="/"
        end
        className={({ isActive }) => (isActive ? "active" : undefined)}
      >
        Home
      </NavLink>
      <NavLink
        to="/rent"
        className={({ isActive }) => (isActive ? "active" : undefined)}
      >
        Rent
      </NavLink>

      {isAuthenticated && (
        <NavLink
          to="/dashboard"
          className={({ isActive }) => (isActive ? "active" : undefined)}
        >
          Dashboard
        </NavLink>
      )}

      {isAuthenticated && isAdmin() && (
        <NavLink
          to="/admin-dashboard"
          className={({ isActive }) => (isActive ? "active" : undefined)}
        >
          Admin Panel
        </NavLink>
      )}

      <div className="auth-links">
        {isAuthenticated ? (
          <>
            <span style={{ color: "#d46b8b", marginRight: "1rem" }}>
              Halo, {user?.username || "User"}!
            </span>
            <button
              onClick={handleLogout}
              style={{
                background: "none",
                border: "none",
                color: "#d46b8b",
                cursor: "pointer",
                fontSize: "1.1rem",
                fontWeight: "600",
                padding: "0.5rem 1rem",
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <NavLink
              to="/login"
              className={({ isActive }) => (isActive ? "active" : undefined)}
            >
              Login
            </NavLink>
            <NavLink
              to="/register"
              className={({ isActive }) => (isActive ? "active" : undefined)}
            >
              Register
            </NavLink>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
