"""TRIPLE CONSTRAINTS: keseimbangan Scope - Time - Cost.

Setiap perubahan ruang lingkup harus diimbangi waktu dan/atau biaya.
Skrip ini menghitung dampak perubahan fitur terhadap anggaran dan margin PM,
serta menandai apakah proyek masih feasible.
"""

from dataclasses import dataclass, field

BASE_BUDGET = 120_000_000
BASE_SDM = 63_000_000
BASE_OPEX = 9_000_000
BASE_WEEKS = 12


@dataclass
class TripleConstraint:
    scope_points: int = 100
    weeks: float = BASE_WEEKS
    budget: int = BASE_BUDGET
    sdm: int = BASE_SDM
    opex: int = BASE_OPEX
    changes: list = field(default_factory=list)

    @property
    def planned_profit(self):
        return self.budget - self.sdm - self.opex

    def apply_scope_change(self, new_scope_points, added_cost=0, added_weeks=0, note=""):
        """Perubahan scope: apakah perlu tambahan biaya/waktu agar margin tetap sehat."""
        self.scope_points = new_scope_points
        old_scope = self.changes[-1][0] if self.changes else 100
        scope_delta = (new_scope_points - old_scope) / old_scope
        self.budget += added_cost
        self.weeks += added_weeks
        self.changes.append((new_scope_points, added_cost, added_weeks, note))
        required_budget = (self.sdm + self.opex) * (1 + scope_delta)
        feasible = self.budget >= required_budget
        return {
            "scope_delta_pct": round(scope_delta * 100, 1),
            "budget_needed": int(required_budget),
            "budget_actual": self.budget,
            "profit": self.planned_profit,
            "feasible": feasible,
            "recommendation": ("Terima (anggaran cukup)" if feasible
                               else "Tolak/audit: perlu tambahan anggaran ke klien"),
        }


if __name__ == "__main__":
    print("=== TRIPLE CONSTRAINTS (Scope - Time - Cost) ===")
    tc = TripleConstraint()
    print(f"Rencana awal: scope 100pt | {tc.weeks} minggu | budget Rp {tc.budget:,}")
    print(f"Profit PM: Rp {tc.planned_profit:,}")
    print()

    print("Klien minta +10% fitur tanpa tambahan budget:")
    print(" ", tc.apply_scope_change(110, note="+fitur monitoring baru"))
    print()
    print("Klien setuju tambah Rp 15 jt + 2 minggu:")
    print(" ", tc.apply_scope_change(110, added_cost=15_000_000, added_weeks=2,
                                     note="termin tambahan disepakati"))