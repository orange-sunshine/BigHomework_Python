"""Game configuration constants."""

# ── Display ──────────────────────────────────────────────────────────────
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# ── Colours ──────────────────────────────────────────────────────────────
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
CYAN = (50, 255, 255)
ORANGE = (255, 165, 50)
PURPLE = (180, 50, 255)
GOLD = (255, 215, 0)
DARK_GOLD = (180, 140, 0)
DARK_RED = (120, 20, 20)
GREY = (100, 100, 100)
DARK_GREY = (40, 40, 40)
HP_BAR_GREEN = (50, 200, 50)
HP_BAR_RED = (200, 50, 50)
XP_BAR_BLUE = (50, 100, 255)

# ── Player ───────────────────────────────────────────────────────────────
PLAYER_SIZE = 24
PLAYER_MAX_HP = 100
PLAYER_START_HP = 100
PLAYER_ATTACK_COOLDOWN = 0.3
PLAYER_ATTACK_DAMAGE = 15
PLAYER_ATTACK_RANGE = 350
PLAYER_START_XP = 0
PLAYER_START_LEVEL = 1

XP_BASE_REQUIREMENT = 50
XP_SCALE_FACTOR = 1.5

# ── Auto level-up bonuses ────────────────────────────────────────────────
LEVEL_UP_HP_BONUS = 5
LEVEL_UP_DMG_BONUS = 2
LEVEL_UP_DEF_BONUS = 1

# ── New stats: defaults ─────────────────────────────────────────────────
PLAYER_DEFENSE = 0
PLAYER_LIFESTEAL = 0.0
PLAYER_HP_REGEN = 0.0
PLAYER_BULLET_COUNT = 1

# ── Critical hits ────────────────────────────────────────────────────────
BASE_CRIT_RATE = 0.05
BASE_CRIT_DAMAGE = 1.50
PENETRATION_RATE = 0.70

# ── Enemy ────────────────────────────────────────────────────────────────
ENEMY_SIZE = 20
ENEMY_BASE_HP = 30
ENEMY_BASE_SPEED = 80
ENEMY_BASE_DAMAGE = 10
ENEMY_BASE_XP_VALUE = 10
ENEMY_SPAWN_MARGIN = 50
ENEMY_ATTACK_RANGE = 100
ENEMY_BULLET_SPEED = 220

# ── Bullet ───────────────────────────────────────────────────────────────
BULLET_SPEED = 500
BULLET_SIZE = 8
BULLET_SIZE_CRIT = 14
BULLET_LIFETIME = 1.5

# ── Wave scaling ─────────────────────────────────────────────────────────
WAVE_BASE_ENEMIES = 50
WAVE_ENEMY_INCREMENT = 5
WAVE_HP_SCALE = 0.20
WAVE_SPEED_SCALE = 0.06
WAVE_DAMAGE_SCALE = 0.12
WAVE_XP_SCALE = 0.12

# ── Divine Power ─────────────────────────────────────────────────────────
DP_VISIBLE_ROWS = 7
NO_MAX = 9999

DIVINE_PERKS = [
    {"key": "xp_modifier",     "max": NO_MAX, "per_level": 0.10, "type": "add"},
    {"key": "attack_damage",   "max": NO_MAX, "per_level": 1.08, "type": "mult"},
    {"key": "max_hp",          "max": NO_MAX, "per_level": 1.05, "type": "mult"},
    {"key": "defense",         "max": NO_MAX, "per_level": 1.08, "type": "mult"},
    {"key": "lifesteal",       "max": NO_MAX, "per_level": 0.01, "type": "add"},
    {"key": "hp_regen",        "max": NO_MAX, "per_level": 0.5,  "type": "add"},
    {"key": "bullet_count",    "max": 50, "per_level": 1,    "type": "add"},
    {"key": "crit_rate",       "max": 50,     "per_level": 0.02, "type": "add"},
    {"key": "crit_damage",     "max": NO_MAX, "per_level": 0.10, "type": "add"},
    {"key": "attack_cooldown", "max": NO_MAX, "per_level": 0.97, "type": "mult"},
    {"key": "piercing",        "max": NO_MAX, "per_level": 1,    "type": "add"},
    {"key": "game_speed",      "max": 5,      "per_level": 1,    "type": "add"},
    {"key": "dp_bonus",        "max": NO_MAX, "per_level": 0.15, "type": "add"},
]

def perk_cost(level: int) -> int:
    """Divine Power cost to upgrade a perk from *level* to *level* + 1."""
    return int(10 * (level + 1) ** 1.4)

# ── Equipment ────────────────────────────────────────────────────────────
EQUIP_DROP_BASE_CHANCE = 0.04
EQUIP_DROP_WAVE_BONUS = 0.005

EQUIP_SLOTS = ["weapon", "armor", "accessory"]
EQUIP_RARITIES = ["white", "blue", "purple", "orange", "red"]
EQUIP_RARITY_COLORS = {
    "white": (200, 200, 200), "blue": (80, 130, 255),
    "purple": (180, 80, 255), "orange": (255, 180, 50), "red": (255, 60, 60),
}
EQUIP_AFFIXES = [
    {"name": "Atk",    "attr": "attack_damage",  "per_tier": [3, 6, 12, 20, 35]},
    {"name": "HP",     "attr": "max_hp",          "per_tier": [10, 25, 50, 90, 150]},
    {"name": "Def",    "attr": "defense",         "per_tier": [2, 4, 8, 14, 22]},
    {"name": "LS",     "attr": "lifesteal",       "per_tier": [0.01, 0.02, 0.04, 0.07, 0.10]},
    {"name": "Regen",  "attr": "hp_regen",        "per_tier": [0.5, 1, 2, 4, 7]},
    {"name": "CritRt", "attr": "crit_rate",       "per_tier": [0.02, 0.05, 0.09, 0.14, 0.20]},
    {"name": "CritDmg","attr": "crit_damage",     "per_tier": [0.05, 0.12, 0.22, 0.35, 0.50]},
    {"name": "XP",     "attr": "xp_modifier",     "per_tier": [0.05, 0.10, 0.20, 0.35, 0.50]},
    {"name": "Range",  "attr": "attack_range",    "per_tier": [20, 45, 80, 130, 200]},
]
