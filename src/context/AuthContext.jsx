import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);  // user diset awalnya null

  const login = (userData) => {
    setUser(userData);  // Menyimpan data user ketika login
  };

  const logout = () => {
    setUser(null);  // Menghapus data user ketika logout
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}  {/* Membungkus komponen anak dengan nilai context */}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);  // Hook untuk mengakses AuthContext
