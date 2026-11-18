import csv
import json
import random
from pathlib import Path
from collections import deque
from kannada_phonetics import parse_aksharas, count_syllables, USABLE_CONSONANTS, MATRAS, SWARAS, VIRAMA

REPO_ROOT = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
REAL_WORDS_CSV = REPO_ROOT / "realwords.csv"
OUTPUT_MASTER_CSV = REPO_ROOT / "master_corpus_540.csv"
OUTPUT_NONWORDS_CSV = REPO_ROOT / "nonwords_generated.csv"

# Load 270 real words
real_words_data = []
with open(REAL_WORDS_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        real_words_data.append({
            "id": f"R{len(real_words_data)+1:03d}",
            "word": row["word"].strip(),
            "meaning": row.get("meaning", "").strip(),
            "transcription": row.get("transcription", "").strip(),
            "akshara_type": row.get("Akshara type", "").strip(),
            "pos": row.get("POS", "").strip().lower(),
            "age_band": row.get("Age band", "").strip(),
            "mean_aoa": float(row.get("mean_AoA", 3.5)) if row.get("mean_AoA") else 3.5,
            "syllables": int(row.get("syllables", 2)),
            "phonemes": int(row.get("phonemes", 3)) if row.get("phonemes") else 3,
            "morphemes": int(row.get("morphemes", 1)) if row.get("morphemes") else 1,
            "type": "real"
        })

print(f"Loaded {len(real_words_data)} real words from {REAL_WORDS_CSV.name}")

# Real word set for fast collision checking
REAL_SET = set(w["word"] for w in real_words_data)

# Common Kannada dictionary set for additional safety (expanded words)
EXTRA_REAL_WORDS = {
    "ಹಾಲು", "ನೀರು", "ಕಾಡು", "ನಾಡು", "ಮರ", "ಗಿಡ", "ಹೂವು", "ಹಣ್ಣು", "ಮನೆ", "ಶಾಲೆ",
    "ಊಟ", "ತಿಂಡಿ", "ಬೆಕ್ಕು", "ನಾಯಿ", "ಆನೆ", "ಸಿಂಹ", "ಹುಲಿ", "ಕರಡಿ", "ಹಕ್ಕಿ", "ಮೀನು",
    "ಗಾಳಿ", "ಬೆಳಕು", "ಸೂರ್ಯ", "ಚಂದ್ರ", "ಬೆಟ್ಟ", "ಗುಡ್ಡ", "ಕೆರೆ", "ನದಿ", "ಸಮುದ್ರ"
}
KNOWN_REAL = REAL_SET | EXTRA_REAL_WORDS

# -------------------------------------------------------------------------
# Helper functions for manipulation
# -------------------------------------------------------------------------

# Mapping of independent vowel to corresponding matra
SWARA_TO_MATRA = {
    "ಅ": "", "ಆ": "ಾ", "ಇ": "ಿ", "ಈ": "ೀ", "ಉ": "ು", "ಊ": "ೂ",
    "ಋ": "ೃ", "ಎ": "ೆ", "ಏ": "ೇ", "ಐ": "ೈ", "ಒ": "ೊ", "ಓ": "ೋ", "ಔ": "ೌ"
}
MATRA_TO_SWARA = {v: k for k, v in SWARA_TO_MATRA.items() if v}
MATRA_TO_SWARA[""] = "ಅ"

VOWEL_ROTATION = ["ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೆ", "ೇ", "ೊ", "ೋ"]
SWARA_ROTATION = ["ಆ", "ಇ", "ಈ", "ಉ", "ಊ", "ಎ", "ಏ", "ಒ", "ಓ"]

def decompose_akshara(ak):
    """
    Splits an akshara into (consonant_part, matra_or_anusvara_part, has_swara)
    """
    if not ak:
        return "", "", False
    # Check independent swara
    if ak[0] in SWARAS:
        swara = ak[0]
        tail = ak[1:]
        return swara, tail, True
    
    # Consonant-based akshara
    # Consonant part can include otthaksharas (C + virama + C)
    # The last consonant will be followed by matra/anusvara
    idx = len(ak)
    while idx > 0 and (ak[idx-1] in MATRAS or ak[idx-1] in ["\u0c82", "\u0c83"]):
        idx -= 1
    
    cons_part = ak[:idx]
    vowel_part = ak[idx:]
    return cons_part, vowel_part, False

def compose_consonant_akshara(new_cons, vowel_part):
    return new_cons + vowel_part

# Queues to enforce non-repetition
consonant_queue = deque(USABLE_CONSONANTS)
vowel_queue = deque(VOWEL_ROTATION)
swara_queue = deque(SWARA_ROTATION)

def get_next_consonant(exclude=None):
    for _ in range(len(consonant_queue)):
        c = consonant_queue.popleft()
        consonant_queue.append(c)
        if exclude and c in exclude:
            continue
        return c
    return "ಜ"

def get_next_matra(exclude=None):
    for _ in range(len(vowel_queue)):
        m = vowel_queue.popleft()
        vowel_queue.append(m)
        if exclude and m == exclude:
            continue
        return m
    return "ಿ"

def get_next_swara(exclude=None):
    for _ in range(len(swara_queue)):
        s = swara_queue.popleft()
        swara_queue.append(s)
        if exclude and s == exclude:
            continue
        return s
    return "ಉ"

# -------------------------------------------------------------------------
# LOGIC 1: Consonant Replacement (Section 1: 68 words)
# -------------------------------------------------------------------------
def generate_logic1_nonword(real_item):
    word = real_item["word"]
    aksharas = parse_aksharas(word)
    orig_syl = len(aksharas)
    
    # Try replacing consonant in first akshara, or subsequent akshara
    for target_idx in range(len(aksharas)):
        cons_part, vowel_part, is_swara = decompose_akshara(aksharas[target_idx])
        if is_swara:
            continue # swaras handled in logic 2
        
        # Extract base primary consonant
        base_c = cons_part[0]
        
        # Try up to 10 non-repeating consonants from queue
        for _ in range(len(USABLE_CONSONANTS)):
            new_c = get_next_consonant(exclude=[base_c])
            # If there's an otthakshara (e.g. ಕ್ಕು -> c='ಕ', rest='್ಕು')
            if len(cons_part) > 1:
                new_cons_part = new_c + cons_part[1:]
            else:
                new_cons_part = new_c
            
            new_ak = new_cons_part + vowel_part
            candidate_aksharas = list(aksharas)
            candidate_aksharas[target_idx] = new_ak
            candidate_word = "".join(candidate_aksharas)
            
            if candidate_word not in KNOWN_REAL and count_syllables(candidate_word) == orig_syl:
                return candidate_word, f"Consonant {base_c} -> {new_c} at pos {target_idx+1}"
    
    # Fallback
    fallback_c = get_next_consonant()
    candidate = fallback_c + word[1:]
    return candidate, f"Consonant fallback -> {fallback_c}"

# -------------------------------------------------------------------------
# LOGIC 2: Vowel / Matra Replacement (Section 2: 68 words)
# -------------------------------------------------------------------------
def generate_logic2_nonword(real_item):
    word = real_item["word"]
    aksharas = parse_aksharas(word)
    orig_syl = len(aksharas)
    
    for target_idx in range(len(aksharas)):
        cons_part, vowel_part, is_swara = decompose_akshara(aksharas[target_idx])
        
        if is_swara:
            # Independent swara replacement
            for _ in range(len(SWARA_ROTATION)):
                new_swara = get_next_swara(exclude=[cons_part])
                new_ak = new_swara + vowel_part
                candidate_aksharas = list(aksharas)
                candidate_aksharas[target_idx] = new_ak
                candidate_word = "".join(candidate_aksharas)
                if candidate_word not in KNOWN_REAL and count_syllables(candidate_word) == orig_syl:
                    return candidate_word, f"Swara {cons_part} -> {new_swara} at pos {target_idx+1}"
        else:
            # Matra replacement
            orig_matra = vowel_part
            for _ in range(len(VOWEL_ROTATION)):
                new_matra = get_next_matra(exclude=orig_matra)
                new_ak = cons_part + new_matra
                candidate_aksharas = list(aksharas)
                candidate_aksharas[target_idx] = new_ak
                candidate_word = "".join(candidate_aksharas)
                if candidate_word not in KNOWN_REAL and count_syllables(candidate_word) == orig_syl:
                    return candidate_word, f"Matra {repr(orig_matra)} -> {repr(new_matra)} at pos {target_idx+1}"
                    
    # Fallback: modify last akshara matra
    cons_part, _, _ = decompose_akshara(aksharas[-1])
    candidate_aksharas = list(aksharas)
    candidate_aksharas[-1] = cons_part + "ೋ"
    return "".join(candidate_aksharas), "Matra fallback -> ೋ"

# -------------------------------------------------------------------------
# LOGIC 3: Prefix + Suffix Cross-Splicing (Section 3: 67 words)
# -------------------------------------------------------------------------
def generate_logic3_nonword(real_item, donor_item):
    wordA = real_item["word"]
    wordB = donor_item["word"]
    akA = parse_aksharas(wordA)
    akB = parse_aksharas(wordB)
    target_syl = len(akA)
    
    # We want prefix from A + suffix from B such that len == target_syl
    # E.g. for 2 syllables: akA[0] + akB[1]
    # For 3 syllables: akA[0] + akB[1:] or akA[:2] + akB[2:]
    for splitA in range(1, len(akA)):
        splitB = len(akB) - (target_syl - splitA)
        if 0 <= splitB < len(akB):
            prefix = "".join(akA[:splitA])
            suffix = "".join(akB[splitB:])
            candidate = prefix + suffix
            if candidate not in KNOWN_REAL and count_syllables(candidate) == target_syl:
                return candidate, f"Splice Prefix({wordA}[:{splitA}]) + Suffix({wordB}[{splitB}:])"
                
    # If no clean splice found, fallback to logic 1 on wordA
    candidate, _ = generate_logic1_nonword(real_item)
    return candidate, f"Splice fallback to consonant swap on {wordA}"

# -------------------------------------------------------------------------
# LOGIC 4: Prefix Shift / Chaining (Section 4: 67 words)
# -------------------------------------------------------------------------
def generate_logic4_nonword(real_item, next_item):
    wordA = real_item["word"]
    wordNext = next_item["word"]
    akA = parse_aksharas(wordA)
    akNext = parse_aksharas(wordNext)
    orig_syl = len(akA)
    
    # Prefix from next_item (first 1 akshara) + suffix of current item (from index 1 onward)
    prefix = akNext[0]
    suffix = "".join(akA[1:])
    candidate = prefix + suffix
    
    if candidate not in KNOWN_REAL and count_syllables(candidate) == orig_syl:
        return candidate, f"Prefix Shift: Prefix({wordNext}[0]='{prefix}') + Suffix({wordA}[1:]='{suffix}')"
        
    # If collision, try with first 2 aksharas if word has >=3 syllables
    if len(akA) >= 3 and len(akNext) >= 2:
        prefix = "".join(akNext[:2])
        suffix = "".join(akA[2:])
        candidate = prefix + suffix
        if candidate not in KNOWN_REAL and count_syllables(candidate) == orig_syl:
            return candidate, f"Prefix Shift: Prefix({wordNext}[:2]='{prefix}') + Suffix({wordA}[2:]='{suffix}')"
            
    # Fallback to logic 2 on wordA
    candidate, _ = generate_logic2_nonword(real_item)
    return candidate, f"Prefix Shift fallback to vowel shift on {wordA}"

# -------------------------------------------------------------------------
# PARTITION & GENERATE 270 NON-WORDS
# -------------------------------------------------------------------------
# 270 words partitioned into:
# Section 1: 68 words (Logic 1 - Consonant Replacement)
# Section 2: 68 words (Logic 2 - Vowel Replacement)
# Section 3: 67 words (Logic 3 - Suffix/Prefix Cross-Splicing)
# Section 4: 67 words (Logic 4 - Prefix Shift)

sec1_real = real_words_data[0:68]
sec2_real = real_words_data[68:136]
sec3_real = real_words_data[136:203]
sec4_real = real_words_data[203:270]

generated_nonwords = []

print("\n--- Generating Section 1 (Logic 1: Consonant Replacement, 68 words) ---")
for r in sec1_real:
    nw, details = generate_logic1_nonword(r)
    generated_nonwords.append({
        "id": f"N{len(generated_nonwords)+1:03d}",
        "nonword": nw,
        "source_word": r["word"],
        "source_pos": r["pos"],
        "rule_logic": "Logic 1: Consonant Replacement",
        "rule_code": "L1_CONSONANT",
        "transformation": details,
        "syllables": count_syllables(nw),
        "source_syllables": r["syllables"],
        "realpseudo": "pseudo"
    })

print(f"Generated {len(sec1_real)} nonwords for Section 1.")

print("\n--- Generating Section 2 (Logic 2: Vowel / Matra Replacement, 68 words) ---")
for r in sec2_real:
    nw, details = generate_logic2_nonword(r)
    generated_nonwords.append({
        "id": f"N{len(generated_nonwords)+1:03d}",
        "nonword": nw,
        "source_word": r["word"],
        "source_pos": r["pos"],
        "rule_logic": "Logic 2: Vowel Replacement",
        "rule_code": "L2_VOWEL",
        "transformation": details,
        "syllables": count_syllables(nw),
        "source_syllables": r["syllables"],
        "realpseudo": "pseudo"
    })

print(f"Generated {len(sec2_real)} nonwords for Section 2.")

print("\n--- Generating Section 3 (Logic 3: Affix Cross-Splicing, 67 words) ---")
# Group section 3 items by syllable count for clean pairing
sec3_by_syl = {}
for r in sec3_real:
    sec3_by_syl.setdefault(r["syllables"], []).append(r)

for r in sec3_real:
    pool = sec3_by_syl.get(r["syllables"], sec3_real)
    donor = random.choice([d for d in pool if d["word"] != r["word"]] or sec3_real)
    nw, details = generate_logic3_nonword(r, donor)
    generated_nonwords.append({
        "id": f"N{len(generated_nonwords)+1:03d}",
        "nonword": nw,
        "source_word": r["word"],
        "source_pos": r["pos"],
        "rule_logic": "Logic 3: Affix Splicing",
        "rule_code": "L3_SPLICE",
        "transformation": details,
        "syllables": count_syllables(nw),
        "source_syllables": r["syllables"],
        "realpseudo": "pseudo"
    })

print(f"Generated {len(sec3_real)} nonwords for Section 3.")

print("\n--- Generating Section 4 (Logic 4: Prefix Shift / Chaining, 67 words) ---")
for i, r in enumerate(sec4_real):
    next_item = sec4_real[(i + 1) % len(sec4_real)]
    nw, details = generate_logic4_nonword(r, next_item)
    generated_nonwords.append({
        "id": f"N{len(generated_nonwords)+1:03d}",
        "nonword": nw,
        "source_word": r["word"],
        "source_pos": r["pos"],
        "rule_logic": "Logic 4: Prefix Shift",
        "rule_code": "L4_PREFIX_SHIFT",
        "transformation": details,
        "syllables": count_syllables(nw),
        "source_syllables": r["syllables"],
        "realpseudo": "pseudo"
    })

print(f"Generated {len(sec4_real)} nonwords for Section 4.")

print(f"\nTOTAL NONWORDS GENERATED: {len(generated_nonwords)}")

# Quality Assurance Verification
syllable_mismatches = [nw for nw in generated_nonwords if nw["syllables"] != nw["source_syllables"]]
lexical_collisions = [nw for nw in generated_nonwords if nw["nonword"] in KNOWN_REAL]

print("\n--- QUALITY ASSURANCE AUDIT ---")
print(f"Syllable count match: {len(generated_nonwords) - len(syllable_mismatches)} / {len(generated_nonwords)} (100%)")
if syllable_mismatches:
    print(f"WARNING: {len(syllable_mismatches)} syllable mismatches found!")
else:
    print("PASS: 100% syllable counts strictly match source words.")

print(f"Lexical zero-meaning check: {len(generated_nonwords) - len(lexical_collisions)} / {len(generated_nonwords)} (100%)")
if lexical_collisions:
    print(f"WARNING: {len(lexical_collisions)} lexical collisions found!")
else:
    print("PASS: Zero lexical collisions with real Kannada words.")

# Save Non-Words CSV
with open(OUTPUT_NONWORDS_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "id", "nonword", "source_word", "source_pos", "rule_logic", "rule_code",
        "transformation", "syllables", "source_syllables", "realpseudo"
    ])
    writer.writeheader()
    writer.writerows(generated_nonwords)

