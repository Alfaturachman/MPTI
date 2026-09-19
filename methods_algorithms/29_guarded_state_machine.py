"""STATE MACHINE FORMAL DENGAN GUARD.

Transisi status unit/akun/transaksi diformalkan dengan guard condition.
Contoh: unit TIDAK boleh berubah Dipesan -> Disewa sebelum pembayaran lunas
DAN kontrak digital sudah ditandatangani.
"""

TRANSACTION_STATES = {"Menunggu Bayar", "Terkonfirmasi", "Disewa",
                      "Selesai", "Dibatalkan"}

EXPECTED_TRANSITION = {
    ("Menunggu Bayar", "Terkonfirmasi"): lambda ctx: ctx["pay_success"],
    ("Terkonfirmasi", "Disewa"): lambda ctx: ctx["kontrak_signed"],
    ("Disewa", "Selesai"): lambda ctx: ctx["unit_dikembalikan"],
    ("Menunggu Bayar", "Dibatalkan"): lambda ctx: ctx.get("expired", False),
}


def guarded_transition(state, target, context):
    if target not in TRANSACTION_STATES:
        raise ValueError(f"Status tujuan tidak dikenal: {target}")
    guard = EXPECTED_TRANSITION.get((state, target))
    if guard is None:
        raise ValueError(f"Transisi ilegal {state} -> {target}")
    ok = guard(context)
    if not ok:
        raise ValueError(f"Guard ditolak: {state} -> {target} "
                         f"(syarat belum terpenuhi: {_describe((state, target))})")
    return target


def _describe(edge):
    return {
        ("Menunggu Bayar", "Terkonfirmasi"): "pembayaran lunas",
        ("Terkonfirmasi", "Disewa"): "kontrak digital ditandatangani",
        ("Disewa", "Selesai"): "unit dikembalikan & lolos inspeksi",
    }.get(edge, "-")


if __name__ == "__main__":
    print("=== STATE MACHINE FORMAL (GUARDED) ===")
    trx = {"id": "RSV-009", "state": "Menunggu Bayar", "pay_success": True,
           "kontrak_signed": False, "unit_dikembalikan": False}

    try:
        guarded_transition(trx["state"], "Terkonfirmasi", trx)
        trx["state"] = "Terkonfirmasi"
        print("1) -> Terkonfirmasi (pembayaran lunas)")
    except ValueError as e:
        print("1) DITOLAK:", e)

    try:
        guarded_transition(trx["state"], "Disewa", trx)  # kontrak belum tanda tangan
    except ValueError as e:
        print("2) DITOLAK:", e)  # guard kontrak_signed == False

    trx["kontrak_signed"] = True
    trx["state"] = guarded_transition(trx["state"], "Disewa", trx)
    print("3) -> Disewa (kontrak sudah ditandatangani)")