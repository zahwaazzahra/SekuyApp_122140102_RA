import React, { createContext, useContext, useState } from 'react';

const SepedaContext = createContext();

export const useSepeda = () => {
  return useContext(SepedaContext);
};

export const SepedaProvider = ({ children }) => {
  const [selectedBike, setSelectedBike] = useState(null);

  const selectBike = (bike) => {
    setSelectedBike(bike);
  };

  return (
    <SepedaContext.Provider value={{ selectedBike, selectBike }}>
      {children}
    </SepedaContext.Provider>
  );
};
