# Frontend Code Context from 'src'

This document contains the consolidated code from the 'src' directory.
It is intended for AI context or documentation purposes.

---

## File: `App.css`

```
/* Reset dasar */
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #fff0f5;
  color: #333;
}

/* Navbar */
.navbar {
  background-color: #ff69b4;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.navbar a {
  color: white;
  text-decoration: none;
  margin-left: 1rem;
  font-weight: bold;
}

.navbar a:hover {
  text-decoration: underline;
}

/* Container umum */
.container {
  max-width: 800px;
  margin: 2rem auto;
  background-color: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Judul */
h1, h2, h3, h4 {
  color: #e75480;
  margin-bottom: 1rem;
}

/* Tombol */
button {
  background-color: #ff69b4;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1rem;
}

button:hover {
  background-color: #e75480;
}

/* Input dan Select */
input[type="text"],
input[type="date"],
input[type="number"],
select {
  padding: 0.5rem;
  width: 100%;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}

/* Radio button */
input[type="radio"] {
  margin-right: 0.5rem;
}

/* Kartu sepeda */
.bike-card {
  border: 2px solid #ffb6c1;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  background-color: #fff8f9;
  transition: transform 0.2s ease;
}

.bike-card:hover {
  transform: scale(1.02);
  box-shadow: 0 0 12px rgba(255, 105, 180, 0.3);
}

/* QR Code */
.qr-container {
  margin-top: 1rem;
  text-align: center;
}

.qr-container img {
  border: 4px dashed #ff69b4;
  padding: 1rem;
  border-radius: 12px;
  background: #fff0f5;
}

/* Tiket */
.ticket {
  border: 2px dashed #ff69b4;
  padding: 1.5rem;
  border-radius: 10px;
  background-color: #fff;
}

/* Responsive */
@media (max-width: 600px) {
  .container {
    padding: 1rem;
    margin: 1rem;
  }

  .navbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .navbar a {
    margin: 0.5rem 0;
  }
}

```

## File: `App.jsx`

```
// App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar";
import Home from "./pages/Home";
import Rent from "./pages/Rent";
import Payment from "./pages/Payment.jsx";
import Confirmation from "./pages/Confirmation";
import Login from "./pages/Login";
import Register from "./pages/Register";
import UserDashboard from "./pages/UserDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./pages/AdminDashboard"; // Contoh import AdminDashboard

const App = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Rute yang Dilindungi untuk user biasa */}
        <Route
          path="/rent"
          element={
            <ProtectedRoute>
              <Rent />
            </ProtectedRoute>
          }
        />
        <Route
          path="/payment"
          element={
            <ProtectedRoute>
              <Payment />
            </ProtectedRoute>
          }
        />
        <Route
          path="/confirmation"
          element={
            <ProtectedRoute>
              <Confirmation />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <UserDashboard />
            </ProtectedRoute>
          }
        />

        {/* Rute yang Dilindungi khusus untuk Admin */}
        <Route
          path="/admin-dashboard"
          element={
            <ProtectedRoute adminOnly={true}>
              <AdminDashboard />
              {/* Pastikan kamu punya komponen AdminDashboard */}
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
};

export default App;

```

## File: `index.css`

```
/* src/index.css */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f0f0f0;
}

```

## File: `main.jsx`

```
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './styles/global.css'
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter> {/* <-- Di sini sudah ada Router */}
      <App />
    </BrowserRouter>
  </React.StrictMode>
);

```

## File: `components\ErrorBoundary.jsx`

```
import React, { Component } from 'react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.log(error, info);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}

export default ErrorBoundary;

```

## File: `components\Listsepeda.jsx`

```
import React from 'react';
import { useFetchBikes } from '../hooks/useFetchBikes';  // Mengimpor hook yang telah diperbaiki

const ListSepeda = () => {
  const { bikes, loading, error } = useFetchBikes();  // Mengambil data sepeda

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h2>Daftar Sepeda:</h2>
      <ul>
        {bikes.map((bike) => (
          <li key={bike.id}>
            {bike.name} - Rp{bike.price}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ListSepeda;

```

## File: `components\navbar.jsx`

```
// components/navbar.jsx
import React from "react";
import { NavLink } from "react-router-dom";
import "../styles/navbar.css";
import { useAuth } from "../hooks/useAuth";

const Navbar = () => {
  const { isAuthenticated, logout, user, isAdmin } = useAuth(); // Tambahkan isAdmin

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

      {/* Contoh penggunaan isAdmin untuk menampilkan link admin dashboard */}
      {isAuthenticated && isAdmin() && (
        <NavLink
          to="/admin-dashboard" // Ganti dengan path dashboard admin yang sebenarnya
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

```

## File: `components\ProtectedRoute.jsx`

```
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { isAuthenticated, loading, isAdmin } = useAuth(); // Tambahkan isAdmin

  if (loading) {
    return <p>Memverifikasi akses...</p>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Jika rute ini hanya untuk admin, dan user bukan admin, redirect ke home
  if (adminOnly && !isAdmin()) {
    return <Navigate to="/" replace />; // Atau ke halaman 403 / unauthorized
  }

  return children;
};

export default ProtectedRoute;

```

## File: `context\AuthContext.jsx`

```
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

```

## File: `context\Bikecontext.jsx`

```
import { createContext, useContext, useState } from "react";

const BikeContext = createContext();

export function BikeProvider({ children }) {
  const [selectedBike, setSelectedBike] = useState(null);

  return (
    <BikeContext.Provider value={{ selectedBike, setSelectedBike }}>
      {children}
    </BikeContext.Provider>
  );
}

export function useBike() {
  return useContext(BikeContext);
}

```

## File: `context\SepedaContext.jsx`

```
import React, { createContext, useContext, useState } from 'react';

const SepedaContext = createContext();

export const useSepeda = () => {
  return useContext(SepedaContext);
};

export const SepedaProvider = ({ children }) => {
  const [selectedBike, setSelectedBike] = useState(null);

  const selectBike = (bike) => {
    setSelectedBike(bike);
  };

  return (
    <SepedaContext.Provider value={{ selectedBike, selectBike }}>
      {children}
    </SepedaContext.Provider>
  );
};

```

## File: `hooks\useAuth.js`

