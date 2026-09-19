# DOKUMEN SPESIFIKASI FITUR SISTEM & SOP OPERASIONAL
# SISTEM INFORMASI MANAJEMEN RENTAL IPHONE (NORIZ)

**Mata Kuliah:** Manajemen Proyek Teknologi Informasi  
**Proyek:** Rancang Bangun Sistem Informasi Manajemen Rental iPhone (NORIZ)  
**Tujuan Dokumen:** Memisahkan secara tegas antara **Fitur Perangkat Lunak (Website / Sistem)** yang dikembangkan oleh tim developer dengan **Prosedur Manual / Fisik (Aktivitas Offline Gerai)** yang dijalankan oleh staf manusia di dunia nyata.

---

## 1. BATASAN SISTEM (SYSTEM BOUNDARY)

Dalam perancangan sistem informasi, sering terjadi kerancuan antara fungsi software dan pekerjaan manual manusia. Dalam sistem **NORIZ**, batasannya ditetapkan sebagai berikut:

* **Fitur Sistem (Website / Software):** Segala fungsionalitas yang berjalan di dalam kode aplikasi web, database server, antarmuka layar, dan API. Sistem bertugas mengolah data, menghitung kalkulasi, menyimpan foto/dokumen, mencatat audit trail, serta mengubah status transaksi.
* **Prosedur Offline / Fisik (SOP Gerai):** Tindakan fisik nyata yang dilakukan oleh manusia (petugas kasir, teknisi, penyewa) menggunakan panca indera, tangan, dan perangkat keras pembantu di meja konter gerai fisik. Sistem informasi **tidak melakukan tindakan fisik ini**, melainkan **menerima hasil input/verifikasi** dari staf manusia.

---

## 2. KOMPARASI FITUR SISTEM VS AKTIVITAS OFFLINE

Berikut adalah rincian pembagian tanggung jawab antara prosedur fisik manusia di gerai dengan fitur perangkat lunak:

1. **Verifikasi e-KTP Asli**
   * **Prosedur Offline / Fisik (SOP Gerai):** Petugas meraba kekakuan fisik kartu *polycarbonate*, menyorotkan senter sinar UV pada lambang Garuda, dan menempelkan kartu ke alat USB NFC Reader di meja konter.
   * **Fitur Sistem Informasi (Website / Database):** Web POS menampilkan antarmuka checklist verifikasi fisik KTP dan mencatat status `Lolos Uji UV & NFC` ke database.

2. **Verifikasi Pelajar & Wali**
   * **Prosedur Offline / Fisik (SOP Gerai):** Petugas memeriksa fisik lembaran Kartu Keluarga (KK) asli dan melakukan panggilan telepon/video call ke nomor orang tua pelajar untuk konfirmasi izin sewa.
   * **Fitur Sistem Informasi (Website / Database):** Form web menyimpan data penjamin (Nama & NIK Wali), foto scan KK, serta checklist konfirmasi `Persetujuan Orang Tua Terverifikasi`.

3. **Penitipan Dokumen Jaminan**
   * **Prosedur Offline / Fisik (SOP Gerai):** Petugas secara manual membuka pintu brankas fisik gerai dan memasukkan KTP asli ke dalam kotak loker tertentu.
   * **Fitur Sistem Informasi (Website / Database):** Sistem otomatis meng-assign nomor slot loker fisik (misal: `BRANKAS-LOKER-A03`), menerbitkan Tanda Terima Jaminan ber-QR Code, dan mencatat status `Disimpan di Loker`.

4. **Pengecekan Kondisi Awal iPhone**
   * **Prosedur Offline / Fisik (SOP Gerai):** Petugas bersama penyewa mengamati kemulusan bodi HP, mengetes fungsi tombol volume/power, Face ID, True Tone, mikrofon, dan kelengkapan kabel/adaptor.
   * **Fitur Sistem Informasi (Website / Database):** Form BAST Digital menyediakan input persentase *Battery Health* awal, checklist opsi fungsi hardware, dan tombol upload foto 4 sisi bodi HP via kamera gawai.

