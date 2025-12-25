#melody_trainer.py
import math
import time
from audio import PitchDetector
from utils import NoteUtils
from ui import UI
import pygame

class ChordTrainer:
    def __init__(self, target_chords, lives=1000, tolerance=0.5, timeout=5):
        self.target_chords = target_chords
        self.current_index = 0
        self.lives = lives
        self.tolerance = tolerance
        self.timeout = timeout
        self.detector = PitchDetector()
        self.ui = UI()
        self.detected_notes = set()
        self.last_feedback = ""

    def check_pitch(self, pitch):
        if pitch == 0:
            return

        detected_note = NoteUtils.freq_to_note(pitch)
        current_chord = self.target_chords[self.current_index]

        if detected_note is None:
            return

        if detected_note in current_chord and detected_note not in self.detected_notes:
            self.detected_notes.add(detected_note)
            self.last_feedback = f"✔ Detected {detected_note}"
            print(f"[DEBUG] Detected chord note: {detected_note}")
        else:
            self.last_feedback = f"✘ Got {detected_note}"
            print(f"[DEBUG] Wrong or repeated note: {detected_note}")

        print(f"[DEBUG] Detected so far: {self.detected_notes} / Target: {current_chord}")

    def play(self):
        print("🎹 Starting Chord Trainer...")
        self.detector.start(self.check_pitch)

        while self.current_index < len(self.target_chords) and self.lives > 0:
            self.detected_notes = set()
            current_chord = self.target_chords[self.current_index]
            print(f"\n🎵 Play: {current_chord} (you have {self.lives} lives)")
            start_time = time.time()

            while time.time() - start_time < self.timeout:
                self.ui.draw(current_chord, self.lives, self.last_feedback)
                if self.ui.check_quit():
                    self.detector.stop()
                    return
                if set(current_chord) == self.detected_notes:
                    break
                time.sleep(0.05)

            if set(current_chord) == self.detected_notes:
                self.current_index += 1
            else:
                self.lives -= 1
                self.last_feedback = "Missed some notes!"

        self.detector.stop()
        self.ui.draw("Done", self.lives, "Game Over" if self.lives == 0 else "Well Done!")
        time.sleep(2)
        pygame.quit()