```
import { useState, useEffect, useCallback } from "react";
import Cookies from "js-cookie";

const API_URL = "http://localhost:6543";

// Daftar email admin yang di-hardcode
const ADMIN_EMAILS = ["admin@example.com"]; // Tambahkan email admin di sini

export function useAuth() {
  const [user, setUser] = useState(() => {
    const cookieUser = Cookies.get("user");
    return cookieUser ? JSON.parse(cookieUser) : null;
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const readUserFromCookie = useCallback(() => {
    const cookieUser = Cookies.get("user");
    if (cookieUser) {
      try {
        return JSON.parse(cookieUser);
      } catch (e) {
        console.error("Failed to parse user cookie:", e);
        Cookies.remove("user");
        return null;
      }
    }
    return null;
  }, []);

  useEffect(() => {
    const initialUser = readUserFromCookie();
    setUser(initialUser);
    setLoading(false);
  }, [readUserFromCookie]);

  // Fungsi untuk mengecek apakah user adalah admin
  const isAdmin = useCallback(() => {
    return user && ADMIN_EMAILS.includes(user.email);
  }, [user]);

  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        const errorMessage = data.error || "Login failed.";
        setError(errorMessage);
        setLoading(false);
        return { success: false, error: errorMessage };
      }

      Cookies.set("user", JSON.stringify(data.user), {
        sameSite: "Lax",
        expires: 7,
      });

      setUser(data.user);
      setLoading(false);
      return { success: true, user: data.user };
    } catch (err) {
      setError("An unexpected error occurred. Please try again.");
      setLoading(false);
      return { success: false, error: "An unexpected error occurred." };
    }
  };

  const register = async (username, email, password, role = "client") => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ username, email, password, role }),
      });

      const data = await res.json();

      if (!res.ok) {
        const errorMessage = data.error || "Registration failed.";
        setError(errorMessage);
        setLoading(false);
        return { success: false, error: errorMessage };
      }

      setLoading(false);
      return { success: true, message: data.message, user: data.user };
    } catch (err) {
      setError("An unexpected error occurred. Please try again.");
      setLoading(false);
      return { success: false, error: "An unexpected error occurred." };
    }
  };

  const logout = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/logout`, {
        method: "POST",
        credentials: "include",
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.error || "Logout failed.");
        setLoading(false);
        return { success: false, error: data.error };
      }

      Cookies.remove("user");
      setUser(null);
      setLoading(false);

      return { success: true, message: "Logout successful." };
    } catch (err) {
      setError("An unexpected error occurred during logout.");
      setLoading(false);
      return {
        success: false,
        error: "An unexpected error occurred during logout.",
      };
    }
  }, []);

  const checkSession = useCallback(() => {
    const currentUser = readUserFromCookie();
    const isValid = !!currentUser;
    return {
      isValid,
      user: isValid ? currentUser : null,
    };
  }, [readUserFromCookie]);

  return {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    checkSession,
    isAdmin, // Tambahkan fungsi isAdmin ke dalam return
  };
}

```

## File: `hooks\useBikes.js`

```
import { useState, useEffect, useCallback } from "react";
import Cookies from "js-cookie";

const API_URL = "http://localhost:6543";

export function useBikes() {
  const [bikes, setBikes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async (endpoint = "/bikes", options = {}) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        credentials: "include", // Penting untuk mengirim cookie autentikasi
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Terjadi kesalahan saat memuat data.");
      }
      return data;
    } catch (err) {
      console.error("API call error:", err); // Log error asli untuk debugging
      setError(
        err.message || "Terjadi kesalahan tidak terduga. Silakan coba lagi."
      );
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  // Ambil semua sepeda saat hook dimuat
  useEffect(() => {
    const fetchAllBikes = async () => {
      const result = await fetchData();
      if (result) {
        setBikes(result);
      } else {
        setBikes([]); // Kosongkan jika ada error atau tidak ada data
      }
    };
    fetchAllBikes();
  }, [fetchData]);

  const getBike = useCallback(
    async (id) => {
      return await fetchData(`/bikes/${id}`);
    },
    [fetchData]
  );

  const createBike = useCallback(
    async (bikeData) => {
      const result = await fetchData("/bikes", {
        method: "POST",
        body: JSON.stringify(bikeData),
      });
      if (result) {
        setBikes((prevBikes) => [...prevBikes, result]); // Tambahkan sepeda baru ke state
        return { success: true, bike: result };
      }
      return { success: false, error: error };
    },
    [fetchData, error]
  );

  const updateBike = useCallback(
    async (id, bikeData) => {
      const result = await fetchData(`/bikes/${id}`, {
        method: "PUT",
        body: JSON.stringify(bikeData),
      });
      if (result) {
        setBikes((prevBikes) =>
          prevBikes.map((bike) => (bike.id === id ? result : bike))
        ); // Update sepeda di state
        return { success: true, bike: result };
      }
      return { success: false, error: error };
    },
    [fetchData, error]
  );

  const deleteBike = useCallback(
    async (id) => {
      const result = await fetchData(`/bikes/${id}`, {
        method: "DELETE",
      });
      if (result && result.message) {
        // Backend mengembalikan {'message': 'Bike deleted successfully'}
        setBikes((prevBikes) => prevBikes.filter((bike) => bike.id !== id)); // Hapus dari state
        return { success: true, message: result.message };
      }
      return { success: false, error: error };
    },
    [fetchData, error]
  );

  return {
    bikes,
    loading,
    error,
    getBike,
    createBike,
    updateBike,
    deleteBike,
  };
}

```

## File: `hooks\useFetchBikes.js`

```
useEffect(() => {
  fetch("http://localhost:8000/api/bikes")  // Pastikan URL API sesuai dengan backend yang benar
    .then((response) => response.json())
    .then((data) => {
      console.log("Data received:", data);  // Debugging: Cek data yang diterima
      setBikes(data);
      setLoading(false);
    })
    .catch((error) => {
      console.error("Error fetching bikes:", error);  // Debugging: Cek error
      setError(error);
      setLoading(false);
    });
}, []);

```

## File: `hooks\useRentals.js`

```
import { useState, useEffect, useCallback } from "react";
import { useAuth } from "./useAuth";

const API_URL = "http://localhost:6543";

