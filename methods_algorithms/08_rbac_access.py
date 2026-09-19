"""RBAC (ROLE-BASED ACCESS CONTROL): otoritas akses berjenjang.

3 peran: petugas konter/kasir, manajer operasional, pemilik (owner).
Memisahkan wewenang lihat laporan vs kelola data berdasarkan peran.
"""

from dataclasses import dataclass

PERMISSIONS = {
    "kasir": {
        "transaksi_harian": True,
        "status_unit_gerai": True,
        "lihat_omzet": False,
        "kelola_laporan_armada": False,
        "rekap_denda": False,
        "kelola_blacklist": False,
    },
    "manajer": {
        "transaksi_harian": True,
        "status_unit_gerai": True,
        "lihat_omzet": True,
        "kelola_laporan_armada": True,
        "rekap_denda": True,
        "kelola_blacklist": True,
    },
    "owner": {
        "transaksi_harian": True,
        "status_unit_gerai": True,
        "lihat_omzet": True,
        "kelola_laporan_armada": True,
        "rekap_denda": True,
        "kelola_blacklist": True,
    },
}


@dataclass
class RBAC:
    role: str
    permissions: dict

    def can(self, action):
        return self.permissions.get(action, False)

    @classmethod
    def for_role(cls, role):
        return cls(role=role, permissions=PERMISSIONS[role])


if __name__ == "__main__":
    print("=== RBAC ACCESS CONTROL ===")
    for role in PERMISSIONS:
        user = RBAC.for_role(role)
        checks = [
            ("transaksi_harian", "Lihat transaksi harian"),
            ("kelola_laporan_armada", "Kelola laporan kesehatan armada"),
            ("kelola_blacklist", "Kelola daftar hitam penyewa"),
        ]
        results = " | ".join(f"{label}={'Y' if user.can(a) else 'N'}"
                             for a, label in checks)
        print(f"  {role:<8} : {results}")