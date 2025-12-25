# main.py
from melody_game import MelodyTrainer

if __name__ == "__main__":
    notes = [
        "A4", "B4", "C5", "A4", "C5", "C5", "B4", "A4", "B4", "E4",
        "B4", "C5", "D5", "B4", "D5", "D5", "C5", "B4", "A4", "E5",
        "A5", "G5", "A5", "G5", "F5", "F5", "E5", "D5", "E5", "A4",
        "F5", "D5", "E5", "C5", "B4", "E4", "C5", "B4", "A4"
    ]
    trainer = MelodyTrainer(notes)
    trainer.play()