export function useRentals() {
  const [rentals, setRentals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user, isAuthenticated, isAdmin } = useAuth(); // Mengambil isAdmin dari useAuth

  const fetchData = useCallback(async (endpoint, options = {}) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        credentials: "include",
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Terjadi kesalahan saat memuat data.");
      }
      return data;
    } catch (err) {
      console.error("API call error:", err);
      setError(
        err.message || "Terjadi kesalahan tidak terduga. Silakan coba lagi."
      );
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  // Ambil semua rental user atau semua rental jika admin
  useEffect(() => {
    const fetchRelevantRentals = async () => {
      if (isAuthenticated) {
        let result;
        if (isAdmin()) {
          // Jika user adalah admin, ambil SEMUA rental dari endpoint admin
          result = await fetchData(`/admin/rentals`);
        } else if (user && user.id) {
          // Jika user biasa, ambil rental khusus user tersebut
          result = await fetchData(`/rentals`);
        } else {
          // Jika terautentikasi tapi user.id tidak ada (misal, data cookie rusak)
          setRentals([]);
          return;
        }

        if (result) {
          setRentals(result);
        } else {
          setRentals([]); // Kosongkan jika ada error atau tidak ada data
        }
      } else {
        setRentals([]); // Kosongkan jika tidak terautentikasi
      }
    };
    fetchRelevantRentals();
  }, [fetchData, isAuthenticated, user, isAdmin]); // isAdmin ditambahkan ke dependency array

  const getRental = useCallback(
    async (id) => {
      if (!isAuthenticated) {
        setError("Anda harus login untuk melihat detail rental.");
        return null;
      }
      // Admin bisa melihat detail rental siapapun, user biasa hanya rentalnya sendiri
      // Perbaikan: endpoint admin harus menyertakan ID rental
      const endpoint = isAdmin() ? `/admin/rentals/${id}` : `/rentals/${id}`;
      return await fetchData(endpoint);
    },
    [fetchData, isAuthenticated, isAdmin]
  );

  const createRental = useCallback(
    async (rentalData) => {
      if (!isAuthenticated || !user) {
        setError("Anda harus login untuk membuat rental.");
        return { success: false, error: "Unauthorized" };
      }

      const payload = {
        ...rentalData,
        user_id: user.id, // Pastikan user_id diambil dari user yang sedang login
      };

      const result = await fetchData("/rentals", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (result) {
        // Setelah membuat rental, pastikan state rentals diperbarui
        setRentals((prevRentals) => [...prevRentals, result]);
        return { success: true, rental: result };
      }
      return { success: false, error: error };
    },
    [fetchData, isAuthenticated, user, error]
  );

  const updateRental = useCallback(
    async (id, rentalData) => {
      if (!isAuthenticated) {
        setError("Anda harus login untuk memperbarui rental.");
        return { success: false, error: "Unauthorized" };
      }
      // Admin bisa update rental siapapun, user biasa hanya rentalnya sendiri
      const endpoint = isAdmin() ? `/admin/rentals/${id}` : `/rentals/${id}`;
      const result = await fetchData(endpoint, {
        method: "PUT",
        body: JSON.stringify(rentalData),
      });
      if (result) {
        setRentals((prevRentals) =>
          prevRentals.map((rental) => (rental.id === id ? result : rental))
        ); // Update rental di state
        return { success: true, rental: result };
      }
      return { success: false, error: error };
    },
    [fetchData, isAuthenticated, error, isAdmin]
  );

  const cancelRental = useCallback(
    async (id) => {
      if (!isAuthenticated) {
        setError("Anda harus login untuk membatalkan rental.");
        return { success: false, error: "Unauthorized" };
      }
      // Admin bisa membatalkan rental siapapun, user biasa hanya rentalnya sendiri
      const endpoint = isAdmin() ? `/admin/rentals/${id}` : `/rentals/${id}`;
      const result = await fetchData(endpoint, {
        method: "DELETE", // Backend menggunakan DELETE untuk cancel
      });
      if (result && result.message) {
        // Backend mengembalikan {'message': 'Rental ... cancelled successfully'}
        setRentals((prevRentals) =>
          prevRentals.map((rental) =>
            rental.id === id ? { ...rental, status: "cancelled" } : rental
          )
        ); // Update status di state
        return { success: true, message: result.message };
      }
      return { success: false, error: error };
    },
    [fetchData, isAuthenticated, error, isAdmin]
  );

  // Fungsi BARU: updateRentalStatus
  const updateRentalStatus = useCallback(
    async (id, newStatus) => {
      if (!isAuthenticated) {
        setError("Anda harus login untuk mengubah status rental.");
        return { success: false, error: "Unauthorized" };
      }
      // Admin bisa update status rental siapapun, user biasa hanya rentalnya sendiri
      const endpoint = isAdmin() ? `/admin/rentals/${id}` : `/rentals/${id}`;
      const result = await fetchData(endpoint, {
        method: "PUT",
        body: JSON.stringify({ status: newStatus }), // Hanya kirim status
      });
      if (result) {
        setRentals((prevRentals) =>
          prevRentals.map((rental) => (rental.id === id ? result : rental))
        );
        return { success: true, rental: result };
      }
      return { success: false, error: error };
    },
    [fetchData, isAuthenticated, isAdmin, error]
  );

  // Fungsi BARU: deleteRental (penghapusan permanen)
  const deleteRental = useCallback(
    async (id) => {
      if (!isAuthenticated) {
        setError("Anda harus login untuk menghapus rental.");
        return { success: false, error: "Unauthorized" };
      }
      // Admin bisa menghapus rental siapapun, user biasa tidak bisa
      if (!isAdmin()) {
        setError("Anda tidak memiliki izin untuk menghapus rental.");
        return { success: false, error: "Forbidden" };
      }
      const endpoint = `/admin/rentals/${id}`; // Endpoint khusus admin untuk delete permanen
      const result = await fetchData(endpoint, {
        method: "DELETE",
      });
      if (result && result.message) {
        setRentals((prevRentals) =>
          prevRentals.filter((rental) => rental.id !== id)
        ); // Hapus dari state
        return { success: true, message: result.message };
      }
      return { success: false, error: error };
    },
    [fetchData, isAuthenticated, isAdmin, error]
  );

  return {
    rentals,
    loading,
    error,
    getRental,
    createRental,
    updateRental,
    cancelRental,
    updateRentalStatus, // <-- Fungsi baru ini sudah ditambahkan
    deleteRental, // <-- Fungsi delete permanen juga ditambahkan
  };
}

```

## File: `hooks\useRentForm.js`

```
import { useState } from 'react';

export const useRentForm = () => {
  const [bikeType, setBikeType] = useState('');
  const [date, setDate] = useState('');
  const [duration, setDuration] = useState('');

  return {
    bikeType,
    setBikeType,
    date,
    setDate,
    duration,
    setDuration,
  };
};

```

## File: `hooks\useSpaceData.js`

```
import { useState, useEffect } from 'react';

const useSepedaData = (url) => {
  const [data, setData] = useState([]);      // Menyimpan data sepeda
  const [loading, setLoading] = useState(true); // Status loading
  const [error, setError] = useState(null);     // Untuk menyimpan error

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(url); // Ambil data dari API
        if (!res.ok) throw new Error('Gagal mengambil data');
        const json = await res.json(); // Ubah ke format JSON
        setData(json);                 // Simpan datanya
      } catch (err) {
        setError(err.message);        // Simpan error jika ada
      } finally {
        setLoading(false);            // Hentikan loading
      }
    };

    fetchData();
  }, [url]); // Hook akan jalan ulang jika url berubah

  return { data, loading, error }; // Kembalikan hasilnya
};

export default useSepedaData;

