import subprocess

BUNDLE_PATH = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\index.f9505d51fec8273c6b0b.bundle.js"

with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

target = 'fr=(0,t.zS)(Ge,mr,a).default,fr.message=i.Ay.t("loading"),'

# We set continue_after_error: true, show_detailed_errors: false, max_load_time: 5000,
# and if storyOption is false, empty out fr.images so it only preloads essential audio!
replacement = 'fr=(0,t.zS)(Ge,mr,a).default,fr.message=i.Ay.t("loading"),fr.continue_after_error=!0,fr.show_detailed_errors=!1,fr.max_load_time=5000,fr.images=(fr.images||[]).filter(x=>x.includes("arrow")||x.includes("coin")),'

if target in text:
    text = text.replace(target, replacement, 1)
    with open(BUNDLE_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("Bundle patched successfully with continue_after_error=true and optimized preload images!")
    res = subprocess.run(["node", "--check", BUNDLE_PATH], capture_output=True, text=True)
    if res.returncode == 0:
        print("Bundle syntax validation: PASSED!")
    else:
        print("Bundle syntax error:\n", res.stderr)
else:
    print("Target not found in bundle!")
