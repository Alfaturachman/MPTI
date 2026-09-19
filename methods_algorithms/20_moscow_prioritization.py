"""MOSCOW PRIORITIZATION: Must - Should - Could - Won't.

Memisahkan spesifikasi wajib kontrak (Must) dari fitur 'nice to have'.
Alat kontrol ruang lingkup: Won't tidak boleh masuk lingkup proyek saat ini.
"""

FEATURES = [
    ("Anti-collision reservasi", "M"),
    ("CRUD Master Unit & Penyewa", "M"),
    ("Pembayaran & kontrak digital", "M"),
    ("Verifikasi KTP fisik (NFC/UV)", "M"),
    ("Denda overtime otomatis", "M"),
    ("Data wiping & audit trail", "M"),
    ("Dashboard laporan manajerial", "S"),
    ("Notifikasi WhatsApp gateway", "S"),
    ("Analitik prediksi omzet", "C"),
    ("Export laporan Excel", "C"),
    ("Integrasi kamera pengenalan wajah", "W"),
]

ORDER = {"M": 0, "S": 1, "C": 2, "W": 3}


def plan_sprint(features):
    """Susun rencana rilis berdasarkan MoSCoW."""
    sorted_f = sorted(features, key=lambda x: ORDER[x[1]])
    plan = {"Sprint 1-2 (harus)": [], "Sprint 3 (seharusnya)": [],
            "Backlog (bisa)": [], "Luar scope": []}
    for name, cat in sorted_f:
        if cat == "M":
            plan["Sprint 1-2 (harus)"].append(name)
        elif cat == "S":
            plan["Sprint 3 (seharusnya)"].append(name)
        elif cat == "C":
            plan["Backlog (bisa)"].append(name)
        else:
            plan["Luar scope"].append(name)
    return plan


if __name__ == "__main__":
    print("=== MOSCOW PRIORITIZATION ===")
    for bucket, items in plan_sprint(FEATURES).items():
        print(f"\n{bucket}:")
        for item in items:
            print("  -", item)
    print("\n=> Won't = di luar kesepakatan kontrak, tidak dijadwalkan.")