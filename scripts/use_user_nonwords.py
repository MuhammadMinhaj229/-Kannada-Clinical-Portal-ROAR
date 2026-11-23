import openpyxl
import csv
import sys
from pathlib import Path

REPO = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
sys.path.insert(0, str(REPO / "scripts"))
from kannada_phonetics import count_syllables

XLSM = Path(r"C:\Users\User\.gemini\antigravity\brain\384e9f2d-2c0d-4f84-a3bf-138e1df437bd\.user_uploaded\media_1794754075883_6d51365a.xlsm")
REAL_CSV = REPO / "realwords.csv"

# 1. Load real words and their metadata from realwords.csv
real_words_map = {}
real_words_list = []
with open(REAL_CSV, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        w = r['word'].strip()
        pos = r['POS'].strip().lower()
        real_words_map[w] = {
            "word": w,
            "transcription": r.get('transcription', ''),
            "meaning": r.get('meaning', ''),
            "pos": pos,
            "age_band": r.get('Age band', ''),
            "mean_aoa": r.get('mean_AoA', ''),
            "syllables": r.get('syllables', '1'),
            "realpseudo": "real",
            "rule_logic": "Original Real Word",
            "source_word": "",
            "source_word_2": "",
            "transformation": ""
        }
        real_words_list.append(real_words_map[w])

print(f"Loaded {len(real_words_list)} real words from realwords.csv.")

# 2. Load SourceWords sheet from XLSM for exact syllable counts & POS of all source words
wb = openpyxl.load_workbook(XLSM, data_only=True)
ws_sw = wb['SourceWords']
xlsm_sw_map = {}
for r in range(2, ws_sw.max_row + 1):
    w = str(ws_sw.cell(row=r, column=2).value or '').strip()
    pos = str(ws_sw.cell(row=r, column=5).value or '').strip().lower()
    syl = ws_sw.cell(row=r, column=8).value
    if w:
        xlsm_sw_map[w] = {
            "pos": pos or "noun",
            "syllables": int(syl) if syl is not None else count_syllables(w)
        }

print(f"Loaded {len(xlsm_sw_map)} source words from XLSM SourceWords sheet.")

# 3. Load user's 270 non-words from Candidates sheet
ws = wb['Candidates']

METHOD_MAP = {
    'A_vowel': 'Logic 2: Vowel Replacement',
    'B_consonant': 'Logic 1: Consonant Replacement',
    'C_suffix_prefix': 'Logic 3: Affix Splicing',
    'D_prefix_suffix': 'Logic 4: Prefix Shift'
}

nonwords_list = []
for r in range(2, ws.max_row + 1):
    vals = [ws.cell(row=r, column=c).value for c in range(1, 11)]
    if not vals[0]:
        continue
    nonword_id = str(vals[0]).strip()
    nonword = str(vals[1]).strip()
    method = str(vals[2]).strip()
    source_word_1 = str(vals[3] or '').strip()
    source_word_2 = str(vals[5] or '').strip()
    transformation = str(vals[7] or '').strip()

    sw1_info = xlsm_sw_map.get(source_word_1) or real_words_map.get(source_word_1, {})
    sw2_info = xlsm_sw_map.get(source_word_2) or real_words_map.get(source_word_2, {})

    source_pos = sw1_info.get("pos", "noun")
    sw1_syllables = int(sw1_info.get("syllables") or count_syllables(source_word_1)) if source_word_1 else 0
    sw2_syllables = int(sw2_info.get("syllables") or count_syllables(source_word_2)) if source_word_2 else ""
    nw_syllables = count_syllables(nonword)

    item = {
        "id": nonword_id,
        "nonword": nonword,
        "source_word": source_word_1,
        "source_word_2": source_word_2,
        "source_pos": source_pos,
        "rule_logic": METHOD_MAP.get(method, method),
        "method": method,
        "transformation": transformation,
        "syllables": nw_syllables,
        "source_word_1_syllables": sw1_syllables,
        "source_word_2_syllables": sw2_syllables,
        "realpseudo": "pseudo"
    }
    nonwords_list.append(item)

print(f"Loaded {len(nonwords_list)} non-words from XLSM (with source_word_2 for {sum(1 for x in nonwords_list if x['source_word_2'])} items).")

# 4. Write nonwords_generated.csv
out_nonwords = REPO / "nonwords_generated.csv"
with open(out_nonwords, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "id", "nonword", "source_word", "source_word_2", "source_pos", "rule_logic",
        "method", "transformation", "syllables", "source_word_1_syllables",
        "source_word_2_syllables", "realpseudo"
    ])
    writer.writeheader()
    writer.writerows(nonwords_list)
print(f"Saved {len(nonwords_list)} nonwords to {out_nonwords}")

# 5. Write master_corpus_540.csv
master_540 = []
for rw in real_words_list:
    master_540.append({
        "word": rw["word"],
        "realpseudo": "real",
        "pos": rw["pos"],
        "rule_logic": "Original Real Word",
        "source_word": "",
        "source_word_2": "",
        "transformation": "",
        "syllables": rw["syllables"],
        "source_word_1_syllables": "",
        "source_word_2_syllables": "",
        "meaning": rw["meaning"],
        "age_band": rw["age_band"]
    })

for nw in nonwords_list:
    master_540.append({
        "word": nw["nonword"],
        "realpseudo": "pseudo",
        "pos": nw["source_pos"],
        "rule_logic": nw["rule_logic"],
        "source_word": nw["source_word"],
        "source_word_2": nw["source_word_2"],
        "transformation": nw["transformation"],
        "syllables": nw["syllables"],
        "source_word_1_syllables": nw["source_word_1_syllables"],
        "source_word_2_syllables": nw["source_word_2_syllables"],
        "meaning": "",
        "age_band": ""
    })

out_master = REPO / "master_corpus_540.csv"
with open(out_master, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "word", "realpseudo", "pos", "rule_logic", "source_word", "source_word_2",
        "transformation", "syllables", "source_word_1_syllables",
        "source_word_2_syllables", "meaning", "age_band"
    ])
    writer.writeheader()
    writer.writerows(master_540)
print(f"Saved {len(master_540)} items to {out_master}")
