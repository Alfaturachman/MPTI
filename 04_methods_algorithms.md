# METODE & ALGORITMA — PROYEK SISTEM INFORMASI MANAJEMEN RENTAL IPHONE (NORIZ)

Dokumen pemetaan metode manajemen proyek dan algoritma bisnis/sistem yang digunakan dalam proyek NORIZ, beserta penjelasan fungsinya.

---

## A. METODE & ALGORITMA YANG SUDAH DITERAPKAN

### A.1 Metode Manajemen Proyek

**Critical Chain Buffer** (Strategi 2+1 Bulan)
- Deskripsi: Target internal tim 8 minggu + buffer PM 4 minggu (UAT, bugfix, training, Go-Live). Konsep terkait: *Parkinson's Law*.
- Fungsi: Melindungi tanggal pengiriman kontrak (12 minggu) dari risiko keterlambatan developer, bug lapangan, dan permintaan klien. Buffer memberi ruang aman bagi PM tanpa mengganggu komitmen ke klien.

**Triple Constraints**
- Deskripsi: Keseimbangan *Scope – Time – Cost* (ruang lingkup, waktu 12 minggu, biaya Rp 75 juta).
- Fungsi: Menjadi kerangka keputusan utama PM — setiap perubahan ruang lingkup harus diimbangi penyesuaian waktu/biaya.

**Lean Agile Team + Sprint**
- Deskripsi: Tim ramping 4 orang, kerja dalam 3 sprint (M2–M8) dengan *Daily Standup* 15 menit.
- Fungsi: Memperpendek jalur komunikasi, meminimalkan overhead, dan mendeteksi *blocker* coding sejak dini setiap hari.

**WBS & Timeline 6 Fase**
- Deskripsi: Perincian pekerjaan dari Minggu 1 hingga 12 dalam 6 fase.
- Fungsi: Menjadi acuan progres harian, dasar penyusunan jadwal per anggota tim, dan alat pelaporan ke klien.

**Contingency Fund (~4%)**
- Deskripsi: Dana cadangan sebesar Rp 3.000.000 (4% dari total proyek).
- Fungsi: Mengantisipasi lonjakan biaya tak terduga; sisa dana yang tidak terpakai menjadi laba tambahan PM.

**Matriks Risiko Probability–Impact**
- Deskripsi: Penilaian risiko (programmer malas/sakit, scope creep, bug UAT) berdasarkan peluang & dampak.
- Fungsi: Menentukan prioritas mitigasi dan tindakan preventif PM terhadap ancaman terhadap triple constraints.

**Kontrol Scope Creep berbasis kontrak**
- Deskripsi: Dokumen spesifikasi bisnis dijadikan pegangan hukum; fitur tambahan dialihkan ke "Fase 2".
- Fungsi: Menjaga ruang lingkup proyek tetap sesuai kontrak sehingga waktu dan biaya tidak membengkak.

**RBAC (Role-Based Access Control)**
- Deskripsi: 3 jenjang akses — Petugas Konter/Kasir, Manajer Operasional, Pemilik/Owner.
- Fungsi: Menjamin keamanan data dan memisahkan wewenang lihat vs kelola laporan sesuai peran pengguna.

### A.2 Algoritma Bisnis / Sistem

**Anti-Collision Reservasi** (*interval scheduling*)
- Deskripsi: Satu unit fisik tidak boleh dipakai 2 penyewa pada rentang waktu bersinggungan; disisipkan *buffer time* 2 jam pembersihan.
- Fungsi: Mencegah tumbukan jadwal sewa dan menjamin kesiapan unit (pemeriksaan, sanitasi, *data wiping*) antarpenyewa.

**Hold Timeout 60 menit** (auto-cancel)
- Deskripsi: Reservasi berstatus *Menunggu Pembayaran* dibatalkan otomatis jika tidak lunas dalam 60 menit.
- Fungsi: Menghindari unit terkunci sia-sia oleh pemesan yang tidak membayar, sehingga unit kembali *Tersedia*.

**Formula Denda Overtime**
- Deskripsi: Denda = ⌈jam keterlambatan⌉ × tarif/jam, dengan *grace period* 15 menit, pembulatan ke atas, dan aturan ekstrem 6 jam (denda 1 hari + penalti 50%).
- Fungsi: Menghitung penalti keterlambatan secara otomatis, adil (ada toleransi), dan konsistabel antar transaksi.

**Anti-Fraud Multi-Layer**
- Deskripsi: NFC chip test, UV inspection, *liveness detection* (biometrik wajah), *1-to-1 match* rekening, multi-document rule, anti-switching (cocok IMEI).
- Fungsi: Mencegah penyewaan dengan KTP palsu, identitas curian, pembayaran pihak ketiga, dan unit yang ditukar saat pengembalian.

**State Machine Status**
- Deskripsi: Status unit (6 status) dan status akun penyewa (4 status) dengan transisi terdefinisi.
- Fungsi: Memastikan setiap unit/akun hanya berada pada satu kondisi sah dan menjadi dasar validasi tiap transaksi.

**Audit Trail Data Wiping**
- Deskripsi: Alur status *Menunggu Reset → Sedang Diproses → Terverifikasi Bersih*, merekam petugas, waktu, ID unit.
- Fungsi: Menjamin kepatuhan privasi data (mencegah kebocoran data penyewa sebelumnya) dan tercatatnya eksekusi *factory reset*.

