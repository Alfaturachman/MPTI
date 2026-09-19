"""FORMULA DENDA OVERTIME (KETERLAMBATAN).

Aturan:
- Grace period: keterlambatan <= 15 menit tidak kena denda.
- Pembulatan: > 15 menit dibulatkan ke atas menjadi 1 jam penuh.
- Ekstrem: > 6 jam tanpa konfirmasi = denda 1 hari penuh + penalti 50% dari sewa harian.
- Rumus dasar: Denda = ceil(jam terlambat) x Tarif Overtime/jam.
"""

import math
from datetime import datetime, timedelta

GRACE_MINUTES = 15
EXTREME_HOURS = 6
EXTREME_PENALTY_PCT = 0.50


def calc_overtime_fine(due_time, return_time, tariff_per_hour, daily_rate):
    late_min = max(0, (return_time - due_time).total_seconds() // 60)

    if late_min == 0:
        return {"status": "Tepat waktu", "late_minutes": 0, "fine": 0}

    if late_min <= GRACE_MINUTES:
        return {"status": "Dalam grace period", "late_minutes": int(late_min),
                "fine": 0, "note": f"Toleransi {GRACE_MINUTES} menit"}

    late_hours = late_min / 60
    if late_hours > EXTREME_HOURS:
        fine = daily_rate + daily_rate * EXTREME_PENALTY_PCT
        return {"status": "Keterlambatan ekstrem", "late_hours": round(late_hours, 2),
                "fine": fine, "note": f"> {EXTREME_HOURS} jam, denda 1 hari + 50%"}

    hours_charged = math.ceil(late_hours)
    fine = hours_charged * tariff_per_hour
    return {"status": "Standar", "late_hours": round(late_hours, 2),
            "charged_hours": hours_charged, "fine": fine,
            "note": f"{hours_charged} jam x Rp {tariff_per_hour}"}


if __name__ == "__main__":
    print("=== FORMULA DENDA OVERTIME ===")
    due = datetime(2026, 1, 12, 20, 0)
    cases = {
        "Kembali tepat waktu (20:00)": due,
        "Terlambat 10 menit (grace)": due + timedelta(minutes=10),
        "Terlambat 1 jam 5 menit": due + timedelta(hours=1, minutes=5),
        "Terlambat 7 jam (ekstrem)": due + timedelta(hours=7),
    }
    for label, ret in cases.items():
        print(f"{label}: {calc_overtime_fine(due, ret, tariff_per_hour=30_000, daily_rate=120_000)}")