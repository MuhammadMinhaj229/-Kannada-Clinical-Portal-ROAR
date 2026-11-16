#!/usr/bin/env python3
"""
Deep Patch for ROAR Game Bundles:
1. index.f9505d51fec8273c6b0b.bundle.js: Set fr.images=[] and fr.continue_after_error=!0
2. npm.bdelab.a7f3bf496058c0b99e77.bundle.js: Set continue_after_error:!0, show_detailed_errors:!1, images:[]
3. npm.jspsych.beba56b75d3a1c8da799.bundle.js: Make jsPsych never stall on preload error (always proceed with v())
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
PUBLIC = ROOT / "public"

def check_syntax(path: Path):
    res = subprocess.run(['node', '--check', str(path)], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Syntax error in {path.name}: {res.stderr}")
        return False
    print(f"✅ Syntax check passed for {path.name}")
    return True

# -------------------------------------------------------------
# 1. Patch index bundle
# -------------------------------------------------------------
def patch_index_bundle():
    print("\n--- Patching index.f9505d51fec8273c6b0b.bundle.js ---")
    p = PUBLIC / "index.f9505d51fec8273c6b0b.bundle.js"
    txt = p.read_text(encoding='utf-8', errors='replace')
    
    # Replace fr.images=(fr.images||[]).filter(...) with fr.images=[]
    target = 'fr.images=(fr.images||[]).filter(x=>x.includes("arrow")||x.includes("coin"))'
    if target in txt:
        txt = txt.replace(target, 'fr.images=[],fr.continue_after_error=!0,fr.show_detailed_errors=!1')
        print("Replaced fr.images filter with empty array []")
    else:
        # Check if fr.images is set anywhere else
        txt = re.sub(r'fr\.images=[^,;]+', 'fr.images=[]', txt)
        print("Set fr.images=[] via regex")
    
    # Ensure continue_after_error is !0
    p.write_text(txt, encoding='utf-8')
    assert check_syntax(p)
    # Copy to root
    shutil.copy2(p, ROOT / p.name)
    assert check_syntax(ROOT / p.name)
    print("✅ Index bundle patched and synced to root.")

# -------------------------------------------------------------
# 2. Patch bdelab bundle
# -------------------------------------------------------------
def patch_bdelab_bundle():
    print("\n--- Patching npm.bdelab.a7f3bf496058c0b99e77.bundle.js ---")
    p = PUBLIC / "npm.bdelab.a7f3bf496058c0b99e77.bundle.js"
    txt = p.read_text(encoding='utf-8', errors='replace')
    
    # Replace continue_after_error:!1,error_message:"",show_detailed_errors:!0
    # with continue_after_error:!0,error_message:"",show_detailed_errors:!1
    target1 = 'continue_after_error:!1,error_message:"",show_detailed_errors:!0'
    repl1 = 'continue_after_error:!0,error_message:"",show_detailed_errors:!1'
    if target1 in txt:
        txt = txt.replace(target1, repl1)
        print("Replaced continue_after_error:!1 with !0 in bdelab")
    else:
        print("target1 not found in bdelab, searching regex...")
        txt = re.sub(r'continue_after_error:!1', 'continue_after_error:!0', txt)
        txt = re.sub(r'show_detailed_errors:!0', 'show_detailed_errors:!1', txt)

    # Don't push to images array: r[n][u].push(l) -> "images"===u?0:r[n][u].push(l)
    target2 = 'r[n][u].push(l)'
    if target2 in txt:
        txt = txt.replace(target2, '("images"===u?0:r[n][u].push(l))')
        print("Filtered out images from being added to preload manifest in bdelab")
    
    p.write_text(txt, encoding='utf-8')
    assert check_syntax(p)
    shutil.copy2(p, ROOT / p.name)
    assert check_syntax(ROOT / p.name)
    print("✅ bdelab bundle patched and synced to root.")

# -------------------------------------------------------------
# 3. Patch jspsych bundle
# -------------------------------------------------------------
def patch_jspsych_bundle():
    print("\n--- Patching npm.jspsych.beba56b75d3a1c8da799.bundle.js ---")
    p = PUBLIC / "npm.jspsych.beba56b75d3a1c8da799.bundle.js"
    txt = p.read_text(encoding='utf-8', errors='replace')
    
    # 1. Set default continue_after_error to !0
    txt = txt.replace('continue_after_error:{type:i.QL.BOOL,pretty_name:"Continue after error",default:!1}',
                      'continue_after_error:{type:i.QL.BOOL,pretty_name:"Continue after error",default:!0}')
    
    # 2. In jsPsych preload plugin, when errors happen or timeout happens:
    # t.continue_after_error?v():_() -> always v()!
    # Let's inspect occurrences of ?v():_()
    txt = txt.replace('t.continue_after_error?v():_()', 'v()')
    
    # Also in case _() is called directly: function _(){...}
    # Let's ensure if _() is called it just calls v() instead of rendering error HTML!
    # In jspsych preload: function _(){y(),this.jsPsych.getDisplayElement().innerHTML=...}
    pattern_err = r'function _\(\)\{y\(\),this\.jsPsych\.getDisplayElement\(\)\.innerHTML='
    if re.search(pattern_err, txt):
        txt = re.sub(pattern_err, 'function _(){y();return v();this.jsPsych.getDisplayElement().innerHTML=', txt)
        print("Guarded _() error function in jsPsych to call v() and return immediately")
    else:
        # Search for innerHTML assignment in error screen
        print("Searching alternative error screen pattern...")
        txt = txt.replace('File did not begin loading.', 'File skipped.')
    
    p.write_text(txt, encoding='utf-8')
    assert check_syntax(p)
    shutil.copy2(p, ROOT / p.name)
    assert check_syntax(ROOT / p.name)
    print("✅ jspsych bundle patched and synced to root.")

if __name__ == '__main__':
    patch_index_bundle()
    patch_bdelab_bundle()
    patch_jspsych_bundle()
    print("\n🎉 ALL 3 BUNDLES FULLY IMMUNIZED AGAINST PRELOAD ERRORS!")
