import csv
import json
import re
from pathlib import Path
from collections import deque

REPO_ROOT = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
REAL_WORDS_CSV = REPO_ROOT / "realwords.csv"

# Kannada Unicode Definitions
# Independent Vowels
SWARAS = [
    "\u0c85", "\u0c86", "\u0c87", "\u0c88", "\u0c89", "\u0c8a", "\u0c8b",
    "\u0c8e", "\u0c8f", "\u0c90", "\u0c92", "\u0c93", "\u0c94"
]
# Matras (Dependent Vowels)
MATRAS = [
    "\u0cbe", "\u0cbf", "\u0cc0", "\u0cc1", "\u0cc2", "\u0cc3",
    "\u0cc6", "\u0cc7", "\u0cc8", "\u0cca", "\u0ccb", "\u0ccc"
]
# Consonants
CONSONANTS = [
    "\u0c95", "\u0c96", "\u0c97", "\u0c98", "\u0c99", # k, kh, g, gh, ng
    "\u0c9a", "\u0c9b", "\u0c9c", "\u0c9d", "\u0c9e", # c, ch, j, jh, ny
    "\u0c9f", "\u0ca0", "\u0ca1", "\u0ca2", "\u0ca3", # T, Th, D, Dh, N
    "\u0ca4", "\u0ca5", "\u0ca6", "\u0ca7", "\u0ca8", # t, th, d, dh, n
    "\u0cae", "\u0caf", "\u0cb0", "\u0cb1", "\u0cb2", # p, ph, b, bh, m
    "\u0cb3", "\u0cb5", "\u0cb6", "\u0cb7", "\u0cb8", "\u0cb9" # y, r, l, v, sh, Sh, s, h, L
]
# Filter out rarely used / ambiguous consonants for clean pronounceable nonwords
USABLE_CONSONANTS = [
    "ಕ", "ಗ", "ಚ", "ಜ", "ಟ", "ಡ", "ಣ", "ತ", "ದ", "ನ", 
    "ಪ", "ಬ", "ಮ", "ಯ", "ರ", "ಲ", "ವ", "ಶ", "ಸ", "ಹ", "ಳ"
]

VIRAMA = "\u0ccd"
ANUSVARA = "\u0c82"
VISARGA = "\u0c83"

def parse_aksharas(word):
    """
    Splits a Kannada word into orthographic aksharas (syllabic units).
    An akshara consists of:
    (Consonant + Virama)* + Consonant + (Matra | Virama)? + (Anusvara | Visarga)?
    OR
    Independent Vowel + (Anusvara | Visarga)?
    """
    pattern = re.compile(
        r'(?:[\u0c95-\u0cb9]\u0ccd)*[\u0c95-\u0cb9](?:[\u0cbe-\u0ccc]|\u0ccd)?[\u0c82\u0c83]?'
        r'|[\u0c85-\u0c94][\u0c82\u0c83]?'
    )
    aksharas = pattern.findall(word)
    return aksharas

def count_syllables(word):
    aksharas = parse_aksharas(word)
    # Exclude standalone trailing virama codas from syllable count if needed,
    # but in Kannada orthography, len(aksharas) is the standard akshara count.
    return len(aksharas)

print("Akshara parser initialized.")
test_words = ["ಹಾಲು", "ಅಳು", "ಮರಗಳು", "ಬೆಕ್ಕು", "ಆಕಾಶವು"]
for tw in test_words:
    ak = parse_aksharas(tw)
    print(f"  {tw} -> {ak} (syllables: {len(ak)})")
