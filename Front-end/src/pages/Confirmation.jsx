import { useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";
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

      <div className="rental-item">
        <div className="rental-header">
          <h3>🎟️ Tiket Sewa Sepeda</h3>
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
