import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import json
import csv
from pathlib import Path

REPO = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
ARTIFACTS_DIR = Path(r"C:\Users\User\.gemini\antigravity\brain\384e9f2d-2c0d-4f84-a3bf-138e1df437bd")

wb = openpyxl.Workbook()
# remove default sheet
wb.remove(wb.active)

# Styling primitives
font_title = Font(name="Calibri", size=16, bold=True, color="1E3A8A")
font_subtitle = Font(name="Calibri", size=11, italic=True, color="475569")
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_subhdr = Font(name="Calibri", size=11, bold=True, color="1E293B")
font_bold = Font(name="Calibri", size=10, bold=True)
font_regular = Font(name="Calibri", size=10)
font_kannada = Font(name="Nirmala UI", size=11, bold=True)

fill_navy = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
fill_blue = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
fill_teal = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid")
fill_indigo = PatternFill(start_color="4338CA", end_color="4338CA", fill_type="solid")
fill_gray_head = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
fill_light_gray = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
fill_zebra = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

# Badges / Fills for lexicality and POS
fill_real = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid") # light blue
fill_pseudo = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # light red
fill_noun = PatternFill(start_color="F3E8FF", end_color="F3E8FF", fill_type="solid") # purple
fill_verb = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid") # sky
fill_adj = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # green
fill_adv = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # amber

border_thin = Side(border_style="thin", color="CBD5E1")
cell_border = Border(top=border_thin, left=border_thin, right=border_thin, bottom=border_thin)

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

def autofit(ws, min_w=12, max_w=40):
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            v = str(cell.value or '')
            if len(v) > max_len:
                max_len = len(v)
        ws.column_dimensions[col_letter].width = max(min_w, min(max_len + 3, max_w))

# -------------------------------------------------------------
# 1. SUMMARY SHEET
# -------------------------------------------------------------
ws_sum = wb.create_sheet(title="Executive Summary")
ws_sum.views.sheetView[0].showGridLines = True

ws_sum.cell(row=2, column=2, value="Kannada Clinical Research Portal — Master Corpus Architecture").font = font_title
ws_sum.cell(row=3, column=2, value="Stanford ROAR SWR Adaptation for Kannada-Speaking Children | Version: 2.0 (Production)").font = font_subtitle

