# main.py
from melody_game import MelodyTrainer

if __name__ == "__main__":
    notes = [
        "A4", "B4", "C4", "A4", "C4", "C4", "B4", "A4", "B4", "E4",
        "B4", "C4", "D4", "B4", "D4", "D4", "C4", "B4", "A4", "E4",
        "A4", "G4", "A4", "G4", "F4", "F4", "E4", "D4", "E4", "A4",
        "F4", "D4", "E4", "C4", "B4", "E4", "C4", "B4", "A4"
    ]
    trainer = MelodyTrainer(notes)
    trainer.play()