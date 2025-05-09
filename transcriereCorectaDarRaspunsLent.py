import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import time
import numpy as np
import threading
import queue
import os

# Setări
duration = 5  # secunde
sample_rate = 16000
channels = 1
file_queue = queue.Queue()

# Încarcă modelul Whisper
model = whisper.load_model("large")  # sau "medium" dacă vrei mai rapid

def record_loop():
    print("🎙️ Thread de înregistrare activ...")

    try:
        while True:
            #print(f"\n🔴 Înregistrare audio ({duration} sec)...")
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
            sd.wait()

            # Normalizează volumul
            normalized = np.int16((recording / np.max(np.abs(recording))) * 32767)

            # Creează un nume de fișier cu timestamp
            filename = f"recording_{int(time.time()*1000)}.wav"
            filepath = os.path.join("Recordings", filename)

            # Scrie fișierul WAV
            write(filepath, sample_rate, normalized)
            file_queue.put(filepath)  # adaugă în coadă
            #print(f"📁 Fișier salvat: {filepath}")
    except Exception as e:
        print(f"❌ Eroare în threadul de înregistrare: {e}")

def transcribe_loop():
    print("🧠 Thread de transcriere activ...")

    while True:
        try:
            audio_path = file_queue.get()  # blochează până apare un fișier
            #print(f"📂 Procesare: {audio_path}")

            result = model.transcribe(
                audio_path,
                language="ro",
                fp16=False,
                temperature=0
            )
            print(f"\n📄{result['text']}")

            os.remove(audio_path)
            #print(f"🗑️ Fișier șters: {audio_path}")
        except Exception as e:
            print(f"❌ Eroare la transcriere: {e}")

# Pornește thread-urile
rec_thread = threading.Thread(target=record_loop, daemon=True)
trans_thread = threading.Thread(target=transcribe_loop, daemon=True)

rec_thread.start()
trans_thread.start()

# Menține aplicația activă
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n⏹️ Oprit manual. Thread-urile se vor închide.")
