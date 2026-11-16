#!/usr/bin/env python3
"""
Patch the ROAR bundle to remove ALL .webp entries from the preload manifest (Ge JSON).
This permanently fixes the "Error loading file: /audio/..." errors on Vercel.
Keeps .mp3 audio files intact so game sounds still work.
"""

import re
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
BUNDLE_PUBLIC = ROOT / "public" / "index.f9505d51fec8273c6b0b.bundle.js"
BUNDLE_ROOT = ROOT / "index.f9505d51fec8273c6b0b.bundle.js"


def find_ge_json(content: str):
    """Find the Ge JSON.parse block in the bundle."""
    # Pattern: const Ge=JSON.parse(' ... ')  or JSON.parse(" ... ")
    # The JSON string can be very long, we need to find it carefully
    patterns = [
        r'const Ge=JSON\.parse\(\'((?:[^\'\\]|\\.)*)\'\)',
        r'const Ge=JSON\.parse\("((?:[^"\\]|\\.)*)"\)',
        r'Ge=JSON\.parse\(\'((?:[^\'\\]|\\.)*)\'\)',
        r'Ge=JSON\.parse\("((?:[^"\\]|\\.)*)"\)',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.DOTALL)
        if m:
            return m
    return None


def remove_webp_from_array(arr):
    """Remove all .webp entries from a list, keep everything else."""
    if not isinstance(arr, list):
        return arr
    return [item for item in arr if not (isinstance(item, str) and item.lower().endswith('.webp'))]


