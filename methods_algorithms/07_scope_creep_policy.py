"""KONTROL SCOPE CREEP BERBASIS KONTRAK.

Dokumen spesifikasi bisnis menjadi pegangan hukum. Fitur tambahan di luar
kontrak dialihkan ke "Fase 2 Pengembangan" pasca-pelunasan proyek utama.
"""

from dataclasses import dataclass, field

CONTRACT_FEATURES = [
    "CRUD Master Produk & Inventaris",
    "Anti-collision reservasi",
    "Pembayaran & kontrak digital",
    "Serah terima & verifikasi anti-fraud",
    "Denda overtime & ganti rugi",
    "Data wiping & audit trail",
    "Laporan & monitoring",
]


@dataclass
class ScopeContract:
    contract: list = field(default_factory=lambda: list(CONTRACT_FEATURES))
    phase2_queue: list = field(default_factory=list)
    rejected: list = field(default_factory=list)

    def request(self, feature, is_in_contract=False):
        if is_in_contract:
            return {"status": "diterima", "feature": feature, "bucket": "kontrak"}
        self.phase2_queue.append(feature)
        return {"status": "dialihkan ke Fase 2", "feature": feature, "bucket": "phase2"}

    def after_project_done(self):
        return {"antrian_fase2": self.phase2_queue}


if __name__ == "__main__":
    print("=== KONTROL SCOPE CREEP ===")
    sc = ScopeContract()
    print("Fitur dalam kontrak:", len(sc.contract))
    print(sc.request("Analitik prediksi omzet (baru)", is_in_contract=False))
    print(sc.request("Export laporan ke Excel", is_in_contract=False))
    print(sc.request("Modul blacklist", is_in_contract=True))
    print("Antrian Fase 2 yang menunggu setelah pelunasan:", sc.phase2_queue)