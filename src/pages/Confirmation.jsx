import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useMemo } from "react";

function Confirmation() {
  const location = useLocation();
  const navigate = useNavigate();
  const { bike, tanggal = "", durasi = 0, total = 0, metode = "" } = location.state || {};

  const ticketId = useMemo(() => Math.floor(Math.random() * 1000000), []);

  useEffect(() => {
    if (!bike || !tanggal || durasi <= 0 || total <= 0 || !metode) {
      navigate("/");
    }
  }, [bike, tanggal, durasi, total, metode, navigate]);

  return (
    <div className="container confirmation-container">
      {/* konten Confirmation */}
      <h2>Konfirmasi Pembayaran</h2>
      <p>Terima kasih telah menyewa sepeda bersama <strong>Seku</strong>!</p>
      
      <div className="ticket">
        <h3>🎟️ Tiket Sewa Sepeda</h3>
        <p><strong>Sepeda:</strong> {bike?.title}</p>
        <p><strong>Tanggal Sewa:</strong> {tanggal}</p>
        <p><strong>Durasi:</strong> {durasi} hari</p>
        <p><strong>Total Bayar:</strong> Rp {total.toLocaleString()}</p>
        <p><strong>Metode Pembayaran:</strong> {metode === "tunai" ? "Tunai" : "QRIS"}</p>
        <p><strong>ID Tiket:</strong> #{ticketId}</p>
        <p style={{ fontSize: "0.9rem", marginTop: "1rem", color: "#999" }}>
          Tunjukkan tiket ini saat pengambilan sepeda
        </p>
      </div>
    </div>
  );
}

export default Confirmation;