**Formula Ganti Rugi Total Loss**
- Deskripsi: Biaya penggantian = nilai pasar wajar unit + 10% biaya disrupsi operasional.
- Fungsi: Standar perhitungan tuntutan ganti rugi atas kehilangan/penggelapan unit yang jelas dan transparan.

**Immutability & Soft-Delete**
- Deskripsi: Data transaksi lunas bersifat permanen; penghapusan hanya *soft-delete* dengan catatan alasan audit.
- Fungsi: Menjaga integritas laporan keuangan dan menyediakan jejak audit untuk kepentingan hukum/akuntansi.

---

## B. KANDIDAT PENAMBAHAN (BELUM DITERAPKAN)

### B.1 Sisi Manajemen Proyek

**CPM (Critical Path Method)**
- Deskripsi: Diagram jaringan & ketergantungan antar aktivitas proyek semua fase.
- Fungsi: Menemukan jalur kritis (rangkaian aktivitas terpanjang) sehingga PM tahu aktivitas mana yang tidak boleh terlambat agar tanggal Go-Live aman.

**PERT**
- Deskripsi: Estimasi 3 titik — *optimistic*, *most likely*, *pessimistic* per aktivitas.
- Fungsi: Menghasilkan estimasi durasi yang lebih realistis dengan mempertimbangkan ketidakpastian, cocok untuk mengisi detail tiap fase.

**EVM (Earned Value Management)**
- Deskripsi: Pengukuran progress per termin: SV/SVV, SPI, dan CPI.
- Fungsi: Membandingkan rencana vs realisasi waktu & biaya sehingga PM tahu posisi proyek (*ahead/behind schedule* dan *over/under budget*).

**MoSCoW Prioritization**
- Deskripsi: Kategorisasi fitur — *Must–Should–Could–Won't*.
- Fungsi: Alat kontrol ruang lingkup; memisahkan spesifikasi wajib kontrak dari fitur "nice to have" yang bisa dialihkan ke Fase 2.

**Buffer Fever Chart**
- Deskripsi: Monitoring konsumsi buffer critical chain dalam zona hijau/kuning/merah.
- Fungsi: Memberi sinyal dini apakah cadangan waktu PM terkikis cepat atau aman, sehingga mitigasi bisa diambil sebelum buffer habis.

**RACI Matrix**
- Deskripsi: Pemetaan peran *Responsible–Accountable–Consulted–Informed* per aktivitas.
- Fungsi: Menghapus ambiguitas tanggung jawab antar 4 anggota tim dan memperkuat akuntabilitas.

**DoD + Sprint Retrospective**
- Deskripsi: Standar *Definition of Done* untuk tiap sprint dan sesi introspeksi rutin.
- Fungsi: Menjamin suatu fitur "selesai" benar-benar layak rilis, serta memperbaiki proses sprint berikutnya secara berkelanjutan.

**RPO / RTO**
- Deskripsi: Target *Recovery Point Objective* & *Recovery Time Objective* untuk backup database.
- Fungsi: Mendefinisikan seberapa cepat sistem pulih (RTO) dan seberapa banyak data yang boleh hilang (RPO) saat disaster — melengkapi konfigurasi auto-backup harian.

### B.2 Sisi Algoritma Sistem (Sesuai Konteks Rental)

**Fleet Load-Balancing (greedy)**
- Deskripsi: Sistem mengalokasikan unit dengan utilisasi atau BH% terendah saat pemesanan (mis. pilih unit tersedia dengan BH tertinggi).
- Fungsi: Meratakan beban pemakaian armada sehingga keausan & degradasi baterai antar unit merata dan umur armada lebih panjang.

**Risk Scoring Penyewa**
- Deskripsi: Skor berbobot — kategori penyewa, riwayat telat, sisa denda belum lunas, domisili, riwayat blacklist.
- Fungsi: Landasan keputusan otomatis: wajib/tidaknya deposit finansial dan ambang batas *blacklist* — mewujudkan kalimat "sistem analisis risiko" pada dokumen bisnis.

**Peak / Surge Pricing**
- Deskripsi: Multiplikator tarif pada jam/akhir pekan atau event ramai.
- Fungsi: Mengoptimalkan pendapatan pada periode permintaan tinggi dan mengarahkan permintaan ke jam longgar.

**Scheduler / Cron Job**
- Deskripsi: Proses berjalan otomatis terjadwal — deteksi tagihan denda overtime dan auto-cancel invoice lewat 60 menit.
- Fungsi: Menghilangkan ketergantungan pada tindakan manual petugas; penagihan & pembatalan berjalan tepat waktu 24/7.

**State Machine Formal (dengan guard)**
- Deskripsi: Transisi status unit/akun/transaksi diformalkan dengan *guard condition* (mis. kontrak wajib ditandatangani sebelum unit berubah *Dipesan → Disewa*).
- Fungsi: Mencegah transisi status ilegal yang dapat menyebabkan penyalahgunaan atau pembayaran tidak sesuai SOP.

**Image Similarity (SSIM / feature match)**
- Deskripsi: Komparasi otomatis foto baseline saat serah terima vs foto kondisi saat pengembalian.
- Fungsi: Membantu petugas mendeteksi goresan/kerusakan baru dengan cepat, mengurangi kegagapan inspeksi visual manual.

**Forecast Battery Health (BH%)**
- Deskripsi: Regresi sederhana / moving average atas riwayat penurunan BH% per unit.
- Fungsi: Memprediksi kapan BH% menyentuh ambang kelaikan 80% sehingga PM bisa merencanakan pergantian/turun unit sebelum terjadi.