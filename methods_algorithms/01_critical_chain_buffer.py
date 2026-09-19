"""STRATEGI 2 + 1 BULAN: target internal 8 minggu + buffer PM 4 minggu.
Membantu PM melindungi tanggal Go-Live dari risiko keterlambatan tim.
"""

CONTRACT_WEEKS = 12
INTERNAL_DEADLINE_WEEK = 8
BUFFER_WEEKS = CONTRACT_WEEKS - INTERNAL_DEADLINE_WEEK

SPRINT_PLAN = {
    "Fase 1 (Inisiasi & Desain)": (1, 2),
    "Fase 2 (Sprint 1: Master Data)": (3, 4),
    "Fase 3 (Sprint 2: Transaksi)": (5, 6),
    "Fase 4 (Sprint 3: Denda & Wiping)": (7, 8),
    "Fase 5 (Buffer: UAT & Bugfix)": (9, 10),
    "Fase 6 (Buffer: Deploy & Handover)": (11, 12),
}


def build_plan(contract_weeks=CONTRACT_WEEKS, internal_weeks=INTERNAL_DEADLINE_WEEK):
    """Susun peta fase: fase pengembangan vs fase buffer."""
    plan = {"development": [], "buffer": []}
    for name, (start, end) in SPRINT_PLAN.items():
        bucket = "development" if end <= internal_weeks else "buffer"
        plan[bucket].append(f"{name}: M{start}-M{end}")
    return plan


def simulate_parkinson(slip_weeks=1):
    """Efek Parkinson: pekerjaan mengisi waktu yang tersedia.
    Tim diberi target internal M8. Jika rajin/malas, dilihat dampaknya ke buffer."""
    finish = INTERNAL_DEADLINE_WEEK + slip_weeks
    remaining_buffer = BUFFER_WEEKS - slip_weeks
    message = ("Tim aman" if remaining_buffer >= 0
               else "Terlambat melewati kontrak!")
    return {
        "finish_week": finish,
        "remaining_buffer_weeks": remaining_buffer,
        "status": message,
    }


if __name__ == "__main__":
    print("=== CRITICAL CHAIN BUFFER (2+1 Bulan) ===")
    print(f"Kontrak klien: {CONTRACT_WEEKS} minggu")
    print(f"Target internal tim: M{INTERNAL_DEADLINE_WEEK} (code freeze & QA pass)")
    print(f"Buffer PM: {BUFFER_WEEKS} minggu (UAT, bugfix, training, Go-Live)")
    print()

    plan = build_plan()
    print("Fase pengembangan:")
    for item in plan["development"]:
        print("  -", item)
    print("Fase buffer PM:")
    for item in plan["buffer"]:
        print("  -", item)

    print()
    print("Simulasi Parkinson's Law (tim slip 1 minggu):")
    print(simulate_parkinson())
    print()
    print("Simulasi slip 4 minggu (buffer habis):")
    print(simulate_parkinson(slip_weeks=4))