import { createContext, useContext, useState } from "react";

const BikeContext = createContext();

export function BikeProvider({ children }) {
  const [selectedBike, setSelectedBike] = useState(null);

  return (
    <BikeContext.Provider value={{ selectedBike, setSelectedBike }}>
      {children}
    </BikeContext.Provider>
  );
}

export function useBike() {
  return useContext(BikeContext);
}
