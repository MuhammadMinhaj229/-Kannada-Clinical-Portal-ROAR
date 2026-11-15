import json
import shutil
import os

bundle_path = r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/public/index.f9505d51fec8273c6b0b.bundle.js'
bak_path = bundle_path + '.original.bak'

with open(bak_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("Original bundle size:", len(text))

# ===========================================================
# PATCH 1: Force language to 'kn' in the defaultToEnglish detector
# This makes the app use Kannada resources and Kannada audio paths
# ===========================================================
old_lookup = 'lookup:e=>"en"})'
new_lookup = 'lookup:e=>"kn"})'
count1 = text.count(old_lookup)
print(f"Found {count1} occurrences of defaultToEnglish lookup")
text = text.replace(old_lookup, new_lookup, 1)

# Also change fallbackLng to kn
old_fallback = 'fallbackLng:"en"'
new_fallback = 'fallbackLng:"kn"'
count2 = text.count(old_fallback)
print(f"Found {count2} occurrences of fallbackLng:\"en\"")
text = text.replace(old_fallback, new_fallback, 1)

# ===========================================================
# PATCH 2: Replace the English translation (P=JSON.parse) with Kannada
# ===========================================================
kn_path = r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/src-original/src/locales/kn/translation.json'
with open(kn_path, 'r', encoding='utf-8') as f:
    kn_data = json.load(f)

kn_json_str = json.dumps(kn_data, ensure_ascii=False)
kn_js_literal = kn_json_str.replace('\\', '\\\\').replace("'", "\\'")

marker = "Welcome to the Single Word Recognition activity!"
marker_pos = text.find(marker)
if marker_pos == -1:
    # Try another marker
    marker = "labID"
    marker_pos = text.find(f'P=JSON.parse')
    print("Using alternative marker, found at:", marker_pos)
else:
    print(f"Found English marker at pos {marker_pos}")

# Locate the JSON.parse that contains the English translations
# Look for P=JSON.parse('...')
p_assign_pos = text.find('P=JSON.parse(')
if p_assign_pos == -1:
    print("ERROR: Cannot find P=JSON.parse(")
else:
    print(f"Found P=JSON.parse at {p_assign_pos}")
    # read until end of JSON.parse call
    start_prefix = "P=JSON.parse('"
    start_pos = text.find(start_prefix)
    end_suffix = "')"
    # find the end after start_pos
    end_pos = text.find(end_suffix, start_pos + len(start_prefix))
    
    old_slice = text[start_pos:end_pos + len(end_suffix)]
    print(f"Old slice length: {len(old_slice)} chars")
    print("Old start preview:", old_slice[:120])
    
    new_slice = f"P=JSON.parse('{kn_js_literal}')"
    text = text[:start_pos] + new_slice + text[end_pos + len(end_suffix):]
    print(f"Replaced. New bundle size: {len(text)}")

# ===========================================================
# PATCH 3: Add 'kn' wordlist entry pointing to English practice CSV 
# so the app doesn't crash when looking for kn wordlist
# The English CSV is embedded in the bundle and auto-resolves
# ===========================================================
# In the bundle, the ie={en:{...}, ...} object defines wordlists per language
# We need to add kn entry. First find the ie object
ie_pos = text.find('ie={en:{dataPracticeURL:D')
if ie_pos != -1:
    # Also look for de entry to append after
    de_entry_search = 'de:{dataPracticeURL:'
    de_pos = text.find(de_entry_search, ie_pos)
    if de_pos != -1:
        # Find the end of de entry: next '}}'
        de_end = text.find('}}', de_pos)
        # We want to insert after the de entry closing
        insert_pos = de_end + 2  # After '}}'
        old_insert_text = text[de_end:de_end+30]
        print(f"de entry ends, text around end: {old_insert_text}")
        # Insert kn entry as a copy of English
        # Actually the values are variable references - just point kn to same as en
        # Find what D, q, U, G, M look like (they are CSV data embedded)
        # Instead: inject a wrapper that overrides wordlist for kn after app loads
        # Best approach: patch kn entry to use same as en wordlist  
        # Find the D= variable (English practice CSV)
        # Note: in bundle these are all resolved inline, D refers to the first en CSV
        # For now: add kn with same as en
        kn_entry = ',kn:{dataPracticeURL:D,dataValidatedURL:q,dataNewURL:U,dataNewEasyURL:G,dataValidatedURL2:M}'
        text = text[:insert_pos] + kn_entry + text[insert_pos:]
        print(f"Added kn wordlist entry at {insert_pos}")
else:
    print("WARNING: Could not find ie= wordlist object to inject kn entry")

# ===========================================================
# PATCH 4: Add kn to i18next resources 
# ===========================================================
resources_pos = text.find('resources:{en:{translation:P}')
if resources_pos != -1:
    old_resources = 'resources:{en:{translation:P},es:{translation:L},it:{translation:N},pt:{translation:z},de:{translation:F}}'
    new_resources = 'resources:{kn:{translation:P},en:{translation:P},es:{translation:L},it:{translation:N},pt:{translation:z},de:{translation:F}}'
    text = text.replace(old_resources, new_resources, 1)
    print("Added kn to i18next resources")
else:
    print("WARNING: Could not find resources object")

# ===========================================================
# WRITE OUTPUT
# ===========================================================
with open(bundle_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"\nSUCCESS: Patched bundle written to {bundle_path}")
print(f"Final bundle size: {len(text)} chars")