def remove_webp_recursive(obj):
    """Recursively remove .webp entries from all arrays in nested object."""
    if isinstance(obj, dict):
        return {k: remove_webp_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        cleaned = remove_webp_from_array(obj)
        return [remove_webp_recursive(item) for item in cleaned]
    else:
        return obj


def patch_bundle(bundle_path: Path) -> bool:
    print(f"\n{'='*60}")
    print(f"Patching: {bundle_path}")
    print(f"File exists: {bundle_path.exists()}")
    
    if not bundle_path.exists():
        print(f"ERROR: Bundle not found at {bundle_path}")
        return False

    content = bundle_path.read_text(encoding='utf-8', errors='replace')
    print(f"Bundle size: {len(content):,} bytes")

    # First, let's check what .webp references exist
    webp_refs = re.findall(r'[\w_-]+\.webp', content)
    print(f"Total .webp references before patch: {len(webp_refs)}")
    if webp_refs:
        unique_webp = set(webp_refs)
        print(f"Unique .webp files: {unique_webp}")

    # Strategy 1: Find and patch the Ge JSON.parse block
    m = find_ge_json(content)
    
    if m:
        print(f"\nFound Ge JSON block at position {m.start()}-{m.end()}")
        raw_json_str = m.group(1)
        print(f"JSON string length: {len(raw_json_str)}")
        
        try:
            # Unescape the JSON string (it's inside JS string quotes)
            # Handle both single and double quoted versions
            json_str = raw_json_str.encode('raw_unicode_escape').decode('unicode_escape')
        except Exception:
            json_str = raw_json_str
        
        try:
            ge_data = json.loads(json_str)
            print(f"Successfully parsed Ge JSON")
            print(f"Top-level keys: {list(ge_data.keys())}")
            
            # Count .webp before removal
            original_str = json.dumps(ge_data)
            webp_before = len(re.findall(r'\.webp', original_str))
            print(f".webp entries in Ge JSON before: {webp_before}")
            
            # Remove all .webp from the whole structure
            ge_cleaned = remove_webp_recursive(ge_data)
            
            new_str = json.dumps(ge_cleaned, separators=(',', ':'))
            webp_after = len(re.findall(r'\.webp', new_str))
            print(f".webp entries in Ge JSON after: {webp_after}")
            
            # Re-escape for JS string embedding
            escaped = new_str.replace('\\', '\\\\').replace("'", "\\'")
            
            # Reconstruct the full replacement
            original_full = m.group(0)
            # Determine quote style used
            if "JSON.parse('" in original_full:
                new_full = original_full[:original_full.index("'") + original_full[:original_full.index("'")].count("'") + 1]
                # Simpler: just replace the inner JSON string
                quote_char = "'"
                prefix = original_full[:original_full.index("JSON.parse('") + len("JSON.parse('")]
                suffix = "')"
                new_full = prefix + escaped + suffix
            else:
                prefix = original_full[:original_full.index('JSON.parse("') + len('JSON.parse("')]
                escaped_dq = new_str.replace('\\', '\\\\').replace('"', '\\"')
                suffix = '")'
                new_full = prefix + escaped_dq + suffix
            
            new_content = content[:m.start()] + new_full + content[m.end():]
            print(f"\n✅ Ge JSON patched successfully")
            
        except json.JSONDecodeError as e:
            print(f"JSON decode failed: {e}")
            print("Falling back to regex-based string replacement...")
            new_content = content
            ge_data = None
    else:
        print("Ge JSON.parse block NOT found with standard patterns")
        print("Trying alternative search...")
        new_content = content
        ge_data = None

    # Strategy 2: Regardless of Ge JSON parse success, also do regex replacement
    # on ALL webp array entries in the bundle
    # Pattern: "filename.webp" in a JSON array context
    # Remove entries like: "arrow_left_p2.webp", "break.webp", etc.
    
    # Remove .webp strings from JSON arrays - pattern: ["...", "file.webp", "..."]
    # We'll replace them with empty string removal
    def remove_webp_from_json_array_string(text):
        """Remove .webp entries from JSON arrays using regex."""
        # Pattern: "something.webp" optionally with comma before/after
        # Remove: ,"file.webp" or "file.webp", or "file.webp" alone
        result = text
        
        # Remove: ,"filename.webp" (comma before)
        result = re.sub(r',\s*"[^"]*\.webp"', '', result)
        result = re.sub(r",\s*'[^']*\.webp'", '', result)
        
        # Remove: "filename.webp", (comma after)  
        result = re.sub(r'"[^"]*\.webp"\s*,', '', result)
        result = re.sub(r"'[^']*\.webp'\s*,", '', result)
        
        # Remove: "filename.webp" (standalone, no comma)
        result = re.sub(r'"[^"]*\.webp"', '""', result)
        result = re.sub(r"'[^']*\.webp'", "''", result)
        
        return result
    
    # Apply regex removal to the content
    new_content2 = remove_webp_from_json_array_string(new_content)
    
    webp_after_regex = len(re.findall(r'[\w_-]+\.webp', new_content2))
    print(f"\n.webp references after regex removal: {webp_after_regex}")
    
    # Write the patched content
    # Backup original first
    backup_path = bundle_path.with_suffix('.js.bak')
    if not backup_path.exists():
        shutil.copy2(bundle_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    bundle_path.write_text(new_content2, encoding='utf-8')
    print(f"✅ Patched bundle written: {bundle_path}")
    print(f"New size: {len(new_content2):,} bytes")
    
    # Validate JS syntax
    result = subprocess.run(
        ['node', '--check', str(bundle_path)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ JS syntax check PASSED")
    else:
        print(f"❌ JS syntax check FAILED:")
        print(result.stderr)
        # Restore backup
        shutil.copy2(backup_path, bundle_path)
        print("Restored from backup due to syntax error")
        return False
    
    return True


def verify_no_webp_preload(bundle_path: Path):
    """Verify that the preload error images are gone."""
    content = bundle_path.read_text(encoding='utf-8', errors='replace')
    problem_files = [
        'arrow_left_p2.webp', 'arrow_p3.webp', 'arrow_right_p2.webp',
        'break.webp', 'adventurer1.webp', 'adventurer2.webp', 'adventurer3.webp',
        'animated_left_key.webp', 'animated_right_key.webp', 'arrow_p2.webp',
        'arrowkey_lex.webp', 'arrowkey_lex_left.webp', 'arrowkey_lex_right.webp',
        'coin_bag.webp', 'coin_bag_old.webp', 'coin_icon.webp',
        'ending.webp', 'ending_background.webp', 'ending_coinbag.webp'
    ]
    print(f"\n{'='*60}")
    print(f"VERIFICATION: Checking for remaining problem .webp entries in {bundle_path.name}")
    all_clear = True
    for f in problem_files:
        # Check if it still appears as a quoted string (not just in comments/paths)
        matches = list(re.finditer(re.escape(f'"' + f + '"'), content))
        if matches:
            print(f"  ⚠️  STILL FOUND: \"{f}\" ({len(matches)} occurrences)")
            all_clear = False
        else:
            print(f"  ✅ REMOVED: {f}")
    
    if all_clear:
        print(f"\n🎉 ALL PROBLEM .WEBP FILES REMOVED FROM BUNDLE!")
    else:
        print(f"\n⚠️  Some entries remain - check manually")
    
    return all_clear


if __name__ == '__main__':
    print("🔧 ROAR Bundle Preload Image Patch Script")
    print(f"Working directory: {ROOT}")
    
    success = True
    
    # Patch public bundle
    if patch_bundle(BUNDLE_PUBLIC):
        verify_no_webp_preload(BUNDLE_PUBLIC)
    else:
        print("❌ Failed to patch public bundle")
        success = False
    
    # Copy patched public bundle to root
    print(f"\n{'='*60}")
    print("Copying patched bundle from public/ to root...")
    try:
        shutil.copy2(BUNDLE_PUBLIC, BUNDLE_ROOT)
        print(f"✅ Copied to root: {BUNDLE_ROOT}")
        # Validate root copy
        result = subprocess.run(['node', '--check', str(BUNDLE_ROOT)], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Root bundle syntax check PASSED")
        else:
            print(f"❌ Root bundle syntax check FAILED: {result.stderr}")
            success = False
        verify_no_webp_preload(BUNDLE_ROOT)
    except Exception as e:
        print(f"❌ Copy failed: {e}")
        success = False
    
    print(f"\n{'='*60}")
    if success:
        print("✅ PATCH COMPLETE - Ready to commit and push!")
    else:
        print("❌ PATCH HAD ERRORS - Review above output")
    
    sys.exit(0 if success else 1)
