"""STATE MACHINE STATUS UNIT (6 status).

Setiap unit fisik hanya boleh berada pada satu dari 6 status sistematis.
Transisi terdefinisi mencegah operasi ilegal (mis. unit Disewa diubah
langsung menjadi Tersedia tanpa melewati pemeriksaan & reset).
"""

UNIT_STATES = (
    "Tersedia",
    "Dipesan",
    "Disewa",
    "Menunggu Pemeriksaan & Reset",
    "Dalam Perbaikan",
    "Afkir / Hilang",
)

TRANSITIONS = {
    "Tersedia": ("Dipesan",),
    "Dipesan": ("Disewa", "Tersedia"),
    "Disewa": ("Menunggu Pemeriksaan & Reset", "Dalam Perbaikan", "Afkir / Hilang"),
    "Menunggu Pemeriksaan & Reset": ("Tersedia", "Dalam Perbaikan"),
    "Dalam Perbaikan": ("Menunggu Pemeriksaan & Reset", "Afkir / Hilang"),
    "Afkir / Hilang": (),
}


def can_transition(current, target):
    return target in TRANSITIONS.get(current, ())


def transition(unit_code, current, target):
    if not can_transition(current, target):
        raise ValueError(
            f"{unit_code}: tidak valid {current} -> {target}")
    return target


if __name__ == "__main__":
    print("=== STATE MACHINE STATUS UNIT ===")
    u = "IP15P-001"
    flow = ["Tersedia", "Dipesan", "Disewa",
            "Menunggu Pemeriksaan & Reset", "Tersedia"]
    state = flow[0]
    for nxt in flow[1:]:
        try:
            state = transition(u, state, nxt)
            print(f"  {u}: -> {state}")
        except ValueError as e:
            print("  DITOLAK:", e)
            break
    print()
    try:
        transition(u, "Disewa", "Tersedia")  # ilegal: lewati pemeriksaan
    except ValueError as e:
        print("Uji transisi ilegal ->", e)