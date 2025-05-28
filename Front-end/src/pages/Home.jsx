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
          {bikes.map((bike) => (
            <li key={bike.id} className="bike-item">
              {" "}
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
