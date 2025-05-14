import { useState } from 'react';

export const useRentForm = () => {
  const [bikeType, setBikeType] = useState('');
  const [date, setDate] = useState('');
  const [duration, setDuration] = useState('');

  return {
    bikeType,
    setBikeType,
    date,
    setDate,
    duration,
    setDuration,
  };
};
