import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar';
import Home from './pages/Home';
import Rent from './pages/Rent';
import Payment from './pages/Payment';
import Confirmation from './pages/Confirmation';  // Import komponen Confirmation

const App = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/rent" element={<Rent />} />
        <Route path="/payment" element={<Payment />} />
        <Route path="/confirmation" element={<Confirmation />} /> 
      </Routes>
    </>
  );
};

export default App;
