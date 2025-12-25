# melody_game.py (ENHANCED VERSION)
import math
import time
from audio import PitchDetector
from utils import NoteUtils
from ui import UI
import pygame
import serial
import serial.tools.list_ports


class MelodyTrainer:
    def __init__(self, target_notes, lives=1000, tolerance=0.5, timeout=3,
                 use_arduino=False, arduino_port=None):
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

        # Arduino LED integration
        self.use_arduino = use_arduino
        self.arduino = None
        if self.use_arduino:
            self.connect_arduino(arduino_port)

    def connect_arduino(self, port=None):
        """Connect to Arduino for LED control"""
        try:
            if port is None:
                # Auto-detect Arduino
                ports = serial.tools.list_ports.comports()
                for p in ports:
                    if 'Arduino' in p.description or 'USB' in p.description:
                        port = p.device
                        break

            if port is None:
                print("⚠️  No Arduino found. LED features disabled.")
                self.use_arduino = False
                return

            self.arduino = serial.Serial(port, 115200, timeout=1)
            time.sleep(2)  # Wait for Arduino reset
            print(f"✓ Arduino connected on {port}")

            # Send command to switch to Trainer mode (Mode 3)
            self.arduino.write(b"M3\n")
            time.sleep(0.5)

        except Exception as e:
            print(f"⚠️  Arduino connection failed: {e}")
            self.use_arduino = False
            self.arduino = None

    def note_to_led(self, note):
        """Convert note name to LED index (matching your LED strip mapping)"""
        # Your LED strip: 60 LEDs for MIDI notes 36 (C2) to 96 (C7)
        NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

        try:
            name = note[:-1]
            octave = int(note[-1])
            semitone_index = NOTE_NAMES.index(name)
            midi_number = (octave + 1) * 12 + semitone_index

            # Map to LED range (36-96 -> 0-59)
            MIDI_START = 36  # C2
            MIDI_END = 96  # C7
            NUM_LEDS = 60

            if midi_number < MIDI_START or midi_number > MIDI_END:
                return None

            led_index = int((midi_number - MIDI_START) * NUM_LEDS / (MIDI_END - MIDI_START + 1))
            return min(led_index, NUM_LEDS - 1)
        except:
            return None

    def send_target_note(self, note):
        """Send target note to Arduino to light up the LED"""
        if not self.use_arduino or self.arduino is None:
            return

        led_index = self.note_to_led(note)
        if led_index is not None:
            # Format: "T<LED_INDEX>\n" for Target note
            command = f"T{led_index}\n"
            self.arduino.write(command.encode())

    def send_played_note(self, note, correct=False):
        """Send played note to Arduino with success/failure indicator"""
        if not self.use_arduino or self.arduino is None:
            return

        led_index = self.note_to_led(note)
        if led_index is not None:
            # Format: "P<LED_INDEX>,<CORRECT>\n" for Played note
            # CORRECT: 1 = correct, 0 = incorrect
            command = f"P{led_index},{1 if correct else 0}\n"
            self.arduino.write(command.encode())

    def clear_leds(self):
        """Clear all LEDs"""
        if self.use_arduino and self.arduino is not None:
            self.arduino.write(b"C\n")

    def check_pitch(self, pitch):
        target_note = self.target_notes[self.current_index]
        target_freq = NoteUtils.note_to_freq(target_note)

        if pitch == 0:
            return

        detected_note = NoteUtils.freq_to_note(pitch)
        semitone_diff = 12 * math.log2(pitch / target_freq)

        print(f"[DEBUG] Detected: {pitch:.2f} Hz -> {detected_note}, target: {target_note}")

        if abs(semitone_diff) <= self.tolerance:
            self.last_feedback = f"Correct! {detected_note}"
            self.current_note_hit = True
            # Send correct note feedback to Arduino
            self.send_played_note(detected_note, correct=True)
        else:
            self.last_feedback = f"Not {target_note}, got {detected_note}"
            # Send incorrect note feedback to Arduino
            self.send_played_note(detected_note, correct=False)

    def play(self):
        print("🎹 Starting Melody Trainer...")
        if self.use_arduino:
            print("🔵 Arduino LED mode active")

        self.detector.start(self.check_pitch)

        while self.current_index < len(self.target_notes) and self.lives > 0:
            self.current_note_hit = False
            current_note = self.target_notes[self.current_index]
            print(f"\n🎵 Play: {current_note} (you have {self.lives} lives)")

            # Send target note to Arduino
            self.send_target_note(current_note)

            start_time = time.time()

            while time.time() - start_time < self.timeout:
                self.ui.draw(current_note, self.lives, self.last_feedback)

                if self.ui.check_quit():
                    self.detector.stop()
                    self.clear_leds()
                    if self.arduino:
                        self.arduino.close()
                    return

                if self.current_note_hit:
                    time.sleep(1.5)  # Pause after correct note
                    break

                time.sleep(0.05)

            if self.current_note_hit:
                self.current_index += 1
            else:
                self.lives -= 1
                self.last_feedback = "Missed!"

        self.detector.stop()
        self.ui.draw("Done", self.lives, "Game Over" if self.lives == 0 else "Well Done!")

        # Cleanup
        if self.use_arduino and self.arduino:
            self.clear_leds()
            self.arduino.close()

        time.sleep(2)
        pygame.quit()


# Updated main.py
if __name__ == "__main__":
    notes = [
        "A4", "B4", "C5", "A4", "C5", "C5", "B4", "A4", "B4", "E4",
        "B4", "C5", "D5", "B4", "D5", "D5", "C5", "B4", "A4", "E5",
        "A5", "G5", "A5", "G5", "F5", "F5", "E5", "D5", "E5", "A4",
        "F5", "D5", "E5", "C5", "B4", "E4", "C5", "B4", "A4"
    ]

    # Enable Arduino LED support
    # Set arduino_port=None for auto-detection, or specify like '/dev/cu.usbmodem1401'
    trainer = MelodyTrainer(notes, use_arduino=True, arduino_port=None)
    trainer.play()