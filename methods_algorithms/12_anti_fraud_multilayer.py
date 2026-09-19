"""ANTI-FRAUD MULTI-LAYER.

Lapisan pemeriksaan untuk mencegah KTP palsu, identitas curian, pembayaran
dari pihak ketiga, dan unit ditukar saat pengembalian:
1. NFC chip test (e-KTP asli wajib merespons chip)
2. UV inspection (hologram + serat mikro)
3. Liveness detection (swafoto + gerakan acak)
4. 1-to-1 match rekening (nama rekening = nama KTP / KK)
5. Multi-document rule (minimal 1 dokumen pembanding)
6. Anti-switching (cocok IMEI saat pengembalian)
"""

MIN_DOCUMENTS = 2


class AntiFraudEngine:
    def __init__(self):
        self.checks = {}

    def run_check(self, name, passed, note=""):
        self.checks[name] = {"passed": passed, "note": note}

    def evaluate(self, nfc_ok=False, uv_ok=False, liveness_ok=False,
                 account_name_match=False, document_count=0,
                 imei_match=False):
        self.run_check("NFC chip", nfc_ok)
        self.run_check("UV hologram", uv_ok)
        self.run_check("Liveness detection", liveness_ok)
        self.run_check("1-to-1 match rekening", account_name_match)
        self.run_check(f"Multi-document (>= {MIN_DOCUMENTS})",
                       document_count >= MIN_DOCUMENTS, f"{document_count} dokumen")
        self.run_check("Anti-switching IMEI", imei_match)
        return all(c["passed"] for c in self.checks.values())

    def report(self):
        for name, c in self.checks.items():
            mark = "PASS" if c["passed"] else "FAIL"
            print(f"  [{mark}] {name:<28} {c['note']}")


if __name__ == "__main__":
    print("=== ANTI-FRAUD MULTI-LAYER ===")
    print("Skenario 1 - KTP asli, rekening sesuai:")
    af = AntiFraudEngine()
    ok = af.evaluate(nfc_ok=True, uv_ok=True, liveness_ok=True,
                     account_name_match=True, document_count=2, imei_match=True)
    af.report()
    print("  HASIL:", "DITERIMA" if ok else "DITOLAK")
    print()
    print("Skenario 2 - KTP palsu (tidak ada chip NFC):")
    af = AntiFraudEngine()
    ok = af.evaluate(nfc_ok=False, uv_ok=False, liveness_ok=True,
                     account_name_match=True, document_count=1, imei_match=True)
    af.report()
    print("  HASIL:", "DITERIMA" if ok else "DITOLAK")