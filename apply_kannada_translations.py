import os
import json
import shutil

bundle_path = r'C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\index.f9505d51fec8273c6b0b.bundle.js'
bak_path = bundle_path + '.original.bak'

# 1. Ensure backup exists
if not os.path.exists(bak_path):
    shutil.copyfile(bundle_path, bak_path)
    print(f"Created backup: {bak_path}")

# 2. Read Kannada translation JSON
kn_path = r'C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\src-original\src\locales\kn\translation.json'
with open(kn_path, 'r', encoding='utf-8') as f:
    kn_data = json.load(f)

# Convert to JSON string
kn_json_str = json.dumps(kn_data, ensure_ascii=False)
# In Webpack, JSON.parse('...') expects a string literal inside JS code:
# Escape single quotes and backslashes
kn_js_literal = kn_json_str.replace('\\', '\\\\').replace("'", "\\'")

with open(bak_path, 'r', encoding='utf-8', errors='ignore') as f:
    bundle_text = f.read()

# 3. Locate the target English JSON.parse('...')
marker = "Welcome to the Single Word Recognition activity!"
marker_pos = bundle_text.find(marker)
if marker_pos == -1:
    print("Error: Could not find English translation marker in bundle.")
    exit(1)

start_prefix = "JSON.parse('{\""
start_pos = bundle_text.rfind(start_prefix, 0, marker_pos)
end_suffix = "}')"
end_pos = bundle_text.find(end_suffix, marker_pos)

if start_pos == -1 or end_pos == -1:
    print(f"Error locating JSON.parse boundaries: start={start_pos}, end={end_pos}")
    exit(1)

old_slice = bundle_text[start_pos : end_pos + len(end_suffix)]
print(f"Found old slice (length {len(old_slice)} chars)")

new_slice = f"JSON.parse('{kn_js_literal}')"
new_bundle_text = bundle_text[:start_pos] + new_slice + bundle_text[end_pos + len(end_suffix):]

with open(bundle_path, 'w', encoding='utf-8') as out_f:
    out_f.write(new_bundle_text)

print(f"SUCCESS: Replaced translation dictionary in {bundle_path}")
print(f"New bundle size: {len(new_bundle_text)} characters")
