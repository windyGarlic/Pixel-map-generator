import pygame
import sys
import random
from start_menu import SettingsManager

settings_manager = SettingsManager("settings.json")
settings_manager.load_settings()

water_amount = settings_manager.get_setting("water_amount")
tree_amount = settings_manager.get_setting("tree_amount")
mountain_amount = settings_manager.get_setting("mountain_amount")
lake_amount = settings_manager.get_setting("lake_amount")

def calculate_range_land(water_amount):
    if water_amount >= 50:
        upper_bound = 150000
        lower_bound = 100000  
    else:
        upper_bound = 75000
        lower_bound = 55000  

    step_size = (upper_bound - lower_bound) / 100
    lower_limit = lower_bound + water_amount * step_size
    upper_limit = upper_bound + water_amount * step_size * 2

    return lower_limit, upper_limit

lower_limit, upper_limit = calculate_range_land(water_amount)

# Use settings
volume = settings_manager.get_setting("volume", default=50)

pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
PIXEL_SIZE = 6 # Size of each pixel on the map
GRID_WIDTH, GRID_HEIGHT = WIDTH // PIXEL_SIZE, HEIGHT // PIXEL_SIZE
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Map Generator")

# Define colors
LAND_COLOR = (17, 227, 30)  # Green
WATER_COLOR = (65, 105, 225)  # Blue
TREE_COLOR = (139, 69, 19)  # Brown
MOUNTAIN_COLOR = (128, 128, 128)  # Grey

class Land:
    def __init__(self):
        self.color = LAND_COLOR

class Water:
    def __init__(self):
        self.color = WATER_COLOR

class Tree:
    def __init__(self):
        self.color = TREE_COLOR

class Mountain:
    def __init__(self):
        self.color = MOUNTAIN_COLOR

# Forest generation parameters
FOREST_DENSITY = 1  # Initial density of trees in the map
FOREST_SURVIVAL_THRESHOLD = 3  # Number of neighboring trees for survival
FOREST_GROWTH_THRESHOLD = 1  # Number of neighboring trees for a new tree to grow
SOLITARY_TREE_DEATH_PROBABILITY = 100

def simulate_forest_growth(forest_map):
    new_forest_map = []
    for y in range(GRID_HEIGHT):
        new_row = []
        for x in range(GRID_WIDTH):
            # Count neighboring trees
            tree_count = sum(1 for dx in range(-1, 2) for dy in range(-1, 2)
                             if 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT
                             and isinstance(forest_map[y + dy][x + dx], Tree))
            # Apply cellular automata rules
            if isinstance(forest_map[y][x], Tree):
                # Tree survives if it has enough neighboring trees
                if tree_count >= FOREST_SURVIVAL_THRESHOLD:
                    new_row.append(Tree())
                else:
                    # Solitary trees have a higher chance of dying off
                    if tree_count == 0:
                        # Increase the chance of solitary trees dying off
                        if random.random() < SOLITARY_TREE_DEATH_PROBABILITY:
                            new_row.append(Water())
                        else:
                            new_row.append(Tree())
                    else:
                        new_row.append(Water())
            else:
                # Empty cell becomes a tree if it has enough neighboring trees
                if tree_count >= FOREST_GROWTH_THRESHOLD:
                    # New tree grows in a cell with at least one neighboring tree
                    new_row.append(Tree())
                else:
                    new_row.append(Water())
        new_forest_map.append(new_row)
    return new_forest_map

# Generate the initial forest map
def generate_forest_map():
    forest_map = []

    # Initialize with trees based on density
    for _ in range(GRID_HEIGHT):
        row = [Tree() if random.random() < FOREST_DENSITY else Water() for _ in range(GRID_WIDTH)]
        forest_map.append(row)

    return forest_map

# Generate the initial forest map
forest_map = generate_forest_map()

# Simulate forest growth for a certain number of iterations
for _ in range(8):  # Adjust the number of iterations as needed
    forest_map = simulate_forest_growth(forest_map)

