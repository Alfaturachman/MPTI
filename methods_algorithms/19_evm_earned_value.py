"""EVM (EARNED VALUE MANAGEMENT): SV, SPI, CV, CPI.

Membandingkan rencana (PV) vs realisasi biaya (AC) vs nilai pekerjaan yang
selesai (EV) untuk menilai posisi proyek pada periode tertentu.
"""


def evm_report(pv, ev, ac):
    result = {}
    result["PV"] = pv
    result["EV"] = ev
    result["AC"] = ac
    result["SV"] = round(ev - pv, 2)      # schedule variance (positif = lebih cepat)
    result["CV"] = round(ev - ac, 2)      # cost variance    (positif = di bawah budget)
    result["SPI"] = round(ev / pv, 2)     # schedule performance index (>=1 bagus)
    result["CPI"] = round(ev / ac, 2)     # cost performance index      (>=1 bagus)
    result["schedule_status"] = "Ahead of schedule" if result["SPI"] >= 1 else "Behind schedule"
    result["cost_status"] = "Under budget" if result["CPI"] >= 1 else "Over budget"
    result["est_final_cost"] = round(ac / result["CPI"], 2)
    return result


if __name__ == "__main__":
    print("=== EVM - EARNED VALUE MANAGEMENT ===")
    print("Review termin 1 (target progres 30%, budget termin Rp 36 jt):")
    report = evm_report(pv=36_000_000, ev=33_000_000, ac=38_500_000)
    for k, v in report.items():
        print(f"  {k:<16}: {v}")
    print()
    print(f"Perkiraan biaya akhir bila tren berlanjut: Rp {report['est_final_cost']:,}")
    print("=> PM: percepat mitigasi (CPI < 1) agar margin 40% tidak tergerus.")