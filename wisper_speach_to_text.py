import whisper
import os

# Cale completă către fișierul audio
audio_path = r"C:\Users\dan-alexandru.gligor\OneDrive - Accenture\Documents\Sound Recordings\Test.m4a"

# Verificare existență fișier
if not os.path.exists(audio_path):
    raise FileNotFoundError(f"Fișierul nu există: {audio_path}")

# Încarcă modelul Whisper
model = whisper.load_model("base")  # poți schimba cu "small", "medium", "large"

# Rulează transcrierea
print("🔁 Transcriere în curs...")
result = model.transcribe(audio_path, language="ro")

# Scrie în fișier cu alternanță Speaker 1 / Speaker 2
output_path = "transcriere.txt"
with open(output_path, "w", encoding="utf-8") as f:
    speaker = 1
    for segment in result["segments"]:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"].strip()
        f.write(f"[{start:.2f} - {end:.2f}] Speaker {speaker}: {text}\n")
        speaker = 2 if speaker == 1 else 1

print(f"✅ Transcriere finalizată: {output_path}")
