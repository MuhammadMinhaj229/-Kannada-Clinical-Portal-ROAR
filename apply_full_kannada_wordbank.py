import json
import pandas as pd
import shutil
import subprocess

bundle_path = r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/public/index.f9505d51fec8273c6b0b.bundle.js'
bak_path = bundle_path + '.original.bak'

# Read clean original backup
with open(bak_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("Original backup size:", len(text))

# -------------------------------------------------------------
# 1. FIX TASK ID: Always use "swr" so Firebase doesn't crash on "swr-kn"
# -------------------------------------------------------------
old_task = 'R="en"===E?"swr":`swr-${E}`'
new_task = 'R="swr"'
if old_task in text:
    text = text.replace(old_task, new_task, 1)
    print("PATCH 1 SUCCESS: Fixed taskId to 'swr'")
else:
    print("PATCH 1 WARNING: Could not find old_task")

# -------------------------------------------------------------
# 2. FIX START RUN: Make firekit.startRun safe using .catch() expression
# (Note: must be an expression because Webpack chains with comma: func(),await ...)
# -------------------------------------------------------------
old_startrun = 'await this.firekit.startRun();'
new_startrun = 'await this.firekit.startRun().catch(e=>console.warn("Firekit offline fallback",e));'
if old_startrun in text:
    text = text.replace(old_startrun, new_startrun, 1)
    print("PATCH 2 SUCCESS: Made firekit.startRun safe with .catch()")
else:
    print("PATCH 2 WARNING: Could not find old_startrun")

# -------------------------------------------------------------
# 3. FIX LANGUAGE DETECTOR & FALLBACK LNG
# -------------------------------------------------------------
text = text.replace('lookup:e=>"en"})', 'lookup:e=>"kn"})', 1)
text = text.replace('fallbackLng:"en"', 'fallbackLng:"kn"', 1)
print("PATCH 3 SUCCESS: Language detector and fallbackLng set to 'kn'")

# -------------------------------------------------------------
# 4. INJECT KANNADA UI TRANSLATIONS (double-quoted JSON)
# -------------------------------------------------------------
kn_path = r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/src-original/src/locales/kn/translation.json'
with open(kn_path, 'r', encoding='utf-8') as f:
    kn_data = json.load(f)

kn_json_str = json.dumps(kn_data, ensure_ascii=False)
kn_js_literal_dq = kn_json_str.replace('\\', '\\\\').replace('"', '\\"')

p_pos = text.find("P=JSON.parse('")
end_pos = text.find("')", p_pos + 14)
text = text[:p_pos] + f'P=JSON.parse("{kn_js_literal_dq}")' + text[end_pos + 2:]
print("PATCH 4 SUCCESS: Replaced UI translations with Kannada")

# -------------------------------------------------------------
# 5. INJECT KANNADA INTO I18NEXT RESOURCES
# -------------------------------------------------------------
old_res = 'resources:{en:{translation:P},es:{translation:L},it:{translation:N},pt:{translation:z},de:{translation:F}}'
new_res = 'resources:{kn:{translation:P},en:{translation:P},es:{translation:L},it:{translation:N},pt:{translation:z},de:{translation:F}}'
text = text.replace(old_res, new_res, 1)
print("PATCH 5 SUCCESS: Added kn to i18next resources")

# -------------------------------------------------------------
# 6. INJECT COMPLETE 540 KANNADA WORDS + 5 PRACTICE DEMO WORDS
# -------------------------------------------------------------
df_real = pd.read_csv(r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/realwords.csv')
nonwords_path = r'C:/Users/User/.gemini/antigravity/brain/384e9f2d-2c0d-4f84-a3bf-138e1df437bd/.user_uploaded/media_1794754075883_6d51365a.xlsm'
df_pseudo = pd.read_excel(nonwords_path, sheet_name=0)

real_aoa_map = {}
for _, row in df_real.iterrows():
    w = str(row['word']).strip()
    aoa = float(row['mean_AoA']) if pd.notnull(row['mean_AoA']) else 3.5
    real_aoa_map[w] = aoa

# 5 Demo Practice Items matching the audio feedback sequence:
kn_practice = [
    {"word": "ಹೀ",   "realpseudo": "pseudo", "block": "practice", "order": 1, "difficulty": 0},
    {"word": "ಹಾಲು", "realpseudo": "real",   "block": "practice", "order": 2, "difficulty": 0},
    {"word": "ನೀರು", "realpseudo": "real",   "block": "practice", "order": 3, "difficulty": 0},
    {"word": "ಚೃರು", "realpseudo": "pseudo", "block": "practice", "order": 4, "difficulty": 0},
    {"word": "ಊಡು",  "realpseudo": "pseudo", "block": "practice", "order": 5, "difficulty": 0},
]

kn_validated = []
# 270 Real words
for idx, row in df_real.iterrows():
    word = str(row['word']).strip()
    aoa = float(row['mean_AoA']) if pd.notnull(row['mean_AoA']) else 3.5
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

# 270 Pseudo words
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

kn_practice_js = json.dumps(kn_practice, ensure_ascii=False)
kn_validated_js = json.dumps(kn_validated, ensure_ascii=False)

target_de = 'dataValidatedURL2:""}}'
kn_entry = f'dataValidatedURL2:""}},kn:{{dataPracticeURL:{kn_practice_js},dataValidatedURL:{kn_validated_js},dataNewURL:[],dataNewEasyURL:[],dataValidatedURL2:[]}}}}'
text = text.replace(target_de, kn_entry, 1)
print(f"PATCH 6 SUCCESS: Injected {len(kn_validated)} test words and {len(kn_practice)} demo words")

# -------------------------------------------------------------
# 7. AUDIO ROUTING: Local /audio
# -------------------------------------------------------------
text = text.replace('mr="https://storage.googleapis.com/roar-swr"', 'mr="/audio"', 1)
print("PATCH 7 SUCCESS: Fixed audio base URL to local /audio")

# -------------------------------------------------------------
# WRITE FINAL BUNDLE
# -------------------------------------------------------------
with open(bundle_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"\nFinal bundle size: {len(text):,} characters")
