#audio.py for chords
import sounddevice as sd
import numpy as np
import threading
import librosa

class ChordDetector:
    def __init__(self, samplerate=22050, duration=1.0):
        self.samplerate = samplerate
        self.duration = duration
        self.buffer = []
        self.lock = threading.Lock()
        self.chord_callback = None
        self.stream = None

    def start(self, callback):
        self.chord_callback = callback
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.samplerate)
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        with self.lock:
            self.buffer.append(indata.copy())

        # If we've collected enough time, analyze it
        total_frames = int(self.duration * self.samplerate)
        flat_buffer = np.concatenate(self.buffer, axis=0).flatten()
        if len(flat_buffer) >= total_frames:
            self.buffer = []  # Reset buffer
            self.detect_chord(flat_buffer[:total_frames])

    def detect_chord(self, audio):
        audio = audio.astype(np.float32)

        if np.max(np.abs(audio)) < 0.02:
            print("[DEBUG] Ignored low-volume input")
            return

        chroma = librosa.feature.chroma_stft(y=audio, sr=self.samplerate)
        chroma_mean = np.mean(chroma, axis=1)

        detected_chord = match_chord(chroma_mean)
        print(f"[DEBUG] Chromagram: {chroma_mean.round(2)} -> Chord: {detected_chord}")
        if detected_chord and self.chord_callback:
            self.chord_callback(detected_chord)

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()

# --- Chord matching (very simple)

CHORD_TEMPLATES = {
    "C": [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],  # C, E, G
    "D": [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # D, F#, A
    "G": [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],  # G, B, D
    "Am": [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], # A, C, E
    # Add more chords...
}

def match_chord(chroma_vector, threshold=0.8):
    scores = {}
    for chord, template in CHORD_TEMPLATES.items():
        score = np.dot(chroma_vector, template)
        scores[chord] = score

    best_chord = max(scores, key=scores.get)
    if scores[best_chord] < threshold:
        print(f"[DEBUG] Low confidence ({scores[best_chord]:.2f}) — skipping")
        return None
    return best_chord
