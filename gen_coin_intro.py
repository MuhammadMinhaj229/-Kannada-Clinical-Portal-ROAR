import asyncio
import edge_tts
import shutil
import os

async def gen():
    voice = "kn-IN-SapnaNeural"
    text = "ಅದ್ಭುತ! ನೀವು ಚಿನ್ನದ ನಾಣ್ಯವನ್ನು ಗಳಿಸಿದ್ದೀರಿ!"
    out_path = r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/public/audio/kn/desktop/coin_intro.mp3'
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_path)
    print("Synthesized coin_intro.mp3 successfully!")
    
    # Mirror to en/desktop as well
    en_path = r'C:/Users/User/.gemini/antigravity/scratch/roar-word-replica/public/audio/en/desktop/coin_intro.mp3'
    shutil.copyfile(out_path, en_path)
    print("Mirrored to en/desktop!")

asyncio.run(gen())
