"""AUDIT TRAIL DATA WIPING (PRIVACY COMPLIANCE).

Setiap unit selesai disewa WAJIB di-factory reset sebelum disewakan lagi guna
mencegah kebocoran data pribadi penyewa sebelumnya. Alur status:
Menunggu Reset -> Sedang Diproses -> Terverifikasi Bersih.
Sistem merekam petugas, waktu, dan konfirmasi layar sambutan (Hello Screen).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta

WIPE_FLOW = [
    "Menunggu Reset",
    "Sedang Diproses",
    "Terverifikasi Bersih",
]


@dataclass
class WipeRecord:
    unit_id: str
    officer_id: str
    executed_at: datetime
    hello_screen_confirmed: bool = False
    status: str = "Menunggu Reset"


@dataclass
class WipingAuditLog:
    records: list = field(default_factory=list)

    def start(self, unit_id, officer_id, executed_at):
        self.records.append(WipeRecord(unit_id, officer_id, executed_at))

    def mark_in_progress(self, index):
        if self.records[index].status != "Menunggu Reset":
            raise ValueError("Hanya record 'Menunggu Reset' yang bisa dimulai.")
        self.records[index].status = "Sedang Diproses"

    def confirm_verified(self, index, hello_screen_confirmed=True):
        rec = self.records[index]
        if rec.status != "Sedang Diproses":
            raise ValueError("Hanya proses berjalan yang bisa diverifikasi.")
        if not hello_screen_confirmed:
            raise ValueError("Layar Hello Screen belum terkonfirmasi - reset tidak sah.")
        rec.status = "Terverifikasi Bersih"
        rec.hello_screen_confirmed = True

    def release_to_available(self, index):
        rec = self.records[index]
        if rec.status != "Terverifikasi Bersih":
            raise ValueError("Unit belum bersih - tidak boleh rilis ke Tersedia.")
        rec.status = "Rilis -> Tersedia"


if __name__ == "__main__":
    print("=== AUDIT TRAIL DATA WIPING ===")
    log = WipingAuditLog()
    t0 = datetime(2026, 1, 14, 9, 30)
    log.start("IP15P-001", "TECH-02", t0)
    log.start("IP14P-003", "TECH-01", t0 + timedelta(minutes=15))

    print("1) Teknisi mulai reset unit 1:")
    log.mark_in_progress(0)
    print("   ", [(r.unit_id, r.status) for r in log.records])

    print("2) Coba konfirmasi tanpa Hello Screen -> ditolak:")
    try:
        log.confirm_verified(0, hello_screen_confirmed=False)
    except ValueError as e:
        print("    DITOLAK:", e)

    print("3) Reset selesai, Hello Screen terkonfirmasi:")
    log.confirm_verified(0)
    log.release_to_available(0)
    print("   ", [(r.unit_id, r.status) for r in log.records])
    print("    *) Unit siap disewakan kembali ke pelanggan berikutnya.")