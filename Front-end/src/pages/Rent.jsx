// pages/Rent.jsx
import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useToast } from "../components/Toast"; // Import useToast

const Rent = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { showToast } = useToast(); // Initialize useToast
  const { bike } = location.state || {};

  const [tanggal, setTanggal] = useState("");
  const [durasi, setDurasi] = useState(1);

  if (!bike) {
    return <p>No bike data available</p>;
  }

  const handleLanjut = () => {
    if (!tanggal) {
      showToast("Silakan pilih tanggal sewa", "info"); // Use showToast
      return;
    }
    navigate("/payment", {
      state: { bike, tanggal, durasi },
    });
  };

  return (
    <div className="container rent-container">
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
