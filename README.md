# SekuApp - Aplikasi Penyewaan Sepeda

## Overview

SekuApp adalah aplikasi penyewaan sepeda yang dirancang untuk memudahkan pengguna dalam menyewa sepeda secara online. Aplikasi ini menyediakan fitur-fitur dasar seperti melihat daftar sepeda yang tersedia, melakukan penyewaan, melacak riwayat penyewaan, serta fungsionalitas admin untuk mengelola sepeda dan rental.

Aplikasi ini dibagi menjadi dua bagian utama:
* **Backend**: Dibangun menggunakan framework Pyramid dengan Python dan SQLAlchemy sebagai ORM, serta PostgreSQL sebagai database. Backend ini menyediakan API RESTful untuk seluruh fungsionalitas aplikasi.
* **Frontend**: Dibangun menggunakan React.js dan Vite, menyediakan antarmuka pengguna yang interaktif dan responsif.

## Fitur

### Fitur Pengguna
* Melihat daftar sepeda yang tersedia.
* Memesan sepeda (memilih tanggal dan durasi sewa).
* Melakukan pembayaran (tunai atau non-tunai/QRIS).
* Melihat konfirmasi penyewaan dengan detail tiket.
* Mengakses *dashboard* pengguna untuk melihat riwayat penyewaan.
* Membatalkan penyewaan yang masih berstatus 'pending'.
* Registrasi akun baru.
* Login dan Logout akun.

### Fitur Admin
* Mengelola daftar sepeda (menambah, mengubah, menghapus).
* Melihat seluruh riwayat penyewaan pengguna.
* Mengubah status penyewaan (misal: dari 'pending' ke 'completed').
* Menghapus data penyewaan secara permanen (hanya untuk admin).

## Struktur Folder

### Backend
```
SekuApp_122140102_RA/Back-end/
├── alembic/
│   ├── versions/
│   │   ├── 20250528_1a41e7bb9051.py
│   │   └── 20250528_4f6d5a0493b1.py
│   └── env.py
├── seku_backend/
│   ├── models/
│   │   ├── init.py
│   │   ├── bike.py
│   │   ├── meta.py
│   │   ├── rental.py
│   │   └── user.py
│   ├── scripts/
│   │   ├── init.py
│   │   └── initialize_db.py
│   ├── views/
│   │   ├── init.py
│   │   ├── auth.py
│   │   ├── bike.py
│   │   ├── default.py
│   │   ├── notfound.py
│   │   └── rental.py
│   ├── init.py
│   ├── cors.py
│   ├── pshell.py
│   ├── routes.py
│   ├── static/
│   │   └── theme.css
│   └── tests.py
├── development.ini
├── production.ini
├── pytest.ini
├── setup.py
├── CHANGES.txt
└── README.txt
```

### Frontend
```
SekuApp_122140102_RA/Front-end/
├── public/
│   ├── db.json
│   └── sepeda.json
├── src/
│   ├── components/
│   │   ├── ConfirmDialog.jsx
│   │   ├── ErrorBoundary.jsx
│   │   ├── Listsepeda.jsx
│   │   ├── ProtectedRoute.jsx
│   │   ├── Toast.jsx
│   │   └── navbar.jsx
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   ├── Bikecontext.jsx
│   │   └── SepedaContext.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useBikes.js
│   │   ├── useFetchBikes.js
│   │   ├── useRentForm.js
│   │   ├── useRentals.js
│   │   └── useSpaceData.js
│   ├── pages/
│   │   ├── AdminDashboard.jsx
│   │   ├── Confirmation.jsx
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Payment.jsx
│   │   ├── Register.jsx
│   │   ├── Rent.jsx
│   │   └── UserDashboard.jsx
│   ├── redux/
│   │   ├── authSlice.js
│   │   └── store.js
│   ├── styles/
│   │   ├── global.css
│   │   └── navbar.css
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── index.html
├── package.json
├── package-lock.json
├── eslint.config.js
└── vite.config.js
```

## Database Tables (Backend)

Berikut adalah skema tabel yang digunakan di *backend*:

### `users` table
* `id` (BigInteger, Primary Key, Auto-increment): ID unik pengguna.
* `username` (String(255), Not Null): Nama pengguna.
* `email` (String(255), Not Null, Unique): Alamat email pengguna, harus unik.
* `password_hash` (String(255), Not Null): Hash kata sandi pengguna untuk keamanan.
* `created_at` (DateTime): Waktu pembuatan record.
* `updated_at` (DateTime): Waktu terakhir record diperbarui.

