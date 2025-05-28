// pages/UserDashboard.jsx
import React, { useEffect } from "react";
import { useAuth } from "../hooks/useAuth";
import { useRentals } from "../hooks/useRentals";
import { useNavigate } from "react-router-dom";
import { useToast } from "../components/Toast";
import { useConfirmDialog } from "../components/ConfirmDialog";
import "../styles/global.css";

const UserDashboard = () => {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { showToast } = useToast();
  const { confirm } = useConfirmDialog();
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
    const confirmed = await confirm(
      `Apakah Anda yakin ingin membatalkan rental dengan ID Tiket: ${ticketId}?`
    );
    if (confirmed) {
      const result = await cancelRental(rentalId);
      if (result.success) {
        showToast(result.message, "success");
      } else {
        showToast(`Gagal membatalkan rental: ${result.error}`, "error");
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
