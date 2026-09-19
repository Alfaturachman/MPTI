"""PEAK / SURGE PRICING.

Multiplikator tarif saat permintaan tinggi (jam ramai, akhir pekan, libur,
event) dan mengarahkan permintaan ke jam longgar via harga lebih rendah.
"""

BASE_DAILY = 120_000

WEEKEND_MULTIPLIER = 1.25
PEAK_HOUR_MULTIPLIER = 1.10
HOLIDAY_MULTIPLIER = 1.40
OFF_PEAK_DISCOUNT = 0.90


def compute_price(day_weekend, hour, is_holiday):
    price = BASE_DAILY
    notes = []
    if day_weekend:
        price *= WEEKEND_MULTIPLIER
        notes.append("akhir pekan +25%")
    if is_holiday:
        price *= HOLIDAY_MULTIPLIER
        notes.append("libur +40%")
    if 18 <= hour <= 23:
        price *= PEAK_HOUR_MULTIPLIER
        notes.append("jam ramai +10%")
    elif hour < 9:
        price *= OFF_PEAK_DISCOUNT
        notes.append("jam longgar -10%")
    return round(price), notes


if __name__ == "__main__":
    print("=== PEAK / SURGE PRICING ===")
    skenario = [
        ("Senin 08:00 (longgar)", 0, 8, False),
        ("Senin 20:00 (jam ramai)", 0, 20, False),
        ("Sabtu 20:00 (weekend + ramai)", 1, 20, False),
        ("Hari libur nasional 15:00", 0, 15, True),
    ]
    for label, weekend, hour, holiday in skenario:
        price, notes = compute_price(weekend, hour, holiday)
        print(f"{label:<28} -> Rp {price:,}  ({', '.join(notes) or 'tarif dasar'})")