"""IMMUTABLE DATA & SOFT-DELETE.

Data transaksi lunas bersifat permanen (immutable). Penghapusan hanya dilakukan
secara soft-delete dengan pencatatan alasan audit - tidak ada hard-delete
terhadap data transaksi.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TransactionRecord:
    id: int
    amount: int
    status: str
    deleted: bool = False
    delete_reason: str = ""


@dataclass
class TransactionStore:
    records: list = field(default_factory=list)
    audit_trail: list = field(default_factory=list)
    _id_counter: int = 0

    def create(self, amount, status):
        self._id_counter += 1
        rec = TransactionRecord(self._id_counter, amount, status)
        self.records.append(rec)
        return rec

    def soft_delete(self, rec_id, reason, actor):
        rec = self._by_id(rec_id)
        if rec.status == "Lunas":
            raise ValueError("Transaksi lunas BERSIFAT PERMANEN - tidak boleh dihapus.")
        rec.deleted = True
        rec.delete_reason = reason
        self.audit_trail.append({
            "action": "soft_delete",
            "record_id": rec_id,
            "reason": reason,
            "actor": actor,
            "at": datetime.now(),
        })

    def visible(self):
        return [r for r in self.records if not r.deleted]

    def _by_id(self, rec_id):
        return next(r for r in self.records if r.id == rec_id)


if __name__ == "__main__":
    print("=== IMMUTABLE DATA & SOFT-DELETE ===")
    store = TransactionStore()
    t1 = store.create(150_000, "Lunas")
    t2 = store.create(50_000, "Belum Dibayar")
    print("Data aktif:", [(r.id, r.amount, r.status) for r in store.visible()])

    print("Coba hapus transaksi lunas -> ditolak:")
    try:
        store.soft_delete(t1.id, "kesalahan input", "kasir")
    except ValueError as e:
        print("  DITOLAK:", e)

    store.soft_delete(t2.id, "faktur ganda", "kasir")
    print("Soft-delete faktur belum dibayar (id 2), alasan tercatat:")
    print("  Audit trail:", store.audit_trail[-1]["reason"], "oleh", store.audit_trail[-1]["actor"])
    print("  Data aktif setelahnya:", [(r.id, r.amount) for r in store.visible()])