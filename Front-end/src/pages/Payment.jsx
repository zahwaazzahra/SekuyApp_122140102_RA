import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useRentals } from "../hooks/useRentals";
import { useAuth } from "../hooks/useAuth";
import { useToast } from "../components/Toast";
import "../styles/global.css";

const Payment = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { bike, tanggal, durasi } = location.state || {};
  const [paymentMethod, setPaymentMethod] = useState("tunai");
  const [paymentError, setPaymentError] = useState(null);
  const { showToast } = useToast();
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
      showToast("Pembayaran berhasil dikonfirmasi!", "success");
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
      showToast(
        `Gagal memproses pembayaran: ${result.error || rentalHookError}`,
        "error"
      );
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
