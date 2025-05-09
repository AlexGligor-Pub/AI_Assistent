from gtts import gTTS
from pydub import AudioSegment
import pygame
import time
import os
from datetime import datetime

class RomanianSpeaker:
    def __init__(self, speed=1.0):
        self.output_folder = "Recordings"
        os.makedirs(self.output_folder, exist_ok=True)
        self.speed = speed
        pygame.mixer.init()

    def change_speed(self, sound, speed=1.0):
        new_frame_rate = int(sound.frame_rate * speed)
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_frame_rate}).set_frame_rate(sound.frame_rate)

    def to_voice(self, text):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_{timestamp}.mp3"
        path = os.path.join(self.output_folder, filename)

        # Generează fișierul audio
        tts = gTTS(text=text, lang='ro')
        tts.save(path)

        # Modifică viteza
        sound = AudioSegment.from_file(path)
        if self.speed != 1.0:
            sound = self.change_speed(sound, self.speed)
            sound.export(path, format="mp3")

        # Redă
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        print(f"✅ Fișierul a fost salvat: {path}")

speaker = RomanianSpeaker(speed=1)
speaker.to_voice("Aceasta este o voce mai rapidă decât normal.")