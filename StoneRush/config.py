"""
Game constants and configuration
Ported from Constants.java
"""

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GAME_TITLE = "StoneRush"
TARGET_FPS = 60

# World settings
GRAVITY = 800.0  # Positive in Pygame (y increases downward)
PIXELS_PER_METER = 32.0

# Player settings
PLAYER_SIZE = 32.0  # Smaller sprites (32x32 pixels)
PLAYER_SPEED = 200.0
PLAYER_JUMP_VELOCITY = -400.0  # Negative in Pygame (y=0 at top, jumping goes up)
PLAYER_RAM_SPEED = 500.0
PLAYER_RAM_DURATION = 0.3
PLAYER_MAX_LIVES = 3

# Enemy settings
ENEMY_SIZE = 32.0  # Smaller sprites (32x32 pixels)
ENEMY_SPEED = 50.0
ENEMY_PATROL_DISTANCE = 128.0

# Block settings
BLOCK_SIZE = 32.0

# Level settings
LEVEL_WIDTH_BLOCKS = 100
LEVEL_HEIGHT_BLOCKS = 20

# Colors (RGB format, 0-255)
# Converted from LibGDX Color (0.0-1.0) by multiplying by 255
COLOR_PLAYER = (128, 128, 128)  # Gray
COLOR_GROUND = (153, 102, 51)  # Brown (0.6, 0.4, 0.2)
COLOR_CRACKED_BLOCK = (127, 76, 25)  # Darker brown (0.5, 0.3, 0.1)
COLOR_ENEMY = (255, 0, 0)  # Red
COLOR_GOAL = (0, 255, 0)  # Green
COLOR_SKY = (135, 206, 235)  # Sky blue (0.53, 0.81, 0.92)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_DARK_GRAY = (64, 64, 64)
