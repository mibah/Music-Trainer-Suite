# main.py
from melody_game import ChordTrainer

if __name__ == "__main__":
    chords = [
        ["C4", "E4", "G4"],   # C major
        ["A3", "C4", "E4"],   # A minor
        ["D4", "F#4", "A4"],  # D major
        ["E4", "G4", "B4"],   # E minor
        ["F4", "A4", "C5"]    # F major
    ]
    trainer = ChordTrainer(chords)
    trainer.play()