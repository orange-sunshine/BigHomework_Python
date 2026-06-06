"""Entity classes: Player, Enemy, Bullet, XPPickup, and EquipmentItem."""

import math
import random

import pygame

import config


class Player:
    """Stationary turret-style player.

    Stays in the centre of the screen, auto-attacks the nearest enemy.
    Levels up grant automatic stat increases.
    """

    def __init__(self):
        size = config.PLAYER_SIZE
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (config.SCREEN_WIDTH // 2,
                            config.SCREEN_HEIGHT // 2)

        self.hp = config.PLAYER_START_HP
        self.max_hp = config.PLAYER_MAX_HP
        self.xp = config.PLAYER_START_XP
        self.level = config.PLAYER_START_LEVEL
        self.attack_cooldown = config.PLAYER_ATTACK_COOLDOWN
        self.attack_damage = config.PLAYER_ATTACK_DAMAGE
        self.attack_range = config.PLAYER_ATTACK_RANGE
        self.attack_timer = 0.0

        self.piercing = 0
        self.crit_rate = config.BASE_CRIT_RATE
        self.crit_damage = config.BASE_CRIT_DAMAGE
        self.penetration_rate = config.PENETRATION_RATE
        self.xp_modifier = 1.0
        self.game_speed = 0
        self.defense = config.PLAYER_DEFENSE
        self.lifesteal = config.PLAYER_LIFESTEAL
        self.hp_regen = config.PLAYER_HP_REGEN
        self.bullet_count = config.PLAYER_BULLET_COUNT
        self.dp_bonus = 0

    def on_level_up(self):
        """Auto-increase stats when the player gains a level."""
        self.max_hp += config.LEVEL_UP_HP_BONUS
        self.hp += config.LEVEL_UP_HP_BONUS
        self.attack_damage += config.LEVEL_UP_DMG_BONUS
        self.defense += config.LEVEL_UP_DEF_BONUS

    def take_damage(self, amount: float):
        """Reduce HP by *amount* (mitigated by defense), flooring at zero."""
        effective = max(0, amount - self.defense)
        self.hp = max(0, self.hp - effective)

    def gain_xp(self, raw_amount: float):
        """Add XP (modified by xp_modifier) and return True if levelled."""
        self.xp += raw_amount * self.xp_modifier
        needed = self._xp_for_level(self.level)
        if self.xp >= needed:
            self.xp -= needed
            self.level += 1
            return True
        return False

    @staticmethod
    def _xp_for_level(level: int) -> int:
        return int(config.XP_BASE_REQUIREMENT *
                   (config.XP_SCALE_FACTOR ** (level - 1)))

    def get_nearest_enemy(self, enemies: list):
        """Return the closest enemy within attack_range, or None."""
        nearest = None
        range_sq = self.attack_range ** 2
        px, py = self.rect.center
        min_dist_sq = range_sq
        for e in enemies:
            dx = e.rect.centerx - px
            dy = e.rect.centery - py
            dist_sq = dx * dx + dy * dy
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                nearest = e
        return nearest

    def draw(self, surface: pygame.Surface):
        """Render the player as a blue square."""
        pygame.draw.rect(surface, config.BLUE, self.rect)


class Enemy:
    """Hostile entity that moves toward the player."""

    def __init__(self, x: float, y: float):
        """Initialise enemy at (x, y) with base stats."""
        size = config.ENEMY_SIZE
        self.rect = pygame.Rect(x, y, size, size)
        self.hp = config.ENEMY_BASE_HP
        self.speed = config.ENEMY_BASE_SPEED
        self.damage = config.ENEMY_BASE_DAMAGE
        self.xp_value = config.ENEMY_BASE_XP_VALUE
        self.attack_range = config.ENEMY_ATTACK_RANGE
        self.attack_cooldown = 2.0
        self.attack_timer = random.uniform(0, self.attack_cooldown)

    def take_damage(self, amount: float):
        """Reduce HP; return True if the enemy died."""
        self.hp -= amount
        return self.hp <= 0

    def move_towards(self, target_pos: tuple, dt: float):
        """Move toward *target_pos* at self.speed.  Stop within attack_range."""
        cx, cy = self.rect.center
        tx, ty = target_pos
        dx = tx - cx
        dy = ty - cy
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        if dist < self.attack_range:
            return
        self.rect.x += (dx / dist) * self.speed * dt
        self.rect.y += (dy / dist) * self.speed * dt

    def draw(self, surface: pygame.Surface):
        """Render enemy as a red square."""
        pygame.draw.rect(surface, config.RED, self.rect)


class Bullet:
    """Projectile fired by the player toward a target position."""

    def __init__(self, x: float, y: float, target_x: float, target_y: float,
                 damage: float, piercing: int = 0, is_critical: bool = False,
                 owner: str = "player"):
        """Create a bullet at (x, y) flying toward (target_x, target_y).

        *owner* is \"player\" or \"enemy\" — affects rendering.
        """
        size = (config.BULLET_SIZE_CRIT if is_critical else config.BULLET_SIZE)
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (x, y)
        self.damage = damage
        self.piercing = piercing
        self.is_critical = is_critical
        self.owner = owner

        speed = config.BULLET_SPEED if owner == "player" else config.ENEMY_BULLET_SPEED
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
        else:
            self.vx = 0.0
            self.vy = 0.0
        self.lifetime = config.BULLET_LIFETIME

    def update(self, dt: float):
        """Move bullet and reduce lifetime."""
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt
        self.lifetime -= dt

    def is_alive(self) -> bool:
        """Return True while lifetime remains."""
        return self.lifetime > 0

    def is_off_screen(self) -> bool:
        """Return True if bullet is beyond the spawn margin."""
        m = config.ENEMY_SPAWN_MARGIN
        return (self.rect.right < -m or
                self.rect.left > config.SCREEN_WIDTH + m or
                self.rect.bottom < -m or
                self.rect.top > config.SCREEN_HEIGHT + m)

    def draw(self, surface: pygame.Surface):
        """Render bullet — white for crit, yellow for player, red for enemy."""
        if self.owner == "enemy":
            colour = (255, 100, 100)
        else:
            colour = config.WHITE if self.is_critical else config.YELLOW
        pygame.draw.rect(surface, colour, self.rect)


class XPPickup:
    """Experience orb dropped by dead enemies."""

    def __init__(self, x: float, y: float, value: int):
        """Create an XP pickup at (x, y) worth *value* XP."""
        size = config.PICKUP_SIZE
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (x, y)
        self.value = value
        self.lifetime = config.PICKUP_LIFETIME

    def update(self, dt: float):
        """Reduce lifetime each frame."""
        self.lifetime -= dt

    def is_alive(self) -> bool:
        """Return True while lifetime remains."""
        return self.lifetime > 0

    def draw(self, surface: pygame.Surface):
        cx, cy = self.rect.center
        half = config.PICKUP_SIZE // 2
        points = [(cx, cy - half), (cx + half, cy),
                  (cx, cy + half), (cx - half, cy)]
        pygame.draw.polygon(surface, config.GREEN, points)


# ═════════════════════════════════════════════════════════════════════════
#  Equipment
# ═════════════════════════════════════════════════════════════════════════

class EquipmentItem:
    """A piece of equipment with slot, rarity, and affixes."""

    def __init__(self, slot: str, rarity: str, affixes: list[dict]):
        self.slot = slot
        self.rarity = rarity
        self.affixes = affixes

    def to_dict(self) -> dict:
        """Serialize equipment to a JSON-compatible dict."""
        return {"slot": self.slot, "rarity": self.rarity,
                "affixes": self.affixes}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(slot=d["slot"], rarity=d["rarity"], affixes=d["affixes"])

    def total_stat(self, attr: str) -> float:
        return sum(a["value"] for a in self.affixes if a["attr"] == attr)