5. **Serah Terima Perangkat**
   * **Prosedur Offline / Fisik (SOP Gerai):** Petugas menyerahkan kotak unit iPhone fisik dan kabel charger ke tangan penyewa.
   * **Fitur Sistem Informasi (Website / Database):** Petugas menekan tombol `Mulai Sewa (Start Rental)`, sistem mengubah status unit fisik menjadi `Disewa`, dan menyalakan timer hitung mundur masa sewa.

6. **Verifikasi Anti-Tukar Saat Kembali**
   * **Prosedur Offline / Fisik (SOP Gerai):** Petugas membuka menu *Settings > General > About* pada fisik iPhone untuk melihat nomor IMEI dan Serial Number asli perangkat.
   * **Fitur Sistem Informasi (Website / Database):** Kasir memindai QR Code unit; sistem mencocokkan IMEI fisik dengan database kontrak sewa digital, dan memunculkan peringatan jika terjadi ketidaksesuaian.

7. **Pelepasan iCloud / Find My**
   * **Prosedur Offline / Fisik (SOP Gerai):** Penyewa mengetikkan kata sandi Apple ID miliknya di layar iPhone fisik untuk logout akun dan menonaktifkan fitur *Find My iPhone*.
   * **Fitur Sistem Informasi (Website / Database):** Form Check-In di web mewajibkan centang validasi `Status Find My: OFF` sebelum transaksi pengembalian diizinkan untuk diproses lebih lanjut.

8. **Inspeksi Kerusakan & Denda**
   * **Prosedur Offline / Fisik (SOP Gerai):** Petugas meneliti apakah ada lecet baru, layar retak, atau kabel charger yang hilang/rusak.
   * **Fitur Sistem Informasi (Website / Database):** Kasir memilih item kerusakan dari katalog drop-down; sistem secara otomatis menghitung kalkulasi total denda (*overtime* + biaya sparepart) ke invoice penyelesaian.

9. **Sterilisasi Data (Data Wiping)**
   * **Prosedur Offline / Fisik (SOP Gerai):** Teknisi menekan menu fisik iPhone: *Settings > General > Transfer or Reset iPhone > Erase All Content and Settings* hingga muncul layar *Hello Screen*.
   * **Fitur Sistem Informasi (Website / Database):** Sistem mencatat log audit pembersihan data pribadi (`Wipe Status: Verified`), nama teknisi pelaksana, dan waktu eksekusi reset.

10. **Sanitasi Fisik & Charging**
    * **Prosedur Offline / Fisik (SOP Gerai):** Teknisi menyeka bodi iPhone dengan cairan alkohol mikrofiber dan mencolokkan kabel charger ke stopkontak listrik.
    * **Fitur Sistem Informasi (Website / Database):** Form teknisi di web menyediakan checklist `Sanitasi Fisik: Selesai` dan input kapasitas baterai (wajib $\ge 80\%$) sebelum tombol `Release to Available` aktif.

---

## 3. SPESIFIKASI FITUR BERDASARKAN PERAN (ROLE-BASED BREAKDOWN)

### Keterangan Label Klasifikasi:
* **[SISTEM / WEB]:** Fitur perangkat lunak, antarmuka web, logika kode, database, dan integrasi API yang dikerjakan oleh tim pengembang (developer).
* **[OFFLINE / SOP]:** Prosedur manual atau aktivitas fisik di dunia nyata yang dilakukan oleh staf manusia (petugas kasir, teknisi, penyewa) di gerai rental.

---

### A. DASHBOARD PENYEWA (CUSTOMER WEB & MOBILE APP)

Dashboard yang diakses oleh pelanggan melalui browser smartphone atau laptop mereka.

