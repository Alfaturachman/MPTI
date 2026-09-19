"""PERT (PROGRAM EVALUATION AND REVIEW TECHNIQUE): estimasi 3 titik.

Rumus:
  E = (O + 4M + P) / 6        (estimasi ekspektasi)
  Var = ((P - O) / 6) ^ 2     (varians ketidakpastian)
"""

TASKS = {
    "Inisiasi & Desain": (1, 2, 4),
    "Sprint 1 Master Data": (1.5, 2, 3),
    "Sprint 2 Transaksi": (2, 2, 4),
    "Sprint 3 Denda & Wiping": (1.5, 2, 3),
    "UAT & Bugfix": (1, 2, 4),
    "Deploy & Handover": (1, 2, 3),
}


def pert(o, m, p):
    expected = (o + 4 * m + p) / 6
    variance = ((p - o) / 6) ** 2
    return expected, variance


if __name__ == "__main__":
    print("=== PERT - ESTIMASI 3 TITIK ===")
    total_e = total_v = 0
    for name, (o, m, p) in TASKS.items():
        e, v = pert(o, m, p)
        total_e += e
        total_v += v
        print(f"  {name:<24} O={o} M={m} P={p}  ->  E={e:.2f} minggu (Var={v:.3f})")
    print("-" * 60)
    print(f"  Estimasi total proyek : {total_e:.2f} minggu")
    print(f"  Varians total         : {total_v:.3f}")
    import math
    print(f"  Std deviasi           : {math.sqrt(total_v):.2f} minggu")
    print(f"  Rentang realistis     : {total_e - math.sqrt(total_v):.2f} s.d. "
          f"{total_e + math.sqrt(total_v):.2f} minggu")