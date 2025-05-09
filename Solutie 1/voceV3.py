import asyncio
import edge_tts
import os
from datetime import datetime

class RomanianSpeaker:
    def __init__(self, voice="ro-RO-AlinaNeural"): #ro-RO-EmilNeural
        self.voice = voice
        self.output_folder = "Recordings"
        os.makedirs(self.output_folder, exist_ok=True)

    async def to_voice_async(self, text):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.output_folder, f"voice_{timestamp}.mp3")

        communicate = edge_tts.Communicate(text=text, voice=self.voice)
        await communicate.save(path)

        # Redare (doar pe Windows, prin pygame)
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        print(f"✅ Salvat și redat: {path}")

    def to_voice(self, text):
        asyncio.run(self.to_voice_async(text))