#### 1. Registrasi & e-KYC Akun
* **[SISTEM / WEB] Form Registrasi Akun:** Input data diri (Nama, NIK, WhatsApp, Email, Alamat, Akun Medsos).
* **[SISTEM / WEB] Form Khusus Pelajar:** Input data penjamin (Nama Orang Tua, NIK Wali, No. Telepon Wali).
* **[SISTEM / WEB] Unggah Berkas Identitas:** Fitur upload foto KTP asli / KTM / Kartu Pelajar / Kartu Keluarga.
* **[SISTEM / WEB] Swafoto Biometrik (Liveness Detection):** Modul kamera web dengan instruksi acak (kedip mata / toleh kanan) untuk memverifikasi keaslian pemegang akun secara online.

#### 2. Katalog & Pemesanan Online
* **[SISTEM / WEB] Katalog Unit Real-Time:** Filter dinamis berdasarkan model (iPhone 13–16 Pro), kapasitas memori, dan warna unit yang sedang berstatus `Tersedia`.
* **[SISTEM / WEB] Booking Engine Anti-Collision:** Pemilihan paket sewa (12j, 24j, 3h, 7h) dan slot jam ambil di gerai tanpa tabrakan jadwal dengan penyewa lain.
* **[SISTEM / WEB] Tagihan & Payment Gateway:** Penerbitan invoice pembayaran (QRIS / Virtual Account) dengan validasi otomatis keselarasan nama rekening pengirim (*1-to-1 Match Policy*).

#### 3. Kontrak & Monitoring Masa Sewa
* **[SISTEM / WEB] Tanda Tangan Kontrak Digital:** Lembar perjanjian sewa berkekuatan hukum yang ditandatangani via *E-Signature* / OTP SMS.
* **[SISTEM / WEB] Countdown Timer Masa Sewa:** Indikator hitung mundur waktu sewa aktif dan pengingat WhatsApp otomatis H-3 jam sebelum jatuh tempo.
* **[OFFLINE / SOP] Kehadiran di Gerai:** Penyewa secara fisik datang ke gerai rental membawa dokumen asli yang dipersyaratkan untuk mengambil perangkat.

---

### B. DASHBOARD PETUGAS CS & KASIR GERAI (IN-STORE POS)

Antarmuka kerja cepat di layar komputer/tablet meja konter kasir gerai rental.

#### 1. Verifikasi Anti-Fraud di Meja Konter
* **[OFFLINE / SOP] Uji Fisik Sinar UV & Tekstur KTP:** Petugas menyinari KTP dengan senter UV untuk memeriksa pendaran hologram lambang Garuda dan meraba kekakuan kartu *polycarbonate*.
* **[OFFLINE / SOP] Tempel e-KTP ke NFC Reader:** Petugas meletakkan fisik e-KTP di atas alat USB NFC Reader di meja kasir.
* **[SISTEM / WEB] Integrasi Pembaca NFC:** Web kasir membaca data chip RFID e-KTP dan memvalidasi keaslian respon kartu (menampilkan indikator centang hijau `Chip Valid`).
* **[OFFLINE / SOP] Panggilan Konfirmasi Orang Tua:** Petugas menelpon nomor telepon orang tua pelajar untuk memastikan orang tua mengetahui dan menyetujui penyewaan iPhone.
* **[SISTEM / WEB] Checklist Verifikasi Identitas:** Kasir mencentang opsi hasil verifikasi fisik (`KTP Asli Valid`, `Kesesuaian KK Valid`, `Wali Terkonfirmasi`).

#### 2. Manajemen Loker Jaminan Fisik
* **[OFFLINE / SOP] Penyimpanan Fisik Kartu:** Petugas membuka pintu brankas dan memasukkan KTP asli ke dalam laci/loker fisik.
* **[SISTEM / WEB] Assign Slot Loker Otomatis:** Sistem mencatat nomor slot penyimpanan loker (misal: `BRANKAS-LOKER-A03`) dan mencetak Tanda Terima Jaminan digital ber-QR Code.

