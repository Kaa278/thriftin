# PRODUCT REQUIREMENTS DOCUMENT (PRD)
**Nama Produk:** ThriftIn (Modern Preloved & Thrift Marketplace)
**Platform:** Mobile Application (Android & iOS)
**Tech Stack:** Flutter (Frontend), Supabase (Backend/BaaS), PostgreSQL (Database), Firebase Cloud Messaging (Notifikasi)

## 1. Ringkasan Eksekutif
**ThriftIn** adalah aplikasi mobile marketplace modern yang dirancang khusus untuk mewadahi ekosistem transaksi jual beli barang *thrift* (bekas layak pakai) dan *preloved*. Aplikasi ini menawarkan solusi *all-in-one* yang memungkinkan pengguna berperan ganda sebagai Pembeli sekaligus Penjual dalam satu akun terpusat. Dilengkapi dengan fitur unggulan seperti *Live Bidding* (lelang), *Real-time Chat*, dan integrasi pembayaran, ThriftIn bertujuan untuk memberikan pengalaman berbelanja barang bekas yang aman, terstruktur, dan modern.

## 2. Latar Belakang & Masalah
Saat ini, tren thrifting dan preloved semakin meningkat karena harganya yang terjangkau dan dorongan *sustainable fashion*. Namun, sebagian besar transaksi masih dilakukan melalui platform media sosial atau grup obrolan yang tidak terstruktur. Hal ini menimbulkan beberapa masalah:
1. **Pencarian Kurang Efisien:** Pembeli kesulitan mencari barang spesifik yang tersebar di berbagai postingan.
2. **Keamanan Transaksi:** Rentan terhadap penipuan karena tidak ada sistem terpusat.
3. **Proses Lelang Manual:** Lelang (*bidding*) di media sosial sangat manual dan rawan manipulasi.
4. **Komunikasi Berantakan:** Chat antara pembeli dan penjual sering kali tercampur dengan pesan pribadi.

## 3. Tujuan dan Sasaran Produk
1. **Memusatkan Ekosistem Thrifting:** Memberikan platform terpadu untuk discovery produk, negosiasi, hingga checkout.
2. **Sistem Peran Ganda (Dual-Role):** Memudahkan pengguna tanpa perlu membuat akun terpisah untuk berjualan.
3. **Mendigitalisasi Proses Lelang:** Menyediakan fitur *Live Bidding* yang transparan dan *real-time*.
4. **Meningkatkan Kepercayaan:** Menyediakan sistem rating & review yang transparan pasca-transaksi.

## 4. Target Pengguna (User Persona)
*   **Pembeli (Thrifter):** Pengguna (umumnya Gen Z & Milenial) yang mencari pakaian, sepatu, atau barang koleksi bekas dengan kualitas baik dan harga murah.
*   **Penjual (Thrift Store Owner / Individu):** Pemilik toko thrift atau individu yang ingin melakukan *decluttering* lemari pakaian mereka dan mendapatkan uang tambahan.

---

## 5. Kebutuhan Fungsional (Functional Requirements) - Detail Fitur

### 5.1. Manajemen Akun & Autentikasi (Authentication)
*   **Registrasi & Login:** Pengguna dapat mendaftar dan masuk menggunakan Email dan Password.
*   **Reset Password dengan OTP:** Jika lupa password, pengguna dapat meminta kode OTP yang dikirim ke email (terintegrasi dengan *Resend API* via *Supabase Edge Functions*).
*   **Profil Pengguna:** 
    *   Sistem menyimpan data detail: Nama, Email, Nomor Telepon, Alamat Lengkap, Bio, Foto Profil, Jenis Kelamin, dan Tanggal Lahir.
    *   Indikator status *Online* dan *Last Seen*.

### 5.2. Etalase & Pencarian Produk (Discovery)
*   **Katalog Beranda:** Menampilkan produk terbaru, produk *trending*, dan produk berdasarkan kategori (Pakaian, Aksesoris, dll).
*   **Smart Search:** Pencarian produk berbasis teks yang dioptimalkan dengan *Trigram Index* di PostgreSQL untuk pencarian nama produk yang cepat dan toleran terhadap *typo*.
*   **Filter & Sortir:** Menyaring produk berdasarkan kategori, kondisi barang (Baru / Pernah Dipakai), lokasi, dan tipe penjualan (Lelang / Beli Langsung).
*   **Wishlist (Favorit):** Pengguna dapat menekan tombol "Hati" untuk menyimpan produk ke daftar favorit.

