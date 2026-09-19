import os
import sys
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import (
    WD_TABLE_ALIGNMENT,
    WD_CELL_VERTICAL_ALIGNMENT,
    WD_ROW_HEIGHT_RULE,
)
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


# ----------------------------------------------------------------------------
# DATA TIMELINE (7 peran x 6 fase, tiap fase = 2 minggu)
# ----------------------------------------------------------------------------
ROLES = {
    "PROJECT MANAGER\n(PM)": [
        "F1  Inisiasi, Desain & Arsitektur",
        "F2  Sprint 1 - Master Data & Reservasi",
        "F3  Sprint 2 - Transaksi & Anti-Fraud",
        "F4  Sprint 3 - Denda & Data Wiping",
        "F5  Buffer 1 - UAT & Bugfix",
        "F6  Buffer 2 - Deployment & Handover",
    ],
    "BACKEND\nSENIOR": [
        "F1  ERD, Skema DB & API Boilerplate",
        "F2  CRUD Master & Anti-Collision",
        "F3  Payment Gateway & Engine PDF",
        "F4  Check-in, Denda & Data Wiping",
        "F5  Bug Fix & Optimasi Query",
        "F6  Konfigurasi Server Produksi",
    ],
    "BACKEND\nJUNIOR": [
        "F1  Setup Environment & Repo",
        "F2  Endpoint Penyewa & CRUD Dasar",
        "F3  Scheduler Denda & Auto-Cancel",
        "F4  Katalog Kerusakan & API Laporan",
        "F5  Dukungan Bug Fix",
        "F6  Verifikasi Staging ke Produksi",
    ],
    "FRONTEND\nSENIOR": [
        "F1  Repo, Design Tokens & Komponen Dasar",
        "F2  Katalog Publik & Ketersediaan RT",
        "F3  Kasir POS & Kamera Foto 4 Sisi",
        "F4  Inspeksi Pengembalian & Pelaporan",
        "F5  Optimasi Caching & Kecepatan",
        "F6  Final Build di CDN/Produksi",
    ],
    "FRONTEND\nJUNIOR": [
        "F1  Boilerplate & CSS Framework",
        "F2  Formulir Pemesanan & Validasi Form",
        "F3  Scan NFC & UI Form BAST",
        "F4  Checklist Sanitasi & Revisi UI",
        "F5  Perbaikan Bug UI Lintas Device",
        "F6  Verifikasi Kamera Device Gerai",
    ],
    "UI/UX\nDESIGNER": [
        "F1  Riset, Wireframe & Prototipe Figma",
        "F2  Design System & Aset Modul Reservasi",
        "F3  Template Kontrak & BAST Digital",
        "F4  Finalisasi Aset UI & Panduan Desain",
        "F5  Revisi Visual Hasil UAT",
        "F6  User Guide & Visual Pelatihan",
    ],
    "QA TESTER": [
        "F1  Kerangka Master Test Plan",
        "F2  Test Case & Uji Modul Master",
        "F3  Uji Responsivitas & Anti-Fraud",
        "F4  End-to-End Testing & Bug Log",
        "F5  Regression Testing & Berita UAT",
        "F6  UAT Final & Verifikasi Data Produksi",
    ],
}

TOTAL_WEEKS = 12
WEEKS_PER_PHASE = 2

# [Nama Fase, Warna Bar]
PHASES = [
    ("FASE 1\nInisiasi & Arsitektur", "C5E0B4"),
    ("FASE 2\nSprint 1: Master Data", "FFE699"),
    ("FASE 3\nSprint 2: Transaksi", "F8CBAD"),
    ("FASE 4\nSprint 3: Denda & Wiping", "D9E1F2"),
    ("FASE 5\nBuffer 1: UAT & Bugfix", "E2EFDA"),
    ("FASE 6\nBuffer 2: Deploy & Handover", "D9D9D9"),
]

# Milestone: minggu -> keterangan
MILESTONES = {
    8: "★ CODE FREEZE",
    9: "★ UAT",
    12: "★ GO-LIVE",
}


# ----------------------------------------------------------------------------
# HELPER
# ----------------------------------------------------------------------------
def shade(cell, fill):
    """Memberi warna latar pada sel."""
    if fill:
        tc_pr = cell._tc.get_or_add_tcPr()
        s = OxmlElement("w:shd")
        s.set(qn("w:fill"), fill)
        tc_pr.append(s)


def styled(cell, text, size=6.5, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER):
    """Isi sel + pengaturan font & alignment, sekaligus hapus isi lama."""
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    return cell


def set_cell_margins(table, left=0.02, right=0.02, top=0.0, bottom=0.0):
    """Perkecil jarak tepi dalam sel agar teks tidak boros baris."""
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for tag, val in (("w:top", top), ("w:left", left),
                     ("w:bottom", bottom), ("w:right", right)):
        el = OxmlElement(tag)
        el.set(qn("w:w"), str(int(val * 1440)))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tbl_pr.append(mar)


# ----------------------------------------------------------------------------
# DOKUMEN
# ----------------------------------------------------------------------------
doc = Document()
section = doc.sections[0]
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width, section.page_height = section.page_height, section.page_width
section.top_margin = Inches(0.3)
section.bottom_margin = Inches(0.3)
section.left_margin = Inches(0.35)
section.right_margin = Inches(0.35)

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(2)
r = title.add_run("GANTT CHART TIMELINE PROYEK NORIZ")
r.bold = True
r.font.size = Pt(12)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.paragraph_format.space_after = Pt(4)
r = subtitle.add_run("12 Minggu (M1 - M12)  |  Target Internal M1-M8  +  Buffer PM M9-M12")
r.font.size = Pt(8)

