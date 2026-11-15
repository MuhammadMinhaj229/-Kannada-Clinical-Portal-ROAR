"""
The app builds audio URLs as: 
  mr + "/" + language + "/" + device + "/" + filename
  = "https://storage.googleapis.com/roar-swr/kn/desktop/intro_1_ns.mp3"

BUT our server only listens on localhost:8080 and the app makes full https:// URLs to GCS.

The fix is: we need to intercept these at the BROWSER level - which means we need to 
patch mr in the bundle to point to our local server instead of GCS.

Let's check: does the app use relative URLs or absolute URLs for audio?
If it uses absolute GCS URLs, the browser goes directly to GCS bypassing our server.
"""

with open(r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/public/index.f9505d51fec8273c6b0b.bundle.js', 'r', encoding='utf-8') as f:
    text = f.read()

# mr is the bucket URI for audio
# Fix: replace GCS URL with local server audio URL
old_mr = 'mr="https://storage.googleapis.com/roar-swr"'
new_mr = 'mr=""'  # Use empty string = relative URLs -> /kn/desktop/xxx.mp3

if old_mr in text:
    text = text.replace(old_mr, new_mr, 1)
    print("SUCCESS: Changed mr from GCS to relative path (empty string)")
    print("Audio will now be fetched as relative URLs: /kn/desktop/xxx.mp3")
else:
    print("WARNING: Exact old_mr not found, trying other patterns")
    import re
    pos = text.find('mr=')
    while pos != -1:
        snippet = text[max(0, pos):min(len(text), pos+80)]
        if 'storage.googleapis' in snippet or 'roar-swr' in snippet:
            print(f"Found at {pos}: {snippet[:80]}")
        pos = text.find('mr=', pos+3)

with open(r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/public/index.f9505d51fec8273c6b0b.bundle.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Bundle size:", len(text))
