import { useState, useEffect, useCallback } from "react";
import { useAuth } from "./useAuth";

const API_URL = "http://localhost:6543";

export function useRentals() {
  const [rentals, setRentals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user, isAuthenticated, isAdmin } = useAuth();

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

  useEffect(() => {
    const fetchRelevantRentals = async () => {
      if (isAuthenticated) {
        let result;
        if (isAdmin()) {
          result = await fetchData(`/admin/rentals`);
        } else if (user && user.id) {
          result = await fetchData(`/rentals`);
        } else {
          setRentals([]);
          return;
        }

        if (result) {
          setRentals(result);
        } else {
          setRentals([]);
        }
      } else {
        setRentals([]);
      }
    };
    fetchRelevantRentals();
  }, [fetchData, isAuthenticated, user, isAdmin]);

  const getRental = useCallback(
    async (id) => {
      if (!isAuthenticated) {
        setError("Anda harus login untuk melihat detail rental.");
        return null;
      }
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
        user_id: user.id,
      };

      const result = await fetchData("/rentals", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (result) {
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
      const endpoint = isAdmin() ? `/admin/rentals/${id}` : `/rentals/${id}`;
      const result = await fetchData(endpoint, {
        method: "PUT",
        body: JSON.stringify(rentalData),
      });
      if (result) {
        setRentals((prevRentals) =>
          prevRentals.map((rental) => (rental.id === id ? result : rental))
        );
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
      const endpoint = isAdmin() ? `/admin/rentals/${id}` : `/rentals/${id}`;
      const result = await fetchData(endpoint, {
        method: "DELETE",
      });
      if (result && result.message) {
        setRentals((prevRentals) =>
          prevRentals.map((rental) =>
            rental.id === id ? { ...rental, status: "cancelled" } : rental
          )
        );
        return { success: true, message: result.message };
      }
      return { success: false, error: error };
    },
    [fetchData, isAuthenticated, error, isAdmin]
  );

  const updateRentalStatus = useCallback(
    async (id, newStatus) => {
      if (!isAuthenticated) {
        setError("Anda harus login untuk mengubah status rental.");
        return { success: false, error: "Unauthorized" };
      }
      const endpoint = isAdmin() ? `/admin/rentals/${id}` : `/rentals/${id}`;
      const result = await fetchData(endpoint, {
        method: "PUT",
        body: JSON.stringify({ status: newStatus }),
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

  const deleteRental = useCallback(
    async (id) => {
      if (!isAuthenticated) {
        setError("Anda harus login untuk menghapus rental.");
        return { success: false, error: "Unauthorized" };
      }
      if (!isAdmin()) {
        setError("Anda tidak memiliki izin untuk menghapus rental.");
        return { success: false, error: "Forbidden" };
      }
      const endpoint = `/admin/rentals/${id}`;
      const result = await fetchData(endpoint, {
        method: "DELETE",
      });
      if (result && result.message) {
        setRentals((prevRentals) =>
          prevRentals.filter((rental) => rental.id !== id)
        );
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
    updateRentalStatus,
    deleteRental,
  };
}
