"""FLEET LOAD-BALANCING (GREEDY).

Saat pelanggan memesan unit, sistem memilih unit tersedia dengan utililasi
terendah (tie-break: battery health tertinggi) agar beban armada merata dan
umur baterai awet.
"""


class Unit:
    def __init__(self, code, battery_health, utilization):
        self.code = code
        self.battery_health = battery_health
        self.utilization = utilization

    def book(self):
        self.utilization += 1


def pick_unit(available_units):
    """Pilih unit secara greedy: utilisasi naik, lalu BH tertinggi."""
    best = min(available_units, key=lambda u: (u.utilization, -u.battery_health))
    return best


if __name__ == "__main__":
    print("=== FLEET LOAD-BALANCING (GREEDY) ===")
    fleet = [
        Unit("IP15P-001", 96, 3),
        Unit("IP15P-002", 92, 3),
        Unit("IP14P-003", 98, 5),
        Unit("IP13-004", 85, 1),
    ]
    picked = pick_unit(fleet)
    print(f"Unit terpilih: {picked.code} (BH {picked.battery_health}%, utilisasi {picked.utilization})")
    picked.book()
    print("Setelah dipesan, utilisasinya ->", picked.utilization)
    print("Berikutnya terpilih lagi:")
    print(" ->", pick_unit(fleet).code)  # beban kini menyebar ke unit lain