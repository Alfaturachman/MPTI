"""RISK SCORING PENYEWA.

Skor berbobot dari faktor risiko:
- Kategori penyewa (pelajar/karyawan/umum perlu bobot lebih)
- Riwayat keterlambatan pengembalian
- Sisa denda belum lunas
- Domisili (luar kota)
- Riwayat blacklist

Digunakan untuk keputusan: wajib deposit / blacklist.
"""

WEIGHTS = {
    "luar_kota": 15,
    "riwayat_telat": 12,
    "denda_belum_lunas": 20,
    "riwayat_blacklist": 30,
    "kategori_berisiko": 10,
}

DEPOSIT_THRESHOLD = 20
BLACKLIST_THRESHOLD = 50


def risk_score(profile: dict):
    return sum(WEIGHTS[k] for k, flag in profile.items()
               if flag and k in WEIGHTS)


def decision(score):
    if score >= BLACKLIST_THRESHOLD:
        return {"score": score, "action": "BLACKLIST / TANGGUH",
                "note": "Akun dibekukan, butuh penyelesaian denda."}
    if score >= DEPOSIT_THRESHOLD:
        return {"score": score, "action": "WAJIB DEPOSIT",
                "note": "Sistem analisis risiko menilai perlu jaminan finansial."}
    return {"score": score, "action": "DITERIMA",
            "note": "Risiko rendah, lanjut verifikasi normal."}


if __name__ == "__main__":
    print("=== RISK SCORING PENYEWA ===")
    penyewa = {
        "Budi (karyawan, domisili Semarang)": {"luar_kota": False,
                                               "riwayat_telat": False,
                                               "denda_belum_lunas": False,
                                               "riwayat_blacklist": False,
                                               "kategori_berisiko": False},
        "Siti (luar kota, sering telat)": {"luar_kota": True,
                                           "riwayat_telat": True,
                                           "denda_belum_lunas": False,
                                           "riwayat_blacklist": False,
                                           "kategori_berisiko": True},
        "Joko (blacklist, tunggakan denda)": {"luar_kota": False,
                                              "riwayat_telat": True,
                                              "denda_belum_lunas": True,
                                              "riwayat_blacklist": True,
                                              "kategori_berisiko": True},
    }
    for nama, profil in penyewa.items():
        print(f"{nama}: {decision(risk_score(profil))}")