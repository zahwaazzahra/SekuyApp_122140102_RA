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
    const fetchAllBikes = async () => {
      const result = await fetchData();
      if (result) {
        setBikes(result);
      } else {
        setBikes([]);
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
        setBikes((prevBikes) => [...prevBikes, result]);
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
        );
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
        setBikes((prevBikes) => prevBikes.filter((bike) => bike.id !== id));
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
