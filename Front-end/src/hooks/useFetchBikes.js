useEffect(() => {
  fetch("http://localhost:8000/api/bikes")  // Pastikan URL API sesuai dengan backend yang benar
    .then((response) => response.json())
    .then((data) => {
      console.log("Data received:", data);  // Debugging: Cek data yang diterima
      setBikes(data);
      setLoading(false);
    })
    .catch((error) => {
      console.error("Error fetching bikes:", error);  // Debugging: Cek error
      setError(error);
      setLoading(false);
    });
}, []);
