#utils.py for chords
import math

CHORD_NOTE_MAP = {
    "C": ["C4", "E4", "G4"],
    "Am": ["A3", "C4", "E4"],
    "G": ["G3", "B3", "D4"],
    "D": ["D4", "F#4", "A4"],
    # Add more chords as needed
}


class NoteUtils:
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']

    @staticmethod
    def freq_to_note(freq):
        """Convert a frequency in Hz to a note name like C4."""
        if freq == 0 or freq is None:
            return None
        A4 = 440
        semitones = 12 * math.log2(freq / A4)
        midi_number = round(69 + semitones)
        note_name = NoteUtils.NOTE_NAMES[midi_number % 12]
        octave = (midi_number // 12) - 1
        return f"{note_name}{octave}"

    @staticmethod
    def note_to_freq(note):
        """Convert a note name like C4 to frequency in Hz."""
        if isinstance(note, list):
            return [NoteUtils.note_to_freq(n) for n in note]

        name = note[:-1]
        octave = int(note[-1])

        if name not in NoteUtils.NOTE_NAMES:
            raise ValueError(f"Invalid note name: {note}")

        A4 = 440
        semitone_index = NoteUtils.NOTE_NAMES.index(name)
        midi_number = (octave + 1) * 12 + semitone_index
        return A4 * 2 ** ((midi_number - 69) / 12)

    @staticmethod
    def chord_match(detected_notes, target_chord, tolerance_semitones=0.5):
        """
        Check whether all notes in the target chord are present (within tolerance).
        Returns True if all chord notes are matched by the detected notes.
        """
        detected_set = set(detected_notes)
        matched = 0

        for target_note in target_chord:
            for detected_note in detected_set:
                if NoteUtils.note_name_close(detected_note, target_note, tolerance_semitones):
                    matched += 1
                    break

        return matched == len(target_chord)

    @staticmethod
    def note_name_close(detected, target, tolerance_semitones):
        """Check if two note names are within a pitch tolerance."""
        detected_freq = NoteUtils.note_to_freq(detected)
        target_freq = NoteUtils.note_to_freq(target)
        if detected_freq == 0 or target_freq == 0:
            return False
        diff = abs(12 * math.log2(detected_freq / target_freq))
        return diff <= tolerance_semitones
