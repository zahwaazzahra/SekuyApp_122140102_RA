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
