"""MATRIKS RISIKO PROBABILITY-IMPACT: skor risiko = peluang x dampak.

Menentukan tingkat risiko (Low/Medium/High/Critical), mengurutkan prioritas,
dan memasangkan tindakan mitigasi dari PM.
"""

RISK_LEVELS = [
    (20, "Critical"),
    (10, "High"),
    (5, "Medium"),
    (0, "Low"),
]

RISKS = [
    ("Programmer malas/pasif menjelang deadline", 0.5, 9),
    ("Programmer sakit/resign mendadak", 0.25, 10),
    ("Klien scope creep di tengah jalan", 0.7, 6),
    ("UAT menemukan banyak bug di gerai", 0.6, 6),
]

MITIGATIONS = {
    "Programmer malas/pasif menjelang deadline":
        "Daily standup 15 menit, tiket kecil 1-2 hari, intervensi jika macet >= 2 hari",
    "Programmer sakit/resign mendadak":
        "Dokumentasi API rapi (Swagger), buffer 4 minggu sebagai cadangan",
    "Klien scope creep di tengah jalan":
        "Spesifikasi kontrak sebagai pegangan, tambahan dialihkan ke Fase 2",
    "UAT menemukan banyak bug di gerai":
        "Alokasi 2 minggu khusus UAT di buffer PM",
}


def score(probability, impact):
    return probability * impact


def level(s):
    for threshold, name in RISK_LEVELS:
        if s >= threshold:
            return name
    return "?"


if __name__ == "__main__":
    print("=== MATRIKS RISIKO PROBABILITY-IMPACT ===")
    ranked = sorted(
        (score(p, i), risk, p, i) for risk, p, i in RISKS
    )[::-1]
    for s, risk, p, i in ranked:
        print(f"  [{'%02d' % s}] {level(s):<8} P={p:.0%} I={i:<2} | {risk}")
        print(f"        Mitigasi: {MITIGATIONS[risk]}")