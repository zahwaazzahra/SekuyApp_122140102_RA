import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';  // Mengimpor hook untuk navigasi
import Navbar from "../components/navbar";


const Home = () => {
  const [bikes, setBikes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const navigate = useNavigate();  // Hook untuk mengarahkan pengguna ke halaman Rent

  useEffect(() => {
    // Mengambil data sepeda dari db.json yang ada di folder public
    fetch('/db.json')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        setBikes(data.bikes);  // Menyimpan data sepeda dari db.json
        setLoading(false);
      })
      .catch((error) => {
        setError(error);
        setLoading(false);
      });
  }, []);

  // Jika data sedang dimuat
  if (loading) {
    return <p>Loading...</p>;
  }

  // Jika terjadi error
  if (error) {
    return <p>Error: {error.message}</p>;
  }

  // Fungsi untuk menavigasi ke halaman Rent
  const handleRent = (bike) => {
    navigate('/rent', {
      state: { bike }  // Mengirimkan data sepeda yang dipilih ke halaman Rent
    });
  };

  return (
    
    <div className="container home-container">
      {/* konten Home */}
     

      <h1>Data Sepeda</h1>
      {bikes.length === 0 ? (
        <p>No bikes available</p>
      ) : (
        <ul>
          {bikes.map((bike) => (
            <li key={bike.id} style={{ marginBottom: '20px', border: '1px solid #ddd', padding: '10px', borderRadius: '8px' }}>
              {/* Menampilkan gambar thumbnail sepeda */}
              <img 
                src={bike.thumbnail} 
                alt={bike.title} 
                style={{ width: '200px', height: 'auto', borderRadius: '8px' }} 
              />
              
              <h3>{bike.title}</h3>
              <p>{bike.description}</p>
              <p>Harga: Rp {bike.price ? bike.price.toLocaleString() : 'Harga tidak tersedia'}</p>
              
              {/* Button Pesan Sepeda */}
              <button 
                onClick={() => handleRent(bike)} 
                style={{
                  padding: '10px 15px',
                  backgroundColor: '#007bff',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Pesan Sepeda
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Home;
