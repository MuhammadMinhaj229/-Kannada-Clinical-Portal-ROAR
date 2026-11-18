import csv
import json
import random
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
MASTER_CSV = REPO_ROOT / "master_corpus_540.csv"
SESSIONS_JSON = REPO_ROOT / "sessions_data.json"
OUTPUT_DIR = REPO_ROOT / "session_sequences"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Load Master Corpus (270 real + 270 pseudo)
with open(MASTER_CSV, "r", encoding="utf-8") as f:
    master_items = list(csv.DictReader(f))

real_pool = [w for w in master_items if (w.get("realpseudo") or w.get("type")) == "real"]
pseudo_pool = [w for w in master_items if (w.get("realpseudo") or w.get("type")) == "pseudo"]

print(f"Loaded master corpus: {len(real_pool)} real words, {len(pseudo_pool)} non-words.")

# 2. Practice Demo Items (Preserved)
demo_items = [
    {"order": 1, "word": "ಹೀ",   "realpseudo": "pseudo", "type": "pseudo", "pos": "adverb",    "source_word": "ಹಾಗೆ", "block": "practice", "key": "Left"},
    {"order": 2, "word": "ಹಾಲು", "realpseudo": "real",   "type": "real",   "pos": "noun",      "source_word": "ಹಾಲು", "block": "practice", "key": "Right"},
    {"order": 3, "word": "ನೀರು", "realpseudo": "real",   "type": "real",   "pos": "noun",      "source_word": "ನೀರು", "block": "practice", "key": "Right"},
    {"order": 4, "word": "ಚೃರು", "realpseudo": "pseudo", "type": "pseudo", "pos": "noun",      "source_word": "ಚೂರು", "block": "practice", "key": "Left"},
    {"order": 5, "word": "ಊಡು",  "realpseudo": "pseudo", "type": "pseudo", "pos": "verb",      "source_word": "ಊದು",  "block": "practice", "key": "Left"}
]

# -------------------------------------------------------------------------
# Dual-Constraint Sequence Generator
# -------------------------------------------------------------------------

def generate_unpredictable_type_pattern(n_real=45, n_pseudo=45, max_run=3):
    """
    Generates a list of 'real' and 'pseudo' tokens of total length 90
    satisfying:
    - Exactly n_real and n_pseudo
    - Unpredictable runs (lengths 1, 2, or 3)
    - No runs exceeding max_run
    - Never strict 1-by-1 alternation throughout
    """
    while True:
        pattern = []
        rem_real = n_real
        rem_pseudo = n_pseudo
        last_type = None
        current_streak = 0
        
        while rem_real > 0 or rem_pseudo > 0:
            choices = []
            if rem_real > 0:
                if last_type != "real" or current_streak < max_run:
                    choices.append("real")
            if rem_pseudo > 0:
                if last_type != "pseudo" or current_streak < max_run:
                    choices.append("pseudo")
            
            if not choices:
                break # Backtrack
                
            # Random choice weighted inversely by remaining deficit
            if "real" in choices and "pseudo" in choices:
                # If one pool is running very low, favor the other
                weight_real = rem_real / (rem_real + rem_pseudo)
                chosen = "real" if random.random() < weight_real else "pseudo"
            else:
                chosen = choices[0]
                
            pattern.append(chosen)
            if chosen == "real":
                rem_real -= 1
            else:
                rem_pseudo -= 1
                
            if chosen == last_type:
                current_streak += 1
            else:
                last_type = chosen
                current_streak = 1
                
        if len(pattern) == (n_real + n_pseudo):
            # Check run lengths to verify it is not simple alternating
            run_lengths = []
            cur_r = 1
            for k in range(1, len(pattern)):
                if pattern[k] == pattern[k-1]:
                    cur_r += 1
                else:
                    run_lengths.append(cur_r)
                    cur_r = 1
            run_lengths.append(cur_r)
            
            # Ensure we have a healthy mix of runs of 1, 2, and 3
            if 2 in run_lengths and 3 in run_lengths and max(run_lengths) <= max_run:
                return pattern

