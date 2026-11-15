import subprocess

BUNDLE_PATH = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\index.f9505d51fec8273c6b0b.bundle.js"

with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

target = 'Ke=e=>{let r=Math.random()<.5?"corpus_real":"corpus_pseudo";return e[r].length<1&&(r="corpus_pseudo"===r?"corpus_real":"corpus_pseudo"),r}'

replacement = 'Ke=e=>{var p=(window.ROAR_SETTINGS&&window.ROAR_SETTINGS.shufflePattern)||"alternating",last=window._lastItemType||"",st=window._typeStreak||0,r;if(p==="alternating"){r=last==="corpus_real"?"corpus_pseudo":"corpus_real";}else if(p==="constrained"){r=(st>=2)?(last==="corpus_real"?"corpus_pseudo":"corpus_real"):(Math.random()<.5?"corpus_real":"corpus_pseudo");}else if(p==="blocks"){var b=window._blkCount||0;if(b<5&&last){r=last;}else{r=last==="corpus_real"?"corpus_pseudo":"corpus_real";window._blkCount=0;}window._blkCount=(window._blkCount||0)+1;}else{r=Math.random()<.5?"corpus_real":"corpus_pseudo";}if(!e[r]||e[r].length<1){r="corpus_pseudo"===r?"corpus_real":"corpus_pseudo";}if(r===last){window._typeStreak=(window._typeStreak||0)+1;}else{window._typeStreak=1;}window._lastItemType=r;return r;}'

if target in text:
    text = text.replace(target, replacement, 1)
    print("Found target and replaced Ke definition!")
    with open(BUNDLE_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    
    res = subprocess.run(["node", "--check", BUNDLE_PATH], capture_output=True, text=True)
    if res.returncode == 0:
        print("Bundle syntax validation: PASSED!")
    else:
        print("Bundle syntax error:\n", res.stderr)
else:
    print("Target not found! Check if already patched.")
