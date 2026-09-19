"""BUFFER FEVER CHART: monitoring konsumsi buffer critical chain.

Zona berdasarkan rasio konsumsi buffer terhadap total buffer:
- Hijau  (< 33%): aman, lanjut rencana.
- Kuning (33-66%): perhatikan, percept aktivitas jalur kritis.
- Merah  (> 66%): tindakan korektif segera (scope/capacity).
"""

BUFFER_TOTAL_WEEKS = 4


def fever_status(consumed_weeks):
    ratio = consumed_weeks / BUFFER_TOTAL_WEEKS
    if ratio < 0.33:
        zone = "HIJAU"
        action = "Aman - lanjut sesuai rencana, tidak perlu intervensi."
    elif ratio <= 0.66:
        zone = "KUNING"
        action = "Waspada - percep aktivitas jalur kritis & daily follow-up blocker."
    else:
        zone = "MERAH"
        action = "Kritis - kurangi scope/nambah kapasitas, siapkan rencana pemulihan."
    return {"consumed": consumed_weeks, "total": BUFFER_TOTAL_WEEKS,
            "ratio_pct": round(ratio * 100), "zone": zone, "action": action}


if __name__ == "__main__":
    print("=== BUFFER FEVER CHART ===")
    for used in (1, 2, 3):
        s = fever_status(used)
        print(f"  Konsumsi {used}/{s['total']} minggu ({s['ratio_pct']}%): "
              f"ZONA {s['zone']}\n    -> {s['action']}")