```

## File: `pages\AdminDashboard.jsx`

```
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useBikes } from "../hooks/useBikes";
import { useRentals } from "../hooks/useRentals"; // Pastikan deleteRental di-destructure di sini
import "../styles/global.css";

const AdminDashboard = () => {
  const { isAuthenticated, isAdmin, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const {
    bikes,
    loading: bikesLoading,
    error: bikesError,
    createBike,
    updateBike,
    deleteBike,
  } = useBikes();

  const {
    rentals,
    loading: rentalsLoading,
    error: rentalsError,
    cancelRental,
    updateRental,
    // Pastikan deleteRental di-destructure di sini!
    deleteRental, // <-- Tambahkan ini
  } = useRentals();

  const [showBikeForm, setShowBikeForm] = useState(false);
  const [currentBike, setCurrentBike] = useState(null);
  const [bikeTitle, setBikeTitle] = useState("");
  const [bikeDescription, setBikeDescription] = useState("");
  const [bikePrice, setBikePrice] = useState("");
  const [bikeThumbnail, setBikeThumbnail] = useState("");
  const [bikeFormError, setBikeFormError] = useState(null);
  const [bikeFormSuccess, setBikeFormSuccess] = useState(null);

  useEffect(() => {
    if (!authLoading && (!isAuthenticated || !isAdmin())) {
      navigate("/");
    }
  }, [isAuthenticated, isAdmin, authLoading, navigate]);

  if (authLoading || bikesLoading || rentalsLoading) {
    return <p>Memuat data admin...</p>;
  }

  if (bikesError || rentalsError) {
    return (
      <p>Error memuat data: {bikesError?.message || rentalsError?.message}</p>
    );
  }

  // --- Fungsi untuk Sepeda ---
  const handleCreateOrUpdateBike = async (e) => {
    e.preventDefault();
    setBikeFormError(null);
    setBikeFormSuccess(null);

    if (!bikeTitle || !bikeDescription || !bikePrice || !bikeThumbnail) {
      setBikeFormError("Semua field harus diisi.");
      return;
    }

    const bikeData = {
      title: bikeTitle,
      description: bikeDescription,
      price: parseFloat(bikePrice),
      thumbnail: bikeThumbnail,
    };

    let result;
    if (currentBike) {
      result = await updateBike(currentBike.id, bikeData);
    } else {
      result = await createBike(bikeData);
    }

    if (result.success) {
      setBikeFormSuccess(
        currentBike
          ? "Sepeda berhasil diperbarui!"
          : "Sepeda berhasil ditambahkan!"
      );
      resetBikeForm();
    } else {
      setBikeFormError(result.error);
    }
  };

  const handleEditBike = (bike) => {
    setCurrentBike(bike);
    setBikeTitle(bike.title);
    setBikeDescription(bike.description);
    setBikePrice(bike.price.toString());
    setBikeThumbnail(bike.thumbnail);
    setShowBikeForm(true);
    setBikeFormError(null);
    setBikeFormSuccess(null);
  };

  const handleDeleteBike = async (bikeId, bikeTitle) => {
    if (
      window.confirm(`Apakah Anda yakin ingin menghapus sepeda: ${bikeTitle}?`)
    ) {
      const result = await deleteBike(bikeId);
      if (result.success) {
        alert(result.message);
      } else {
        alert(`Gagal menghapus sepeda: ${result.error}`);
      }
    }
  };

  const resetBikeForm = () => {
    setCurrentBike(null);
    setBikeTitle("");
    setBikeDescription("");
    setBikePrice("");
    setBikeThumbnail("");
    setShowBikeForm(false);
  };

  // --- Fungsi untuk Rental ---
  const handleCancelRental = async (rentalId, ticketId) => {
    if (
      window.confirm(
        `Apakah Anda yakin ingin membatalkan rental dengan ID Tiket: ${ticketId}?`
      )
    ) {
      const result = await cancelRental(rentalId);
      if (result.success) {
        alert(result.message);
      } else {
        alert(`Gagal membatalkan rental: ${result.error}`);
      }
    }
  };

  const handleChangeRentalStatus = async (
    rentalId,
    currentStatus,
    newStatus
  ) => {
    if (currentStatus === newStatus) {
      alert("Status sudah sama dengan yang dipilih.");
      return;
    }
    if (
      window.confirm(
        `Ubah status rental ini dari '${currentStatus}' menjadi '${newStatus}'?`
      )
    ) {
      const result = await updateRental(rentalId, { status: newStatus });
      if (result.success) {
        alert(
          `Status rental ${result.rental.ticket_id} berhasil diubah menjadi ${result.rental.status}.`
        );
      } else {
        alert(`Gagal mengubah status rental: ${result.error}`);
      }
    }
  };

  // Fungsi BARU untuk menghapus rental secara permanen oleh Admin
  const handleDeleteRental = async (rentalId, ticketId) => {
    if (
      window.confirm(
        `PERINGATAN: Anda akan menghapus rental dengan ID Tiket: ${ticketId} secara permanen. Tindakan ini tidak dapat dibatalkan. Lanjutkan?`
      )
    ) {
      const result = await deleteRental(rentalId);
      if (result.success) {
        alert(result.message);
      } else {
        alert(`Gagal menghapus rental: ${result.error}`);
      }
    }
  };

  return (
    <div className="container admin-dashboard-container">
      <h1>Dashboard Admin</h1>
      {/* Bagian Manajemen Sepeda */}
      <div className="admin-section">
        <h2>Manajemen Sepeda</h2>
        <button onClick={() => setShowBikeForm(!showBikeForm)}>
          {showBikeForm ? "Tutup Form" : "Tambah Sepeda Baru"}
        </button>

        {showBikeForm && (
          <form onSubmit={handleCreateOrUpdateBike} className="admin-form">
            <h3>{currentBike ? "Edit Sepeda" : "Tambah Sepeda"}</h3>
            {bikeFormError && <p style={{ color: "red" }}>{bikeFormError}</p>}
            {bikeFormSuccess && (
              <p style={{ color: "green" }}>{bikeFormSuccess}</p>
            )}

            <label>Judul Sepeda:</label>
            <input
              type="text"
              value={bikeTitle}
              onChange={(e) => setBikeTitle(e.target.value)}
              placeholder="Judul Sepeda"
              required
            />

            <label>Deskripsi:</label>
            <textarea
              value={bikeDescription}
              onChange={(e) => setBikeDescription(e.target.value)}
              placeholder="Deskripsi Sepeda"
              required
            />

            <label>Harga (per hari):</label>
            <input
              type="number"
              value={bikePrice}
              onChange={(e) => setBikePrice(e.target.value)}
              placeholder="Harga Sepeda"
              min="0"
              step="any"
              required
            />

            <label>URL Thumbnail:</label>
            <input
              type="text"
              value={bikeThumbnail}
              onChange={(e) => setBikeThumbnail(e.target.value)}
              placeholder="URL Gambar Thumbnail"
              required
            />
            <button type="submit">
              {currentBike ? "Update Sepeda" : "Tambahkan Sepeda"}
            </button>
            {currentBike && (
              <button type="button" onClick={resetBikeForm}>
                Batal Edit
              </button>
            )}
          </form>
        )}

        <div className="bike-list-admin">
          {bikes.length === 0 ? (
            <p>Tidak ada sepeda tersedia.</p>
          ) : (
            bikes.map((bike) => (
              <div key={bike.id} className="bike-item-admin">
                <img src={bike.thumbnail} alt={bike.title} />
                <div className="bike-info-admin">
                  <h3>{bike.title}</h3>
                  <p>{bike.description}</p>
                  <p>
                    Harga: Rp {parseFloat(bike.price).toLocaleString("id-ID")}
                  </p>
                </div>
                <div className="bike-actions-admin">
                  <button onClick={() => handleEditBike(bike)}>Edit</button>
                  <button onClick={() => handleDeleteBike(bike.id, bike.title)}>
                    Hapus
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
      {/* Bagian Riwayat Rental */}
      <div className="admin-section">
        <h2>Riwayat Rental Pengguna</h2>
        {rentals.length === 0 ? (
          <p>Belum ada riwayat penyewaan sepeda.</p>
        ) : (
          <div className="rental-list-admin">
            {rentals.map((rental) => (
              <div key={rental.id} className="rental-item-admin">
                <div className="rental-header-admin">
                  <h3>Tiket: {rental.ticket_id}</h3>
                  <p className={`rental-status-admin status-${rental.status}`}>
                    Status: <strong>{rental.status}</strong>
                  </p>
                </div>
                <div className="rental-details-admin">
                  <p>User ID: {rental.user_id}</p>
                  <p>Sepeda ID: {rental.bike_id}</p>
                  <p>Tanggal Sewa: {rental.rental_date}</p>
                  <p>Durasi: {rental.duration_days} hari</p>
                  <p>
                    Total: Rp{" "}
                    {parseFloat(rental.total_amount).toLocaleString("id-ID")}
                  </p>
                  <p>Metode Pembayaran: {rental.payment_method}</p>
                </div>
                <div className="rental-actions-admin">
                  {/* Dropdown untuk mengubah status */}
                  <select
                    value={rental.status}
                    onChange={(e) =>
                      handleChangeRentalStatus(
                        rental.id,
                        rental.status,
                        e.target.value
                      )
                    }
                    style={{
                      marginRight: "10px",
                      padding: "8px",
                      borderRadius: "6px",
                      border: "1px solid #ccc",
                    }}
                  >
                    <option value="pending">Pending</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                  {/* Tombol Batalkan Rental (jika status bukan 'cancelled') */}
                  {rental.status !== "cancelled" && (
                    <button
                      onClick={() =>
                        handleCancelRental(rental.id, rental.ticket_id)
                      }
                      style={{ backgroundColor: "#dc3545" }}
                    >
                      Batalkan
                    </button>
                  )}
                  {/* Tombol Hapus Rental (untuk admin) */}
                  <button
                    onClick={() =>
                      handleDeleteRental(rental.id, rental.ticket_id)
                    }
                    style={{ backgroundColor: "#6c757d", marginLeft: "10px" }} // Warna abu-abu untuk Hapus
                  >
                    Hapus Permanen
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;

```

## File: `pages\Confirmation.jsx`

```
import { useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";
// Pastikan path ini sesuai dengan struktur proyek Anda
import "../styles/global.css";

function Confirmation() {
  const location = useLocation();
  const navigate = useNavigate();
  const {
    bike,
    tanggal = "",
    durasi = 0,
    total = 0,
    metode = "",
    ticket_id = "",
  } = location.state || {};

  useEffect(() => {
    if (
      !bike ||
      !tanggal ||
      durasi <= 0 ||
      total <= 0 ||
      !metode ||
      !ticket_id
    ) {
      navigate("/");
    }
  }, [bike, tanggal, durasi, total, metode, ticket_id, navigate]);

  return (
    <div className="container confirmation-container">
      <h2>Konfirmasi Pembayaran</h2>
      <p>
        Terima kasih telah menyewa sepeda bersama <strong>Seku</strong>!
      </p>

      {/* Menggunakan kelas 'rental-item' agar stylingnya sama dengan dashboard */}
      <div className="rental-item">
        <div className="rental-header">
          <h3>🎟️ Tiket Sewa Sepeda</h3>
          {/* Status tidak ada di konfirmasi, jadi kita bisa hilangkan atau tambahkan placeholder jika diperlukan */}
        </div>
        <div className="rental-details">
          <p>
            <strong>Sepeda:</strong> {bike?.title}
          </p>
          <p>
            <strong>Tanggal Sewa:</strong> {tanggal}
          </p>
          <p>
            <strong>Durasi:</strong> {durasi} hari
          </p>
          <p>
            <strong>Total Bayar:</strong> Rp {total.toLocaleString("id-ID")}
          </p>
          <p>
            <strong>Metode Pembayaran:</strong>{" "}
            {metode === "tunai" ? "Tunai" : "QRIS"}
          </p>
          <p>
            <strong>ID Tiket:</strong> #{ticket_id}
          </p>
        </div>
        <div className="rental-actions">
          <p style={{ fontSize: "0.9rem", margin: "0", color: "#6a4966" }}>
            Tunjukkan tiket ini saat pengambilan sepeda.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Confirmation;

```

## File: `pages\Home.jsx`

```
import React from "react";
import { useNavigate } from "react-router-dom";
import { useBikes } from "../hooks/useBikes";

const Home = () => {
  const { bikes, loading, error } = useBikes();
  const navigate = useNavigate();

  if (loading) {
    return <p>Memuat daftar sepeda...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  const handleRent = (bike) => {
    navigate("/rent", {
      state: { bike },
    });
  };

  return (
    <div className="container home-container">
      <h1>Data Sepeda</h1>
      {bikes.length === 0 ? (
        <p>Tidak ada sepeda tersedia saat ini.</p>
      ) : (
        <ul className="bike-list">
          {" "}
          {/* Gunakan kelas bike-list dari global.css */}
          {bikes.map((bike) => (
            <li key={bike.id} className="bike-item">
              {" "}
              {/* Gunakan kelas bike-item */}
              <img src={bike.thumbnail} alt={bike.title} />
              <h3>{bike.title}</h3>
              <p>{bike.description}</p>
              <p>
                Harga: Rp{" "}
                {bike.price
                  ? parseFloat(bike.price).toLocaleString("id-ID")
                  : "Harga tidak tersedia"}
              </p>
              <button onClick={() => handleRent(bike)}>Pesan Sepeda</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Home;

```

## File: `pages\Login.jsx`

```
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth"; // Sesuaikan path jika berbeda

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const { login, loading, error, isAdmin } = useAuth(); // Tambahkan isAdmin dari useAuth
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage("");

    if (!email || !password) {
      setMessage("Email dan password harus diisi!");
      return;
    }

    const result = await login(email, password);

    if (result.success) {
      // Setelah login sukses, cek apakah user adalah admin
      if (isAdmin()) {
        navigate("/admin-dashboard"); // Redirect ke halaman dashboard admin
      } else {
        navigate("/"); // Redirect ke halaman utama untuk user biasa
      }
    } else {
      setMessage(result.error);
    }
  };

  return (
    <div className="container login-container">
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        {message && (
          <p style={{ color: message.includes("sukses") ? "green" : "red" }}>
            {message}
          </p>
        )}
        {error && <p style={{ color: "red" }}>{error}</p>}
        <div>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            required
          />
        </div>
        <div>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
};

export default Login;

```

## File: `pages\Payment.jsx`

```
import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useRentals } from "../hooks/useRentals";
import { useAuth } from "../hooks/useAuth";
import "../styles/global.css";

const Payment = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { bike, tanggal, durasi } = location.state || {};
  const [paymentMethod, setPaymentMethod] = useState("tunai");
  const [paymentError, setPaymentError] = useState(null);
  const {
    createRental,
    loading: rentalLoading,
    error: rentalHookError,
  } = useRentals();
  const { isAuthenticated } = useAuth();

  if (!bike || !tanggal || !durasi) {
    return (
      <p>Data sewa tidak lengkap. Silakan kembali ke halaman sebelumnya.</p>
    );
  }

  if (!isAuthenticated) {
    return <p>Anda harus login untuk melanjutkan pembayaran.</p>;
  }

  const total = bike.price * durasi;

  const handleBayar = async () => {
    setPaymentError(null);

    const rentalData = {
      bike_id: bike.id,
      rental_date: tanggal,
      duration_days: parseInt(durasi, 10),
      payment_method: paymentMethod,
    };

    const result = await createRental(rentalData);

    if (result.success) {
      navigate("/confirmation", {
        state: {
          bike,
          tanggal,
          durasi,
          total: parseFloat(result.rental.total_amount),
          metode: result.rental.payment_method,
          ticket_id: result.rental.ticket_id,
        },
      });
    } else {
      setPaymentError(result.error || rentalHookError);
    }
  };

  return (
    <div className="container payment-container">
      <h1>Pembayaran</h1>
      <h3>{bike.title}</h3>
      <p>Tanggal sewa: {tanggal}</p>
      <p>Durasi: {durasi} hari</p>
      <p>Total bayar: Rp {total.toLocaleString("id-ID")}</p>

      <div>
        <div>
          <h4>Pilih Metode Pembayaran</h4>
          <div className="payment-method-options">
            <label className="payment-option-label">
              <input
                type="radio"
                value="tunai"
                checked={paymentMethod === "tunai"}
                onChange={(e) => setPaymentMethod(e.target.value)}
              />
              Tunai
            </label>

            <label className="payment-option-label">
              <input
                type="radio"
                value="non-tunai"
                checked={paymentMethod === "non-tunai"}
                onChange={(e) => setPaymentMethod(e.target.value)}
              />
              Non-Tunai (QRIS)
            </label>
          </div>
        </div>

        {paymentMethod === "non-tunai" && (
          <div style={{ textAlign: "center", marginTop: "1rem" }}>
            <img
              src={"https://qris.id/api-doc/assets/img/MPM_QRIS_Dasar.jpg"}
              alt="QRIS Barcode"
              className="qris-image"
              style={{
                width: 300,
                height: 700,
                borderRadius: 16,
                boxShadow: "0 4px 10px rgba(219, 90, 138, 0.3)",
                cursor: "pointer",
                transition: "transform 0.3s ease",
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.transform = "scale(1.05)")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.transform = "scale(1)")
              }
            />
            <p>Silakan scan QR di atas menggunakan aplikasi e-wallet Anda.</p>
          </div>
        )}
      </div>

      {paymentError && (
        <p style={{ color: "red", marginTop: "1rem" }}>Error: {paymentError}</p>
      )}

      <button
        onClick={handleBayar}
        disabled={rentalLoading}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          backgroundColor: "#d46b8b",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        {rentalLoading ? "Memproses Pembayaran..." : "Bayar Sekarang"}
      </button>
    </div>
  );
};

export default Payment;

```

## File: `pages\Register.jsx`

```
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth"; // Sesuaikan path jika berbeda

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const { register, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");

    if (!username || !email || !password) {
      setMessage("Semua kolom harus diisi!");
      return;
    }

    const result = await register(username, email, password);

    if (result.success) {
      setMessage("Registrasi sukses! Silakan login.");
      setUsername("");
      setEmail("");
      setPassword("");
      // Opsional: Redirect ke halaman login setelah registrasi sukses
      // navigate('/login');
    } else {
      setMessage(result.error);
    }
  };

  return (
    <div className="container register-container">
      <h1>Daftar Akun Baru</h1>
      <form onSubmit={handleRegister}>
        {message && (
          <p style={{ color: message.includes("sukses") ? "green" : "red" }}>
            {message}
          </p>
        )}
        {error && <p style={{ color: "red" }}>{error}</p>}
        <div>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            required
          />
        </div>
        <div>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            required
          />
        </div>
        <div>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Mendaftar..." : "Daftar"}
        </button>
      </form>
    </div>
  );
};

export default Register;

```

## File: `pages\Rent.jsx`

```
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Rent = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { bike } = location.state || {};

  const [tanggal, setTanggal] = useState('');
  const [durasi, setDurasi] = useState(1);

  if (!bike) {
    return <p>No bike data available</p>;
  }

  const handleLanjut = () => {
    if (!tanggal) {
      alert("Silakan pilih tanggal sewa");
      return;
    }
    navigate('/payment', {
      state: { bike, tanggal, durasi },
    });
  };

  return (
    <div className="container rent-container">
      {/* konten Rent */}
      <h1>Pesan Sepeda</h1>
      <h3>{bike.title}</h3>
      <img src={bike.thumbnail} alt={bike.title} width="200" />
      <p>Harga: Rp {bike.price.toLocaleString()}</p>

      <div>
        <label>
          Tanggal Sewa:
          <input
            type="date"
            value={tanggal}
            onChange={(e) => setTanggal(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Durasi (hari):
          <input
            type="number"
            min="1"
            value={durasi}
            onChange={(e) => setDurasi(parseInt(e.target.value))}
          />
        </label>
      </div>

      <button onClick={handleLanjut}>Lanjutkan ke Pembayaran</button>
    </div>
  );
};

export default Rent;

```

## File: `pages\UserDashboard.jsx`

```
import React, { useEffect } from "react";
import { useAuth } from "../hooks/useAuth";
import { useRentals } from "../hooks/useRentals";
import { useNavigate } from "react-router-dom";
import "../styles/global.css"; // Pastikan path ini sesuai dengan struktur proyek Anda

const UserDashboard = () => {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const {
    rentals,
    loading: rentalsLoading,
    error: rentalsError,
    cancelRental,
  } = useRentals();
  const navigate = useNavigate();

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate("/login");
    }
  }, [isAuthenticated, authLoading, navigate]);

  if (authLoading || rentalsLoading) {
    return <p>Memuat data...</p>;
  }

  if (rentalsError) {
    return <p>Error memuat riwayat rental: {rentalsError}</p>;
  }

  const handleCancelRental = async (rentalId, ticketId) => {
    if (
      window.confirm(
        `Apakah Anda yakin ingin membatalkan rental dengan ID Tiket: ${ticketId}?`
      )
    ) {
      const result = await cancelRental(rentalId);
      if (result.success) {
        alert(result.message);
      } else {
        alert(`Gagal membatalkan rental: ${result.error}`);
      }
    }
  };

  return (
    <div className="container user-dashboard-container">
      <h1>Dashboard Pengguna</h1>
      <h2>Riwayat Penyewaan Anda</h2>
      {rentals.length === 0 ? (
        <p>Anda belum memiliki riwayat penyewaan sepeda.</p>
      ) : (
        <div className="rental-list">
          {rentals.map((rental) => (
            <div key={rental.id} className="rental-item">
              <div className="rental-header">
                <h3>Tiket: {rental.ticket_id}</h3>
                <p className="rental-status">
                  Status: <strong>{rental.status}</strong>
                </p>
              </div>
              <div className="rental-details">
                <p>Sepeda ID: {rental.bike_id}</p>
                <p>Tanggal Sewa: {rental.rental_date}</p>
                <p>Durasi: {rental.duration_days} hari</p>
                <p>
                  Total Bayar: Rp{" "}
                  {parseFloat(rental.total_amount).toLocaleString("id-ID")}
                </p>
                <p>Metode Pembayaran: {rental.payment_method}</p>
              </div>
              {rental.status === "pending" && (
                <div className="rental-actions">
                  <button
                    onClick={() =>
                      handleCancelRental(rental.id, rental.ticket_id)
                    }
                  >
                    Batalkan Rental
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UserDashboard;

```

## File: `redux\authSlice.js`

```
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  user: null,
  token: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;

```

## File: `redux\store.js`

```
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
  },
});

export default store;

```

## File: `styles\global.css`

```
/* reset & dasar */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Poppins", sans-serif;
  background-color: #fff0f6; /* very soft pink */
  color: #4a3c53; /* dark plum */
  line-height: 1.6;
  padding: 20px;
  min-height: 100vh;
}
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(230, 150, 170, 0.3);
}
h1,
h2,
h3,
h4 {
  font-weight: 700;
  margin-bottom: 15px;
  color: #b83280; /* strong pink */
}
p {
  margin-bottom: 15px;
  font-size: 1.1rem;
  color: #6a4966; /* medium plum */
}
button {
  background-color: #db5a8a; /* pink rose */
  border: none;
  color: white;
  padding: 12px 25px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background-color 0.3s ease;
}
button:hover {
  background-color: #a73662; /* darker pink */
}
input,
select {
  padding: 10px;
  font-size: 1rem;
  border-radius: 6px;
  border: 1.5px solid #ebb7d3;
  margin-bottom: 15px;
  width: 100%;
}
input:focus,
select:focus {
  outline: none;
  border-color: #b83280;
}

/* Home page */
.home-container {
  background-color: #fff0f6;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(219, 90, 138, 0.3);
}

.bike-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.bike-item {
  background: #fce8f3;
  border-radius: 15px;
  padding: 15px;
  box-shadow: 0 4px 12px rgba(219, 90, 138, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: transform 0.3s ease;
}
.bike-item:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 25px rgba(219, 90, 138, 0.4);
}
.bike-item img {
  width: 100%;
  height: 180px;
  border-radius: 12px;
  object-fit: cover;
  margin-bottom: 15px;
}
.bike-item h3 {
  color: #b83280;
}
.bike-item p {
  color: #7e4961;
  margin-bottom: 15px;
}
.bike-item button {
  align-self: stretch;
}

/* Rent page */
.rent-container {
  max-width: 450px;
  margin: 40px auto;
  background-color: #fce8f3;
  padding: 30px 25px;
  border-radius: 12px;
  box-shadow: 0 8px 18px rgba(219, 90, 138, 0.25);
}

.rent-container h1 {
  text-align: center;
  margin-bottom: 25px;
  color: #a9346f;
}

.rent-container img {
  width: 100%;
  border-radius: 12px;
  margin-bottom: 20px;
}

.rent-container label {
  font-weight: 600;
  color: #7e4961;
}

.rent-container input[type="date"],
.rent-container input[type="number"] {
  font-size: 1rem;
}

/* Payment page */
.payment-container {
  max-width: 400px;
  margin: 40px auto;
  background-color: #fff0f6;
  padding: 25px 20px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(219, 90, 138, 0.25);
}

.payment-container h1 {
  text-align: center;
  margin-bottom: 25px;
  color: #b83280;
}

.payment-container label {
  display: inline-flex;
  align-items: center;
  margin-right: 25px;
  font-weight: 600;
  color: #7e4961;
  cursor: pointer;
}

.payment-container input[type="radio"] {
  margin-right: 8px;
  cursor: pointer;
}

.payment-container button {
  width: 100%;
  margin-top: 20px;
}

/* Confirmation page */
.confirmation-container {
  max-width: 460px;
  margin: 40px auto;
  padding: 25px 30px;
  border-radius: 15px;
  background: linear-gradient(135deg, #fce8f3 0%, #d970ad 100%);
  color: #fff;
  box-shadow: 0 10px 25px rgba(219, 90, 138, 0.5);
  font-family: "Courier New", Courier, monospace;
}

.confirmation-container h2 {
  text-align: center;
  margin-bottom: 20px;
}

.ticket {
  background: rgba(255 255 255 / 0.3);
  padding: 20px;
  border-radius: 12px;
  box-shadow: inset 0 0 12px rgba(255 255 255 / 0.5);
}

.ticket p {
  font-weight: 600;
  font-size: 1.15rem;
  margin: 12px 0;
  color: #44062e;
}

.qris-image {
  display: block;
  margin: 20px auto; /* Tengah horizontal dengan jarak atas bawah */
  width: 220px; /* Lebar tetap agar QR cukup besar */
  height: 220px; /* Tinggi sama dengan lebar supaya kotak */
  border-radius: 16px; /* Sudut membulat */
  box-shadow: 0 4px 10px rgba(219, 90, 138, 0.3); /* Bayangan pink lembut */
  transition: transform 0.3s ease;
  cursor: pointer;
}

.qris-image:hover {
  transform: scale(1.05); /* Efek zoom saat hover */
  box-shadow: 0 8px 20px rgba(219, 90, 138, 0.5);
}

/* Styling untuk grup radio button */
.payment-method-options {
  display: flex;
  flex-direction: column;
  gap: 10px; /* Jarak antar opsi */
  margin-top: 15px; /* Sesuaikan jarak atas grup jika perlu */
}

/* Styling untuk setiap label opsi radio */
.payment-option-label {
  display: flex;
  align-items: center; /* Pusatkan secara vertikal */
  cursor: pointer;
  font-weight: 600;
  color: #7e4961; /* Sesuaikan warna teks */
}

/* Penyesuaian input radio agar tidak terlalu besar */
.payment-option-label input[type="radio"] {
  margin-right: 8px;
  cursor: pointer;
  width: auto; /* Pastikan ukuran radio button tidak mengambil lebar penuh */
  margin-bottom: 0; /* Hapus margin bawah default jika ada */
}

/* Styling untuk User Dashboard Container */
.user-dashboard-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Styling untuk daftar rental */
.rental-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

/* Styling untuk setiap item rental (seperti tiket) */
.rental-item {
  background-color: #fffafc; /* Warna latar belakang lebih lembut */
  border: 2px dashed #ffb6c1; /* Garis putus-putus */
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform 0.2s ease;
}

.rental-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(255, 105, 180, 0.25);
}

.rental-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ffe4e6;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.rental-header h3 {
  margin: 0;
  color: #a9346f;
  font-size: 1.25rem;
}

.rental-status {
  margin: 0;
  font-weight: bold;
  color: #db5a8a;
  font-size: 1rem;
}

.rental-status strong {
  color: #e75480; /* Warna lebih kuat untuk status */
}

.rental-details p {
  margin-bottom: 5px;
  font-size: 0.95rem;
  color: #6a4966;
}

.rental-details p:last-child {
  margin-bottom: 0;
}

.rental-actions {
  margin-top: 15px;
  text-align: center;
}

.rental-actions button {
  background-color: #ff69b4;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

.rental-actions button:hover {
  background-color: #e75480;
}

/* Styling for Admin Dashboard */
.admin-dashboard-container {
  padding: 30px;
  background-color: #fcf6f9; /* Lightest pink background */
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(219, 90, 138, 0.2);
}

.admin-dashboard-container h1 {
  text-align: center;
  color: #880e4f; /* Darker pink for main titles */
  margin-bottom: 30px;
}

.admin-section {
  background-color: #fff;
  padding: 25px;
  border-radius: 14px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  margin-bottom: 30px;
}

.admin-section h2 {
  color: #b83280;
  margin-bottom: 20px;
  border-bottom: 2px solid #ffebee;
  padding-bottom: 10px;
}

.admin-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
  padding: 20px;
  background-color: #fef1f6;
  border-radius: 10px;
  border: 1px dashed #ffd8e6;
}

.admin-form label {
  font-weight: 600;
  color: #7e4961;
  margin-bottom: -10px; /* Adjust spacing */
}

.admin-form input[type="text"],
.admin-form input[type="number"],
.admin-form textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ffc1d1;
  border-radius: 8px;
  font-size: 1rem;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.admin-form textarea {
  min-height: 80px;
  resize: vertical;
}

.admin-form button {
  width: auto;
  align-self: flex-start; /* Align button to start */
  margin-right: 10px; /* Space between buttons */
}

.bike-list-admin,
.rental-list-admin {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 25px;
}

.bike-item-admin,
.rental-item-admin {
  background: #fff8fc; /* Lighter background for items */
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(255, 105, 180, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.bike-item-admin:hover,
.rental-item-admin:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 18px rgba(255, 105, 180, 0.25);
}

.bike-item-admin img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
}

.bike-info-admin h3,
.rental-header-admin h3 {
  color: #a9346f;
  margin-bottom: 5px;
  font-size: 1.15rem;
}

.bike-info-admin p,
.rental-details-admin p {
  font-size: 0.95rem;
  color: #6a4966;
  margin-bottom: 5px;
}

.bike-actions-admin,
.rental-actions-admin {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.bike-actions-admin button,
.rental-actions-admin button {
  flex: 1;
  padding: 8px 12px;
  font-size: 0.9rem;
  border-radius: 6px;
}

.bike-actions-admin button:nth-child(1) {
  /* Edit */
  background-color: #28a745; /* Green for edit */
}
.bike-actions-admin button:nth-child(1):hover {
  background-color: #218838;
}

.bike-actions-admin button:nth-child(2) {
  /* Delete */
  background-color: #dc3545; /* Red for delete */
}
.bike-actions-admin button:nth-child(2):hover {
  background-color: #c82333;
}

.rental-header-admin {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ffe4e6;
  padding-bottom: 8px;
  margin-bottom: 8px;
}

.rental-status-admin {
  font-weight: bold;
  font-size: 0.9rem;
  padding: 4px 8px;
  border-radius: 5px;
}

.status-pending {
  background-color: #ffc107; /* Yellow */
  color: #6c4f00;
}
.status-completed {
  background-color: #28a745; /* Green */
  color: white;
}
.status-cancelled {
  background-color: #dc3545; /* Red */
  color: white;
}
/* Tambahkan status lain jika ada */

```

## File: `styles\navbar.css`

```
/* Navbar Styles */
.navbar {
  background-color: #f7d1d9; /* Pink Nude */
  padding: 1rem 2rem;
  box-shadow: 0 2px 5px rgba(212, 107, 139, 0.3);
  display: flex;
  justify-content: center;
  gap: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  font-weight: 600;
  font-family: Arial, sans-serif;
}

.navbar a {
  color: #d46b8b; /* Soft Pink */
  text-decoration: none;
  font-size: 1.1rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.navbar a:hover,
.navbar a.active {
  background-color: #d46b8b; /* Pink */
  color: white;
  box-shadow: 0 4px 8px rgba(212, 107, 139, 0.5);
  cursor: pointer;
}

/* Responsive Navbar */
@media (max-width: 480px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .navbar a {
    font-size: 1.2rem;
    padding: 0.7rem 1.5rem;
  }
}

```
