"""HOLD TIMEOUT 60 MENIT (AUTO-CANCEL).

Reservasi berstatus "Menunggu Pembayaran" memiliki batas kedaluwarsa 60 menit.
Jika tidak lunas, sistem membatalkan otomatis dan mengembalikan unit ke
status "Tersedia".
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta

HOLD_TTL_MINUTES = 60


@dataclass
class Reservation:
    code: str
    unit: str
    payable_until: datetime
    status: str = "Menunggu Pembayaran"


@dataclass
class ReservationRepo:
    reservations: list = field(default_factory=list)

    def process_expired(self, now):
        cancelled = []
        for r in self.reservations:
            if r.status == "Menunggu Pembayaran" and now >= r.payable_until:
                r.status = "Dibatalkan / Kedaluwarsa"
                cancelled.append(r.code)
        return cancelled

    def release_units(self, now):
        """Unit-unit milik reservasi kadaluarsa kembali Tersedia."""
        return [r.unit for r in self.reservations if r.status == "Dibatalkan / Kedaluwarsa"]


if __name__ == "__main__":
    print("=== HOLD TIMEOUT 60 MENIT ===")
    t0 = datetime(2026, 1, 10, 12, 0)
    repo = ReservationRepo(reservations=[
        Reservation("RSV-001", "IP15P-001", t0 + timedelta(minutes=60)),   # belum bayar
        Reservation("RSV-002", "IP14P-003", t0 + timedelta(minutes=40)),   # bayar dalam 40 menit
    ])

    print("Cek pada menit ke-65:", [r.status for r in repo.reservations])
    expired = repo.process_expired(t0 + timedelta(minutes=65))
    print("Auto-cancel:", expired)
    print("Unit dirilis ke Tersedia:", repo.release_units(t0 + timedelta(minutes=65)))
    print("RSV-002 tetap aman:", repo.reservations[1].status)