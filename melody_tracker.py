import sounddevice as sd
import numpy as np
import aubio
import time
import math

# ----------------------
# Note / Frequency Utils
# ----------------------

class NoteUtils:
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']

    @staticmethod
    def freq_to_note(freq):
        if freq == 0:
            return None
        A4 = 440
        semitones = 12 * math.log2(freq / A4)
        midi_number = round(69 + semitones)
        note_name = NoteUtils.NOTE_NAMES[midi_number % 12]
        octave = (midi_number // 12) - 1
        return f"{note_name}{octave}"

    @staticmethod
    def note_to_freq(note):
        name = note[:-1]
        octave = int(note[-1])
        A4 = 440
        semitone_index = NoteUtils.NOTE_NAMES.index(name)
        midi_number = (octave + 1) * 12 + semitone_index
        return A4 * 2 ** ((midi_number - 69) / 12)

# ----------------------
# Pitch Detector Wrapper
# ----------------------

class PitchDetector:
    def __init__(self, samplerate=44100, buf_size=1024):
        self.pitch_o = aubio.pitch("default", buf_size*2, buf_size, samplerate)
        self.pitch_o.set_unit("Hz")
        self.pitch_o.set_silence(-100)
        self.samplerate = samplerate
        self.buf_size = buf_size
        self.stream = None

    def start(self, callback):
        def audio_callback(indata, frames, time, status):
            samples = np.mean(indata, axis=1).astype(np.float32)
            pitch = self.pitch_o(samples)[0]
            callback(pitch)

        self.stream = sd.InputStream(callback=audio_callback, channels=1,
                                     samplerate=self.samplerate, blocksize=self.buf_size)
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()

# ----------------------
# Game Logic: Melody Mode
# ----------------------

class MelodyTrainer:
    def __init__(self, target_notes, lives=100, tolerance=0.5, timeout=3):
        self.target_notes = target_notes
        self.current_index = 0
        self.lives = lives
        self.tolerance = tolerance  # in semitones
        self.timeout = timeout
        self.detector = PitchDetector()
        self.current_note_hit = False

    def check_pitch(self, pitch):
        if pitch == 0:
            #print("check_pitch() called pitch = 0")
            return
        print("check_pitch() called")

        detected_note = NoteUtils.freq_to_note(pitch)
        print(f"[DEBUG] Detected pitch: {pitch:.2f} Hz ({detected_note})")

        target_note = self.target_notes[self.current_index]
        target_freq = NoteUtils.note_to_freq(target_note)

        semitone_diff = 12 * math.log2(pitch / target_freq)
        if abs(semitone_diff) <= self.tolerance:
            print(f"✅ Correct! {detected_note} ≈ {target_note}")
            self.current_note_hit = True
        else:
            print(f"🎯 Detected {detected_note} — not quite {target_note}")

    def play(self):
        print("🎹 Starting Melody Trainer...")
        self.detector.start(self.check_pitch)

        while self.current_index < len(self.target_notes) and self.lives > 0:
            self.current_note_hit = False
            current_note = self.target_notes[self.current_index]
            print(f"\n🎵 Play: {current_note} (you have {self.lives} lives)")

            start_time = time.time()
            while time.time() - start_time < self.timeout:
                if self.current_note_hit:
                    break
                time.sleep(0.1)

            if self.current_note_hit:
                self.current_index += 1
            else:
                self.lives -= 1
                print(f"❌ Missed it! Remaining lives: {self.lives}")

        self.detector.stop()
        if self.lives == 0:
            print("\n💀 Game Over!")
        else:
            print("\n🎉 Melody complete! Well done!")

# ----------------------
# Main CLI Runner
# ----------------------

if __name__ == "__main__":
    melody = ["C4", "E4", "G4", "F4", "D4"]
    game = MelodyTrainer(melody)
    game.play()
