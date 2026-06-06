"""Game systems: wave management, upgrade selection, and collision."""

import math
import random

import pygame

import config
from entities import Enemy


# ═════════════════════════════════════════════════════════════════════════
#  Upgrade definitions
# ═════════════════════════════════════════════════════════════════════════

UPGRADE_DEFS = [
    # ── Common (weight 50) ───────────────────────────────────────────────
    {
        "uid": "hp_boost",
        "name": "Max HP +20",
        "desc": "Increase max HP by 20",
        "rarity": "common",
        "weight": 50,
        "kind": "stat_add",
        "attr": "max_hp",
        "value": 20,
    },
    {
        "uid": "hp_heal",
        "name": "Heal 40 HP",
        "desc": "Restore 40 HP",
        "rarity": "common",
        "weight": 50,
        "kind": "heal",
        "attr": "hp",
        "value": 40,
    },
    {
        "uid": "speed_boost",
        "name": "Speed +10%",
        "desc": "Move 10% faster",
        "rarity": "common",
        "weight": 50,
        "kind": "stat_mult",
        "attr": "speed",
        "value": 1.10,
    },
    {
        "uid": "dmg_boost",
        "name": "Damage +15%",
        "desc": "Attack deals 15% more",
        "rarity": "common",
        "weight": 50,
        "kind": "stat_mult",
        "attr": "attack_damage",
        "value": 1.15,
    },
    {
        "uid": "atk_spd",
        "name": "Faster Attack",
        "desc": "Cooldown -10%",
        "rarity": "common",
        "weight": 50,
        "kind": "stat_mult",
        "attr": "attack_cooldown",
        "value": 0.90,
    },
    # ── Rare (weight 30) ─────────────────────────────────────────────────
    {
        "uid": "piercing",
        "name": "Piercing Shot",
        "desc": "Bullets pass through 1 enemy",
        "rarity": "rare",
        "weight": 30,
        "kind": "special",
        "attr": "piercing",
        "value": 1,
    },
    {
        "uid": "atk_spd_rare",
        "name": "Quick Hands",
        "desc": "Cooldown -20%",
        "rarity": "rare",
        "weight": 30,
        "kind": "stat_mult",
        "attr": "attack_cooldown",
        "value": 0.80,
    },
    {
        "uid": "dmg_rare",
        "name": "Heavy Shot",
        "desc": "Damage +25%",
        "rarity": "rare",
        "weight": 30,
        "kind": "stat_mult",
        "attr": "attack_damage",
        "value": 1.25,
    },
    {
        "uid": "range_rare",
        "name": "Long Shot",
        "desc": "Range +20%",
        "rarity": "rare",
        "weight": 30,
        "kind": "stat_mult",
        "attr": "attack_range",
        "value": 1.20,
    },
    {
        "uid": "max_hp_rare",
        "name": "Max HP +40",
        "desc": "Increase max HP by 40",
        "rarity": "rare",
        "weight": 30,
        "kind": "stat_add",
        "attr": "max_hp",
        "value": 40,
    },
    # ── Legendary (weight 10) ────────────────────────────────────────────
    {
        "uid": "triple_shot",
        "name": "Triple Shot",
        "desc": "Fire 3 bullets in a cone",
        "rarity": "legendary",
        "weight": 10,
        "kind": "special",
        "attr": "triple_shot",
        "value": True,
    },
    {
        "uid": "shield",
        "name": "Energy Shield",
        "desc": "Block one hit",
        "rarity": "legendary",
        "weight": 10,
        "kind": "special",
        "attr": "shield",
        "value": True,
    },
]

# UIDs of special upgrades — these are removed from the pool once taken.
SPECIAL_IDS = {u["uid"] for u in UPGRADE_DEFS if u["kind"] == "special"}


