"""CONTINGENCY FUND (~4%): dana cadangan untuk biaya tak terduga.
Sisa yang tidak terpakai bisa dialihkan menjadi laba tambahan PM.
"""

from dataclasses import dataclass, field

CONTINGENCY_PCT = 0.04


@dataclass
class ContingencyFund:
    total_budget: int
    reserve_used: int = 0
    unexpected_costs: list = field(default_factory=list)

    @property
    def allocation(self):
        return round(self.total_budget * CONTINGENCY_PCT)

    def use(self, amount, reason):
        if amount > self.remaining:
            raise ValueError("Dana cadangan tidak cukup!")
        self.reserve_used += amount
        self.unexpected_costs.append((amount, reason))

    @property
    def remaining(self):
        return self.allocation - self.reserve_used

    def summary(self, planned_profit):
        leftover = self.remaining
        return {
            "alokasi_cadangan": self.allocation,
            "terpakai": self.reserve_used,
            "sisa": leftover,
            "profit_dasar_pm": planned_profit,
            "profit_maksimal_pm": planned_profit + leftover,
            "catatan": "Sisa dana menjadi laba tambahan PM bila tidak terpakai.",
        }


if __name__ == "__main__":
    print("=== CONTINGENCY FUND (~4%) ===")
    fund = ContingencyFund(total_budget=120_000_000)
    print("Alokasi cadangan:", fund.allocation, "Rupiah")
    fund.use(800_000, "Server butuh tambahan storage")
    fund.use(1_200_000, "Biaya sertifikasi unexpected")
    print(fund.summary(planned_profit=48_000_000))