"""RPO / RTO: target cadangan & pemulihan database.

- RPO (Recovery Point Objective): seberapa banyak data yang boleh hilang.
- RTO (Recovery Time Objective): seberapa cepat sistem harus pulih.
Melengkapi konfigurasi auto-backup harian pada server produksi.
"""

BACKUP_INTERVAL_HOURS = 24      # auto-backup setiap 24 jam
RTO_TARGET_HOURS = 6            # target pemulihan
RPO_TARGET_HOURS = 24


def backup_compliance(last_backup_hours_ago, restore_duration_hours):
    data_loss = min(last_backup_hours_ago, RPO_TARGET_HOURS * 2)
    rpo_ok = last_backup_hours_ago <= RPO_TARGET_HOURS
    rto_ok = restore_duration_hours <= RTO_TARGET_HOURS
    return {
        "last_backup": last_backup_hours_ago,
        "maks_data_hilang": data_loss,
        "rpo_ok": rpo_ok,
        "recovery_time": restore_duration_hours,
        "rto_ok": rto_ok,
        "status": "COMPLIANT" if (rpo_ok and rto_ok) else "PERLU PERBAIKAN",
    }


if __name__ == "__main__":
    print("=== RPO / RTO BACKUP & RECOVERY ===")
    print("Target: RPO <= 24 jam | RTO <= 6 jam")
    print()
    skenario = {
        "Backup 6 jam lalu, restore 2 jam": (6, 2),
        "Backup 30 jam lalu (skip), restore 10 jam": (30, 10),
    }
    for label, (h_backup, h_restore) in skenario.items():
        s = backup_compliance(h_backup, h_restore)
        print(f"{label} -> {s['status']} (data hilang max {s['maks_data_hilang']} jam, "
              f"recovery {s['recovery_time']} jam)")