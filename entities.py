"""Entity classes: Player, Enemy, Bullet, and XPPickup."""

import math

import pygame

import config


class Player:
    """Player-controlled character.

    Moves with WASD, auto-attacks the nearest enemy.  Tracks HP, XP,
    and level progression.
    """

    def __init__(self):
        size = config.PLAYER_SIZE
        start_x = (config.SCREEN_WIDTH - size) // 2
        start_y = (config.SCREEN_HEIGHT - size) // 2
        self.rect = pygame.Rect(start_x, start_y, size, size)

        self.speed = config.PLAYER_SPEED
        self.hp = config.PLAYER_START_HP
        self.max_hp = config.PLAYER_MAX_HP
        self.xp = config.PLAYER_START_XP
        self.level = config.PLAYER_START_LEVEL
        self.attack_cooldown = config.PLAYER_ATTACK_COOLDOWN
        self.attack_damage = config.PLAYER_ATTACK_DAMAGE
        self.attack_range = config.PLAYER_ATTACK_RANGE
        self.attack_timer = 0.0

        # Special-ability flags (set by upgrades)
        self.piercing = 0
        self.triple_shot = False
        self.shield = False

    def move(self, dx: float, dy: float):
        """Shift the player by (dx, dy) pixels, clamped to the screen."""
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(pygame.Rect(0, 0, config.SCREEN_WIDTH,
                                       config.SCREEN_HEIGHT))

    def take_damage(self, amount: float):
        """Reduce HP by *amount*, flooring at zero.

        If *shield* is active, the shield absorbs the hit instead.
        """
        if self.shield:
            self.shield = False
            return
        self.hp = max(0, self.hp - amount)

    def gain_xp(self, amount: float):
        """Add XP and return True if the player levelled up."""
        self.xp += amount
        needed = self._xp_for_level(self.level)
        if self.xp >= needed:
            self.xp -= needed
            self.level += 1
            return True
        return False

    @staticmethod
    def _xp_for_level(level: int) -> int:
        """XP threshold to reach the next level."""
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
        """Render the player as a blue square on *surface*."""
        if self.shield:
            pygame.draw.rect(surface, config.CYAN, self.rect, width=3)
        pygame.draw.rect(surface, config.BLUE, self.rect)


class Enemy:
    """Hostile entity that moves toward the player.

    Deals contact damage and grants XP when killed.
    """

    def __init__(self, x: float, y: float):
        size = config.ENEMY_SIZE
        self.rect = pygame.Rect(x, y, size, size)
        self.hp = config.ENEMY_BASE_HP
        self.speed = config.ENEMY_BASE_SPEED
        self.damage = config.ENEMY_BASE_DAMAGE
        self.xp_value = config.ENEMY_BASE_XP_VALUE

    def take_damage(self, amount: float):
        """Reduce HP; returns True if the enemy died."""
        self.hp -= amount
        return self.hp <= 0

    def move_towards(self, target_pos: tuple, dt: float):
        """Move toward *target_pos* at self.speed, scaled by *dt*."""
        cx, cy = self.rect.center
        tx, ty = target_pos
        dx = tx - cx
        dy = ty - cy
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        self.rect.x += (dx / dist) * self.speed * dt
        self.rect.y += (dy / dist) * self.speed * dt

    def draw(self, surface: pygame.Surface):
        """Render the enemy as a red square on *surface*."""
        pygame.draw.rect(surface, config.RED, self.rect)


class Bullet:
    """Projectile fired by the player toward a target position."""

    def __init__(self, x: float, y: float, target_x: float, target_y: float,
                 damage: float, piercing: int = 0):
        size = config.BULLET_SIZE
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (x, y)

        self.damage = damage
        self.piercing = piercing

        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * config.BULLET_SPEED
            self.vy = (dy / dist) * config.BULLET_SPEED
        else:
            self.vx = 0.0
            self.vy = 0.0

        self.lifetime = config.BULLET_LIFETIME

    def update(self, dt: float):
        """Move bullet and decrease lifetime."""
        self.rect.x += self.vx * dt
        self.rect.y += self.vy * dt
        self.lifetime -= dt

    def is_alive(self) -> bool:
        """Returns False if the bullet timed out."""
        return self.lifetime > 0

    def is_off_screen(self) -> bool:
        """Returns True if the bullet is beyond the visible area."""
        m = config.ENEMY_SPAWN_MARGIN
        return (self.rect.right < -m or
                self.rect.left > config.SCREEN_WIDTH + m or
                self.rect.bottom < -m or
                self.rect.top > config.SCREEN_HEIGHT + m)

    def draw(self, surface: pygame.Surface):
        """Render the bullet as a yellow square."""
        pygame.draw.rect(surface, config.YELLOW, self.rect)


class XPPickup:
    """Experience orb dropped by dead enemies."""

    def __init__(self, x: float, y: float, value: int):
        size = config.PICKUP_SIZE
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (x, y)
        self.value = value
        self.lifetime = config.PICKUP_LIFETIME

    def update(self, dt: float):
        """Decrease lifetime every frame."""
        self.lifetime -= dt

    def is_alive(self) -> bool:
        """Returns False when the pickup should despawn."""
        return self.lifetime > 0

    def draw(self, surface: pygame.Surface):
        """Render the XP pickup as a green diamond."""
        cx, cy = self.rect.center
        half = config.PICKUP_SIZE // 2
        points = [
            (cx, cy - half),
            (cx + half, cy),
            (cx, cy + half),
            (cx - half, cy),
        ]
        pygame.draw.polygon(surface, config.GREEN, points)
