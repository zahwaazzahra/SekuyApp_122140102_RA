import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import qrisexample from '../assets/qrisexample.jpg';

const Payment = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { bike, tanggal, durasi } = location.state || {};
  const [paymentMethod, setPaymentMethod] = useState('tunai');

  if (!bike || !tanggal || !durasi) {
    return <p>Data sewa tidak lengkap.</p>;
  }

  const total = bike.price * durasi;

  const handleBayar = () => {
    navigate('/confirmation', {
      state: {
        bike,
        tanggal,
        durasi,
        total,
        metode: paymentMethod,
      },
    });
  };

  return (
    <div className="container payment-container">
      <h1>Pembayaran</h1>
      <h3>{bike.title}</h3>
      <p>Tanggal sewa: {tanggal}</p>
      <p>Durasi: {durasi} hari</p>
      <p>Total bayar: Rp {total.toLocaleString()}</p>

      <div>
        <h4>Pilih Metode Pembayaran</h4>
        <label>
          <input
            type="radio"
            value="tunai"
            checked={paymentMethod === 'tunai'}
            onChange={(e) => setPaymentMethod(e.target.value)}
          /> Tunai
        </label>

        <label style={{ display: 'block', marginTop: '10px' }}>
          <input
            type="radio"
            value="non-tunai"
            checked={paymentMethod === 'non-tunai'}
            onChange={(e) => setPaymentMethod(e.target.value)}
          /> Non-Tunai (QRIS)
        </label>

        {paymentMethod === 'non-tunai' && (
          <div style={{ textAlign: 'center', marginTop: '1rem' }}>
            <img
              src={qrisexample}
              alt="QRIS Barcode"
              className="qris-image"
              style={{ width: 220, height: 220, borderRadius: 16, boxShadow: '0 4px 10px rgba(219, 90, 138, 0.3)', cursor: 'pointer', transition: 'transform 0.3s ease' }}
              onMouseEnter={(e) => (e.currentTarget.style.transform = 'scale(1.05)')}
              onMouseLeave={(e) => (e.currentTarget.style.transform = 'scale(1)')}
            />
            <p>Silakan scan QR di atas menggunakan aplikasi e-wallet Anda.</p>
          </div>
        )}
      </div>

      <button onClick={handleBayar} style={{ marginTop: '20px', padding: '10px 20px', backgroundColor: '#d46b8b', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
        Bayar Sekarang
      </button>
    </div>
  );
};

export default Payment;
