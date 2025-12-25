#melody_trainer.py
import math
import time
from audio import PitchDetector
from utils import NoteUtils
from ui import UI
import pygame

class MelodyTrainer:
    def __init__(self, target_notes, lives=1000, tolerance=0.5, timeout=3):
        self.target_notes = target_notes
        self.current_index = 0
        self.lives = lives
        self.tolerance = tolerance
        self.timeout = timeout
        self.detector = PitchDetector()
        self.ui = UI()
        self.current_note_hit = False
        self.last_feedback = ""
        self.last_update_time = time.time()

    def check_pitch(self, pitch):
        target_note = self.target_notes[self.current_index]
        target_freq = NoteUtils.note_to_freq(target_note)

        if pitch == 0:
            print("[DEBUG] Pitch too low or not detected (0 Hz)")
            return

        detected_note = NoteUtils.freq_to_note(pitch)
        semitone_diff = 12 * math.log2(pitch / target_freq)

        print(f"[DEBUG] Detected pitch: {pitch:.2f} Hz -> {detected_note}, target: {target_note}")

        if abs(semitone_diff) <= self.tolerance:
            self.last_feedback = f"Correct! {detected_note}"
            self.current_note_hit = True
        else:
            self.last_feedback = f"Not {target_note}, got {detected_note}"

    def play(self):
        print("🎹 Starting Melody Trainer...")
        self.detector.start(self.check_pitch)

        while self.current_index < len(self.target_notes) and self.lives > 0:
            self.current_note_hit = False
            current_note = self.target_notes[self.current_index]
            print(f"\n🎵 Play: {current_note} (you have {self.lives} lives)")
            start_time = time.time()

            while time.time() - start_time < self.timeout:
                self.ui.draw(current_note, self.lives, self.last_feedback)
                time.sleep(1.5)  # Add this line for a pause after the correct note
                if self.ui.check_quit():
                    self.detector.stop()
                    return
                if self.current_note_hit:
                    break
                time.sleep(0.05)

            if self.current_note_hit:
                self.current_index += 1
            else:
                self.lives -= 1
                self.last_feedback = "Missed!"

        self.detector.stop()
        self.ui.draw("Done", self.lives, "Game Over" if self.lives == 0 else "Well Done!")
        time.sleep(2)
        pygame.quit()
