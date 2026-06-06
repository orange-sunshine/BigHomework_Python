"""Persistent save/load for Divine Power, perk levels, and equipment.

Uses JSON stored alongside the game executable.
"""

import json
import os

SAVE_FILE = "save_data.json"

# Default blank save state
_DEFAULT_DATA = {
    "lang": "en",
    "dp": 0,
    "total_dp_earned": 0,
    "perk_levels": {
        "xp_modifier": 0, "attack_damage": 0, "max_hp": 0,
        "defense": 0, "lifesteal": 0, "hp_regen": 0, "bullet_count": 0,
        "crit_rate": 0, "crit_damage": 0, "attack_cooldown": 0,
        "piercing": 0, "game_speed": 0, "dp_bonus": 0,
    },
    "equipped": {
        "weapon": None,
        "armor": None,
        "accessory": None,
    },
}


def load_data() -> dict:
    """Read save_data.json, returning a full data dict on success or defaults."""
    if not os.path.isfile(SAVE_FILE):
        return _deep_copy(_DEFAULT_DATA)

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, PermissionError, OSError):
        return _deep_copy(_DEFAULT_DATA)

    return _merge_with_defaults(data)


def save_data(data: dict):
    """Write *data* to save_data.json, gracefully handling errors."""
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except (PermissionError, OSError):
        print("[save_manager] Warning: could not write save file.")


def add_divine_power(dp_earned: int):
    """Add Divine Power and persist."""
    data = load_data()
    data["dp"] += dp_earned
    data["total_dp_earned"] += dp_earned
    save_data(data)


def spend_divine_power(cost: int) -> bool:
    """Spend DP if enough available.  Returns True on success."""
    data = load_data()
    if data["dp"] < cost:
        return False
    data["dp"] -= cost
    save_data(data)
    return True


# ── internal helpers ─────────────────────────────────────────────────────

def _deep_copy(d: dict) -> dict:
    """Return a deep-enough copy for our nested dict."""
    return json.loads(json.dumps(d))


def _merge_with_defaults(data: dict) -> dict:
    """Fill missing keys from defaults so corrupted/old files still work."""
    defaults = _deep_copy(_DEFAULT_DATA)
    defaults.update(data)

    # Merge nested dicts
    for key in ("perk_levels", "equipped"):
        if isinstance(data.get(key), dict):
            defaults[key].update(data[key])

    return defaults
