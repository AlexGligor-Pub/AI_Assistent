import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import time
import numpy as np
import threading
import os
import tkinter as tk
from tkinter import scrolledtext, Toplevel
from olama_aya import prompt_aya
from voceV3 import RomanianSpeaker
from tkhtmlview import HTMLLabel
import webbrowser
import tempfile

SAMPLE_RATE = 16000
CHANNELS = 1
model = whisper.load_model("large")

is_recording = False
recording_thread = None

def start_recording_thread():
    global is_recording

    def record_loop():
        while is_recording:
            timings = []  # listă pentru timpii fiecărei operații

            t1 = time.perf_counter()
            recording = sd.rec(int(5 * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
            sd.wait()
            t2 = time.perf_counter()
            timings.append(f"Înregistrare: {t2 - t1:.2f}s")

            t1 = time.perf_counter()
            normalized = np.int16((recording / np.max(np.abs(recording))) * 32767)
            filename = f"recording_{int(time.time()*1000)}.wav"
            os.makedirs("Recordings", exist_ok=True)
            filepath = os.path.join("Recordings", filename)
            write(filepath, SAMPLE_RATE, normalized)
            t2 = time.perf_counter()
            timings.append(f"Normalizare + Salvare: {t2 - t1:.2f}s")

            t1 = time.perf_counter()
            result = model.transcribe(filepath, language="ro", fp16=False, temperature=0)
            os.remove(filepath)
            t2 = time.perf_counter()
            timings.append(f"Transcriere: {t2 - t1:.2f}s")

            transcribed_text = result['text']
            output_text.insert(tk.END, f"Text transcris: {transcribed_text}\n")

            try:
                label.config(text="Intreaba AI-ul")
                t1 = time.perf_counter()
                ai_response = prompt_aya(transcribed_text)
                t2 = time.perf_counter()
                timings.append(f"Prompt AI: {t2 - t1:.2f}s")

                label.config(text="Afiseaza raspunsul")
                output_text.insert(tk.END, f"AI răspunde: {ai_response}\n\n")
                t1 = time.perf_counter()
                afiseaza_html(str(ai_response))

                
                #speaker = RomanianSpeaker()
                #speaker.to_voice(ai_response)
                t2 = time.perf_counter()
                timings.append(f"Text to Speech: {t2 - t1:.2f}s")

            except Exception as e:
                output_text.insert(tk.END, f"Eroare AI: {e}\n\n")


            # Afișare timpi
            timing_text.delete(1.0, tk.END)
            for line in timings:
                timing_text.insert(tk.END, line + '\n')

            output_text.yview(tk.END)

    global recording_thread
    recording_thread = threading.Thread(target=record_loop, daemon=True)
    recording_thread.start()

# Afișează într-o fereastră HTML
#def afiseaza_html(raspuns):
    #html_win = Toplevel(root)
    #html_win.title("Rezultat HTML")
    #label = HTMLLabel(html_win, html=f"{raspuns}", width=80)
    #label.pack(padx=10, pady=10)
def afiseaza_html(raspuns):
    # Crează un fișier HTML temporar
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_file:
        temp_file.write(raspuns.encode('utf-8'))

    # Deschide fișierul HTML în browser
    webbrowser.open_new_tab(temp_file.name)

def record_audio():
    global is_recording
    if is_recording:
        is_recording = False
        label.config(text="Astept inregistrarea")
        record_button.config(text="Start Recording")
    else:
        is_recording = True
        record_button.config(text="Stop Recording")
        label.config(text="Procesare inregistrare")
        start_recording_thread()

# Interfață grafică
root = tk.Tk()
root.title("Înregistrare și Transcriere AI")

label = tk.Label(root, text="Astept inregistrarea!")
label.pack(pady=5)

record_button = tk.Button(root, text="Start Recording", command=record_audio, width=20)
record_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
output_text.pack(pady=10)

timing_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=7)
timing_text.pack(pady=5)
timing_text.insert(tk.END, "Timpul fiecărei operații va apărea aici...\n")

root.mainloop()
