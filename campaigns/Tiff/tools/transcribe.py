"""Whisper transcript for QA. Usage: python transcribe.py clip.mp4 [--words]
PyAV is broken on this machine, so audio is piped as 16 kHz mono PCM from ffmpeg."""
import subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

path = sys.argv[1]
words = "--words" in sys.argv
pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
model = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = model.transcribe(audio, language="en", word_timestamps=words)
for s in segs:
    print(f"[{s.start:5.2f}-{s.end:5.2f}] {s.text.strip()}")
    if words:
        for w in s.words:
            print(f"    {w.start:5.2f}-{w.end:5.2f} {w.word.strip()}")
