// pages/AdminDashboard.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useBikes } from "../hooks/useBikes";
import { useRentals } from "../hooks/useRentals";
import { useToast } from "../components/Toast";
import { useConfirmDialog } from "../components/ConfirmDialog";
import "../styles/global.css";

const AdminDashboard = () => {
  const { isAuthenticated, isAdmin, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const { confirm } = useConfirmDialog();

  const {
    bikes,
    loading: bikesLoading,
    error: bikesError,
    createBike,
    updateBike,
    deleteBike,
  } = useBikes();

  const {
    rentals,
    loading: rentalsLoading,
    error: rentalsError,
    cancelRental,
    updateRental,
    deleteRental,
  } = useRentals();

  const [showBikeForm, setShowBikeForm] = useState(false);
  const [currentBike, setCurrentBike] = useState(null);
  const [bikeTitle, setBikeTitle] = useState("");
  const [bikeDescription, setBikeDescription] = useState("");
  const [bikePrice, setBikePrice] = useState("");
  const [bikeThumbnail, setBikeThumbnail] = useState("");
  const [bikeFormError, setBikeFormError] = useState(null);
  const [bikeFormSuccess, setBikeFormSuccess] = useState(null);

  useEffect(() => {
    if (!authLoading && (!isAuthenticated || !isAdmin())) {
      navigate("/");
    }
  }, [isAuthenticated, isAdmin, authLoading, navigate]);

  if (authLoading || bikesLoading || rentalsLoading) {
    return <p>Memuat data admin...</p>;
  }

  if (bikesError || rentalsError) {
    return (
      <p>Error memuat data: {bikesError?.message || rentalsError?.message}</p>
    );
  }

  const handleCreateOrUpdateBike = async (e) => {
    e.preventDefault();
    setBikeFormError(null);
    setBikeFormSuccess(null);

    if (!bikeTitle || !bikeDescription || !bikePrice || !bikeThumbnail) {
      setBikeFormError("Semua field harus diisi.");
      return;
    }

    const bikeData = {
      title: bikeTitle,
      description: bikeDescription,
      price: parseFloat(bikePrice),
      thumbnail: bikeThumbnail,
    };

    let result;
    if (currentBike) {
      result = await updateBike(currentBike.id, bikeData);
    } else {
      result = await createBike(bikeData);
    }

    if (result.success) {
      showToast(
        currentBike
          ? "Sepeda berhasil diperbarui!"
          : "Sepeda berhasil ditambahkan!",
        "success"
      );
      resetBikeForm();
    } else {
      setBikeFormError(result.error);
      showToast(`Gagal: ${result.error}`, "error");
    }
  };

  const handleEditBike = (bike) => {
    setCurrentBike(bike);
    setBikeTitle(bike.title);
    setBikeDescription(bike.description);
    setBikePrice(bike.price.toString());
    setBikeThumbnail(bike.thumbnail);
    setShowBikeForm(true);
    setBikeFormError(null);
    setBikeFormSuccess(null);
  };

  const handleDeleteBike = async (bikeId, bikeTitle) => {
    const confirmed = await confirm(
      `Apakah Anda yakin ingin menghapus sepeda: ${bikeTitle}?`
    );
    if (confirmed) {
      const result = await deleteBike(bikeId);
      if (result.success) {
        showToast(result.message, "success");
      } else {
        showToast(`Gagal menghapus sepeda: ${result.error}`, "error");
      }
    }
  };

  const resetBikeForm = () => {
    setCurrentBike(null);
    setBikeTitle("");
    setBikeDescription("");
    setBikePrice("");
    setBikeThumbnail("");
    setShowBikeForm(false);
  };

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

  const handleChangeRentalStatus = async (
    rentalId,
    currentStatus,
    newStatus
  ) => {
    if (currentStatus === newStatus) {
      showToast("Status sudah sama dengan yang dipilih.", "info");
      return;
    }
    const confirmed = await confirm(
      `Ubah status rental ini dari '${currentStatus}' menjadi '${newStatus}'?`
    );
    if (confirmed) {
      const result = await updateRental(rentalId, { status: newStatus });
      if (result.success) {
        showToast(
          `Status rental ${result.rental.ticket_id} berhasil diubah menjadi ${result.rental.status}.`,
          "success"
        );
      } else {
        showToast(`Gagal mengubah status rental: ${result.error}`, "error");
      }
    }
  };

  const handleDeleteRental = async (rentalId, ticketId) => {
    const confirmed = await confirm(
      `PERINGATAN: Anda akan menghapus rental dengan ID Tiket: ${ticketId} secara permanen. Tindakan ini tidak dapat dibatalkan. Lanjutkan?`
    );
    if (confirmed) {
      const result = await deleteRental(rentalId);
      if (result.success) {
        showToast(result.message, "success");
      } else {
        showToast(`Gagal menghapus rental: ${result.error}`, "error");
      }
    }
  };

  return (
    <div className="container admin-dashboard-container">
      <h1>Dashboard Admin</h1>
      <div className="admin-section">
        <h2>Manajemen Sepeda</h2>
        <button onClick={() => setShowBikeForm(!showBikeForm)}>
          {showBikeForm ? "Tutup Form" : "Tambah Sepeda Baru"}
        </button>

        {showBikeForm && (
          <form onSubmit={handleCreateOrUpdateBike} className="admin-form">
            <h3>{currentBike ? "Edit Sepeda" : "Tambah Sepeda"}</h3>
            {bikeFormError && <p style={{ color: "red" }}>{bikeFormError}</p>}
            {bikeFormSuccess && (
              <p style={{ color: "green" }}>{bikeFormSuccess}</p>
            )}

            <label>Judul Sepeda:</label>
            <input
              type="text"
              value={bikeTitle}
              onChange={(e) => setBikeTitle(e.target.value)}
              placeholder="Judul Sepeda"
              required
            />

            <label>Deskripsi:</label>
            <textarea
              value={bikeDescription}
              onChange={(e) => setBikeDescription(e.target.value)}
              placeholder="Deskripsi Sepeda"
              required
            />

            <label>Harga (per hari):</label>
            <input
              type="number"
              value={bikePrice}
              onChange={(e) => setBikePrice(e.target.value)}
              placeholder="Harga Sepeda"
              min="0"
              step="any"
              required
            />

            <label>URL Thumbnail:</label>
            <input
              type="text"
              value={bikeThumbnail}
              onChange={(e) => setBikeThumbnail(e.target.value)}
              placeholder="URL Gambar Thumbnail"
              required
            />
            <button type="submit">
              {currentBike ? "Update Sepeda" : "Tambahkan Sepeda"}
            </button>
            {currentBike && (
              <button type="button" onClick={resetBikeForm}>
                Batal Edit
              </button>
            )}
          </form>
        )}

        <div className="bike-list-admin">
          {bikes.length === 0 ? (
            <p>Tidak ada sepeda tersedia.</p>
          ) : (
            bikes.map((bike) => (
              <div key={bike.id} className="bike-item-admin">
                <img src={bike.thumbnail} alt={bike.title} />
                <div className="bike-info-admin">
                  <h3>{bike.title}</h3>
                  <p>{bike.description}</p>
                  <p>
                    Harga: Rp {parseFloat(bike.price).toLocaleString("id-ID")}
                  </p>
                </div>
                <div className="bike-actions-admin">
                  <button onClick={() => handleEditBike(bike)}>Edit</button>
                  <button onClick={() => handleDeleteBike(bike.id, bike.title)}>
                    Hapus
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
      <div className="admin-section">
        <h2>Riwayat Rental Pengguna</h2>
        {rentals.length === 0 ? (
          <p>Belum ada riwayat penyewaan sepeda.</p>
        ) : (
          <div className="rental-list-admin">
            {rentals.map((rental) => (
              <div key={rental.id} className="rental-item-admin">
                <div className="rental-header-admin">
                  <h3>Tiket: {rental.ticket_id}</h3>
                  <p className={`rental-status-admin status-${rental.status}`}>
                    Status: <strong>{rental.status}</strong>
                  </p>
                </div>
                <div className="rental-details-admin">
                  <p>User ID: {rental.user_id}</p>
                  <p>Sepeda ID: {rental.bike_id}</p>
                  <p>Tanggal Sewa: {rental.rental_date}</p>
                  <p>Durasi: {rental.duration_days} hari</p>
                  <p>
                    Total: Rp{" "}
                    {parseFloat(rental.total_amount).toLocaleString("id-ID")}
                  </p>
                  <p>Metode Pembayaran: {rental.payment_method}</p>
                </div>
                <div className="rental-actions-admin">
                  <select
                    value={rental.status}
                    onChange={(e) =>
                      handleChangeRentalStatus(
                        rental.id,
                        rental.status,
                        e.target.value
                      )
                    }
                    style={{
                      marginRight: "10px",
                      padding: "8px",
                      borderRadius: "6px",
                      border: "1px solid #ccc",
                    }}
                  >
                    <option value="pending">Pending</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                  {rental.status !== "cancelled" && (
                    <button
                      onClick={() =>
                        handleCancelRental(rental.id, rental.ticket_id)
                      }
                      style={{ backgroundColor: "#dc3545" }}
                    >
                      Batalkan
                    </button>
                  )}
                  <button
                    onClick={() =>
                      handleDeleteRental(rental.id, rental.ticket_id)
                    }
                    style={{ backgroundColor: "#6c757d", marginLeft: "10px" }}
                  >
                    Hapus Permanen
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