n_cols = 3 + TOTAL_WEEKS
table = doc.add_table(rows=0, cols=n_cols)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.style = "Table Grid"
table.autofit = False
table.allow_autofit = False
set_cell_margins(table)

# --- Baris banner: nama fase membentang 2 kolom minggu ---
banner = table.add_row().cells
for i in range(n_cols):
    styled(banner[i], "", size=5.5)
for ph, (name, color) in enumerate(PHASES):
    col_a = 3 + ph * WEEKS_PER_PHASE
    merged = banner[col_a].merge(banner[col_a + 1])
    styled(merged, name, size=5.5, bold=True)
    shade(merged, color)
merged = banner[0].merge(banner[2])
styled(merged, "TAHAPAN PROYEK", size=6.0, bold=True)
shade(merged, "B4C6E7")

# --- Baris header kolom ---
hdr = table.add_row().cells
for i, h in enumerate(["No.", "Peran / Tim", "Aktivitas"] + [f"M{n}" for n in range(1, TOTAL_WEEKS + 1)]):
    styled(hdr[i], h, size=6.0, bold=True)
    shade(hdr[i], "D9EAF7")

# --- Baris data per peran ---
row_num = 1
first_data_row = 2
for role, activities in ROLES.items():
    for phase_idx, activity in enumerate(activities):
        row = table.add_row().cells
        styled(row[0], str(row_num), size=6.0)
        start = phase_idx * WEEKS_PER_PHASE + 1
        end = start + 1
        styled(row[2], f"{activity}   [M{start}-M{end}]", size=6.0,
               align=WD_ALIGN_PARAGRAPH.LEFT)
        for m in range(1, TOTAL_WEEKS + 1):
            styled(row[2 + m], "", size=6.0)
            if start <= m <= end:
                shade(row[2 + m], PHASES[phase_idx][1])
        row_num += 1

# --- Gabungkan sel "Peran" setiap 6 baris per peran ---
role_start = first_data_row
for role in ROLES:
    r_len = len(ROLES[role])
    top = table.cell(role_start, 1)
    bottom = table.cell(role_start + r_len - 1, 1)
    merged = top.merge(bottom)
    styled(merged, role, size=6.0, bold=True)
    shade(merged, "F2F2F2")
    role_start += r_len

# --- Baris milestone ---
ms = table.add_row().cells
ms_cell = ms[0].merge(ms[1]).merge(ms[2])
tokens = "    ".join(f"★ M{m} {label}" for m, label in sorted(MILESTONES.items()))
styled(ms_cell, "MILESTONE UTAMA:  " + tokens, size=5.5, align=WD_ALIGN_PARAGRAPH.LEFT)
shade(ms_cell, "FFF2CC")
for m in MILESTONES:
    col = 3 + m - 1
    styled(ms[col], "★", size=6.5, bold=True)
    shade(ms[col], "FFD966")
for i in range(3, n_cols):
    if i not in (3 + m - 1 for m in MILESTONES):
        styled(ms[i], "", size=6.0)

# --- Lebar kolom (total ~11.0 inci = lebar isi halaman landscape A4) ---
widths = [0.25, 1.0, 3.0] + [0.5625] * TOTAL_WEEKS
for row in table.rows:
    for idx, w in enumerate(widths):
        row.cells[idx].width = Inches(w)

# --- Paksa tinggi baris agar muat dalam 1 halaman ---
def row_height(ridx):
    if ridx == 0:
        return 0.17
    if ridx == 1:
        return 0.16
    if ridx == len(table.rows) - 1:
        return 0.20
    return 0.135

for ridx, row in enumerate(table.rows):
    row.height = Inches(row_height(ridx))
    row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

# --- Legenda fase (tabel mini dengan warna) ---
legend_p = doc.add_paragraph()
legend_p.paragraph_format.space_before = Pt(4)
legend_p.paragraph_format.space_after = Pt(1)
r = legend_p.add_run("Legenda Fase:  ")
r.bold = True
r.font.size = Pt(7)

legend_table = doc.add_table(rows=1, cols=len(PHASES))
legend_table.style = "Table Grid"
legend_table.alignment = WD_TABLE_ALIGNMENT.CENTER
legend_table.autofit = False
set_cell_margins(legend_table)
for i, (name, color) in enumerate(PHASES):
    c = legend_table.rows[0].cells[i]
    styled(c, f"{i + 1}. {name.replace(chr(10), ' ')}", size=5.5, bold=True)
    shade(c, color)
    c.width = Inches(1.86)
legend_table.rows[0].height = Inches(0.14)
legend_table.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

# --- Catatan kaki ---
note = doc.add_paragraph()
note.paragraph_format.space_before = Pt(3)
note.paragraph_format.space_after = Pt(0)
r = note.add_run("Keterangan: ")
r.bold = True
r.font.size = Pt(7)
r = note.add_run(
    "Sel berwarna = periode pelaksanaan aktivitas. M1-M12 = 12 minggu proyek. "
    "Fase 1-4 (M1-M8) = target internal & code freeze, Fase 5-6 (M9-M12) = buffer PM "
    "(UAT, bugfix, deployment, Go-Live). Simbol ★ = milestone utama."
)
r.font.size = Pt(7)

# --- Lokasi simpan (bisa via argumen baris perintah) ---
if len(sys.argv) > 1:
    out_path = sys.argv[1]
else:
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "Gantt_Chart_NORIZ_User_Friendly.docx")

doc.save(out_path)
print("SAVED:", out_path)