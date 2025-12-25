# ui.py
import pygame
from pygame import freetype

pygame.init()

SCALE = 0.58
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 0, 0)

BASE_KEY_WIDTH = 60
BASE_KEY_HEIGHT = 250
KEY_WIDTH = int(BASE_KEY_WIDTH * SCALE)
KEY_HEIGHT = int(BASE_KEY_HEIGHT * SCALE)

FONT_SIZE = int(24 * SCALE)
FONT = freetype.SysFont("Arial", int(FONT_SIZE))

WHITE_NOTES = [
    "C1", "D1", "E1", "F1", "G1", "A1", "B1",
    "C2", "D2", "E2", "F2", "G2", "A2", "B2",
    "C3", "D3", "E3", "F3", "G3", "A3", "B3",
    "C4", "D4", "E4", "F4", "G4", "A4", "B4",
    "C5", "D5", "E5", "F5", "G5", "A5", "B5",
    "C6", "D6", "E6", "F6", "G6", "A6", "B6"
]

BLACK_NOTES = {
    "C#1": 0, "D#1": 1, "F#1": 3, "G#1": 4, "A#1": 5,
    "C#2": 7, "D#2": 8, "F#2": 10, "G#2": 11, "A#2": 12,
    "C#3": 14, "D#3": 15, "F#3": 17, "G#3": 18, "A#3": 19,
    "C#4": 21, "D#4": 22, "F#4": 24, "G#4": 25, "A#4": 26,
    "C#5": 28, "D#5": 29, "F#5": 31, "G#5": 32, "A#5": 33,
    "C#6": 35, "D#6": 36, "F#6": 38, "G#6": 39, "A#6": 40,
}

SCREEN_WIDTH = KEY_WIDTH * len(WHITE_NOTES)
SCREEN_HEIGHT = KEY_HEIGHT

class UI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def draw_piano(self, highlighted_notes):
        if isinstance(highlighted_notes, str):
            highlighted_notes = [highlighted_notes]

        white_key_positions = {}

        # Draw white keys
        for i, note in enumerate(WHITE_NOTES):
            x = i * KEY_WIDTH
            white_key_positions[note] = x
            color = HIGHLIGHT_COLOR if note in highlighted_notes else WHITE
            pygame.draw.rect(self.screen, color, (x, SCREEN_HEIGHT - KEY_HEIGHT, KEY_WIDTH, KEY_HEIGHT))
            pygame.draw.rect(self.screen, BLACK, (x, SCREEN_HEIGHT - KEY_HEIGHT, KEY_WIDTH, KEY_HEIGHT), 2)
            FONT.render_to(self.screen, (x + int(5 * SCALE), SCREEN_HEIGHT - int(30 * SCALE)), note, BLACK)

        # Draw black keys
        for note, index in BLACK_NOTES.items():
            if index < len(WHITE_NOTES):
                x = white_key_positions[WHITE_NOTES[index]] + int(KEY_WIDTH * 0.75)
                color = HIGHLIGHT_COLOR if note in highlighted_notes else BLACK
                pygame.draw.rect(self.screen, color, (x, SCREEN_HEIGHT - KEY_HEIGHT, KEY_WIDTH // 2, int(KEY_HEIGHT * 0.6)))
                FONT.render_to(self.screen, (x + int(2 * SCALE), SCREEN_HEIGHT - KEY_HEIGHT + int(5 * SCALE)), note, WHITE)

    def draw(self, current_notes, lives, feedback):
        self.screen.fill(WHITE)
        self.draw_piano(current_notes)
        pygame.display.flip()
        self.clock.tick(60)

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def get_note_from_position(self, x_pos):
        key_index = x_pos // KEY_WIDTH
        if key_index < len(WHITE_NOTES):
            return WHITE_NOTES[key_index]
        return None