### 5.3. Detail Produk (Product Page)
*   **Galeri Multi-Foto:** Mendukung tampilan lebih dari satu foto per produk (disimpan di Supabase Storage).
*   **Informasi Komprehensif:** Menampilkan harga, nama toko (*store name*), rating toko, kondisi barang, lokasi, badge (contoh: "Langka", "Sangat Bagus"), dan deskripsi detail.
*   **Review Produk:** Menampilkan ulasan dan rating (1-5 bintang) dari pembeli sebelumnya.

### 5.4. Mode Penjualan: Live Bidding (Lelang)
*   **Timer Lelang:** Produk tipe *Bidding* menampilkan hitung mundur (countdown) sisa waktu lelang.
*   **Sistem Penawaran (Bid):** Pembeli dapat memasukkan nominal bid. Sistem akan memvalidasi bahwa bid baru harus lebih tinggi dari bid tertinggi saat ini.
*   **Daftar Penawar (Bid History):** Menampilkan riwayat tawaran tertinggi secara transparan.

### 5.5. Real-time Chat (Komunikasi)
*   **Chat Berbasis Produk:** Ruang obrolan (Chat Room) dibuat spesifik antara Pembeli, Penjual, dan tertaut langsung dengan Produk yang sedang didiskusikan.
*   **Fitur Pesan:** Mendukung pengiriman teks, tawaran harga (Offer Amount), dan indikator pesan belum terbaca (*Unread Count*).
*   **Real-time Sync:** Pesan terkirim dan diterima secara instan memanfaatkan fitur *Supabase Realtime*.

### 5.6. Manajemen Transaksi (Checkout & Order)
*   **Keranjang Belanja (Cart):** Pengguna dapat menyimpan produk reguler ke keranjang sebelum *checkout*.
*   **Checkout Flow:**
    *   Pemilihan Alamat Pengiriman.
    *   Pemilihan Metode Pengiriman (contoh: EcoExpress) beserta simulasi biaya ongkir.
    *   Kalkulasi Total: Harga barang + Ongkir + Biaya Layanan - Diskon.
*   **Integrasi Pembayaran:** Mendukung berbagai metode pembayaran via **Duitku Payment Gateway (Sandbox)** yang dikelola oleh *Supabase Edge Functions*.
*   **Order Tracking:** Status pesanan (Menunggu, Diproses, Dikirim, Selesai).

### 5.7. Seller Center (Manajemen Toko)
*   **Tambah Produk Baru:** Penjual dapat mengunggah foto, mengatur nama, harga, deskripsi, lokasi, dan memilih opsi penjualan (Jual Langsung / Lelang).
*   **Manajemen Pesanan:** Penjual dapat melihat pesanan masuk dan mengubah status pengiriman.
*   **Reputasi Toko:** Akumulasi rating dari barang-barang yang telah berhasil terjual.

### 5.8. Sistem Notifikasi (Push Notifications)
*   **Firebase Cloud Messaging (FCM):** Aplikasi mengirimkan *push notification* ke perangkat pengguna (Android/iOS) menggunakan token FCM yang tersimpan di database.
*   **Pemicu Notifikasi:** Pesan chat baru, tawaran (bid) baru yang lebih tinggi, pesanan masuk, dan update status pesanan.

---

## 6. Kebutuhan Non-Fungsional (Non-Functional Requirements)

1.  **Keamanan (Security):**
    *   Basis data dilindungi menggunakan **Row Level Security (RLS)** pada PostgreSQL Supabase (memastikan user hanya bisa menghapus/mengubah data miliknya sendiri).
    *   Otentikasi aman menggunakan enkripsi Supabase Auth.
2.  **Skalabilitas & Performa:**
    *   Pemuatan daftar produk menggunakan teknik *Pagination*.
    *   Penggunaan Index pada database (seperti `idx_products_id_desc`, `idx_chat_messages_unread`) untuk mempercepat query saat data membesar.
3.  **Ketersediaan Aset (Storage):**
    *   Semua foto profil dan foto produk disimpan di *Supabase Storage Buckets* publik untuk akses *read* yang cepat.
