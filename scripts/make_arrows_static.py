import os
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")

# 1. Inspect and extract frame 0 (the solid red/blue filled frame)
left_p2_source = REPO_ROOT / "audio" / "kn" / "shared" / "arrow_left_p2.webp"
right_p2_source = REPO_ROOT / "audio" / "kn" / "shared" / "arrow_right_p2.webp"

im_left = Image.open(left_p2_source)
im_left.seek(0)
frame_left = im_left.copy()

im_right = Image.open(right_p2_source)
im_right.seek(0)
frame_right = im_right.copy()

print(f"Extracted Frame 0: Left={frame_left.size}, Right={frame_right.size}")

# Find all locations of arrow_left_p2.webp and arrow_right_p2.webp in repo
left_files = list(REPO_ROOT.rglob("arrow_left_p2.webp"))
right_files = list(REPO_ROOT.rglob("arrow_right_p2.webp"))

# Also handle arrowkey_lex_left.webp and arrowkey_lex_right.webp if they have blinking
lex_left_source = REPO_ROOT / "audio" / "kn" / "shared" / "arrowkey_lex_left.webp"
lex_right_source = REPO_ROOT / "audio" / "kn" / "shared" / "arrowkey_lex_right.webp"

im_lex_l = Image.open(lex_left_source)
im_lex_l.seek(0)
frame_lex_l = im_lex_l.copy()

im_lex_r = Image.open(lex_right_source)
im_lex_r.seek(0)
frame_lex_r = im_lex_r.copy()

lex_l_files = list(REPO_ROOT.rglob("arrowkey_lex_left.webp"))
lex_r_files = list(REPO_ROOT.rglob("arrowkey_lex_right.webp"))

print(f"Found {len(left_files)} arrow_left_p2 files")
print(f"Found {len(right_files)} arrow_right_p2 files")
print(f"Found {len(lex_l_files)} arrowkey_lex_left files")
print(f"Found {len(lex_r_files)} arrowkey_lex_right files")

# Save as STATIC (single frame, not animated) webp with lossless/high quality
for p in left_files:
    frame_left.save(p, "WEBP", lossless=True)
    print(f"Saved static {p}")

for p in right_files:
    frame_right.save(p, "WEBP", lossless=True)
    print(f"Saved static {p}")

for p in lex_l_files:
    frame_lex_l.save(p, "WEBP", lossless=True)
    print(f"Saved static {p}")

for p in lex_r_files:
    frame_lex_r.save(p, "WEBP", lossless=True)
    print(f"Saved static {p}")

print("\n--- VERIFICATION OF SAVED FILES ---")
for p in [left_files[0], right_files[0], lex_l_files[0], lex_r_files[0]]:
    im = Image.open(p)
    anim = getattr(im, "is_animated", False)
    frames = getattr(im, "n_frames", 1)
    print(f"{p.name}: is_animated={anim}, n_frames={frames}, size={im.size}")