#### 3. Serah Terima Unit (Handover)
* **[SISTEM / WEB] Scan QR Unit Fisik:** Kasir memindai stiker QR pada bodi iPhone untuk menarik spesifikasi unit ke layar form serah terima.
* **[OFFLINE / SOP] Inspeksi Fisik Bersama:** Petugas dan penyewa bersama-sama memeriksa fisik layar, bodi, tombol, Face ID, dan mengecek % Battery Health di menu iPhone.
* **[SISTEM / WEB] Form BAST Digital:** Kasir menginput persentase *Battery Health* awal dan mengambil foto dokumentasi 4 sisi bodi unit menggunakan kamera tablet/laptop kasir.
* **[SISTEM / WEB] E-Sign Serah Terima:** Penyewa dan kasir membubuhkan tanda tangan digital pada Berita Acara Serah Terima (BAST).
* **[OFFLINE / SOP] Penyerahan Fisik Perangkat:** Petugas menyerahkan kotak iPhone dan kelengkapan aksesori ke tangan penyewa.
* **[SISTEM / WEB] Aktivasi Status Sewa:** Kasir mengklik tombol `Start Rental`, status unit di database otomatis berubah menjadi `Disewa`.

#### 4. Pengembalian Unit (Check-In) & Kasir Denda
* **[OFFLINE / SOP] Penerimaan Fisik iPhone:** Petugas menerima unit iPhone dan kelengkapannya dari penyewa.
* **[SISTEM / WEB] Validasi IMEI Anti-Tukar:** Kasir memindai QR unit dan memasukkan nomor IMEI yang tertera di menu iPhone untuk diverifikasi otomatis oleh sistem dengan data kontrak.
* **[OFFLINE / SOP] Logout Apple ID & Matikan Find My:** Petugas meminta penyewa mengetikkan password Apple ID di layar iPhone untuk me-logout akun iCloud di depan petugas.
* **[SISTEM / WEB] Validasi Status Kunci iCloud:** Kasir mencentang checklist wajib `Apple ID Kosong & Activation Lock OFF` di web kasir.
* **[OFFLINE / SOP] Pengecekan Kerusakan Fisik:** Petugas memeriksa apakah ada baret baru, retak layar, atau tombol macet pasca pemakaian.
* **[SISTEM / WEB] Komparasi Baseline Foto:** Layar sistem menampilkan foto kondisi awal (saat serah terima) berdampingan dengan kamera live untuk mendeteksi kecacatan baru secara akurat.
* **[SISTEM / WEB] Kalkulator Denda Otomatis:** Sistem secara otomatis menghitung denda *overtime* per jam berdasarkan selisih jam pengembalian dan menambahkan biaya penggantian sparepart dari katalog drop-down.
* **[SISTEM / WEB] Kasir Pembayaran Denda:** Pemrosesan tagihan pelunasan denda (Tunai / QRIS) dan penerbitan bukti lunas.
* **[OFFLINE / SOP] Pengembalian Jaminan Fisik:** Petugas mengambil KTP asli dari brankas loker dan menyerahkannya kembali ke penyewa setelah sistem mengonfirmasi status `Lunas`.

---

### C. DASHBOARD TEKNISI GERAI & DATA SANITIZER (QC & RESET)

Antarmuka kerja bagi tim teknisi di ruang servis/pemeliharaan gawai.

#### 1. Sterilisasi Data Pribadi (Data Wiping)
* **[OFFLINE / SOP] Eksekusi Factory Reset Manual:** Teknisi menavigasikan menu iOS: *Settings > General > Transfer or Reset iPhone > Erase All Content and Settings* hingga perangkat reboot dan memunculkan layar *Hello Screen*.
* **[SISTEM / WEB] Audit Trail Data Wiping:** Teknisi mencatat konfirmasi pembersihan di sistem NORIZ (ID Teknisi, tanggal & jam reset, dan status `Wipe Completed & Verified`) guna menjamin kepatuhan perlindungan privasi data.

