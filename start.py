import pygame
import sys
import subprocess
import json

class SettingsManager:
    def __init__(self, filename):
        self.filename = filename
        self.settings = {}

    def load_settings(self):
        try:
            with open(self.filename, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            self.settings = {}  # Initialize with default settings

    def save_settings(self):
        with open(self.filename, 'w') as file:
            json.dump(self.settings, file)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
settings_man = SettingsManager('settings.json')

# Fonts
font = pygame.font.Font(None, 22)


def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


def start_main():
    subprocess.Popen(["python3", "main.py"])  # Start main.py as a separate process

def options_menu(screen, settings_manager):
    # Initialize Pygame
    pygame.init()


    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (65, 105, 225)

    # Define fonts
    font = pygame.font.SysFont('Arial', 24)

    running = True
    water_amount = settings_manager.get_setting("water_amount", 50)
    tree_amount = settings_manager.get_setting("tree_amount", 50)
    mountain_amount = settings_manager.get_setting("mountain_amount", 50)

    slider_width = 200
    slider_height = 20
    slider_x = 150
    slider_y = 200
    knob_radius = 10

    water_knob_x = int(slider_x + (slider_width - knob_radius * 2) * (water_amount / 100))
    tree_knob_x = int(slider_x + (slider_width - knob_radius * 2) * (tree_amount / 100))
    mountain_knob_x = int(slider_x + (slider_width - knob_radius * 2) * (mountain_amount / 100))

    water_knob_y = tree_knob_y = mountain_knob_y = slider_y - knob_radius

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if pygame.Rect(slider_x, slider_y, slider_width, slider_height).collidepoint(event.pos):
                        # Update slider position based on mouse click
                        knob_x = event.pos[0]
                        if knob_x < slider_x:
                            knob_x = slider_x
                        elif knob_x > slider_x + slider_width:
                            knob_x = slider_x + slider_width
                        water_amount = int((knob_x - slider_x) / slider_width * 100)
                        water_knob_x = knob_x
                    elif pygame.Rect(slider_x, slider_y + 100, slider_width, slider_height).collidepoint(event.pos):
                        knob_x = event.pos[0]
                        if knob_x < slider_x:
                            knob_x = slider_x
                        elif knob_x > slider_x + slider_width:
                            knob_x = slider_x + slider_width
                        tree_amount = int((knob_x - slider_x) / slider_width * 100)
                        tree_knob_x = knob_x
                    elif pygame.Rect(slider_x, slider_y + 200, slider_width, slider_height).collidepoint(event.pos):
                        knob_x = event.pos[0]
                        if knob_x < slider_x:
                            knob_x = slider_x
                        elif knob_x > slider_x + slider_width:
                            knob_x = slider_x + slider_width
                        mountain_amount = int((knob_x - slider_x) / slider_width * 100)
                        mountain_knob_x = knob_x
                    elif pygame.Rect(200, 600, 100, 50).collidepoint(event.pos): 
                        # Save current slider values
                        settings_manager.set_setting("water_amount", water_amount)
                        settings_manager.set_setting("tree_amount", tree_amount)
                        settings_manager.set_setting("mountain_amount", mountain_amount)
                        settings_manager.save_settings()
                        return 
                    

        # Draw options menu
        draw_text(screen, "Options Menu", font, BLACK, 50, 50)

        # Draw water slider
        pygame.draw.rect(screen, BLACK, (slider_x, slider_y, slider_width, slider_height))
        pygame.draw.circle(screen, BLACK, (water_knob_x, water_knob_y), knob_radius)
        draw_text(screen, "Water", font, BLACK, slider_x - 70, slider_y - 20)
        draw_text(screen, "{}%".format(water_amount), font, BLACK, slider_x + slider_width + 10, slider_y - 20)

        # Draw tree slider
        pygame.draw.rect(screen, BLACK, (slider_x, slider_y + 100, slider_width, slider_height))
        pygame.draw.circle(screen, BLACK, (tree_knob_x, tree_knob_y + 100), knob_radius)
        draw_text(screen, "Tree", font, BLACK, slider_x - 70, slider_y + 80)
        draw_text(screen, "{}%".format(tree_amount), font, BLACK, slider_x + slider_width + 10, slider_y + 80)

        # Draw mountain slider
        pygame.draw.rect(screen, BLACK, (slider_x, slider_y + 200, slider_width, slider_height))
        pygame.draw.circle(screen, BLACK, (mountain_knob_x, mountain_knob_y + 200), knob_radius)
        draw_text(screen, "Mountain", font, BLACK, slider_x - 70, slider_y + 180)
        draw_text(screen, "{}%".format(mountain_amount), font, BLACK, slider_x + slider_width + 10, slider_y + 180)

        # Draw save button anchored to the bottom
        pygame.draw.rect(screen, BLACK, (200, 600, 100, 50))
        draw_text(screen, "Save", font, WHITE, 250, 625)

        pygame.display.flip()

def main():
    # Initialize Pygame
    pygame.init()

    # Set up screen dimensions
    screen_width = 500
    screen_height = 725

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (65, 105, 225)

    # Fonts
    title_font = pygame.font.SysFont('Arial', 48)
    button_font = pygame.font.SysFont('Arial', 24)
    instruction_font = pygame.font.SysFont('Arial', 18)  # Define font for instructions

    # Create the screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Start Menu")

    # Define button dimensions and padding
    button_width = 200
    button_height = 50

    # Define text positions
    title_text_position = (screen_width // 2, 100)
    start_button_position = (screen_width // 2, 300)
    options_button_position = (screen_width // 2, 400)
    exit_button_position = (screen_width // 2, 500)

    instructions = [
        "Instructions:",
        "1. Select your settings from the options menu.",
        "2. You can generate a new map with SPACEBAR.",
        "3. You can zoom with UP/DOWN arrows.",
        "4. Drag to change view."
    ]

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_main()
                elif options_button_rect.collidepoint(event.pos):
                    options_menu(screen, settings_man)  # Pass settings_manager
                elif exit_button_rect.collidepoint(event.pos):
                    running = False

        # Draw title
        draw_text(screen, "Map Generator", title_font, BLACK, *title_text_position)

        # Draw buttons
        start_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, start_button_position[1] - button_height // 2, button_width, button_height)
        options_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, options_button_position[1] - button_height // 2, button_width, button_height)
        exit_button_rect = pygame.Rect(screen_width // 2 - button_width // 2, exit_button_position[1] - button_height // 2, button_width, button_height)

        pygame.draw.rect(screen, BLACK, start_button_rect)
        pygame.draw.rect(screen, BLACK, options_button_rect)
        pygame.draw.rect(screen, BLACK, exit_button_rect)

        # Draw button text
        draw_text(screen, "Start", button_font, WHITE, *start_button_position)
        draw_text(screen, "Options", button_font, WHITE, *options_button_position)
        draw_text(screen, "Exit", button_font, WHITE, *exit_button_position)

        # Draw instructions
        instruction_y = 600
        for instruction in instructions:
            draw_text(screen, instruction, instruction_font, BLACK, screen_width // 2, instruction_y)
            instruction_y += 20  

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
