import pygame
from pygame import freetype

# Initialize pygame
pygame.init()

# Define scaling factor (1.0 = original size)
SCALE = 1.5

# Define constants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 0, 0)  # Red highlight for played key

# Define piano key size (scaled)
BASE_KEY_WIDTH = 60
BASE_KEY_HEIGHT = 200
KEY_WIDTH = int(BASE_KEY_WIDTH * SCALE)
KEY_HEIGHT = int(BASE_KEY_HEIGHT * SCALE)

# Define font (scaled)
FONT_SIZE = int(24)
FONT = freetype.SysFont("Arial", FONT_SIZE)

# Calculate screen size (7 white keys)
SCREEN_WIDTH = KEY_WIDTH * 7
SCREEN_HEIGHT = KEY_HEIGHT

class UI:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def draw_piano(self, current_note):
        """Draw the piano with the highlighted key based on the current note."""
        white_notes = ["C4", "D4", "E4", "F4", "G4", "A4", "B4"]
        black_notes = {
            "C#4": 0,
            "D#4": 1,
            "F#4": 3,
            "G#4": 4,
            "A#4": 5
        }

        white_key_positions = []

        # Draw white keys
        for i, note in enumerate(white_notes):
            x = i * KEY_WIDTH
            white_key_positions.append((note, x))

            color = HIGHLIGHT_COLOR if note == current_note else WHITE
            pygame.draw.rect(self.screen, color, (x, SCREEN_HEIGHT - KEY_HEIGHT, KEY_WIDTH, KEY_HEIGHT))
            pygame.draw.rect(self.screen, BLACK, (x, SCREEN_HEIGHT - KEY_HEIGHT, KEY_WIDTH, KEY_HEIGHT), 2)

            FONT.render_to(self.screen, (x + int(5 * SCALE), SCREEN_HEIGHT - int(30 * SCALE)), note, BLACK)

        # Draw black keys
        for note, index in black_notes.items():
            x = white_key_positions[index][1] + int(KEY_WIDTH * 0.75)

            color = HIGHLIGHT_COLOR if note == current_note else BLACK
            pygame.draw.rect(self.screen, color, (x, SCREEN_HEIGHT - KEY_HEIGHT, KEY_WIDTH // 2, int(KEY_HEIGHT * 0.6)))

            FONT.render_to(self.screen, (x + int(2 * SCALE), SCREEN_HEIGHT - KEY_HEIGHT + int(5 * SCALE)), note, WHITE)

    def draw(self, current_note, lives, feedback):
        self.screen.fill(WHITE)
        self.draw_piano(current_note)
        #FONT.render_to(self.screen, (int(10 * SCALE), int(10 * SCALE)), f"Lives: {lives}", BLACK)
        #FONT.render_to(self.screen, (int(10 * SCALE), int(40 * SCALE)), feedback, BLACK)
        pygame.display.flip()
        self.clock.tick(60)

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False


if __name__ == "__main__":
    ui = UI()
    current_note = "C#4"
    running = True
    while running:
        ui.draw(current_note, lives=5, feedback="Good job!")
        if ui.check_quit():
            running = False
    pygame.quit()
