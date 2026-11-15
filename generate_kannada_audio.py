import os
import asyncio
import edge_tts

OUTPUT_DIR = r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica\public\audio\kn\desktop"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Recommended Voice: kn-IN-SapnaNeural (warm, clear, female educational voice)
VOICE = "kn-IN-SapnaNeural"

# All language-specific voiceover scripts for Kannada assessment
SCRIPTS = {
    "intro_1_ns.mp3": "ಏಕ ಪದ ಗುರುತಿಸುವಿಕೆ ಚಟುವಟಿಕೆಗೆ ಸ್ವಾಗತ! ಈ ಚಟುವಟಿಕೆಯಲ್ಲಿ, ಪರದೆಯ ಮೇಲೆ ಮೂಡುವ ಪದಗಳನ್ನು ನೀವು ನೋಡುತ್ತೀರಿ. ನಂತರ ನೀವು ಕಾಲ್ಪನಿಕ ಪದಗಳು ಮತ್ತು ನೈಜ ಪದಗಳ ನಡುವಿನ ವ್ಯತ್ಯಾಸವನ್ನು ತಿಳಿಸಬೇಕು.",
    
    "intro_2_ns.mp3": "ಕಾಲ್ಪನಿಕ ಪದಗಳು ನೋಡಲು ಸಾಮಾನ್ಯ ಪದಗಳಂತೆ ಕಂಡರೂ ಅವುಗಳಿಗೆ ಯಾವುದೇ ಅರ್ಥವಿರುವುದಿಲ್ಲ. ನೀವು ಕಾಲ್ಪನಿಕ ಪದ ಕಂಡರೆ, ಎಡ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ. ನೈಜ ಪದಗಳು ನಿಮಗೆ ಪರಿಚಿತವಾಗಿರುತ್ತವೆ. ನೀವು ನೈಜ ಪದ ಕಂಡರೆ, ಬಲ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    
    "intro_3_ns.mp3": "ಕಾಲ್ಪನಿಕ ಮತ್ತು ನೈಜ ಪದಗಳಿಗೆ ಯಾವ ಬಾಣದ ಕೀಲಿ ಒತ್ತಬೇಕೆಂದು ನೆನಪಿಸಿಕೊಳ್ಳಿ. ಸಾಧ್ಯವಾದಷ್ಟು ನಿಖರವಾಗಿ ಉತ್ತರಿಸಲು ಪ್ರಯತ್ನಿಸಿ. ಕೆಲವು ಪದಗಳು ಕಠಿಣವಾಗಿರಬಹುದು, ಪರವಾಗಿಲ್ಲ. ಖಚಿತವಿಲ್ಲದಿದ್ದರೆ ನಿಮ್ಮ ಅತ್ಯುತ್ತಮ ಊಹೆಯೊಂದಿಗೆ ಉತ್ತರಿಸಿ!",
    
    "post_practice_ns.mp3": "ಅದ್ಭುತ ಕೆಲಸ! ನೀವು ನಿಜವಾದ ಚಟುವಟಿಕೆಯನ್ನು ಪ್ರಾರಂಭಿಸಲು ಸಿದ್ಧರಿದ್ದೀರಿ! ಶುಭವಾಗಲಿ!",
    
    # Practice Trial 1 Feedback (Item 1 is 'xop' -> Made-up / Pseudo word)
    "feedback_1_correct_ns.mp3": "ಸರಿಯಾಗಿದೆ! ಇದು ಕಾಲ್ಪನಿಕ ಪದ. ಮುಂದುವರಿಯಲು ಎಡ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    "feedback_1_wrong_ns.mp3": "ತಪ್ಪಾಗಿದೆ. ಇದು ಕಾಲ್ಪನಿಕ ಪದ. ಮುಂದುವರಿಯಲು ಎಡ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    
    # Practice Trial 2 Feedback (Item 2 is 'how' -> Real word)
    "feedback_2_correct_ns.mp3": "ಸರಿಯಾಗಿದೆ! ಇದು ನೈಜ ಪದ. ಮುಂದುವರಿಯಲು ಬಲ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    "feedback_2_wrong_ns.mp3": "ತಪ್ಪಾಗಿದೆ. ಇದು ನೈಜ ಪದ. ಮುಂದುವರಿಯಲು ಬಲ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    
    # Practice Trial 3 Feedback (Item 3 is 'after' -> Real word)
    "feedback_3_correct_ns.mp3": "ಸರಿಯಾಗಿದೆ! ಇದು ನೈಜ ಪದ. ಮುಂದುವರಿಯಲು ಬಲ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    "feedback_3_wrong_ns.mp3": "ತಪ್ಪಾಗಿದೆ. ಇದು ನೈಜ ಪದ. ಮುಂದುವರಿಯಲು ಬಲ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    
    # Practice Trial 4 Feedback (Item 4 is 'auler' -> Made-up word)
    "feedback_4_correct_ns.mp3": "ಸರಿಯಾಗಿದೆ! ಇದು ಕಾಲ್ಪನಿಕ ಪದ. ಮುಂದುವರಿಯಲು ಎಡ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    "feedback_4_wrong_ns.mp3": "ತಪ್ಪಾಗಿದೆ. ಇದು ಕಾಲ್ಪನಿಕ ಪದ. ಮುಂದುವರಿಯಲು ಎಡ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    
    # Practice Trial 5 Feedback (Item 5 is 'hom' -> Made-up word)
    "feedback_5_correct_ns.mp3": "ಸರಿಯಾಗಿದೆ! ಇದು ಕಾಲ್ಪನಿಕ ಪದ. ಮುಂದುವರಿಯಲು ಎಡ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    "feedback_5_wrong_ns.mp3": "ತಪ್ಪಾಗಿದೆ. ಇದು ಕಾಲ್ಪನಿಕ ಪದ. ಮುಂದುವರಿಯಲು ಎಡ ಬಾಣದ ಕೀಲಿ ಒತ್ತಿ.",
    
    # Rest break audio prompts
    "mid_block_1_ns.mp3": "ಉತ್ತಮ ಕೆಲಸ! ನೀವು ಮೊದಲ ಭಾಗವನ್ನು ಅರ್ಧದಷ್ಟು ಮುಗಿಸಿದ್ದೀರಿ. ಸ್ವಲ್ಪ ಸಮಯ ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ ಮತ್ತು ಸಿದ್ಧವಾದಾಗ ಮುಂದುವರಿಯಿರಿ.",
    "mid_block_2_ns.mp3": "ಅದ್ಭುತ! ನೀವು ಎರಡನೇ ಭಾಗವನ್ನು ಅರ್ಧದಷ್ಟು ಮುಗಿಸಿದ್ದೀರಿ. ಸ್ವಲ್ಪ ಸಮಯ ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ ಮತ್ತು ಸಿದ್ಧವಾದಾಗ ಮುಂದುವರಿಯಿರಿ.",
    "mid_block_3_ns.mp3": "ಅತ್ಯುತ್ತಮ ಕೆಲಸ! ನೀವು ಮೂರನೇ ಭಾಗವನ್ನು ಅರ್ಧದಷ್ಟು ಮುಗಿಸಿದ್ದೀರಿ. ಸ್ವಲ್ಪ ಸಮಯ ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ ಮತ್ತು ಸಿದ್ಧವಾದಾಗ ಮುಂದುವರಿಯಿರಿ.",
    
    "end_block_1_ns.mp3": "ಅಭಿನಂದನೆಗಳು! ನೀವು ಮೊದಲ ಭಾಗವನ್ನು ಪೂರ್ಣಗೊಳಿಸಿದ್ದೀರಿ. ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ ಮತ್ತು ಸಿದ್ಧವಾದಾಗ ಮುಂದುವರಿಸಿ.",
    "end_block_2_ns.mp3": "ಅಭಿನಂದನೆಗಳು! ನೀವು ಎರಡನೇ ಭಾಗವನ್ನು ಪೂರ್ಣಗೊಳಿಸಿದ್ದೀರಿ. ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ ಮತ್ತು ಸಿದ್ಧವಾದಾಗ ಮುಂದುವರಿಸಿ.",
    "end_block_general_ns.mp3": "ಅಭಿನಂದನೆಗಳು! ನೀವು ಒಂದು ಭಾಗವನ್ನು ಪೂರ್ಣಗೊಳಿಸಿದ್ದೀರಿ.",
    
    # Completion
    "end_game_ns.mp3": "ಅಭಿನಂದನೆಗಳು! ನೀವು ಏಕ ಪದ ಗುರುತಿಸುವಿಕೆ ಚಟುವಟಿಕೆಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಪೂರ್ಣಗೊಳಿಸಿದ್ದೀರಿ. ಧನ್ಯವಾದಗಳು!"
}

async def generate_file(filename, text):
    out_path = os.path.join(OUTPUT_DIR, filename)
    print(f"Generating: {filename}...")
    communicate = edge_tts.Communicate(text, VOICE, rate="-4%")  # slightly slower for clear child comprehension
    await communicate.save(out_path)
    size = os.path.getsize(out_path)
    print(f" -> Saved {filename} ({size} bytes)")

async def main():
    print(f"Starting Kannada Audio Generation using {VOICE}...")
    for fn, txt in SCRIPTS.items():
        await generate_file(fn, txt)
    print("\nALL 21 KANNADA AUDIO FILES GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())
