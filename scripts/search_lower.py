from pathlib import Path
import re

bundle = Path('index.f9505d51fec8273c6b0b.bundle.js')
txt = bundle.read_text(encoding='utf-8')

# Search for class='lower' or class=lower usage patterns
for m in re.finditer(r'class=.lower', txt):
    start = max(0, m.start()-300)
    end = min(len(txt), m.end()+100)
    print('MATCH at', m.start(), ':')
    print(repr(txt[start:end]))
    print('---')

# Also search for img with lower
for m in re.finditer(r'img[^>]*lower[^>]*>', txt):
    start = max(0, m.start()-100)
    end = min(len(txt), m.end()+100)
    print('IMG LOWER:', txt[start:end])
    print('---')

# Search for arrowkey in html strings
for m in re.finditer(r'arrowkey_lex\.webp', txt):
    start = max(0, m.start()-400)
    end = min(len(txt), m.end()+200)
    print('ARROWKEY at', m.start(), ':')
    print(txt[start:end])
    print('---')
