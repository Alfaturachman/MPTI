"""FORECAST BATTERY HEALTH (BH%): prediksi degradasi baterai.

Memakai regresi linear sederhana (metode kuadrat terkecil) atas riwayat BH%
mingguan untuk memprediksi kapan unit menyentuh ambang kelaikan 80% sehingga
PM bisa merencanakan pergantian/turun unit lebih dulu.
"""

MIN_FEASIBLE_BH = 80.0


def linear_regression(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / \
        sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    return a, b


def predict_below_threshold(xs, ys, threshold=MIN_FEASIBLE_BH):
    a, b = linear_regression(xs, ys)
    if b >= 0:
        return {"trend": "BH stabil/naik", "crossing_week": None}
    week = (threshold - a) / b
    return {"trend": "menurun", "yearly_losspct_per_int": f"{abs(b):.2f}",
            "perkiraan_minggu_turun_kelak": f"{week:.0f}" if week > max(xs) else "sudah di bawah ambang",
            "rekomendasi": "pertimbangkan pergantian/resesi unit"}


if __name__ == "__main__":
    print("=== FORECAST BATTERY HEALTH (BH%) ===")
    weeks = list(range(1, 11))                          # minggu ke-1 s.d. ke-10
    bh_hist = [99, 98, 97, 96.5, 95, 94, 92.5, 91, 90, 88.5]

    a, b = linear_regression(weeks, bh_hist)
    y10 = a + b * 10
    print(f"Fungsi tren: BH% = {a:.2f} + ({b:.3f} x minggu)")
    print(f"Prediksi BH% minggu ke-12: {a + b * 12:.1f}%")
    print("Prediksi ambang kelaikan 80%:", predict_below_threshold(weeks, bh_hist))