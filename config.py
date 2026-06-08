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
BAR_BLUE = (50, 100, 255)

# ── Player ───────────────────────────────────────────────────────────────
PLAYER_SIZE = 24
PLAYER_MAX_HP = 100
PLAYER_START_HP = 100
PLAYER_ATTACK_COOLDOWN = 0.3
PLAYER_ATTACK_DAMAGE = 15
PLAYER_ATTACK_RANGE = 350

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
ENEMY_BASE_HP = 15
ENEMY_BASE_SPEED = 40
ENEMY_BASE_DAMAGE = 5
ENEMY_SPAWN_MARGIN = 50
ENEMY_ATTACK_RANGE = 100
ENEMY_BULLET_SPEED = 220

# ── Drops ────────────────────────────────────────────────────────────────
GOLD_BASE = 5
GOLD_WAVE_SCALE = 1.0
DP_DROP_RATIO = 0.5

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

# ── Divine Power ─────────────────────────────────────────────────────────
DP_VISIBLE_ROWS = 7
NO_MAX = 9999

DIVINE_PERKS = [
    {"key": "gold_modifier",   "max": NO_MAX, "per_level": 0.05, "type": "add",  "cost_scale": 1.0},
    {"key": "attack_damage",   "max": NO_MAX, "per_level": 1.02, "type": "mult", "cost_scale": 1.0},
    {"key": "max_hp",          "max": NO_MAX, "per_level": 1.02, "type": "mult", "cost_scale": 1.0},
    {"key": "defense",         "max": NO_MAX, "per_level": 1.02, "type": "mult", "cost_scale": 1.0},
    {"key": "lifesteal",       "max": NO_MAX, "per_level": 0.002,"type": "add",  "cost_scale": 1.0},
    {"key": "hp_regen",        "max": NO_MAX, "per_level": 0.1,  "type": "add",  "cost_scale": 1.0},
    {"key": "bullet_count",    "max": 50,     "per_level": 1,    "type": "add",  "cost_scale": 8.0},
    {"key": "crit_rate",       "max": 50,     "per_level": 0.005,"type": "add",  "cost_scale": 2.5},
    {"key": "crit_damage",     "max": NO_MAX, "per_level": 0.03, "type": "add",  "cost_scale": 1.0},
    {"key": "attack_cooldown", "max": NO_MAX, "per_level": 0.99, "type": "mult", "cost_scale": 1.0},
    {"key": "piercing",        "max": NO_MAX, "per_level": 1,    "type": "add",  "cost_scale": 1.0},
    {"key": "game_speed",      "max": 5,      "per_level": 1,    "type": "add",  "cost_scale": 30.0},
    {"key": "dp_bonus",        "max": NO_MAX, "per_level": 0.05, "type": "add",  "cost_scale": 1.0},
]

def perk_cost(level: int, cost_scale: float = 1.0) -> int:
    """Divine Power cost to upgrade a perk from *level* to *level* + 1.

    Normal perks (cost_scale=1.0) grow slowly via a power function.
    Special perks (cost_scale>1.0) cost proportionally more at every level.
    """
    base = int(5 * (level + 1) ** 1.3)
    return int(base * cost_scale)

# ── Equipment ────────────────────────────────────────────────────────────
EQUIP_DROP_BASE_CHANCE = 0.008
EQUIP_DROP_WAVE_BONUS = 0.001

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
    {"name": "Gold",   "attr": "gold_modifier",   "per_tier": [0.05, 0.10, 0.20, 0.35, 0.50]},
    {"name": "Range",  "attr": "attack_range",    "per_tier": [20, 45, 80, 130, 200]},
]

# ── Upgrade panel tab groups ────────────────────────────────────────────

UPGRADE_TABS = [
    {"key": "attack",  "label_key": "upg_tab_attack",  "upgrades": ["attack_damage", "crit_rate", "crit_damage", "attack_cooldown", "piercing"]},
    {"key": "defense", "label_key": "upg_tab_defense", "upgrades": ["max_hp", "defense", "lifesteal", "hp_regen"]},
    {"key": "economy", "label_key": "upg_tab_economy", "upgrades": ["gold_modifier", "dp_bonus"]},
]

# ── In-game gold upgrades ────────────────────────────────────────────────

GOLD_UPGRADES = [
    {"key": "attack_damage",   "per_level": 3,     "base_cost": 10, "cost_scale": 1.5},
    {"key": "max_hp",          "per_level": 10,    "base_cost": 10, "cost_scale": 1.5},
    {"key": "defense",         "per_level": 1,     "base_cost": 10, "cost_scale": 1.5},
    {"key": "lifesteal",       "per_level": 0.003, "base_cost": 15, "cost_scale": 1.6},
    {"key": "hp_regen",        "per_level": 0.2,   "base_cost": 12, "cost_scale": 1.5},
    {"key": "crit_rate",       "per_level": 0.01,  "base_cost": 20, "cost_scale": 1.6},
    {"key": "crit_damage",     "per_level": 0.05,  "base_cost": 15, "cost_scale": 1.5},
    {"key": "attack_cooldown", "per_level": -0.02, "base_cost": 15, "cost_scale": 1.5},
    {"key": "piercing",        "per_level": 1,     "base_cost": 25, "cost_scale": 1.7},
    {"key": "gold_modifier",   "per_level": 0.05,  "base_cost": 15, "cost_scale": 1.6},
    {"key": "dp_bonus",        "per_level": 0.05,  "base_cost": 20, "cost_scale": 1.6},
]
