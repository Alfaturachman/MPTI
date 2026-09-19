"""LEAN AGILE TEAM + SPRINT: penjadwalan 3 sprint, estimasi story point,
kapasitas tim, dan proyeksi velocity untuk tahu kapan scope selesai.
"""

from dataclasses import dataclass, field

TEAM_DAILY_HOURS = 6 * 4  # 4 developer x 6 jam/hari


@dataclass
class Sprint:
    number: int
    weeks: int
    committed_points: int
    completed_points: int


@dataclass
class VelocityModel:
    sprints: list = field(default_factory=list)

    @property
    def velocity(self):
        done = [s.completed_points for s in self.sprints]
        return sum(done) / len(done) if done else 0

    def forecast_sprints(self, remaining_points):
        v = self.velocity or 1
        return round(remaining_points / v, 1)


def build_daily_standup_report(blockers=None):
    """Daily standup 15 menit: apa yang selesai / dikerjakan / blocker."""
    return {
        "done_yesterday": blockers.get("done", []) if blockers else [],
        "doing_today": blockers.get("doing", []) if blockers else [],
        "blockers": blockers.get("blockers", []) if blockers else [],
    }


if __name__ == "__main__":
    print("=== LEAN AGILE TEAM + SPRINT ===")
    model = VelocityModel(sprints=[
        Sprint(1, 2, 40, 38),
        Sprint(2, 2, 42, 40),
        Sprint(3, 2, 44, 44),
    ])
    print(f"Tim: 4 developer (PM memimpin), Daily Standup 15 menit")
    for s in model.sprints:
        print(f"  Sprint {s.number}: commit {s.committed_points}pt -> selesai {s.completed_points}pt")
    print(f"Rata-rata velocity: {model.velocity:.1f} story points / sprint")
    print(f"Sisa scope ~60pt diperkirakan selesai dalam {model.forecast_sprints(60)} sprint")
    print()
    print("Daily standup hari ini:")
    print(" ", build_daily_standup_report({
        "done": ["CRUD Master Unit", "Form reservasi"],
        "doing": ["Anti-collision algorithm", "PDF BAST"],
        "blockers": ["Menunggu approval design system klien"],
    }))