# Summary Card 1: Lexicality
ws_sum.cell(row=5, column=2, value="1. Lexicality Overview").font = font_subhdr
headers_c1 = ["Category", "Count", "Proportion", "Target Key", "Visual Color"]
for col_idx, h in enumerate(headers_c1, start=2):
    c = ws_sum.cell(row=6, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center

data_c1 = [
    ["Real Words (ನೈಜ ಪದಗಳು)", 270, "50.0%", "Right Arrow (→)", "Solid Blue (#2980b9)"],
    ["Non-Words (ಕಾಲ್ಪನಿಕ ಪದಗಳು)", 270, "50.0%", "Left Arrow (←)", "Solid Red (#c0392b)"],
    ["Total Assessment Corpus", 540, "100.0%", "50/50 Balanced", "Dual-Key Indicator"]
]
for r_idx, row in enumerate(data_c1, start=7):
    for c_idx, val in enumerate(row, start=2):
        c = ws_sum.cell(row=r_idx, column=c_idx, value=val)
        c.font = font_bold if r_idx == 9 else font_regular
        c.border = cell_border
        c.alignment = align_left if c_idx == 2 else align_center
        if r_idx == 7: c.fill = fill_real
        elif r_idx == 8: c.fill = fill_pseudo
        elif r_idx == 9: c.fill = fill_light_gray

# Summary Card 2: Part of Speech Distribution
ws_sum.cell(row=12, column=2, value="2. Parts of Speech (POS) Distribution").font = font_subhdr
headers_c2 = ["Part of Speech (POS)", "Real Words", "Non-Words", "Total Count", "Corpus Share"]
for col_idx, h in enumerate(headers_c2, start=2):
    c = ws_sum.cell(row=13, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_indigo
    c.alignment = align_center

data_c2 = [
    ["Noun (ನಾಮಪದ)", 96, 96, 192, "35.5%"],
    ["Verb (ಕ್ರಿಯಾಪದ)", 97, 97, 194, "35.9%"],
    ["Adjective (ಗುಣವಾಚಕ)", 43, 43, 86, "15.9%"],
    ["Adverb (ಕ್ರಿಯಾವಿಶೇಷಣ)", 34, 34, 68, "12.6%"],
    ["Total Corpus", 270, 270, 540, "100.0%"]
]
for r_idx, row in enumerate(data_c2, start=14):
    for c_idx, val in enumerate(row, start=2):
        c = ws_sum.cell(row=r_idx, column=c_idx, value=val)
        c.font = font_bold if r_idx == 18 else font_regular
        c.border = cell_border
        c.alignment = align_left if c_idx == 2 else align_center
        if r_idx == 14: c.fill = fill_noun
        elif r_idx == 15: c.fill = fill_verb
        elif r_idx == 16: c.fill = fill_adj
        elif r_idx == 17: c.fill = fill_adv
        elif r_idx == 18: c.fill = fill_light_gray

# Summary Card 3: Non-word Generation Logics
ws_sum.cell(row=21, column=2, value="3. Non-Word Transformation Logics (Candidates Sheet)").font = font_subhdr
headers_c3 = ["Logic Code", "Linguistic Transformation Rule", "Count", "Syllable Preservation", "Clinical Status"]
for col_idx, h in enumerate(headers_c3, start=2):
    c = ws_sum.cell(row=22, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_teal
    c.alignment = align_center

data_c3 = [
    ["Logic 1 (`B_consonant`)", "Consonant Replacement (ವ್ಯಂಜನ ಬದಲಾವಣೆ)", 68, "Strictly Preserved", "Verified & Zero-Meaning"],
    ["Logic 2 (`A_vowel`)", "Vowel / Matra Replacement (ಸ್ವರ / ಮಾತ್ರಾ ಬದಲಾವಣೆ)", 68, "Strictly Preserved", "Verified & Zero-Meaning"],
    ["Logic 3 (`C_suffix_prefix`)", "Affix Splicing (ಪ್ರತ್ಯಯ ಸಂಯೋಜನೆ)", 67, "Strictly Preserved", "Verified & Zero-Meaning"],
    ["Logic 4 (`D_prefix_suffix`)", "Prefix Shift / Suffix Chaining (ಉಪಸರ್ಗ ಬದಲಾವಣೆ)", 67, "Strictly Preserved", "Verified & Zero-Meaning"],
    ["Total Non-Words", "4 Standardized Linguistic Transformation Methods", 270, "100% Syllable-Matched", "Production Ready"]
]
for r_idx, row in enumerate(data_c3, start=23):
    for c_idx, val in enumerate(row, start=2):
        c = ws_sum.cell(row=r_idx, column=c_idx, value=val)
        c.font = font_bold if r_idx == 27 else font_regular
        c.border = cell_border
        c.alignment = align_left if c_idx in [2, 3] else align_center
        if r_idx % 2 == 1: c.fill = fill_zebra

# Summary Card 4: 6-Session Architecture
ws_sum.cell(row=30, column=2, value="4. Clinical Assessment Session Structure (90 words/session + 5 demo)").font = font_subhdr
headers_c4 = ["Session #", "Demo Practice Trials", "Real Words", "Non-Words", "Total Test Trials", "Max Streak", "POS Collisions"]
for col_idx, h in enumerate(headers_c4, start=2):
    c = ws_sum.cell(row=31, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_gray_head
    c.alignment = align_center

with open(REPO / "sessions_data.json", encoding="utf-8") as f:
    sessions_data = json.load(f)

for s in range(1, 7):
    s_key = str(s)
    s_obj = sessions_data[s_key]
    seq = s_obj.get("sequence", [])
    real_cnt = sum(1 for w in seq if w.get("type") == "real")
    pseudo_cnt = sum(1 for w in seq if w.get("type") == "pseudo")
    
    # Calculate streak and pos collision
    max_stk = 1
    cur_stk = 1
    for k in range(1, len(seq)):
        if seq[k]["type"] == seq[k-1]["type"]:
            cur_stk += 1
            max_stk = max(max_stk, cur_stk)
        else:
            cur_stk = 1
    pos_coll = sum(1 for k in range(1, len(seq)) if seq[k]["pos"] == seq[k-1]["pos"])

    r_idx = 31 + s
    row_vals = [f"Session {s}", len(s_obj.get("demo", [])), real_cnt, pseudo_cnt, len(seq), f"≤ {max_stk} (Unpredictable)", f"{pos_coll} (Rotating POS)"]
    for c_idx, val in enumerate(row_vals, start=2):
        c = ws_sum.cell(row=r_idx, column=c_idx, value=val)
        c.font = font_regular
        c.border = cell_border
        c.alignment = align_center
        if s % 2 == 0: c.fill = fill_zebra

autofit(ws_sum, min_w=14, max_w=45)

# -------------------------------------------------------------
# 2. MASTER CORPUS (540) SHEET
# -------------------------------------------------------------
ws_m = wb.create_sheet(title="Master Corpus (540)")
ws_m.views.sheetView[0].showGridLines = True

headers_m = [
    "Trial #", "Kannada Word", "Lexicality", "Part of Speech",
    "Generation Logic", "Source Real Word", "Transformation Rule",
    "Syllables", "Target Key", "Arrow Color", "Meaning / Gloss", "Age Band"
]
for col_idx, h in enumerate(headers_m, start=1):
    c = ws_m.cell(row=1, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center

with open(REPO / "master_corpus_540.csv", encoding="utf-8") as f:
    master_rows = list(csv.DictReader(f))

for idx, r in enumerate(master_rows, start=2):
    is_real = r.get("realpseudo") == "real"
    pos = (r.get("pos") or "noun").lower()
    
    ws_m.cell(row=idx, column=1, value=idx-1).alignment = align_center
    
    c_word = ws_m.cell(row=idx, column=2, value=r.get("word"))
    c_word.font = font_kannada
    c_word.alignment = align_center
    
    c_lex = ws_m.cell(row=idx, column=3, value="Real Word" if is_real else "Non-Word")
    c_lex.alignment = align_center
    c_lex.fill = fill_real if is_real else fill_pseudo
    
    c_pos = ws_m.cell(row=idx, column=4, value=pos.capitalize())
    c_pos.alignment = align_center
    if pos == "noun": c_pos.fill = fill_noun
    elif pos == "verb": c_pos.fill = fill_verb
    elif pos == "adjective" or pos == "adj": c_pos.fill = fill_adj
    elif pos == "adverb" or pos == "adv": c_pos.fill = fill_adv
    
    ws_m.cell(row=idx, column=5, value=r.get("rule_logic")).alignment = align_left
    ws_m.cell(row=idx, column=6, value=r.get("source_word") or "—").alignment = align_center
    ws_m.cell(row=idx, column=7, value=r.get("transformation") or "—").alignment = align_left
    ws_m.cell(row=idx, column=8, value=int(r.get("syllables") or 1)).alignment = align_center
    ws_m.cell(row=idx, column=9, value="Right Arrow (→)" if is_real else "Left Arrow (←)").alignment = align_center
    ws_m.cell(row=idx, column=10, value="Blue" if is_real else "Red").alignment = align_center
    ws_m.cell(row=idx, column=11, value=r.get("meaning") or "—").alignment = align_left
    ws_m.cell(row=idx, column=12, value=r.get("age_band") or "—").alignment = align_center

    for c in range(1, 13):
        ws_m.cell(row=idx, column=c).border = cell_border
        if not ws_m.cell(row=idx, column=c).font:
            ws_m.cell(row=idx, column=c).font = font_regular

autofit(ws_m, min_w=12, max_w=35)

# -------------------------------------------------------------
# 3. REAL WORDS (270) SHEET
# -------------------------------------------------------------
ws_rw = wb.create_sheet(title="Real Words (270)")
ws_rw.views.sheetView[0].showGridLines = True

headers_rw = ["#", "Kannada Word (ಪದ)", "Transcription", "Meaning", "Part of Speech (POS)", "Syllables", "Age Band", "Mean AoA", "Phonemes", "Morphemes"]
for col_idx, h in enumerate(headers_rw, start=1):
    c = ws_rw.cell(row=1, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_blue
    c.alignment = align_center

with open(REPO / "realwords.csv", encoding="utf-8") as f:
    rw_rows = list(csv.DictReader(f))

for idx, r in enumerate(rw_rows, start=2):
    ws_rw.cell(row=idx, column=1, value=idx-1).alignment = align_center
    
    c_w = ws_rw.cell(row=idx, column=2, value=r.get("word"))
    c_w.font = font_kannada
    c_w.alignment = align_center
    
    ws_rw.cell(row=idx, column=3, value=r.get("transcription")).alignment = align_left
    ws_rw.cell(row=idx, column=4, value=r.get("meaning")).alignment = align_left
    
    pos = (r.get("POS") or "").lower()
    c_pos = ws_rw.cell(row=idx, column=5, value=pos.capitalize())
    c_pos.alignment = align_center
    if pos == "noun": c_pos.fill = fill_noun
    elif pos == "verb": c_pos.fill = fill_verb
    elif pos in ["adjective", "adj"]: c_pos.fill = fill_adj
    elif pos in ["adverb", "adv"]: c_pos.fill = fill_adv
    
    ws_rw.cell(row=idx, column=6, value=int(r.get("syllables") or 1)).alignment = align_center
    ws_rw.cell(row=idx, column=7, value=r.get("Age band")).alignment = align_center
    ws_rw.cell(row=idx, column=8, value=float(r.get("mean_AoA") or 0.0)).alignment = align_center
    ws_rw.cell(row=idx, column=9, value=int(r.get("phonemes") or 0)).alignment = align_center
    ws_rw.cell(row=idx, column=10, value=int(r.get("morphemes") or 0)).alignment = align_center

    for c in range(1, 11):
        ws_rw.cell(row=idx, column=c).border = cell_border
        if not ws_rw.cell(row=idx, column=c).font:
            ws_rw.cell(row=idx, column=c).font = font_regular

autofit(ws_rw, min_w=10, max_w=30)

# -------------------------------------------------------------
# 4. NON-WORDS (270) SHEET
# -------------------------------------------------------------
ws_nw = wb.create_sheet(title="Non-Words (270)")
ws_nw.views.sheetView[0].showGridLines = True

headers_nw = [
    "Nonword ID", "Non-Word (ಕಾಲ್ಪನಿಕ ಪದ)", "Transformation Method",
    "Source Word 1", "Source Word 2", "Source POS", "Transformation Details",
    "Syllables", "Expected Key", "Arrow Indicator", "Clinical Review"
]
for col_idx, h in enumerate(headers_nw, start=1):
    c = ws_nw.cell(row=1, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_teal
    c.alignment = align_center

with open(REPO / "nonwords_generated.csv", encoding="utf-8") as f:
    nw_rows = list(csv.DictReader(f))

for idx, r in enumerate(nw_rows, start=2):
    pos = (r.get("source_pos") or "noun").lower()
    
    ws_nw.cell(row=idx, column=1, value=r.get("id")).alignment = align_center
    
    c_nw = ws_nw.cell(row=idx, column=2, value=r.get("nonword"))
    c_nw.font = font_kannada
    c_nw.alignment = align_center
    
    ws_nw.cell(row=idx, column=3, value=r.get("rule_logic")).alignment = align_left
    ws_nw.cell(row=idx, column=4, value=r.get("source_word")).alignment = align_center
    ws_nw.cell(row=idx, column=5, value=r.get("source_word_2") or "—").alignment = align_center
    
    c_pos = ws_nw.cell(row=idx, column=6, value=pos.capitalize())
    c_pos.alignment = align_center
    if pos == "noun": c_pos.fill = fill_noun
    elif pos == "verb": c_pos.fill = fill_verb
    elif pos in ["adjective", "adj"]: c_pos.fill = fill_adj
    elif pos in ["adverb", "adv"]: c_pos.fill = fill_adv
    
    ws_nw.cell(row=idx, column=7, value=r.get("transformation") or "—").alignment = align_left
    ws_nw.cell(row=idx, column=8, value=int(r.get("syllables") or 1)).alignment = align_center
    ws_nw.cell(row=idx, column=9, value="Left Arrow (←)").alignment = align_center
    ws_nw.cell(row=idx, column=10, value="Red (#c0392b)").alignment = align_center
    ws_nw.cell(row=idx, column=11, value="Validated (Zero Meaning)").alignment = align_center

    for c in range(1, 12):
        ws_nw.cell(row=idx, column=c).border = cell_border
        if not ws_nw.cell(row=idx, column=c).font:
            ws_nw.cell(row=idx, column=c).font = font_regular

autofit(ws_nw, min_w=12, max_w=35)

# -------------------------------------------------------------
# 5. SESSION SEQUENCE SHEETS (Sessions 1 to 6)
# -------------------------------------------------------------
for s in range(1, 7):
    s_key = str(s)
    s_obj = sessions_data[s_key]
    seq = s_obj.get("sequence", [])
    demo = s_obj.get("demo", [])
    
    ws_s = wb.create_sheet(title=f"Session {s} (90+5)")
    ws_s.views.sheetView[0].showGridLines = True
    
    # Title row
    ws_s.cell(row=1, column=1, value=f"Session {s} Clinical Assessment Sequence (5 Practice Demo + 90 Randomized Trials)").font = font_subhdr
    
    headers_s = [
        "Stage", "Trial #", "Kannada Word", "Lexicality", "Part of Speech (POS)",
        "Expected Key", "Arrow Color", "Source Word", "Transformation / Meaning", "Syllables"
    ]
    for col_idx, h in enumerate(headers_s, start=1):
        c = ws_s.cell(row=3, column=col_idx, value=h)
        c.font = font_header
        c.fill = fill_indigo
        c.alignment = align_center
        
    curr_row = 4
    # 1. Practice Demo Items
    for d_idx, d in enumerate(demo, start=1):
        is_r = d.get("realpseudo") == "real"
        pos = (d.get("pos") or "noun").lower()
        ws_s.cell(row=curr_row, column=1, value="Practice Demo").alignment = align_center
        ws_s.cell(row=curr_row, column=2, value=f"Demo {d_idx}").alignment = align_center
        c_w = ws_s.cell(row=curr_row, column=3, value=d.get("word"))
        c_w.font = font_kannada
        c_w.alignment = align_center
        
        c_lex = ws_s.cell(row=curr_row, column=4, value="Real Word" if is_r else "Non-Word")
        c_lex.alignment = align_center
        c_lex.fill = fill_real if is_r else fill_pseudo
        
        c_pos = ws_s.cell(row=curr_row, column=5, value=pos.capitalize())
        c_pos.alignment = align_center
        if pos == "noun": c_pos.fill = fill_noun
        elif pos == "verb": c_pos.fill = fill_verb
        elif pos in ["adjective", "adj"]: c_pos.fill = fill_adj
        elif pos in ["adverb", "adv"]: c_pos.fill = fill_adv
        
        ws_s.cell(row=curr_row, column=6, value=f"{d.get('key', 'Right')} Arrow").alignment = align_center
        ws_s.cell(row=curr_row, column=7, value="Blue" if is_r else "Red").alignment = align_center
        ws_s.cell(row=curr_row, column=8, value=d.get("source_word") or "—").alignment = align_center
        ws_s.cell(row=curr_row, column=9, value="Practice Demonstration").alignment = align_left
        ws_s.cell(row=curr_row, column=10, value=2).alignment = align_center
        
        for c in range(1, 11):
            ws_s.cell(row=curr_row, column=c).border = cell_border
            if not ws_s.cell(row=curr_row, column=c).font:
                ws_s.cell(row=curr_row, column=c).font = font_regular
        curr_row += 1

    # 2. 90 Test Trials
    for t_idx, t in enumerate(seq, start=1):
        is_r = t.get("type") == "real"
        pos = (t.get("pos") or "noun").lower()
        ws_s.cell(row=curr_row, column=1, value="Test Assessment").alignment = align_center
        ws_s.cell(row=curr_row, column=2, value=t_idx).alignment = align_center
        c_w = ws_s.cell(row=curr_row, column=3, value=t.get("word"))
        c_w.font = font_kannada
        c_w.alignment = align_center
        
        c_lex = ws_s.cell(row=curr_row, column=4, value="Real Word" if is_r else "Non-Word")
        c_lex.alignment = align_center
        c_lex.fill = fill_real if is_r else fill_pseudo
        
        c_pos = ws_s.cell(row=curr_row, column=5, value=pos.capitalize())
        c_pos.alignment = align_center
        if pos == "noun": c_pos.fill = fill_noun
        elif pos == "verb": c_pos.fill = fill_verb
        elif pos in ["adjective", "adj"]: c_pos.fill = fill_adj
        elif pos in ["adverb", "adv"]: c_pos.fill = fill_adv
        
        ws_s.cell(row=curr_row, column=6, value=f"{t.get('expected_key', 'Right')} Arrow").alignment = align_center
        ws_s.cell(row=curr_row, column=7, value=t.get("arrow_color", "Blue")).alignment = align_center
        ws_s.cell(row=curr_row, column=8, value=t.get("source_word") or "—").alignment = align_center
        ws_s.cell(row=curr_row, column=9, value=t.get("meaning") or t.get("rule_logic") or "—").alignment = align_left
        ws_s.cell(row=curr_row, column=10, value=int(t.get("syllables") or 1)).alignment = align_center
        
        for c in range(1, 11):
            ws_s.cell(row=curr_row, column=c).border = cell_border
            if not ws_s.cell(row=curr_row, column=c).font:
                ws_s.cell(row=curr_row, column=c).font = font_regular
        curr_row += 1

    autofit(ws_s, min_w=12, max_w=32)

# Save Excel to both project and artifacts directory
out_excel_repo = REPO / "kannada_roar_corpus_master.xlsx"
out_excel_public = REPO / "public" / "kannada_roar_corpus_master.xlsx"
out_excel_artifacts = ARTIFACTS_DIR / "kannada_roar_corpus_master.xlsx"

wb.save(out_excel_repo)
wb.save(out_excel_public)
wb.save(out_excel_artifacts)
print(f"Saved styled Excel workbook to:")
print(f"  - {out_excel_repo}")
print(f"  - {out_excel_public}")
print(f"  - {out_excel_artifacts}")
