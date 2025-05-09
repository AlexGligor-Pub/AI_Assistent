import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import time
import numpy as np

# Setări
duration = 7  # mai mult context = mai bine
sample_rate = 16000
channels = 1

# Încarcă cel mai precis model Whisper
model = whisper.load_model("large")  # sau "large-v3"

print("🎙️ Transcriere live cu acuratețe maximă... Ctrl+C pentru oprire.")

try:
    while True:
        print(f"\n🔴 Înregistrare audio ({duration} sec)...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
        sd.wait()

        # Normalizează volumul
        audio_normalized = np.int16((recording / np.max(np.abs(recording))) * 32767)

        # Salvează temporar
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            write(temp_wav.name, sample_rate, audio_normalized)
            result = model.transcribe(
                temp_wav.name,
                language="ro",
                fp16=False,          # important pentru CPU
                temperature=0        # stabilitate, fără variații inutile
            )
            print(f"📄 {result['text']}")

except KeyboardInterrupt:
    print("\n⏹️ Transcriere oprită manual.")