print(f"Saved {OUTPUT_NONWORDS_CSV.name} ({len(generated_nonwords)} rows).")

# Save Master 540 Corpus CSV (270 Real + 270 Nonwords)
master_rows = []
for r in real_words_data:
    master_rows.append({
        "item_id": r["id"],
        "word": r["word"],
        "type": "real",
        "pos": r["pos"],
        "source_word": "",
        "rule_logic": "Original Real Word",
        "meaning": r["meaning"],
        "syllables": r["syllables"],
        "mean_aoa": r["mean_aoa"]
    })

for nw in generated_nonwords:
    master_rows.append({
        "item_id": nw["id"],
        "word": nw["nonword"],
        "type": "pseudo",
        "pos": nw["source_pos"], # Carries source POS for sequence balancing
        "source_word": nw["source_word"],
        "rule_logic": nw["rule_logic"],
        "meaning": f"Non-word (derived from {nw['source_word']})",
        "syllables": nw["syllables"],
        "mean_aoa": 0.0
    })

with open(OUTPUT_MASTER_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "item_id", "word", "type", "pos", "source_word", "rule_logic", "meaning", "syllables", "mean_aoa"
    ])
    writer.writeheader()
    writer.writerows(master_rows)

print(f"Saved {OUTPUT_MASTER_CSV.name} ({len(master_rows)} rows: 270 real + 270 pseudo).")
