import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import time
import numpy as np
import threading
import queue
import os

# Config
DURATION = 5
SAMPLE_RATE = 16000
CHANNELS = 1
NUM_WORKERS = 2

# Cozi și sincronizare
file_queue = queue.Queue()
results_map = {}
results_lock = threading.Lock()
results_ready = threading.Condition(results_lock)

# Stare
record_index = 0
next_to_print = 0

# Model Whisper
model = whisper.load_model("large")

# 🎙️ Thread: Înregistrare audio
def record_loop():
    global record_index
    print("🎙️ Thread înregistrare activ...")

    try:
        while True:
            #print(f"\n🔴 Înregistrare audio ({DURATION} sec)...")
            recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
            sd.wait()

            normalized = np.int16((recording / np.max(np.abs(recording))) * 32767)

            filename = f"recording_{int(time.time()*1000)}.wav"
            filepath = os.path.join("Recordings", filename)

            write(filepath, SAMPLE_RATE, normalized)

            file_queue.put((record_index, filepath))
            #print(f"📁 Fișier salvat: {filepath} [index={record_index}]")
            record_index += 1

    except Exception as e:
        print(f"❌ Eroare la înregistrare: {e}")

# 🧠 Thread: Worker de transcriere
def transcribe_worker(worker_id):
    print(f"🧠 Worker-{worker_id} activ...")

    while True:
        try:
            index, path = file_queue.get()
            #print(f"👷 Worker-{worker_id} prelucrează [index={index}]")

            result = model.transcribe(path, language="ro", fp16=False, temperature=0)

            os.remove(path)

            with results_ready:
                results_map[index] = result["text"]
                results_ready.notify_all()

        except Exception as e:
            print(f"❌ Worker-{worker_id} eroare: {e}")

# 🖨️ Thread: Afișare în ordine
def print_loop():
    global next_to_print
    #print("🖨️ Thread afișare activ...")

    while True:
        with results_ready:
            while next_to_print not in results_map:
                results_ready.wait()

            print(f"\n📄 [{next_to_print}] {results_map[next_to_print]}")
            del results_map[next_to_print]
            next_to_print += 1

# Pornire fire
threading.Thread(target=record_loop, daemon=True).start()

for i in range(NUM_WORKERS):
    threading.Thread(target=transcribe_worker, args=(i+1,), daemon=True).start()

threading.Thread(target=print_loop, daemon=True).start()

# Ține programul activ
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n⏹️ Program oprit manual.")
