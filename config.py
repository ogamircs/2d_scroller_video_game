"""
Game Configuration
All game constants and tunable values in one place.
"""

# =============================================================================
# DISPLAY
# =============================================================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Side-Scrolling Shooter"

# =============================================================================
# LEVEL
# =============================================================================
LEVEL_WIDTH = 2000
LEVEL_HEIGHT = 600

# =============================================================================
# COLORS
# =============================================================================
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (100, 100, 100)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_SKY_BLUE = (135, 206, 235)
COLOR_DARK_BLUE = (50, 50, 80)

# Entity colors
PLAYER_COLOR = (0, 200, 100)        # Green
ENEMY_COLOR = (200, 50, 50)         # Red
BULLET_COLOR = (255, 255, 0)        # Yellow
PLATFORM_COLOR = (100, 100, 100)    # Gray

# UI colors
HEALTH_BAR_BG = (60, 60, 60)
HEALTH_BAR_FG = (0, 200, 0)
HEALTH_BAR_LOW = (200, 50, 50)

# =============================================================================
# PHYSICS
# =============================================================================
GRAVITY = 1500          # pixels/second^2
TERMINAL_VELOCITY = 800 # max fall speed

# =============================================================================
# PLAYER
# =============================================================================
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 48
PLAYER_SPEED = 300          # pixels/second
JUMP_VELOCITY = -550        # negative = up
PLAYER_MAX_HEALTH = 100
PLAYER_INVINCIBILITY_TIME = 1.0  # seconds after taking damage

# =============================================================================
# SHOOTING
# =============================================================================
SHOOT_COOLDOWN = 0.25       # seconds between shots
BULLET_WIDTH = 12
BULLET_HEIGHT = 6
BULLET_SPEED = 600          # pixels/second
BULLET_DAMAGE = 25
BULLET_LIFETIME = 2.0       # seconds

# =============================================================================
# ENEMIES
# =============================================================================
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32
ENEMY_SPEED = 150           # pixels/second
ENEMY_HEALTH = 50
ENEMY_DAMAGE = 15           # damage on contact

# =============================================================================
# SPAWNING
# =============================================================================
SPAWN_INTERVAL = 2.5        # seconds between spawns
SPAWN_MARGIN = 50           # pixels off-screen

# =============================================================================
# UI
# =============================================================================
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_X = 10
HEALTH_BAR_Y = 10

# =============================================================================
# ASSETS
# =============================================================================
import os
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "sprites")
