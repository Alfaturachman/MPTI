"""CPM (CRITICAL PATH METHOD): mencari jalur kritis proyek.

Jalur kritis = rangkaian aktivitas terpanjang tanpa slack; keterlambatan pada
jalur ini menunda tanggal Go-Live, sehingga harus dikawal ketat PM.
"""

ACTIVITIES = {
    "A: Inisiasi & Desain": (2, []),
    "B: Sprint 1 Master Data": (2, ["A: Inisiasi & Desain"]),
    "C: Sprint 2 Transaksi": (2, ["B: Sprint 1 Master Data"]),
    "D: Sprint 3 Denda & Wiping": (2, ["C: Sprint 2 Transaksi"]),
    "E: UAT & Bugfix": (2, ["D: Sprint 3 Denda & Wiping"]),
    "F: Deploy & Handover": (2, ["E: UAT & Bugfix"]),
}


def critical_path(tasks):
    order = []
    while len(order) < len(tasks):
        for name, (dur, deps) in tasks.items():
            if name not in order and all(d in order for d in deps):
                order.append(name)

    es, ef = {}, {}
    for name in order:
        dur, deps = tasks[name]
        start = max([ef[d] for d in deps], default=0)
        es[name], ef[name] = start, start + dur

    project_duration = max(ef.values())
    ls, lf = {}, {}
    for name in reversed(order):
        dur, deps = tasks[name]
        finish = min([ls[d] for d in order if name in tasks[d][1]], default=project_duration)
        lf[name], ls[name] = finish, finish - dur

    slack = {name: ls[name] - es[name] for name in order}
    critical = [name for name in order if slack[name] == 0]
    return es, ef, ls, lf, slack, critical, project_duration


if __name__ == "__main__":
    print("=== CPM - CRITICAL PATH METHOD ===")
    es, ef, ls, lf, slack, critical, duration = critical_path(ACTIVITIES)
    print(f"Durasi proyek minimum: {duration} minggu")
    print("Aktivitas / ES / EF / LS / LF / Slack:")
    for name in ACTIVITIES:
        mark = " *" if slack[name] == 0 else ""
        print(f"  {name:<28} ES={es[name]} EF={ef[name]} LS={ls[name]} LF={lf[name]} "
              f"Slack={slack[name]}{mark}")
    print()
    print("JALUR KRITIS:", " -> ".join(critical))
    print("=> Aktivitas ini TIDAK BOLEH telat agar Go-Live aman.")