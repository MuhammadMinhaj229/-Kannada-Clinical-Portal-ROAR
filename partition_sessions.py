import pandas as pd
import json

# Load real words
df_real = pd.read_csv(r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/realwords.csv')
# Load pseudo words
nonwords_path = r'C:/Users/User/.gemini/antigravity/brain/384e9f2d-2c0d-4f84-a3bf-138e1df437bd/.user_uploaded/media_1794754075883_6d51365a.xlsm'
df_pseudo = pd.read_excel(nonwords_path, sheet_name=0)

# Sort or balance by difficulty (syllables / mean_AoA)
df_real['aoa'] = pd.to_numeric(df_real['mean_AoA'], errors='coerce').fillna(3.5)
df_real['syllables'] = pd.to_numeric(df_real['syllables'], errors='coerce').fillna(2)

# Partition 270 real words into 6 sessions of 45 words each
# We can do stratified sampling or block partitioning so each session gets easy, medium, and harder words
sessions = {i: {"real": [], "pseudo": [], "demo": []} for i in range(1, 7)}

# Demo words (5 per session - can be shared or session-specific)
demo_templates = [
    {"word": "ಹೀ",   "realpseudo": "pseudo", "block": "practice", "order": 1},
    {"word": "ಹಾಲು", "realpseudo": "real",   "block": "practice", "order": 2},
    {"word": "ನೀರು", "realpseudo": "real",   "block": "practice", "order": 3},
    {"word": "ಚೃರು", "realpseudo": "pseudo", "block": "practice", "order": 4},
    {"word": "ಊಡು",  "realpseudo": "pseudo", "block": "practice", "order": 5},
]

# Distribute 270 real words (45 per session)
real_records = df_real.to_dict(orient='records')
pseudo_records = df_pseudo.to_dict(orient='records')

for idx, r in enumerate(real_records):
    sess_id = (idx % 6) + 1
    sessions[sess_id]["real"].append({
        "id": f"R{idx+1:03d}",
        "word": r['word'],
        "meaning": r.get('meaning', ''),
        "transcription": r.get('transcription', ''),
        "akshara_type": r.get('Akshara type', ''),
        "aoa": r.get('aoa', 3.5),
        "syllables": int(r.get('syllables', 2)),
        "realpseudo": "real"
    })

for idx, p in enumerate(pseudo_records):
    sess_id = (idx % 6) + 1
    sessions[sess_id]["pseudo"].append({
        "id": str(p.get('nonword_id', f"N{idx+1:03d}")),
        "word": p['nonword'],
        "method": p.get('method', ''),
        "source_word": p.get('source_word_1', ''),
        "realpseudo": "pseudo"
    })

for i in range(1, 7):
    sessions[i]["demo"] = list(demo_templates)
    print(f"Session {i}: {len(sessions[i]['real'])} real, {len(sessions[i]['pseudo'])} pseudo, {len(sessions[i]['demo'])} demo words")

# Save structured sessions file
with open(r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/sessions_data.json', 'w', encoding='utf-8') as f:
    json.dump(sessions, f, ensure_ascii=False, indent=2)

print("Saved sessions_data.json successfully!")
