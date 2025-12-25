# utils.py for arppeggios
import math

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