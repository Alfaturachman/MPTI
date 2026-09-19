"""RACI MATRIX: Responsible - Accountable - Consulted - Informed.

Memetakan peran per aktivitas dan memvalidasi agar setiap aktivitas punya
tepat satu Accountable dan minimal satu Responsible.
"""

ROLES = ["PM", "Backend", "Frontend", "UI/UX", "QA"]

MATRIX = {
    "Sprint Planning":      {"PM": "A", "Backend": "R", "Frontend": "R",
                             "UI/UX": "C", "QA": "C"},
    "Desain UI/UX":         {"PM": "C", "UI/UX": "R", "Frontend": "I",
                             "Backend": "I", "QA": "I"},
    "Pengembangan API":     {"PM": "C", "Backend": "R", "QA": "I",
                             "Frontend": "C", "UI/UX": "I"},
    "Pengembangan UI":      {"PM": "C", "Frontend": "R", "Backend": "C",
                             "UI/UX": "C", "QA": "I"},
    "Pengujian & UAT":      {"PM": "A", "QA": "R", "Backend": "C",
                             "Frontend": "C", "UI/UX": "C"},
    "Go-Live & Handover":   {"PM": "A/R", "Backend": "R", "Frontend": "R",
                             "UI/UX": "C", "QA": "C"},
}


def validate(mx):
    issues = []
    for activity, mapping in mx.items():
        if list(mapping.values()).count("A") != 1 and "A/R" not in mapping.values():
            issues.append(f"{activity}: Accountable tidak tepat satu.")
        if "R" not in mapping.values():
            issues.append(f"{activity}: tidak ada Responsible.")
    return issues or ["VALID - setiap aktivitas punya 1 A dan >= 1 R."]


if __name__ == "__main__":
    print("=== RACI MATRIX ===")
    header = "Aktivitas".ljust(22) + "".join(r.ljust(10) for r in ROLES)
    print(header)
    for activity, mapping in MATRIX.items():
        cells = "".join(mapping.get(r, "-").ljust(10) for r in ROLES)
        print(f"{activity:<22}{cells}")
    print()
    print("Validasi:", validate(MATRIX))
    print("R = eksekutor | A = penanggung jawab | C = konsultasi | I = info")