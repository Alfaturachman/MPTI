"""ANTI-COLLISION RESERVASI (interval scheduling + buffer 2 jam).

Satu unit fisik tidak boleh dipakai 2 penyewa pada rentang waktu yang
bersinggungan. Sistem wajib menyisipkan buffer time 2 jam setelah akhir sewa
penyewa A sebelum awal sewa penyewa B (pembersihan & data wiping).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta

BUFFER_HOURS = 2


@dataclass
class Booking:
    renter: str
    start: datetime
    end: datetime


@dataclass
class UnitCalendar:
    unit_code: str
    bookings: list = field(default_factory=list)

    def available(self, start, end):
        """Cek sehat secara keseluruhan tanpa konflik di semua booking."""
        for b in self.bookings:
            if self._overlaps(b, start, end):
                return False
        return True

    @staticmethod
    def _overlaps(b, start, end):
        b_start = b.start - timedelta(hours=BUFFER_HOURS)
        return start < b.end and b_start < end

    def book(self, renter, start, end):
        if not self.available(start, end):
            raise ValueError(f"Bentrok jadwal untuk {self.unit_code}")
        self.bookings.append(Booking(renter, start, end))

    def next_free(self, start, duration_hours):
        """Cari slot kosong pertama setelah waktu start."""
        cursor = start
        for i in range(10):
            end = cursor + timedelta(hours=duration_hours)
            if self.available(cursor, end):
                return cursor, end
            cursor = max(b.end for b in self.bookings) + timedelta(hours=BUFFER_HOURS)
        return None


if __name__ == "__main__":
    print("=== ANTI-COLLISION RESERVASI (buffer 2 jam) ===")
    t0 = datetime(2026, 1, 10, 8, 0)
    cal = UnitCalendar("IP15P-001")
    cal.book("Andi", t0, t0 + timedelta(hours=24))          # Andi 10 Jan 08:00 s.d 11 Jan 08:00

    start_b = t0 + timedelta(hours=23)                       # mencoba mulai 11 Jan 07:00
    end_b = start_b + timedelta(hours=24)
    print("Andi booking:", cal.bookings[0].start, "->", cal.bookings[0].end)
    print("Budi mencoba mulai 07:00 (sebelum buffer 2 jam):", cal.available(start_b, end_b))
    try:
        cal.book("Budi", start_b, end_b)
    except ValueError as e:
        print("  DITOLAK:", e)

    print("Slot bebas berikutnya yang aman (24 jam):", cal.next_free(t0, 24))