"""Game systems: Divine Power, equipment generation, wave management."""

import random

import config
from entities import Enemy, EquipmentItem


# ═════════════════════════════════════════════════════════════════════════
#  Divine Power helpers
# ═════════════════════════════════════════════════════════════════════════

def calculate_divine_power(player_level: int, kills: int,
                           wave_number: int, dp_bonus: float = 0) -> int:
    """Return DP earned, scaled by dp_bonus multiplier."""
    base = player_level * wave_number / 5 + kills / 10
    return int(base * (1 + dp_bonus))


def apply_permanent_bonuses(player, save_data: dict):
    """Mutate *player* with perks and equipment from *save_data*."""
    for perk_def in config.DIVINE_PERKS:
        key = perk_def["key"]
        level = save_data.get("perk_levels", {}).get(key, 0)
        if level <= 0:
            continue
        ptype = perk_def["type"]
        per_level = perk_def["per_level"]
        if ptype == "add":
            old = getattr(player, key)
            setattr(player, key, old + per_level * level)
        elif ptype == "mult":
            old = getattr(player, key)
            setattr(player, key, old * (per_level ** level))
        if key == "max_hp":
            player.hp = player.max_hp

    equipped = save_data.get("equipped", {})
    for slot in config.EQUIP_SLOTS:
        item_data = equipped.get(slot)
        if item_data is None:
            continue
        try:
            item = EquipmentItem.from_dict(item_data)
        except (KeyError, TypeError):
            continue
        for affix in item.affixes:
            attr = affix.get("attr")
            value = affix.get("value", 0)
            if attr is None:
                continue
            old = getattr(player, attr, None)
            if old is not None:
                setattr(player, attr, old + value)
                if attr == "max_hp":
                    player.hp += value


# ═════════════════════════════════════════════════════════════════════════
#  Equipment generation
# ═════════════════════════════════════════════════════════════════════════

def generate_equipment(wave: int) -> EquipmentItem:
    """Create a random equipment drop scaled by current wave."""
    tier_weights = _rarity_weights_for_wave(wave)
    rarity = random.choices(config.EQUIP_RARITIES,
                            weights=tier_weights, k=1)[0]
    tier = config.EQUIP_RARITIES.index(rarity)
    slot = random.choice(config.EQUIP_SLOTS)
    num_affixes = tier + 1

    pool = list(config.EQUIP_AFFIXES)
    random.shuffle(pool)
    chosen_affixes = pool[:num_affixes]
    affixes = [{"name": a["name"], "attr": a["attr"],
                "value": a["per_tier"][tier]} for a in chosen_affixes]

    return EquipmentItem(slot=slot, rarity=rarity, affixes=affixes)


def should_drop_equipment(wave: int) -> bool:
    chance = config.EQUIP_DROP_BASE_CHANCE + config.EQUIP_DROP_WAVE_BONUS * wave
    return random.random() < chance


def _rarity_weights_for_wave(wave: int) -> list[float]:
    base = [30, 30, 15, 4, 1]
    shift = wave // 5
    for _ in range(shift):
        base = [w * 0.6 for w in base]
        base[-1] = max(base[-1], 1)
    return base


# ═════════════════════════════════════════════════════════════════════════
#  Wave manager
# ═════════════════════════════════════════════════════════════════════════

class WaveManager:
    """Controls enemy wave progression and spawn timing."""

    def __init__(self):
        self.wave_number = 1
        self.enemies_in_wave = config.WAVE_BASE_ENEMIES
        self.enemies_spawned = 0
        self.enemies_killed = 0
        self.spawn_timer = 0.0

    def update(self, dt: float, enemy_list: list):
        if self.enemies_spawned < self.enemies_in_wave:
            if self.spawn_timer <= 0:
                count = self.enemies_in_wave - self.enemies_spawned
                for _ in range(count):
                    x, y = self._random_edge_position()
                    enemy = Enemy(x, y)
                    self._scale_enemy(enemy)
                    enemy_list.append(enemy)
                self.enemies_spawned = self.enemies_in_wave
            else:
                self.spawn_timer -= dt

        if self.enemies_spawned >= self.enemies_in_wave and len(enemy_list) == 0:
            self._next_wave()

    def on_enemy_killed(self):
        self.enemies_killed += 1

    def _random_edge_position(self):
        side = random.randint(0, 3)
        m = config.ENEMY_SPAWN_MARGIN
        if side == 0:
            return random.uniform(0, config.SCREEN_WIDTH), -m
        elif side == 1:
            return (random.uniform(0, config.SCREEN_WIDTH),
                    config.SCREEN_HEIGHT + m)
        elif side == 2:
            return -m, random.uniform(0, config.SCREEN_HEIGHT)
        else:
            return (config.SCREEN_WIDTH + m,
                    random.uniform(0, config.SCREEN_HEIGHT))

    def _scale_enemy(self, enemy: Enemy):
        w = self.wave_number
        enemy.hp = int(config.ENEMY_BASE_HP * (1 + w * config.WAVE_HP_SCALE))
        enemy.speed = config.ENEMY_BASE_SPEED * (1 + w * config.WAVE_SPEED_SCALE)
        enemy.damage = config.ENEMY_BASE_DAMAGE * (1 + w * config.WAVE_DAMAGE_SCALE)
        enemy.xp_value = int(config.ENEMY_BASE_XP_VALUE *
                             (1 + w * config.WAVE_XP_SCALE))
        enemy.attack_cooldown = max(0.4, 2.0 - w * 0.08)
        enemy.attack_range = config.ENEMY_ATTACK_RANGE + w * 5

    def _next_wave(self):
        self.wave_number += 1
        self.enemies_in_wave = (config.WAVE_BASE_ENEMIES
                                + self.wave_number * config.WAVE_ENEMY_INCREMENT)
        self.enemies_spawned = 0
        self.spawn_timer = 1.0
