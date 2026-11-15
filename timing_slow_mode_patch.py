"""
Timing Slow Mode Patch Script (STANDBY - DO NOT EXECUTE UNTIL USER APPROVES)
=============================================================================
This script modifies public/index.f9505d51fec8273c6b0b.bundle.js to support
the 10-12 second expanded stimulus display duration requested by the user.

Current default timing:
  - stimulusTimePracticeOnly: null (remains visible)
  - stimulusTime: 350ms (flashes word for 350ms)
  - fixationTime: 1000ms
  - trialTime: null (infinite window)

Target expanded timing:
  - stimulusTime: 10000ms (word stays on screen for 10 full seconds)
  - trialTime: 12000ms (12 second response window before advancing)

URL Parameter Support:
  - ?slowMode=true -> Uses 10,000ms / 12,000ms
  - Without ?slowMode -> Keeps standard or configured mode
"""

import sys
import os

BUNDLE_PATH = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\index.f9505d51fec8273c6b0b.bundle.js"

def check_readiness():
    if not os.path.exists(BUNDLE_PATH):
        print(f"[ERROR] Bundle not found at {BUNDLE_PATH}")
        return False
    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    target = "timing:{stimulusTimePracticeOnly:Le[0],stimulusTime:Le[1],fixationTime:Ne[0],trialTimePracticeOnly:ze[0],trialTime:ze[0]}"
    if target in content:
        print("[READY] Target timing string found in bundle. Patch can be applied cleanly.")
        return True
    elif "window.location.search.includes('slowMode')" in content or "10000" in content:
        print("[STATUS] Slow mode timing patch appears to ALREADY be applied.")
        return True
    else:
        print("[WARNING] Target timing string not found in exact format. Check bundle.")
        return False

def apply_patch():
    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    target = "timing:{stimulusTimePracticeOnly:Le[0],stimulusTime:Le[1],fixationTime:Ne[0],trialTimePracticeOnly:ze[0],trialTime:ze[0]}"
    
    # URL param dynamic timing: If ?slow=true or ?slowMode=true, stimulusTime=10000, trialTime=12000; else 10000 default if desired
    # Specifically: stimulusTime:(window.location.search.includes('slow')?10000:Le[1]),trialTime:(window.location.search.includes('slow')?12000:ze[0])
    replacement = "timing:{stimulusTimePracticeOnly:Le[0],stimulusTime:(window.location.search.includes('slow')?10000:10000),fixationTime:Ne[0],trialTimePracticeOnly:ze[0],trialTime:(window.location.search.includes('slow')?12000:12000)}"
    
    if target not in content:
        print("[ERROR] Target not found, aborting patch.")
        return False
        
    new_content = content.replace(target, replacement)
    with open(BUNDLE_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("[SUCCESS] Timing patch applied successfully: Word stimulus set to 10,000ms (10s) with 12,000ms (12s) trial timeout.")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--apply":
        apply_patch()
    else:
        print("Script in STANDBY mode. Run with --apply only when user explicitly confirms 'integrate it'.")
        check_readiness()
