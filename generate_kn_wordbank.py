import pandas as pd
import json

# 1. Load real words
df_real = pd.read_csv(r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/realwords.csv')

# 2. Load pseudo words
nonwords_path = r'C:/Users/User/.gemini/antigravity/brain/384e9f2d-2c0d-4f84-a3bf-138e1df437bd/.user_uploaded/media_1794754075883_6d51365a.xlsm'
df_pseudo = pd.read_excel(nonwords_path, sheet_name=0)

print(f"Loaded {len(df_real)} real words, {len(df_pseudo)} pseudo words")

# Build map of real words for difficulty matching
real_aoa_map = {}
for _, row in df_real.iterrows():
    w = str(row['word']).strip()
    aoa = float(row['mean_AoA']) if pd.notnull(row['mean_AoA']) else 3.5
    real_aoa_map[w] = aoa

# 3. Create practice demo items (5 items)
kn_practice = [
    {"word": "ಹೀ",   "realpseudo": "pseudo", "block": "practice", "order": 1, "difficulty": -1.5},
    {"word": "ಹಾಲು", "realpseudo": "real",   "block": "practice", "order": 2, "difficulty": -1.5},
    {"word": "ನೀರು", "realpseudo": "real",   "block": "practice", "order": 3, "difficulty": -1.5},
    {"word": "ಚೃರು", "realpseudo": "pseudo", "block": "practice", "order": 4, "difficulty": -1.5},
    {"word": "ಊಡು",  "realpseudo": "pseudo", "block": "practice", "order": 5, "difficulty": -1.5},
]

# 4. Create validated test items (540 items: 270 real + 270 pseudo)
kn_validated = []

# Add all 270 real words
for idx, row in df_real.iterrows():
    word = str(row['word']).strip()
    aoa = float(row['mean_AoA']) if pd.notnull(row['mean_AoA']) else 3.5
    # Standardize difficulty b around mean=0, std=1.5
    b_val = round((aoa - 3.5) / 1.0, 3)
    kn_validated.append({
        "word": word,
        "realpseudo": "real",
        "corpusId": "kn-real",
        "a": 1.0,
        "b": b_val,
        "c": 0.25,
        "d": 0.0
    })

# Add all 270 pseudo words
for idx, row in df_pseudo.iterrows():
    word = str(row['nonword']).strip()
    src_word = str(row['source_word_1']).strip() if pd.notnull(row.get('source_word_1')) else ""
    src_aoa = real_aoa_map.get(src_word, 3.5)
    b_val = round((src_aoa - 3.5) / 1.0, 3)
    kn_validated.append({
        "word": word,
        "realpseudo": "pseudo",
        "corpusId": "kn-pseudo",
        "a": 1.0,
        "b": b_val,
        "c": 0.25,
        "d": 0.0
    })

print(f"Total validated items generated: {len(kn_validated)}")
print(f"Real items: {sum(1 for x in kn_validated if x['realpseudo'] == 'real')}")
print(f"Pseudo items: {sum(1 for x in kn_validated if x['realpseudo'] == 'pseudo')}")

# Save json for inspection
with open(r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/kn_wordbank_540.json', 'w', encoding='utf-8') as f:
    json.dump({
        "practice": kn_practice,
        "validated": kn_validated
    }, f, ensure_ascii=False, indent=2)

print("Saved kn_wordbank_540.json successfully!")
