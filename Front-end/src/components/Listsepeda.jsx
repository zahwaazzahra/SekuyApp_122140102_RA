import React from "react";
import { useFetchBikes } from "../hooks/useFetchBikes";

const ListSepeda = () => {
  const { bikes, loading, error } = useFetchBikes();

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h2>Daftar Sepeda:</h2>
      <ul>
        {bikes.map((bike) => (
          <li key={bike.id}>
            {bike.name} - Rp{bike.price}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ListSepeda;
