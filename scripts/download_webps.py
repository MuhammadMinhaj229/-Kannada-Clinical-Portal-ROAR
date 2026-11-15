import os
import urllib.request
import re

BUNDLE = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\index.f9505d51fec8273c6b0b.bundle.js"
BASE_DIR = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\audio"

SHARED_DIR = os.path.join(BASE_DIR, "shared")
KN_SHARED_DIR = os.path.join(BASE_DIR, "kn", "shared")

os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(KN_SHARED_DIR, exist_ok=True)

with open(BUNDLE, 'r', encoding='utf-8') as f:
    text = f.read()

webps = sorted(list(set(re.findall(r'[\w\-]+(?:\.webp|\.png|\.jpg|\.svg)', text))))

print(f"Total files to locate & download: {len(webps)}")

GCS_PREFIXES = [
    "https://storage.googleapis.com/roar-swr/shared/",
    "https://storage.googleapis.com/roar-swr/en/shared/",
    "https://storage.googleapis.com/roar-swr/en/desktop/",
    "https://storage.googleapis.com/roar-swr/"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

success_count = 0
failed = []

for filename in webps:
    downloaded = False
    for prefix in GCS_PREFIXES:
        url = prefix + filename
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    data = resp.read()
                    # Write to shared/
                    path1 = os.path.join(SHARED_DIR, filename)
                    with open(path1, 'wb') as out1:
                        out1.write(data)
                    
                    # Write to kn/shared/
                    path2 = os.path.join(KN_SHARED_DIR, filename)
                    with open(path2, 'wb') as out2:
                        out2.write(data)
                    
                    print(f"[OK] {filename} ({len(data)} bytes) from {url}")
                    downloaded = True
                    success_count += 1
                    break
        except Exception:
            continue
    
    if not downloaded:
        print(f"[FAIL] Could not find {filename}")
        failed.append(filename)

print(f"\nDownload summary: {success_count}/{len(webps)} downloaded successfully.")
if failed:
    print(f"Failed files ({len(failed)}): {failed}")
