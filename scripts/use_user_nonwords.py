import openpyxl
import csv
import json
from pathlib import Path

XLSM = Path(r"C:\Users\User\.gemini\antigravity\brain\384e9f2d-2c0d-4f84-a3bf-138e1df437bd\.user_uploaded\media_1794754075883_6d51365a.xlsm")
REPO = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
REAL_CSV = REPO / "realwords.csv"

# 1. Load real words and their metadata
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
            "transformation": ""
        }
        real_words_list.append(real_words_map[w])

print(f"Loaded {len(real_words_list)} real words.")

# 2. Load user's 270 non-words from Candidates sheet
wb = openpyxl.load_workbook(XLSM, data_only=True)
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
    transformation = str(vals[7] or '').strip()

    source_info = real_words_map.get(source_word_1, {})
    source_pos = source_info.get("pos", "noun")
    syllables = source_info.get("syllables", "1")

    item = {
        "id": nonword_id,
        "nonword": nonword,
        "source_word": source_word_1,
        "source_pos": source_pos,
        "rule_logic": METHOD_MAP.get(method, method),
        "method": method,
        "transformation": transformation,
        "syllables": syllables,
        "realpseudo": "pseudo"
    }
    nonwords_list.append(item)

print(f"Loaded {len(nonwords_list)} non-words from XLSM.")

# 3. Write nonwords_generated.csv
out_nonwords = REPO / "nonwords_generated.csv"
with open(out_nonwords, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "id", "nonword", "source_word", "source_pos", "rule_logic", "method", "transformation", "syllables", "realpseudo"
    ])
    writer.writeheader()
    writer.writerows(nonwords_list)
print(f"Saved {len(nonwords_list)} nonwords to {out_nonwords}")

# 4. Write master_corpus_540.csv
master_540 = []
# Interleave or append: 270 real + 270 pseudo
for rw in real_words_list:
    master_540.append({
        "word": rw["word"],
        "realpseudo": "real",
        "pos": rw["pos"],
        "rule_logic": "Original Real Word",
        "source_word": "",
        "transformation": "",
        "syllables": rw["syllables"],
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
        "transformation": nw["transformation"],
        "syllables": nw["syllables"],
        "meaning": "",
        "age_band": ""
    })

out_master = REPO / "master_corpus_540.csv"
with open(out_master, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "word", "realpseudo", "pos", "rule_logic", "source_word", "transformation", "syllables", "meaning", "age_band"
    ])
    writer.writeheader()
    writer.writerows(master_540)
print(f"Saved {len(master_540)} items to {out_master}")
