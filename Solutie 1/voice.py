from gtts import gTTS
import pygame
import time
import os
from datetime import datetime

class RomanianSpeaker:
    def __init__(self):
        self.output_folder = "Recordings"
        os.makedirs(self.output_folder, exist_ok=True)
        pygame.mixer.init()

    def to_voice(self, text):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_{timestamp}.mp3"
        path = os.path.join(self.output_folder, filename)

        # Generează fișierul audio
        tts = gTTS(text=text, lang='ro')
        tts.save(path)

        # Redă fișierul
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        print(f"✅ Fișierul a fost salvat: {path}")


speaker = RomanianSpeaker()
speaker.to_voice("Salut, Alex! Aceasta este o voce generată de Google.")