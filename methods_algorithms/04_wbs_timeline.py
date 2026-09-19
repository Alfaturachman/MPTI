"""WBS & TIMELINE 6 FASE: rincian pekerjaan per peran dan rentang minggu.

Menghasilkan baris timeline seperti yang dipakai Gantt Chart (7 peran x 6 fase),
menjadi acuan progres harian dan dasar pelaporan ke klien.
"""

ROLES = {
    "Project Manager (PM)": [
        "Inisiasi, Desain & Arsitektur",
        "Sprint 1 - Master Data & Reservasi",
        "Sprint 2 - Transaksi & Anti-Fraud",
        "Sprint 3 - Denda & Data Wiping",
        "Buffer 1 - UAT & Bugfix",
        "Buffer 2 - Deployment & Handover",
    ],
    "Backend Senior": [
        "ERD, Skema DB & API Boilerplate",
        "CRUD Master & Anti-Collision",
        "Payment Gateway & Engine PDF",
        "Check-in, Denda & Data Wiping",
        "Bug Fix & Optimasi Query",
        "Konfigurasi Server Produksi",
    ],
    "Backend Junior": [
        "Setup Environment & Repo",
        "Endpoint Penyewa & CRUD Dasar",
        "Scheduler Denda & Auto-Cancel",
        "Katalog Kerusakan & API Laporan",
        "Dukungan Bug Fix",
        "Verifikasi Staging ke Produksi",
    ],
    "Frontend Senior": [
        "Repo, Design Tokens & Komponen",
        "Katalog Publik & Ketersediaan RT",
        "Kasir POS & Kamera Foto 4 Sisi",
        "Inspeksi Pengembalian & Pelaporan",
        "Optimasi Caching & Kecepatan",
        "Final Build di CDN/Produksi",
    ],
    "Frontend Junior": [
        "Boilerplate & CSS Framework",
        "Formulir Pemesanan & Validasi",
        "Scan NFC & UI Form BAST",
        "Checklist Sanitasi & Revisi UI",
        "Perbaikan Bug UI Lintas Device",
        "Verifikasi Kamera Device Gerai",
    ],
    "UI/UX Designer": [
        "Riset, Wireframe & Prototipe Figma",
        "Design System & Aset Reservasi",
        "Template Kontrak & BAST Digital",
        "Finalisasi Aset UI & Panduan",
        "Revisi Visual Hasil UAT",
        "User Guide & Visual Pelatihan",
    ],
    "QA Tester": [
        "Kerangka Master Test Plan",
        "Test Case & Uji Modul Master",
        "Uji Responsivitas & Anti-Fraud",
        "End-to-End Testing & Bug Log",
        "Regression Testing & Berita UAT",
        "UAT Final & Verifikasi Data",
    ],
}

PHASE_MONTHS = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12)]


def build_wbs():
    rows = []
    for role, activities in ROLES.items():
        for idx, activity in enumerate(activities):
            m1, m2 = PHASE_MONTHS[idx]
            rows.append({"role": role, "activity": activity, "month_start": m1, "month_end": m2})
    return rows


if __name__ == "__main__":
    print("=== WBS & TIMELINE (6 Fase x 7 Peran) ===")
    for r in build_wbs():
        print(f"M{r['month_start']:>2}-M{r['month_end']:<2} | {r['role']:<22} | {r['activity']}")
    print(f"\nTotal aktivitas: {len(build_wbs())} baris")