### `bikes` table
* `id` (BigInteger, Primary Key, Auto-increment): ID unik sepeda.
* `title` (String(255), Not Null): Judul atau nama sepeda.
* `description` (Text, Nullable): Deskripsi detail sepeda.
* `price` (DECIMAL(10, 2), Not Null): Harga sewa sepeda per hari.
* `thumbnail` (String(255), Nullable): URL gambar thumbnail sepeda.
* `created_at` (DateTime): Waktu pembuatan record.
* `updated_at` (DateTime): Waktu terakhir record diperbarui.

### `rentals` table
* `id` (BigInteger, Primary Key, Auto-increment): ID unik penyewaan.
* `user_id` (BigInteger, Foreign Key ke `users.id`, Not Null): ID pengguna yang menyewa.
* `bike_id` (BigInteger, Foreign Key ke `bikes.id`, Not Null): ID sepeda yang disewa.
* `rental_date` (Date, Not Null): Tanggal mulai penyewaan.
* `duration_days` (Integer, Not Null, Default 1): Durasi penyewaan dalam hari.
* `total_amount` (DECIMAL(10, 2), Not Null): Total biaya penyewaan.
* `payment_method` (String(50), Not Null): Metode pembayaran (misal: 'tunai', 'non-tunai').
* `ticket_id` (String(255), Unique): ID tiket unik untuk setiap penyewaan.
* `status` (String(50), Not Null, Default 'pending'): Status penyewaan (misal: 'pending', 'completed', 'cancelled').
* `created_at` (DateTime): Waktu pembuatan record.
* `updated_at` (DateTime): Waktu terakhir record diperbarui.

## API Endpoints (Backend)

Base URL: `http://localhost:6543`

### Authentication
* **POST `/register`**
    * Deskripsi: Mendaftarkan pengguna baru.
    * Request Body (JSON):
        ```json
        {
            "username": "string",
            "email": "string (unique)",
            "password": "string"
        }
        ```
    * Response (JSON): `{ "message": "Registration successful", "user": { ...user_data... } }` atau `{"error": "..."}` jika gagal.
* **POST `/login`**
    * Deskripsi: Melakukan login pengguna.
    * Request Body (JSON):
        ```json
        {
            "email": "string",
            "password": "string"
        }
        ```
    * Response (JSON): `{ "message": "Login successful", "user": { ...user_data... } }` dengan `Set-Cookie` header untuk sesi.
* **POST `/logout`**
    * Deskripsi: Melakukan logout pengguna.
    * Request Body: None
    * Response (JSON): `{ "message": "Logout successful" }` dengan `Set-Cookie` header untuk menghapus sesi.

### Bike Management
* **GET `/bikes`**
    * Deskripsi: Mengambil daftar semua sepeda.
    * Request Body: None
    * Response (JSON): `[ { ...bike_data... }, ... ]`
* **GET `/bikes/{id}`**
    * Deskripsi: Mengambil detail sepeda berdasarkan ID.
    * URL Params: `id` (integer)
    * Response (JSON): `{ ...bike_data... }` atau `{"error": "Bike not found"}`
* **POST `/bikes`**
    * Deskripsi: Menambah sepeda baru (membutuhkan autentikasi admin).
    * Request Body (JSON):
        ```json
        {
            "title": "string",
            "description": "string (optional)",
            "price": "number",
            "thumbnail": "string (optional)"
        }
        ```
    * Response (JSON): `{ ...new_bike_data... }`
* **PUT `/bikes/{id}`**
    * Deskripsi: Memperbarui detail sepeda berdasarkan ID (membutuhkan autentikasi admin).
    * URL Params: `id` (integer)
    * Request Body (JSON): (field yang ingin diupdate)
        ```json
        {
            "title": "string (optional)",
            "description": "string (optional)",
            "price": "number (optional)",
            "thumbnail": "string (optional)"
        }
        ```
    * Response (JSON): `{ ...updated_bike_data... }`
* **DELETE `/bikes/{id}`**
    * Deskripsi: Menghapus sepeda berdasarkan ID (membutuhkan autentikasi admin).
    * URL Params: `id` (integer)
    * Response (JSON): `{ "message": "Bike deleted successfully" }`

### Rental Management (User)
* **GET `/rentals`**
    * Deskripsi: Mengambil riwayat penyewaan untuk pengguna yang sedang login.
    * Request Body: None
    * Response (JSON): `[ { ...rental_data... }, ... ]`
* **GET `/rentals/{id}`**
    * Deskripsi: Mengambil detail penyewaan berdasarkan ID untuk pengguna yang sedang login.
    * URL Params: `id` (integer)
    * Response (JSON): `{ ...rental_data... }` atau `{"error": "Rental not found or forbidden"}`
* **POST `/rentals`**
    * Deskripsi: Membuat penyewaan baru.
    * Request Body (JSON):
        ```json
        {
            "bike_id": "integer",
            "rental_date": "string (YYYY-MM-DD)",
            "duration_days": "integer",
            "payment_method": "string (e.g., 'tunai', 'non-tunai')"
        }
        ```
    * Response (JSON): `{ ...new_rental_data... }`
