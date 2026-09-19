"""FORMULA GANTI RUGI TOTAL LOSS / PENGGELAPAN.

Rumus:
  Biaya Penggantian = Nilai Pasar Wajar Unit Sejenis + Disrupsi Operasional (10%)
Tenggat penyelesaian maksimal 3x24 jam sebelum dilimpahkan ke jalur hukum.
"""

DISRUPTION_PCT = 0.10
SETTLEMENT_DEADLINE_DAYS = 3
WEEK = 7 * 24


def total_loss_claim(market_value):
    disruption = market_value * DISRUPTION_PCT
    return {
        "nilai_pasar": market_value,
        "disrupsi_operasional": disruption,
        "total_ganti_rugi": market_value + disruption,
        "tenggat_pelunasan": f"{SETTLEMENT_DEADLINE_DAYS} x 24 jam",
    }


def settle_or_escalate(claim, paid_hours):
    if paid_hours <= SETTLEMENT_DEADLINE_DAYS * 24:
        return "Diselesaikan oleh penyewa (damai)."
    return "Dilimpahkan ke jalur hukum (dokumen jaminan sebagai alat bukti)."


if __name__ == "__main__":
    print("=== GANTI RUGI TOTAL LOSS ===")
    claim = total_loss_claim(market_value=14_500_000)
    for k, v in claim.items():
        print(f"  {k:<22}: {v}")
    print()
    print("Bayar di hari ke-2 (48 jam):", settle_or_escalate(claim, 48))
    print("Bayar di hari ke-5 (120 jam):", settle_or_escalate(claim, 120))