class UpgradeManager:
    """Handles random upgrade generation with rarity weighting.

    Tracks which special upgrades have already been taken so they
    are not offered again.  Stat upgrades may appear multiple times.
    """

    def __init__(self):
        self.taken_specials: set[str] = set()

    def pick_upgrades(self, n: int) -> list[dict]:
        """Return *n* distinct upgrades chosen by weighted rarity.

        Special upgrades the player already owns are excluded from the pool.
        """
        pool = [u for u in UPGRADE_DEFS if u["uid"] not in self.taken_specials]
        chosen: list[dict] = []
        for _ in range(n):
            if not pool:
                break
            weights = [u["weight"] for u in pool]
            pick = random.choices(pool, weights=weights, k=1)[0]
            chosen.append(pick)
            pool.remove(pick)
        return chosen

    def mark_taken(self, upgrade: dict):
        """Record a special upgrade as owned so it isn't offered again."""
        if upgrade["uid"] in SPECIAL_IDS:
            self.taken_specials.add(upgrade["uid"])

    def apply_upgrade(self, player, upgrade: dict):
        """Mutate *player* according to the upgrade's effect."""
        kind = upgrade["kind"]
        attr = upgrade["attr"]
        val = upgrade["value"]

        if kind == "stat_add":
            old = getattr(player, attr)
            setattr(player, attr, old + val)
            # Also heal by the same amount when max_hp is increased
            if attr == "max_hp":
                player.hp += val

        elif kind == "stat_mult":
            old = getattr(player, attr)
            setattr(player, attr, old * val)

        elif kind == "heal":
            player.hp = min(player.max_hp, player.hp + val)

        elif kind == "special":
            setattr(player, attr, val)

        if upgrade["uid"] in SPECIAL_IDS:
            self.mark_taken(upgrade)


# ═════════════════════════════════════════════════════════════════════════
#  Wave manager  (unchanged from Stage 2)
# ═════════════════════════════════════════════════════════════════════════

class WaveManager:
    """Controls enemy wave progression and spawn timing.

    Each wave spawns a fixed number of enemies with scaled stats.
    A new wave begins when all enemies from the current wave are dead.
    """

    def __init__(self):
        self.wave_number = 1
        self.enemies_in_wave = config.WAVE_BASE_ENEMIES
        self.enemies_spawned = 0
        self.enemies_killed = 0
        self.spawn_timer = 0.0
        self.spawn_interval = config.WAVE_SPAWN_INTERVAL
        self.pause_between_waves = 1.0
        self.wave_done = False

    def update(self, dt: float, enemy_list: list):
        """Spawn enemies on a timer and check for wave completion.

        Args:
            dt: Delta time in seconds.
            enemy_list: Mutable list of active Enemy instances.
        """
        if self.enemies_spawned < self.enemies_in_wave:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                x, y = self._random_edge_position()
                enemy = Enemy(x, y)
                self._scale_enemy(enemy)
                enemy_list.append(enemy)
                self.enemies_spawned += 1
                self.spawn_timer = self.spawn_interval

        if (self.enemies_spawned >= self.enemies_in_wave
                and len(enemy_list) == 0
                and not self.wave_done):
            self._next_wave()

    def on_enemy_killed(self):
        """Increment kill counter.  Called once per enemy death."""
        self.enemies_killed += 1

    # ── internal helpers ────────────────────────────────────────────────

    def _random_edge_position(self):
        """Return (x, y) outside the visible screen on a random edge."""
        side = random.randint(0, 3)
        m = config.ENEMY_SPAWN_MARGIN
        if side == 0:
            x = random.uniform(0, config.SCREEN_WIDTH)
            y = -m
        elif side == 1:
            x = random.uniform(0, config.SCREEN_WIDTH)
            y = config.SCREEN_HEIGHT + m
        elif side == 2:
            x = -m
            y = random.uniform(0, config.SCREEN_HEIGHT)
        else:
            x = config.SCREEN_WIDTH + m
            y = random.uniform(0, config.SCREEN_HEIGHT)
        return x, y

    def _scale_enemy(self, enemy: Enemy):
        """Multiply enemy base stats by the wave scaling factor."""
        w = self.wave_number
        enemy.hp = int(config.ENEMY_BASE_HP *
                       (1 + w * config.WAVE_HP_SCALE))
        enemy.speed = (config.ENEMY_BASE_SPEED *
                       (1 + w * config.WAVE_SPEED_SCALE))
        enemy.damage = (config.ENEMY_BASE_DAMAGE *
                        (1 + w * config.WAVE_DAMAGE_SCALE))
        enemy.xp_value = int(config.ENEMY_BASE_XP_VALUE *
                             (1 + w * config.WAVE_XP_SCALE))

    def _next_wave(self):
        """Advance to the next wave and reset spawn counters."""
        self.wave_number += 1
        self.enemies_in_wave = (config.WAVE_BASE_ENEMIES
                                + self.wave_number * config.WAVE_ENEMY_INCREMENT)
        self.enemies_spawned = 0
        self.spawn_interval = max(
            config.WAVE_MIN_SPAWN_INTERVAL,
            config.WAVE_SPAWN_INTERVAL - self.wave_number * 0.08
        )
        self.spawn_timer = self.pause_between_waves
