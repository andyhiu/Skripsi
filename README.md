# Sistem Material PT Sampurna Abadi Makmur

Sistem ini merupakan aplikasi berbasis web yang digunakan untuk monitoring dan pengelolaan material antara admin pusat dan cabang (Tuban dan Mahendradatta). Sistem ini dibangun untuk membantu perusahaan dalam mengelola stok material, proses pengiriman, transaksi penjualan, serta pembuatan laporan secara terintegrasi dan lebih efisien.

## Deskripsi Sistem

Sistem ini dirancang untuk mempermudah pengelolaan operasional material mulai dari pusat hingga cabang. Admin pusat memiliki kendali penuh terhadap data material, pengiriman stok, serta monitoring seluruh aktivitas cabang. Sementara itu, user cabang bertugas untuk mengelola transaksi harian, pengeluaran operasional, serta konfirmasi stok yang diterima dari pusat.

## Teknologi yang Digunakan

* Python (Flask)
* MySQL (XAMPP / phpMyAdmin)
* HTML dan CSS
* JavaScript

## Role Pengguna

### 1. Admin Pusat

* Mengelola user
* Mengelola data material dan harga
* Mengirim stok ke cabang
* Monitoring stok seluruh cabang
* Melihat laporan keseluruhan

### 2. User Cabang

* Konfirmasi stok dari pusat
* Input transaksi penjualan
* Input pengeluaran operasional
* Membuat laporan harian
* Melihat stok cabang

## Fitur Utama

* Login multi user (Admin dan Cabang)
* Manajemen user
* Manajemen material dan harga
* Pengiriman stok ke cabang
* Konfirmasi stok cabang
* Monitoring stok pusat dan cabang
* Input transaksi penjualan
* Input pengeluaran
* Laporan harian
* Generate laporan PDF
* Generate nota transaksi dan pengiriman

## Cara Menjalankan Sistem

1. Clone repository ini:
   git clone https://github.com/andyhiu/Skripsi.git

2. Masuk ke folder project:
   cd Skripsi

3. Jalankan XAMPP (Apache dan MySQL)

4. Import database ke phpMyAdmin dari file:
   /database/database.sql

5. Install dependency (jika belum ada):
   pip install flask
   pip install mysql-connector-python

6. Jalankan aplikasi:
   python app.py

7. Buka browser:
   http://127.0.0.1:5000

## Akun Login 

Admin:

* Username: admin
* Password: 123

Cabang:

* Username: tuban
* Password: 123

## Struktur Project

Skripsi/
│
├── app.py
├── config.py
├── templates/
├── static/
├── database/
│   └── database.sql
├── .gitignore
└── README.md

## Catatan

Sistem ini dibuat sebagai tugas akhir (skripsi) dan berfokus pada integrasi pengelolaan material antara pusat dan cabang secara terstruktur dan efisien.

## Author

Christopher Randy Hiu
Sistem Informasi
ITB STIKOM Bali
