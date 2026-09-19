"""SCHEDULER / CRON JOB: tugas otomatis terjadwal 24/7.

Pekerjaan yang berjalan tanpa campur tangan petugas:
1. Auto-cancel invoice melewati batas 60 menit.
2. Deteksi keterlambatan overtime & penagihan otomatis.
3. Pembaruan blacklist penyewa.
"""

from datetime import datetime, timedelta

INVOICE_TTL = 60  # menit


def cancel_expired_invoices(invoices, now):
    expired = [inv for inv in invoices
               if inv["status"] == "unpaid" and now >= inv["payable_until"]]
    for inv in expired:
        inv["status"] = "cancelled"
        inv["unit_status"] = "available"
    return [inv["code"] for inv in expired]


def detect_overtime(rentals, now):
    """Rental yang melewati jatuh tempo tanpa perpanjangan -> beri sanksi otomatis."""
    overdue = [r for r in rentals if r["due_at"] < now and not r["extended"]]
    for r in overdue:
        r["overtime"] = (now - r["due_at"]).total_seconds() // 3600
    return overdue


def update_blacklist(renters):
    return [r["name"] for r in renters if r["unpaid_fine"] > 0 and r["risk_score"] >= 50]


if __name__ == "__main__":
    print("=== SCHEDULER / CRON JOB ===")
    now = datetime(2026, 1, 15, 10, 0)

    invoices = [
        {"code": "INV-001", "status": "unpaid", "payable_until": now - timedelta(minutes=70), "unit_status": "on-hold"},
        {"code": "INV-002", "status": "unpaid", "payable_until": now + timedelta(minutes=30)},
    ]
    print("Auto-cancel invoice lewat 60 menit:", cancel_expired_invoices(invoices, now))

    rentals = [{"id": "RT-001", "due_at": now - timedelta(hours=2), "extended": False},
               {"id": "RT-002", "due_at": now + timedelta(days=1), "extended": False}]
    print("Deteksi overtime:", [(r["id"], f"{r['overtime']} jam") for r in detect_overtime(rentals, now)])

    renters = [{"name": "Joko", "unpaid_fine": 150_000, "risk_score": 55},
               {"name": "Siti", "unpaid_fine": 0, "risk_score": 30}]
    print("Update blacklist:", update_blacklist(renters))