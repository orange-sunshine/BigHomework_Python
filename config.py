"""Game configuration constants.

All tunable game parameters live here so balancing only touches one file.
"""

# ── Display ──────────────────────────────────────────────────────────────
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# ── Colours (R, G, B) ────────────────────────────────────────────────────
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
CYAN = (50, 255, 255)
ORANGE = (255, 165, 50)
PURPLE = (180, 50, 255)
GREY = (100, 100, 100)
DARK_GREY = (40, 40, 40)
HP_BAR_GREEN = (50, 200, 50)
HP_BAR_RED = (200, 50, 50)
XP_BAR_BLUE = (50, 100, 255)

# ── Player ───────────────────────────────────────────────────────────────
PLAYER_SIZE = 24
PLAYER_SPEED = 280
PLAYER_MAX_HP = 100
PLAYER_START_HP = 100
PLAYER_ATTACK_COOLDOWN = 0.3
PLAYER_ATTACK_DAMAGE = 15
PLAYER_ATTACK_RANGE = 350
PLAYER_START_XP = 0
PLAYER_START_LEVEL = 1

XP_BASE_REQUIREMENT = 50
XP_SCALE_FACTOR = 1.5

# ── Enemy ────────────────────────────────────────────────────────────────
ENEMY_SIZE = 20
ENEMY_BASE_HP = 30
ENEMY_BASE_SPEED = 80
ENEMY_BASE_DAMAGE = 10
ENEMY_BASE_XP_VALUE = 10
ENEMY_SPAWN_MARGIN = 50

# ── Bullet ───────────────────────────────────────────────────────────────
BULLET_SPEED = 500
BULLET_SIZE = 8
BULLET_LIFETIME = 1.5

# ── XP Pickup ────────────────────────────────────────────────────────────
PICKUP_SIZE = 8
PICKUP_LIFETIME = 8.0

# ── Wave scaling ─────────────────────────────────────────────────────────
WAVE_BASE_ENEMIES = 3
WAVE_ENEMY_INCREMENT = 2
WAVE_SPAWN_INTERVAL = 2.0
WAVE_MIN_SPAWN_INTERVAL = 0.4
WAVE_HP_SCALE = 0.15
WAVE_SPEED_SCALE = 0.05
WAVE_DAMAGE_SCALE = 0.08
WAVE_XP_SCALE = 0.10
