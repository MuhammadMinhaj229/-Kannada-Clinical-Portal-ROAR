import os
import shutil

en_dir = r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/public/audio/en/desktop'
kn_dir = r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/public/audio/kn/desktop'

files = os.listdir(kn_dir)
print("Current kn files:", len(files))

# For any file ending with _ns.mp3, let's create the non _ns counterpart
created = []
for f in files:
    if f.endswith('_ns.mp3'):
        base = f[:-7] + '.mp3' # e.g. intro_1.mp3
        kn_target = os.path.join(kn_dir, base)
        en_target = os.path.join(en_dir, base)
        if not os.path.exists(kn_target):
            shutil.copyfile(os.path.join(kn_dir, f), kn_target)
            created.append(base)
        if not os.path.exists(en_target):
            shutil.copyfile(os.path.join(en_dir, f), en_target)

print("Created counterparts:", created)
print("Total kn files now:", len(os.listdir(kn_dir)))
print("Total en files now:", len(os.listdir(en_dir)))