def generate_map():
    terrain_map = []

    # Initialize with water
    for _ in range(GRID_HEIGHT):
        row = [Water() for _ in range(GRID_WIDTH)]
        terrain_map.append(row)

    # Define possible tree density ranges
    density_ranges = {
        'low': (0.01, 0.03),    # Low density range
        'medium': (0.04, 0.07), # Medium density range
        'high': (0.08, 0.1)     # High density range
    }

    # Map the tree amount setting to the density ranges
    tree_density_range = density_ranges['medium']  # Default to medium density
    if tree_amount <= 33:
        tree_density_range = density_ranges['low']
    elif tree_amount <= 66:
        tree_density_range = density_ranges['medium']
    else:
        tree_density_range = density_ranges['high']

    # Calculate the probability of a tree spawning based on the density range
    min_density, max_density = tree_density_range 
    min_density *= 2
    max_density *= 2 
    tree_spawn_probability = random.uniform(min_density, max_density)

    # Calculate the probability of a mountain spawning based on the mountain amount setting
    mountain_spawn_probability = mountain_amount / 100
    mountain_spawn_probability = mountain_spawn_probability / 10
    # Add land masses
    for _ in range(4):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        for _ in range(random.randint(lower_limit, upper_limit)):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                        terrain_map[ny][nx] = Land()
            x += random.randint(-1, 1)
            y += random.randint(-1, 1)

    # Add mountains based on the calculated probability and adjacent land
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            if random.random() < mountain_spawn_probability:
                has_adjacent_land = any(isinstance(terrain_map[y + dy][x + dx], Land) for dx in range(-1, 2) for dy in range(-1, 2) if 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT)
                if has_adjacent_land:
                    terrain_map[y][x] = Mountain()

    # Add trees based on the calculated probability
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if isinstance(terrain_map[y][x], Land) and random.random() < tree_spawn_probability:
                terrain_map[y][x] = Tree()

    return terrain_map

zoom_level = 1
zoom_increment = 0.5

# Initialize cached surfaces
cached_terrain_map = pygame.Surface((WIDTH, HEIGHT))
cached_terrain_map.fill((255, 255, 255))  # Fill with background color
cached_mountain_image = pygame.Surface((int(PIXEL_SIZE * zoom_level * 2), int(PIXEL_SIZE * zoom_level * 2)))
cached_tree_image = pygame.Surface((int(PIXEL_SIZE * zoom_level), int(PIXEL_SIZE * zoom_level)))


def draw_map(terrain_map):
    for y, row in enumerate(terrain_map):
        for x, terrain in enumerate(row):
            # Adjust position based on viewport
            draw_x = (x - viewport_x) * PIXEL_SIZE * zoom_level
            draw_y = (y - viewport_y) * PIXEL_SIZE * zoom_level

            # Adjust size for mountain
            terrain_size = PIXEL_SIZE * zoom_level

            if isinstance(terrain, Mountain):
                # Adjust position and size for mountains to occupy a 2x2 area
                draw_x -= PIXEL_SIZE * zoom_level / 2
                draw_y -= PIXEL_SIZE * zoom_level / 2
                terrain_size *= 2  # Double the size for mountains

            rect = pygame.Rect(draw_x, draw_y, terrain_size, terrain_size)

            if isinstance(terrain, Mountain):
                mountain_image = pygame.image.load("img/mount.png")
                mountain_image = pygame.transform.scale(mountain_image, (int(terrain_size), int(terrain_size)))
                window.blit(mountain_image, rect.topleft)
            elif isinstance(terrain, Tree):
                tree_image = pygame.image.load("img/tree2.png")
                tree_image = pygame.transform.scale(tree_image, (int(terrain_size), int(terrain_size)))
                window.blit(tree_image, rect.topleft)
            else:
                pygame.draw.rect(window, terrain.color, rect)

# Generate the initial map
terrain_map = generate_map()

viewport_x = 0
viewport_y = 0
dragging = False
drag_start_x = 0
drag_start_y = 0

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Start dragging
                dragging = True
                drag_start_x, drag_start_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                # Stop dragging
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                # Calculate dragging distance
                drag_dx, drag_dy = event.pos[0] - drag_start_x, event.pos[1] - drag_start_y
                # Update viewport position
                viewport_x -= int(drag_dx / (PIXEL_SIZE * zoom_level))
                viewport_y -= int(drag_dy / (PIXEL_SIZE * zoom_level))
                # Clamp viewport position to stay within bounds
                viewport_x = max(0, min(viewport_x, GRID_WIDTH - int(WIDTH / (PIXEL_SIZE * zoom_level))))
                viewport_y = max(0, min(viewport_y, GRID_HEIGHT - int(HEIGHT / (PIXEL_SIZE * zoom_level))))
                # Update drag start position for next motion event
                drag_start_x, drag_start_y = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                terrain_map = generate_map()
            elif event.key == pygame.K_DOWN:
                # Zoom out by decreasing the zoom level
                zoom_level -= zoom_increment
                if zoom_level < 0.1:
                    zoom_level = 0.1
            elif event.key == pygame.K_UP:
                # Zoom in by increasing the zoom level
                zoom_level += zoom_increment
                if zoom_level > 5:
                    zoom_level = 5

    # Draw everything
    window.fill((255, 255, 255))
    draw_map(terrain_map)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
