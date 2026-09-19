"""DEFINITION OF DONE (DOD): gerbang kelulusan tiap sprint.

Sebuah fitur dinyatakan 'selesai' hanya bila seluruh kriteria DoD terpenuhi.
Digabung dengan Sprint Retrospective untuk memperbaiki proses berikutnya.
"""

DOD_CHECKLIST = [
    "Kode ditulis & masuk repositori (code committed)",
    "Unit test / test case lulus",
    "Berjalan di environment staging (bukan cuma lokal)",
    "Tidak ada bug kritis (blocker) tersisa",
    "QA telah melakukan uji fungsional & menyetujui",
    "Dokumentasi API / user manual diperbarui",
]


def evaluate_dod(completed: set, sprint_no):
    missing = [c for c in DOD_CHECKLIST if c not in completed]
    done = len(completed) >= len(DOD_CHECKLIST)
    return {
        "sprint": sprint_no,
        "done": done,
        "passed": sorted(completed),
        "missing": missing,
        "verdict": "RELEASE READY" if done else "BELUM SIAP - lengkapi DoD",
    }


def retro(survey):
    """Sprint retrospective sederhana dari umpan balik tim."""
    ok = len([s for s in survey if s >= 7]) / len(survey) if survey else 0
    return {"kepuasan_tim_pct": round(ok * 100), "note":
            "Teruskan yang berjalan baik; perbaiki proses sprint berikutnya."}


if __name__ == "__main__":
    print("=== DEFINITION OF DONE ===")
    partial = {"Kode ditulis & masuk repositori (code committed)",
               "Unit test / test case lulus"}
    full = set(DOD_CHECKLIST)
    print("Sprint 1 (fitur reservasi):", evaluate_dod(partial, 1)["verdict"])
    print("   missing:", evaluate_dod(partial, 1)["missing"])
    print("Sprint 2 (fitur pembayaran):", evaluate_dod(full, 2)["verdict"])
    print()
    print("Sprint Retrospective (skor tim 1-10):", retro([7, 8, 7, 9]))