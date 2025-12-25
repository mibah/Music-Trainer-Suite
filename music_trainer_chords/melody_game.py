#melody_trainer.py
import math
import time
from utils import NoteUtils
from ui import UI
import pygame
from audio import ChordDetector
from utils import NoteUtils, CHORD_NOTE_MAP  # add CHORD_NOTE_MAP



# ...

class MelodyTrainer:
    def __init__(self, target_chords, lives=1000, timeout=3):
        self.target_chords = target_chords
        self.current_index = 0
        self.lives = lives
        self.timeout = timeout
        self.detector = ChordDetector()
        self.ui = UI()
        self.current_chord_hit = False
        self.last_feedback = ""

    def check_chord(self, detected_chord):
        target = self.target_chords[self.current_index]
        print(f"[DEBUG] Detected: {detected_chord}, Target: {target}")
        if detected_chord == target:
            self.last_feedback = f"Correct! {detected_chord}"
            self.current_chord_hit = True
        else:
            self.last_feedback = f"Got {detected_chord}, need {target}"

    def play(self):
        print("🎹 Starting Chord Trainer...")
        self.detector.start(self.check_chord)

        while self.current_index < len(self.target_chords) and self.lives > 0:
            self.current_chord_hit = False
            current_chord = self.target_chords[self.current_index]
            current_notes = CHORD_NOTE_MAP.get(current_chord, [])

            print(f"\n🎵 Play: {current_chord} (you have {self.lives} lives)")
            start_time = time.time()

            while time.time() - start_time < self.timeout:
                self.ui.draw(current_notes, self.lives, self.last_feedback)
                if self.ui.check_quit():
                    self.detector.stop()
                    return
                if self.current_chord_hit:
                    break
                time.sleep(0.05)

            if self.current_chord_hit:
                self.current_index += 1
            else:
                self.lives -= 1
                self.last_feedback = "Missed!"

        self.detector.stop()
        self.ui.draw([], self.lives, "Game Over" if self.lives == 0 else "Well Done!")
        time.sleep(2)
        pygame.quit()