#### 2. QC Perangkat, Baterai, & Sanitasi
* **[OFFLINE / SOP] Pengisian Daya Baterai:** Teknisi mencolokkan unit ke stopkontak pengisian daya hingga baterai terisi minimal $\ge 80\%$.
* **[OFFLINE / SOP] Pembersihan Fisik (Sanitasi Unit):** Teknisi menyeka permukaan layar dan bodi unit menggunakan kain mikrofiber serta cairan disinfektan khusus gawai.
* **[SISTEM / WEB] Pembaruan Data Kesehatan Baterai:** Teknisi menginput angka *Battery Health* (%) terbaru ke database unit fisik.
* **[SISTEM / WEB] Tombol Rilis Ketersediaan (Release to Available):** Setelah seluruh checklist terisi, teknisi menekan tombol rilis yang otomatis mengubah status unit dari `Menunggu Pemeriksaan & Reset` menjadi `Tersedia` di katalog pemesanan publik.

#### 3. Tiket Pemeliharaan & Perbaikan (Maintenance)
* **[OFFLINE / SOP] Pengerjaan Servis Fisik:** Teknisi membawa unit ke lab servis resmi untuk penggantian layar pecah, pergantian baterai drop ($<80\%$), atau perbaikan modul kamera.
* **[SISTEM / WEB] Manajemen Tiket Servis:** Sistem mencatat nomor tiket servis, status unit `Dalam Perbaikan (Maintenance)`, riwayat pergantian sparepart, dan biaya perbaikan aktual.

---

### D. DASHBOARD ADMINISTRATOR & PEMILIK USAHA (SUPERADMIN / OWNER)

Pusat kendali berbasis web untuk mengelola master data, aturan bisnis, dan laporan manajerial.

#### 1. Pengaturan Master Data & Kebijakan
* **[SISTEM / WEB] Master Katalog Model:** CRUD data seri iPhone, kapasitas memori, varian warna, dan gambar display.
* **[SISTEM / WEB] Master Inventaris Fisik (Armada):** Pendaftaran unit fisik baru (IMEI 1 & 2, Serial Number), pencetakan stiker QR Code unik, dan tracking siklus status unit.
* **[SISTEM / WEB] Master Skema Tarif & Paket:** Konfigurasi matriks harga sewa dinamis per durasi (12j/24j/3h/7h), tarif denda overtime per jam, dan batas menit toleransi (*grace period*).
* **[SISTEM / WEB] Master Biaya Kerusakan:** Penetapan tabel tarif standar ganti rugi suku cadang fisik resmi (LCD, kamera, bodi, kabel).
* **[SISTEM / WEB] Master Kapasitas Loker Brankas:** Konfigurasi kode slot loker brankas fisik yang tersedia di gerai.

#### 2. Keamanan & Analisis Manajerial
* **[SISTEM / WEB] Manajemen Hak Akses (RBAC):** Pembuatan dan pembatasan hak akses akun staf kasir, staf teknisi, dan admin.
* **[SISTEM / WEB] Database Blacklist:** Manajemen daftar hitam NIK KTP dan nomor telepon bermasalah untuk pencegahan dini penggelapan unit.
* **[SISTEM / WEB] Dashboard Monitoring Eksekutif:** Grafik omzet berkala, visualisasi rasio armada disewa vs di gerai, dan notifikasi unit keterlambatan (*overdue alert*).
* **[SISTEM / WEB] Laporan Keuangan & Logistik:** Rekapitulasi pendapatan sewa, penerimaan denda, laporan riwayat penurunan *Battery Health* armada, serta rekap dokumen jaminan fisik yang sedang berada di brankas gerai.