4.  **UX / UI (Pengalaman Pengguna):**
    *   Menggunakan navigasi *Bottom Tab Bar* yang responsif.
    *   Menampilkan UI *Skeleton Loading* (via package `skeletonizer`) saat data sedang dimuat dari server agar aplikasi terasa lebih cepat.
5.  **In-App Updates:** Mendukung pembaruan aplikasi langsung dari dalam aplikasi (menggunakan package `in_app_update`).

---

## 7. Arsitektur Sistem & Tech Stack

| Komponen | Teknologi yang Digunakan | Fungsi |
| :--- | :--- | :--- |
| **Frontend / Mobile App** | Flutter & Dart | Membangun UI/UX aplikasi untuk Android dan iOS dari satu *codebase*. |
| **Backend / Database** | Supabase (PostgreSQL) | Menyimpan seluruh entitas relasional (User, Product, Order, Chat). |
| **Storage** | Supabase Storage | Mengelola penyimpanan file media (Gambar Produk, Avatar). |
| **Serverless Functions**| Supabase Edge Functions | Menjalankan logika *backend* terisolasi (Contoh: Hit API Duitku & Resend OTP). |
| **Push Notifications** | Firebase (FCM) | Mengelola pengiriman notifikasi ke perangkat pengguna secara *real-time*. |
| **Payment Gateway** | Duitku (Sandbox) | Simulasi pembuatan kode bayar dan virtual account. |
| **Email Service** | Resend | Mengirimkan kode OTP ke email pengguna. |

---

## 8. Struktur Database Utama (Core Entities)
*(Referensi berdasarkan `supabase_schema.sql`)*

1.  `users`: Tabel profil pengguna ganda (Pembeli & Penjual).
2.  `products` & `product_images`: Detail barang thrift dan galeri fotonya.
3.  `bids`: Mencatat riwayat penawaran pada barang lelang.
4.  `orders`: Mencatat transaksi jual beli yang terjadi.
5.  `chat_rooms` & `chat_messages`: Mencatat relasi komunikasi antar pengguna.
6.  `reviews`: Mencatat ulasan pasca-pembelian.
7.  `password_reset_otps`: Mencatat siklus hidup OTP untuk pemulihan akun.
8.  `user_fcm_tokens`: Menyimpan token perangkat untuk keperluan Notifikasi Push.

---

## 9. Pembagian Tugas Tim (Jobdesk)
Proyek ini dikembangkan oleh 3 orang anggota dengan pembagian tugas sebagai berikut:

**1. Erdhika (Backend, Cloud, & UI/UX Design)**
*   **UI/UX Design:** Membuat *wireframe* dan desain antarmuka aplikasi menggunakan Figma.
*   **Database & Cloud:** Merancang dan mengelola *schema* database PostgreSQL di Supabase.
*   **Serverless & Auth:** Menangani logika *backend* dengan Edge Functions (contoh: integrasi Resend OTP, endpoint Duitku Sandbox).
*   **Notifikasi:** Mengatur integrasi Firebase Cloud Messaging (FCM) dan koneksinya ke database.

**2. Anggota 2 (Frontend App - Core & Buyer Features)**
*   **Autentikasi & Profil:** Membangun UI dan integrasi logika Login, Register, Lupa Password, serta halaman Profil.
*   **Discovery Produk:** Membangun UI/UX Beranda (Home), sistem pencarian cerdas (*Smart Search*), *filtering*, dan detail halaman produk.
*   **Interaksi Pembeli:** Membangun fitur *Wishlist/Favorite* dan *Real-time Chat* (berbasis ruang obrolan produk).

**3. Anggota 3 (Frontend App - Seller Center & Transaksi)**
*   **Seller Center:** Membangun seluruh antarmuka khusus Penjual, termasuk formulir "Tambah Produk Baru" (unggahan gambar multi-foto, *picker* kondisi, harga), dan manajemen status pesanan.
*   **Fitur Lelang:** Membangun integrasi *Live Bidding* secara *real-time* termasuk UI *countdown timer* dan input penawaran.
*   **Checkout & Pembayaran:** Menangani *flow* keranjang, halaman pembayaran akhir, simulasi kalkulasi ongkir, dan UI ulasan (*review*).