* **PUT `/rentals/{id}`**
    * Deskripsi: Memperbarui detail penyewaan (oleh pengguna yang bersangkutan).
    * URL Params: `id` (integer)
    * Request Body (JSON): (field yang ingin diupdate)
        ```json
        {
            "rental_date": "string (YYYY-MM-DD, optional)",
            "duration_days": "integer (optional)",
            "payment_method": "string (optional)",
            "status": "string (optional, e.g., 'completed')"
        }
        ```
    * Response (JSON): `{ ...updated_rental_data... }`
* **DELETE `/rentals/{id}`**
    * Deskripsi: Membatalkan penyewaan (mengubah status menjadi 'cancelled').
    * URL Params: `id` (integer)
    * Response (JSON): `{ "message": "Rental {ticket_id} cancelled successfully" }`

### Rental Management (Admin)
* **GET `/admin/rentals`**
    * Deskripsi: Mengambil daftar semua penyewaan (membutuhkan autentikasi admin).
    * Request Body: None
    * Response (JSON): `[ { ...rental_data... }, ... ]`
* **PUT `/admin/rentals/{id}`**
    * Deskripsi: Memperbarui detail penyewaan apa pun (membutuhkan autentikasi admin).
    * URL Params: `id` (integer)
    * Request Body (JSON): (field yang ingin diupdate)
        ```json
        {
            "rental_date": "string (YYYY-MM-DD, optional)",
            "duration_days": "integer (optional)",
            "total_amount": "number (optional)",
            "payment_method": "string (optional)",
            "ticket_id": "string (optional)",
            "status": "string (optional)"
        }
        ```
    * Response (JSON): `{ ...updated_rental_data... }`
* **DELETE `/admin/rentals/{id}`**
    * Deskripsi: Menghapus data penyewaan secara permanen (membutuhkan autentikasi admin).
    * URL Params: `id` (integer)
    * Response (JSON): `{ "message": "Rental {ticket_id} (ID: {id}) deleted successfully." }`

## Cara Menjalankan Aplikasi

### Persyaratan
* Python 3.x
* Node.js dan npm/yarn
* PostgreSQL (untuk backend)

### Menjalankan Backend

1.  **Navigasi ke direktori `Back-end`**:
    ```bash
    cd SekuyApp_122140102_RA/Back-end
    ```
2.  **Buat Virtual Environment Python**:
    ```bash
    python3 -m venv env
    ```
3.  **Aktifkan Virtual Environment**:
    * Di Windows: `.\env\Scripts\activate`
    * Di macOS/Linux: `source env/bin/activate`
4.  **Upgrade Packaging Tools**:
    ```bash
    env/bin/pip install --upgrade pip setuptools
    ```
5.  **Instal Dependensi Project**:
    ```bash
    env/bin/pip install -e ".[testing]"
    ```
6.  **Konfigurasi Database (PostgreSQL)**:
    Pastikan PostgreSQL server Anda berjalan. Buat database dan user sesuai dengan konfigurasi di `development.ini`. Secara *default*:
    * Database: `sekudb`
    * User: `seku-user`
    * Password: `mypassword`
    ```ini
    # development.ini
    sqlalchemy.url = postgresql://seku-user:mypassword@localhost:5432/sekudb
    ```
7.  **Inisialisasi dan Upgrade Database dengan Alembic**:
    * Generate revisi pertama (jika belum ada):
        ```bash
        env/bin/alembic -c development.ini revision --autogenerate -m "init"
        ```
    * Upgrade database ke revisi terbaru:
        ```bash
        env/bin/alembic -c development.ini upgrade head
        ```
8.  **Muat Data Awal ke Database**:
    ```bash
    env/bin/initialize_seku_backend_db development.ini
    ```
    Script ini akan membuat tabel dan mengisi data contoh (pengguna, sepeda, rental) jika database masih kosong.
9.  **Jalankan Backend**:
    ```bash
    env/bin/pserve development.ini
    ```
    Backend akan berjalan di `http://localhost:6543`.

### Menjalankan Frontend

1.  **Navigasi ke direktori `Front-end`**:
    ```bash
    cd SekuyApp_122140102_RA/Front-end
    ```
2.  **Instal Dependensi Node.js**:
    ```bash
    npm install
    # atau
    yarn install
    ```
3.  **Jalankan Aplikasi Frontend**:
    ```bash
    npm run dev
    # atau
    yarn dev
    ```
    Aplikasi frontend akan berjalan, biasanya di `http://localhost:5173`.

## Copyright

© 2025 Zahwa Azzahra (122140102)