def sequence_session_words(real_words_45, pseudo_words_45):
    """
    Sequences 45 real and 45 pseudo words into a 90-word trial stream satisfying:
    1. Unpredictable lexicality pattern (runs of 1 to 3)
    2. Parts of Speech continuity: No two consecutive words have the same POS
       (checking real pos and pseudo source_pos)
    """
    pattern = generate_unpredictable_type_pattern(n_real=45, n_pseudo=45, max_run=3)
    
    # Organize available words by POS
    real_by_pos = defaultdict(list)
    for w in real_words_45:
        real_by_pos[w["pos"]].append(w)
        
    pseudo_by_pos = defaultdict(list)
    for w in pseudo_words_45:
        pseudo_by_pos[w["pos"]].append(w)
        
    for k in real_by_pos:
        random.shuffle(real_by_pos[k])
    for k in pseudo_by_pos:
        random.shuffle(pseudo_by_pos[k])
        
    sequence = []
    last_pos = None
    
    for trial_idx, target_type in enumerate(pattern):
        pool_dict = real_by_pos if target_type == "real" else pseudo_by_pos
        
        # Candidate POS: those that have available words and are NOT last_pos
        available_pos = [p for p, words in pool_dict.items() if len(words) > 0 and p != last_pos]
        
        if not available_pos:
            # If no non-colliding POS available, take any POS with available words
            available_pos = [p for p, words in pool_dict.items() if len(words) > 0]
            
        # Select POS from available, prioritizing the largest remaining pool
        available_pos.sort(key=lambda p: -len(pool_dict[p]))
        chosen_pos = available_pos[0]
        
        chosen_word = pool_dict[chosen_pos].pop()
        last_pos = chosen_pos
        
        item_record = {
            "trial_number": trial_idx + 1,
            "word": chosen_word["word"],
            "type": target_type,
            "realpseudo": target_type,
            "pos": chosen_pos,
            "source_word": chosen_word.get("source_word", chosen_word["word"]),
            "rule_logic": chosen_word.get("rule_logic", "Original Real Word"),
            "syllables": int(chosen_word.get("syllables", 2)),
            "expected_key": "Right" if target_type == "real" else "Left",
            "arrow_color": "Blue" if target_type == "real" else "Red",
            "meaning": chosen_word.get("meaning", "")
        }
        sequence.append(item_record)
        
    return sequence

# -------------------------------------------------------------------------
# PARTITION INTO 6 SESSIONS & EXPORT
# -------------------------------------------------------------------------
sessions_dict = {}

# Partition 270 real words into 6 groups of 45
random.seed(42) # Deterministic base seed for reproducibility
shuffled_real = list(real_pool)
shuffled_pseudo = list(pseudo_pool)
random.shuffle(shuffled_real)
random.shuffle(shuffled_pseudo)

for sess_id in range(1, 7):
    real_slice = shuffled_real[(sess_id - 1) * 45 : sess_id * 45]
    pseudo_slice = shuffled_pseudo[(sess_id - 1) * 45 : sess_id * 45]
    
    seq_90 = sequence_session_words(real_slice, pseudo_slice)
    
    # Check consecutive POS collisions
    pos_collisions = sum(1 for i in range(1, len(seq_90)) if seq_90[i]["pos"] == seq_90[i-1]["pos"])
    
    # Check max streak
    max_streak = 0
    cur_streak = 1
    for i in range(1, len(seq_90)):
        if seq_90[i]["type"] == seq_90[i-1]["type"]:
            cur_streak += 1
            max_streak = max(max_streak, cur_streak)
        else:
            cur_streak = 1
            
    print(f"Session {sess_id}: 90 words generated. Max lexicality streak={max_streak}, POS collisions={pos_collisions}")
    
    # Export individual session CSV
    sess_csv = OUTPUT_DIR / f"session_{sess_id}_sequence_90.csv"
    with open(sess_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "trial_number", "word", "type", "realpseudo", "pos", "source_word", "rule_logic",
            "syllables", "expected_key", "arrow_color", "meaning"
        ])
        writer.writeheader()
        writer.writerows(seq_90)
        
    sessions_dict[str(sess_id)] = {
        "demo": demo_items,
        "sequence": seq_90,
        "real": [w for w in seq_90 if w["type"] == "real"],
        "pseudo": [w for w in seq_90 if w["type"] == "pseudo"]
    }

# Save updated sessions_data.json for application engine and dashboard
with open(SESSIONS_JSON, "w", encoding="utf-8") as f:
    json.dump(sessions_dict, f, ensure_ascii=False, indent=2)

print(f"\nSaved {SESSIONS_JSON.name} with 6 partitioned and sequenced sessions.")
print(f"Saved 6 individual session sequence CSV files in {OUTPUT_DIR}/")
