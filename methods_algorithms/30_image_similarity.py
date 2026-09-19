"""IMAGE SIMILARITY (SSIM SEDERHANA): komparasi foto baseline vs foto kembali.

Menghitung persentase kemiripan dua foto unit (awal serah terima vs kondisi
saat pengembalian). Kemiripan rendah -> kemungkinan goresan/kerusakan baru,
sehingga otomatis menandai untuk inspeksi petugas.

Implementasi ringan tanpa library: membandingkan piksel jika ukuran sama.
Gunakan Pillow bila tersedia untuk benar-benar membaca file gambar (.jpg/.png).
"""


def mean_abs_difference(px_a, px_b):
    """Rata-rata selisih absolut 3 kanal RGB dua list piksel."""
    n = len(px_a)
    if n == 0:
        return 0.0
    diff = sum(abs(a - b) for pa, pb in zip(px_a, px_b)
               for a, b in zip(pa, pb)) / (n * 3)
    return diff


def similarity_percent(px_a, px_b, threshold=90.0):
    diff = mean_abs_difference(px_a, px_b)
    sim = max(0.0, 100.0 - diff)
    return {
        "similarity_pct": round(sim, 2),
        "scratch_detected": sim < threshold,
        "inspeksi": "WAJIB inspeksi visual petugas" if sim < threshold else "OK - sesuai baseline",
    }


def load_image_pixels(path):
    """Muatan piksel via Pillow (opsional). Jika tidak ada, baca naik."""
    try:
        from PIL import Image
        img = Image.open(path).convert("RGB").resize((200, 150))
        return list(img.getdata())
    except ImportError:
        raise RuntimeError("Pillow tidak terpasang. Gunakan simulasi piksel saja.")


if __name__ == "__main__":
    print("=== IMAGE SIMILARITY (SSIM SEDERHANA) ===")
    # Simulasi piksel: baseline mulus, kembali ada coretan.
    pixel = (200, 210, 220)
    baseline = [pixel] * 1000
    returned = [pixel] * 950 + [(60, 60, 60)] * 50     # 50 piksel menjadi gelap (cacat baru)

    print("Komparasi foto serah terima vs foto kembali:")
    print(" ", similarity_percent(baseline, baseline))  # identik
    print(" ", similarity_percent(baseline, returned))  # ada perbedaan -> deteksi goresan