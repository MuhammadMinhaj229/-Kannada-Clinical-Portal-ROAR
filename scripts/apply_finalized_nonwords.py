import csv
from pathlib import Path
from collections import Counter

REPO = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
FINAL_CSV = REPO / "scripts" / "finalized_nonwords_270.csv"
REAL_CSV = REPO / "realwords.csv"

# 1. Load 270 real words
real_words = []
real_set = set()
with open(REAL_CSV, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        w = r["word"].strip()
        real_set.add(w)
        real_words.append({
            "word": w,
            "pos": r["POS"].strip().lower(),
            "syllables": r.get("syllables", "2").strip(),
            "meaning": r.get("meaning", "").strip(),
            "age_band": r.get("Age band", "").strip(),
        })

print(f"Real words loaded: {len(real_words)} (unique: {len(real_set)})")

# 2. Load 270 finalized non-words from Non-Word edited(final)
nonwords = []
nw_set = set()
collisions = []
duplicates = []
edited_count = 0
method_counts = Counter()
pos_counts = Counter()

with open(FINAL_CSV, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        nid = r["Nonword ID"].strip()
        nw = r["Non-Word edited(final)"].strip()
        method = r["Transformation Method"].strip()
        sw1 = r["Source Word 1"].strip()
        sw2 = r["Source Word 2"].strip()
        if sw2 == "—":
            sw2 = ""
        pos = r["Source POS"].strip().lower()
        trans = r["Transformation Details"].strip()
        sw1_syl = r["Source Word 1 Syllables"].strip()
        sw2_syl = r["Source Word 2 Syllables"].strip()
        if sw2_syl == "—":
            sw2_syl = ""
        nw_syl = r["Non word Syllables edited"].strip()
        is_edited = r["edited"].strip().lower() == "true"

        if is_edited:
            edited_count += 1
        if nw in real_set:
            collisions.append((nid, nw))
        if nw in nw_set:
            duplicates.append((nid, nw))
        nw_set.add(nw)
        method_counts[method] += 1
        pos_counts[pos] += 1

        nonwords.append({
            "id": nid,
            "nonword": nw,
            "source_word": sw1,
            "source_word_2": sw2,
            "source_pos": pos,
            "rule_logic": method,
            "method": method,
            "transformation": trans,
            "syllables": nw_syl,
            "source_word_1_syllables": sw1_syl,
            "source_word_2_syllables": sw2_syl,
            "realpseudo": "pseudo"
        })

print(f"Finalized non-words loaded: {len(nonwords)} (unique: {len(nw_set)}, edited: {edited_count})")
print(f"Collisions with real words: {collisions}")
print(f"Duplicate non-words: {duplicates}")
print(f"Methods: {dict(method_counts)}")
print(f"POS: {dict(pos_counts)}")

assert len(nonwords) == 270, f"Expected 270 nonwords, got {len(nonwords)}"
assert len(real_words) == 270, f"Expected 270 real words, got {len(real_words)}"

# 3. Overwrite nonwords_generated.csv & public/nonwords_generated.csv
nw_fields = [
    "id", "nonword", "source_word", "source_word_2", "source_pos", "rule_logic",
    "method", "transformation", "syllables", "source_word_1_syllables",
    "source_word_2_syllables", "realpseudo"
]
for out_nw in [REPO / "nonwords_generated.csv", REPO / "public" / "nonwords_generated.csv"]:
    with open(out_nw, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=nw_fields)
        w.writeheader()
        w.writerows(nonwords)
    print(f"Wrote {out_nw}")

# 4. Overwrite master_corpus_540.csv & public/master_corpus_540.csv
master_rows = []
for rw in real_words:
    master_rows.append({
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
for nw in nonwords:
    master_rows.append({
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

master_fields = [
    "word", "realpseudo", "pos", "rule_logic", "source_word", "source_word_2",
    "transformation", "syllables", "source_word_1_syllables",
    "source_word_2_syllables", "meaning", "age_band"
]
for out_m in [REPO / "master_corpus_540.csv", REPO / "public" / "master_corpus_540.csv"]:
    with open(out_m, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=master_fields)
        w.writeheader()
        w.writerows(master_rows)
    print(f"Wrote {out_m}")
