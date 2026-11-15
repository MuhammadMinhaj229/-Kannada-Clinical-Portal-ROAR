"""
Patch Bundle v5:
- Integrates Dynamic Settings (window.ROAR_SETTINGS)
- Hooks Real-time Telemetry (to /api/results/trial and /api/results/session)
- Filters Validated Words by Session Query Parameter (?session=1..6)
"""

import os
import subprocess

BUNDLE_PATH = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\index.f9505d51fec8273c6b0b.bundle.js"

with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
    bundle = f.read()

# 1. Patch timing definition to use window.ROAR_SETTINGS
target_timing = "timing:{stimulusTimePracticeOnly:Le[0],stimulusTime:Le[1],fixationTime:Ne[0],trialTimePracticeOnly:ze[0],trialTime:ze[0]}"
repl_timing = "timing:{stimulusTimePracticeOnly:Le[0],stimulusTime:((window.ROAR_SETTINGS&&window.ROAR_SETTINGS.stimulusDisplayMode==='infinite')?null:(window.ROAR_SETTINGS&&window.ROAR_SETTINGS.stimulusTimeMs?window.ROAR_SETTINGS.stimulusTimeMs:Le[1])),fixationTime:((window.ROAR_SETTINGS&&window.ROAR_SETTINGS.fixationTimeMs)?window.ROAR_SETTINGS.fixationTimeMs:Ne[0]),trialTimePracticeOnly:ze[0],trialTime:((window.ROAR_SETTINGS&&window.ROAR_SETTINGS.trialTimeoutMs)?window.ROAR_SETTINGS.trialTimeoutMs:ze[0])}"

if target_timing in bundle:
    bundle = bundle.replace(target_timing, repl_timing)
    print("[1] Timing definition hooked to ROAR_SETTINGS: SUCCESS")
else:
    print("[1] Target timing not found or already patched")

# 2. Patch stimulus_duration in test_response
target_dur = 'stimulus_duration:()=>{const e=o.session.get("config"),{userMode:r}=e;let a=e.timing.stimulusTime;'
repl_dur = 'stimulus_duration:()=>{if(window.ROAR_SETTINGS&&window.ROAR_SETTINGS.stimulusDisplayMode==="infinite")return null;if(window.ROAR_SETTINGS&&window.ROAR_SETTINGS.stimulusTimeMs)return window.ROAR_SETTINGS.stimulusTimeMs;const e=o.session.get("config"),{userMode:r}=e;let a=e.timing.stimulusTime;'

if target_dur in bundle:
    bundle = bundle.replace(target_dur, repl_dur)
    print("[2] stimulus_duration hooked to ROAR_SETTINGS: SUCCESS")
else:
    print("[2] Target stimulus_duration not found or already patched")

# 3. Patch telemetry in on_data_update & on_finish
target_telemetry = 'opts.on_finish=r($e.opts.on_finish,()=>{e.firekit.finishRun()});const a=new Se;$e.opts.on_data_update=r($e.opts.on_data_update,r=>{r.save_trial&&e.firekit.writeTrial(r,a.computedScoreCallback.bind(a))})'
repl_telemetry = 'opts.on_finish=r($e.opts.on_finish,()=>{e.firekit.finishRun();try{const p=new URLSearchParams(window.location.search);fetch("/api/results/session",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({participant:p.get("participant")||"Anonymous",session:p.get("session")||"1"})}).catch(()=>{})}catch(_){}});const a=new Se;$e.opts.on_data_update=r($e.opts.on_data_update,r=>{if(r.save_trial){e.firekit.writeTrial(r,a.computedScoreCallback.bind(a));try{const p=new URLSearchParams(window.location.search);fetch("/api/results/trial",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({participant:p.get("participant")||"Anonymous",session:p.get("session")||"1",stage:r.assessment_stage,word:r.word,correct:!!r.correct,rt:Math.round(r.rt||0),response:r.keyboard_response||r.button_response||"",trial_index:r.trial_index})}).catch(()=>{})}catch(_){}}})'

if target_telemetry in bundle:
    bundle = bundle.replace(target_telemetry, repl_telemetry)
    print("[3] Telemetry hooked into on_data_update and on_finish: SUCCESS")
else:
    print("[3] Target telemetry string not found or already patched")

# 4. Patch session-specific word filtering
target_validated = 'validated:d(i.Ay.language,a(r.validated))'
repl_validated = 'validated:d(i.Ay.language,(()=>{let v=a(r.validated);const p=new URLSearchParams(window.location.search);const s=parseInt(p.get("session"),10);if(s>=1&&s<=6){return v.filter((_,idx)=>(idx%6)===(s-1));}return v;})())'

if target_validated in bundle:
    bundle = bundle.replace(target_validated, repl_validated)
    print("[4] Session filtering hooked into validated words: SUCCESS")
else:
    print("[4] Target validated string not found or already patched")

with open(BUNDLE_PATH, "w", encoding="utf-8") as f:
    f.write(bundle)

print("\nValidating bundle syntax with node --check...")
res = subprocess.run(["node", "--check", BUNDLE_PATH], capture_output=True, text=True)
if res.returncode == 0:
    print("Bundle syntax validation: PASSED! Zero errors.")
else:
    print("Bundle syntax error:\n", res.stderr)
