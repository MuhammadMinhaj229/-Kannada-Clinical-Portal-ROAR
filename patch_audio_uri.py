import re

bundle_path = r'C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\index.f9505d51fec8273c6b0b.bundle.js'
with open(bundle_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'mr="https://storage.googleapis.com/roar-swr"'
replacement = 'mr="/audio"'

if target in text:
    new_text = text.replace(target, replacement, 1)
    with open(bundle_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("SUCCESS: Patched mediaAssets base URI to /audio in bundle!")
else:
    print("Target string not found!")
