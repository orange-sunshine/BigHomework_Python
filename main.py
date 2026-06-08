"""Entry point — stationary turret survivor with DP / Equipment.

Player stays in the centre of the screen and auto-attacks.
Kills drop gold for in-run upgrades and DP for permanent progression.
"""

import math
import random

import pygame

import config
import i18n
import save_manager
from entities import Player, Enemy, Bullet, EquipmentItem
from systems import (WaveManager,
                     apply_permanent_bonuses,
                     generate_equipment, should_drop_equipment)
from ui import (draw_menu, draw_hud,
                draw_divine_power_screen, draw_equipment_screen,
                draw_game_over)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH,
                                      config.SCREEN_HEIGHT))
    pygame.display.set_caption("Survivor's Legacy")
    clock = pygame.time.Clock()
    font = i18n.L.create_font(28)
    font_lg = i18n.L.create_font(42)

    # ── State machine ────────────────────────────────────────────────────
    (MENU, PLAYING, GAME_OVER,
     DIVINE_POWER, EQUIPMENT) = range(5)
    state = MENU

    # ── Persistent save ─────────────────────────────────────────────────
    save_data = save_manager.load_data()
    i18n.L.LANG = save_data.get("lang", "en")

    # ── Per-run state ───────────────────────────────────────────────────
    player = Player()
    enemies: list[Enemy] = []
    bullets: list[Bullet] = []
    enemy_bullets: list[Bullet] = []
    wave_manager = WaveManager()
    kills = 0
    gold = 0
    gold_upgrades: dict = {}
    dp_earned_this_run = 0
    equip_notification = ""
    notif_timer = 0.0

    # Divine Power screen state
    dp_selected_index = 0
    dp_notification = ""
    dp_scroll_offset = 0

    # Upgrade panel
    show_upgrade_panel = False
    upgrade_tab = 0

    # Speed system
    SPEED_TIERS = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
    time_scale = 1.0
    speed_idx = 0

    # Clickable button rects (filled each frame's draw pass)
    click_buttons: dict[str, pygame.Rect] = {}

    running = True
    while running:
        dt = min(clock.tick(config.FPS) / 1000.0, 0.05)

        # ── Event handling ──────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ── MOUSE ─────────────────────────────────────────────────────
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for action, rect in click_buttons.items():
                    if not rect.collidepoint(event.pos):
                        continue

                    # MENU actions
                    if state == MENU and action == "start":
                        gold_upgrades = {g["key"]: 0
                                         for g in config.GOLD_UPGRADES}
                        (kills, gold, dp_earned_this_run,
                         equip_notification, notif_timer, time_scale,
                         speed_idx) = _start_new_run(
                             player, enemies, bullets, enemy_bullets,
                             wave_manager, save_data)
                        state = PLAYING
                    elif state == MENU and action == "dp":
                        state = DIVINE_POWER
                        dp_selected_index = 0
                        dp_scroll_offset = 0
                        dp_notification = ""
                    elif state == MENU and action == "equip":
                        state = EQUIPMENT
                    elif state == MENU and action == "lang":
                        _toggle_lang(save_data)
                    elif state == MENU and action == "clear_data":
                        _clear_save_data(save_data)
                    elif state == MENU and action == "exit_game":
                        running = False

                    # GAME OVER
                    elif state == GAME_OVER and action == "continue":
                        save_manager.add_divine_power(dp_earned_this_run)
                        save_data = save_manager.load_data()
                        (kills, gold, dp_earned_this_run,
                         equip_notification, notif_timer, time_scale,
                         speed_idx) = _reset_run_state()
                        state = MENU

                    # PLAYING → settlement (awards DP like death)
                    elif state == PLAYING and action == "exit":
                        state = GAME_OVER
                    elif state == PLAYING and action == "speed":
                        max_i = min(player.game_speed,
                                    len(SPEED_TIERS) - 1)
                        speed_idx = (speed_idx + 1) % (max_i + 1)
                        time_scale = SPEED_TIERS[speed_idx]

                    elif state == PLAYING and action == "upgrade":
                        show_upgrade_panel = not show_upgrade_panel
                    elif state == PLAYING and action.startswith("tab_"):
                        upgrade_tab = int(action[4:])
                    elif state == PLAYING and action.startswith("buy_"):
                        key = action[4:]
                        for cfg in config.GOLD_UPGRADES:
                            if cfg["key"] == key:
                                level = gold_upgrades.get(key, 0)
                                cost = int(cfg["base_cost"]
                                           * (cfg["cost_scale"] ** level))
                                if gold >= cost:
                                    gold -= cost
                                    gold_upgrades[key] = level + 1
                                    old_val = getattr(player, key)
                                    setattr(player, key,
                                            old_val + cfg["per_level"])
                                break

                    # EQUIPMENT
                    elif state == EQUIPMENT and action == "back":
                        save_data = save_manager.load_data()
                        state = MENU

                    # DIVINE POWER
                    elif state == DIVINE_POWER and action == "back":
                        save_data = save_manager.load_data()
                        state = MENU
                    elif state == DIVINE_POWER and action == "buy":
                        dp_notification = _buy_dp_perk(save_data,
                                                       dp_selected_index)
                    elif state == DIVINE_POWER and action == "scroll_up":
                        dp_scroll_offset = max(0, dp_scroll_offset - 1)
                    elif state == DIVINE_POWER and action == "scroll_down":
                        max_off = max(0, len(config.DIVINE_PERKS)
                                      - config.DP_VISIBLE_ROWS)
                        dp_scroll_offset = min(max_off, dp_scroll_offset + 1)
                    elif state == DIVINE_POWER:
                        # Clicked a perk row → select it
                        for perk in config.DIVINE_PERKS:
                            if perk["key"] == action:
                                dp_selected_index = config.DIVINE_PERKS.index(perk)
                                break

            # ── MOUSE WHEEL (Divine Power scroll) ──────────────────────
            if (event.type == pygame.MOUSEBUTTONDOWN
                    and state == DIVINE_POWER):
                max_off = max(0, len(config.DIVINE_PERKS)
                              - config.DP_VISIBLE_ROWS)
                if event.button == 4:  # scroll up
                    dp_scroll_offset = max(0, dp_scroll_offset - 1)
                elif event.button == 5:  # scroll down
                    dp_scroll_offset = min(max_off, dp_scroll_offset + 1)

            # ── KEYS ─────────────────────────────────────────────────────
            if event.type == pygame.KEYDOWN:
                # MENU
                if state == MENU:
                    if event.key == pygame.K_RETURN:
                        gold_upgrades = {g["key"]: 0
                                         for g in config.GOLD_UPGRADES}
                        (kills, gold, dp_earned_this_run,
                         equip_notification, notif_timer, time_scale,
                         speed_idx) = _start_new_run(
                             player, enemies, bullets, enemy_bullets,
                             wave_manager, save_data)
                        state = PLAYING
                    elif event.key == pygame.K_d:
                        state = DIVINE_POWER
                        dp_selected_index = 0
                        dp_scroll_offset = 0
                        dp_notification = ""
                    elif event.key == pygame.K_e:
                        state = EQUIPMENT
                    elif event.key == pygame.K_l:
                        _toggle_lang(save_data)

                # GAME OVER
                elif state == GAME_OVER and event.key == pygame.K_RETURN:
                    save_manager.add_divine_power(dp_earned_this_run)
                    save_data = save_manager.load_data()
                    (kills, gold, dp_earned_this_run,
                     equip_notification, notif_timer, time_scale,
                     speed_idx) = _reset_run_state()
                    state = MENU

                # DIVINE POWER
                elif state == DIVINE_POWER:
                    if event.key == pygame.K_UP:
                        dp_selected_index = max(0, dp_selected_index - 1)
                    elif event.key == pygame.K_DOWN:
                        dp_selected_index = min(
                            len(config.DIVINE_PERKS) - 1,
                            dp_selected_index + 1)
                    # Keep selected perk visible
                    if dp_selected_index < dp_scroll_offset:
                        dp_scroll_offset = dp_selected_index
                    if dp_selected_index >= (dp_scroll_offset
                                             + config.DP_VISIBLE_ROWS):
                        dp_scroll_offset = (dp_selected_index
                                            - config.DP_VISIBLE_ROWS + 1)
                    elif event.key == pygame.K_RETURN:
                        dp_notification = _buy_dp_perk(save_data,
                                                       dp_selected_index)
                    elif event.key == pygame.K_ESCAPE:
                        save_data = save_manager.load_data()
                        state = MENU

                # PLAYING
                elif state == PLAYING:
                    if event.key == pygame.K_m:
                        state = GAME_OVER
                    elif event.key == pygame.K_u:
                        show_upgrade_panel = not show_upgrade_panel
                    elif event.key == pygame.K_ESCAPE:
                        show_upgrade_panel = False
                    elif event.key == pygame.K_TAB:
                        max_i = min(player.game_speed,
                                    len(SPEED_TIERS) - 1)
                        speed_idx = (speed_idx + 1) % (max_i + 1)
                        time_scale = SPEED_TIERS[speed_idx]

                # EQUIPMENT
                elif state == EQUIPMENT and event.key == pygame.K_ESCAPE:
                    state = MENU

        # ── Update (PLAYING only) ──────────────────────────────────────
        if state == PLAYING:
            game_dt = dt * time_scale

            # Clamp speed_idx to available tiers
            if hasattr(player, "game_speed"):
                max_i = min(player.game_speed, len(SPEED_TIERS) - 1)
                speed_idx = min(speed_idx, max_i)
                time_scale = SPEED_TIERS[speed_idx]

            # Auto-attack
            player.attack_timer -= game_dt
            if player.attack_timer <= 0:
                target = player.get_nearest_enemy(enemies)
                if target is not None:
                    _fire_bullet(player, target, bullets)
                    player.attack_timer = player.attack_cooldown

            # Update bullets
            for bullet in bullets[:]:
                bullet.update(game_dt)
                if not bullet.is_alive() or bullet.is_off_screen():
                    bullets.remove(bullet)

                    # HP regeneration
            if player.hp_regen > 0 and player.hp < player.max_hp:
                player.hp = min(player.max_hp,
                                player.hp + player.hp_regen * game_dt)

            # Enemy wave spawning
            wave_manager.update(game_dt, enemies)

            # Update enemies & contact damage
            for enemy in enemies[:]:
                enemy.move_towards(player.rect.center, game_dt)
                if player.rect.colliderect(enemy.rect):
                    player.take_damage(enemy.damage * game_dt)

                # Enemy shoots at player
                enemy.attack_timer -= game_dt
                if enemy.attack_timer <= 0:
                    dx = player.rect.centerx - enemy.rect.centerx
                    dy = player.rect.centery - enemy.rect.centery
                    if math.hypot(dx, dy) < enemy.attack_range:
                        eb = Bullet(enemy.rect.centerx, enemy.rect.centery,
                                    player.rect.centerx, player.rect.centery,
                                    enemy.damage, owner="enemy")
                        enemy_bullets.append(eb)
                        enemy.attack_timer = enemy.attack_cooldown

            # Bullet ↔ enemy collisions (swept rect to prevent tunneling)
            for bullet in bullets[:]:
                swept = bullet.rect.inflate(abs(bullet.vx * game_dt),
                                            abs(bullet.vy * game_dt))
                hit = swept.collidelist(enemies)
                if hit != -1:
                    enemy = enemies[hit]
                    died = enemy.take_damage(bullet.damage)
                    # Lifesteal
                    if player.lifesteal > 0:
                        heal = bullet.damage * player.lifesteal
                        player.hp = min(player.max_hp,
                                        player.hp + heal)
                    if died:
                        enemies.remove(enemy)
                        kills += 1
                        wave_manager.on_enemy_killed()
                        # Gold + DP drop
                        gold_base = enemy.gold_value
                        gold_pre = gold_base * player.gold_modifier
                        gold += int(gold_pre + 0.5)
                        dp_from_kill = max(1, int(
                            gold_base * config.DP_DROP_RATIO
                            * (1 + player.dp_bonus) + 0.5))
                        dp_earned_this_run += dp_from_kill

                        if should_drop_equipment(wave_manager.wave_number):
                            msg = _try_equip_drop(save_data, wave_manager)
                            if msg:
                                equip_notification = msg
                                notif_timer = 3.0

                    if bullet.piercing > 0:
                        retention = min(0.95, config.PENETRATION_RATE
                                        + player.piercing * 0.02)
                        bullet.damage *= retention
                        bullet.piercing -= 1
                    else:
                        bullets.remove(bullet)

            # Enemy bullets update & collision with player
            for bullet in enemy_bullets[:]:
                bullet.update(game_dt)
                if (not bullet.is_alive()
                        or bullet.is_off_screen()
                        or bullet.rect.colliderect(player.rect)):
                    enemy_bullets.remove(bullet)
                    if bullet.rect.colliderect(player.rect):
                        player.take_damage(bullet.damage)

            # Timers
            if notif_timer > 0:
                notif_timer -= dt

            # Player death
            if player.hp <= 0:
                state = GAME_OVER

        # ── Draw ────────────────────────────────────────────────────────
        screen.fill(config.DARK_GREY)

        if state == MENU:
            click_buttons = draw_menu(screen, font, save_data)

        elif state == PLAYING:
            for bullet in bullets:
                bullet.draw(screen)
            for bullet in enemy_bullets:
                bullet.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            player.draw(screen)
            click_buttons = draw_hud(screen, font, player, wave_manager,
                                     kills, gold, dp_earned_this_run,
                                     equip_notification,
                                     notif_timer, time_scale,
                                     show_upgrade_panel, upgrade_tab,
                                     gold_upgrades)

        elif state == GAME_OVER:
            click_buttons = draw_game_over(screen, font,
                                           wave_manager.enemies_killed,
                                           dp_earned_this_run)

        elif state == DIVINE_POWER:
            click_buttons = draw_divine_power_screen(
                screen, font, font_lg, save_data, dp_selected_index,
                dp_notification, dp_scroll_offset)

        elif state == EQUIPMENT:
            click_buttons = draw_equipment_screen(screen, font, font_lg,
                                                  save_data)

        pygame.display.flip()

    pygame.quit()


# ═════════════════════════════════════════════════════════════════════════
#  Helper functions
# ═════════════════════════════════════════════════════════════════════════

def _start_new_run(player, enemies, bullets, enemy_bullets,
                   wave_manager, save_data):
    """Reset per-run state and apply permanent bonuses.

    Returns tuple of initial (kills, gold, dp_earned_this_run,
    equip_notification, notif_timer, time_scale, speed_idx).
    """
    player.__init__()
    apply_permanent_bonuses(player, save_data)
    enemies.clear()
    bullets.clear()
    enemy_bullets.clear()
    wave_manager.__init__()
    return (0, 0, 0, "", 0.0, 1.0, 0)


def _reset_run_state():
    """Return clean initial values for per-run tracking variables."""
    return (0, 0, 0, "", 0.0, 1.0, 0)


def _buy_dp_perk(save_data: dict, selected_index: int) -> str:
    """Purchase the selected perk if affordable.  Returns notification text."""
    perks = config.DIVINE_PERKS
    if selected_index < 0 or selected_index >= len(perks):
        return ""
    perk = perks[selected_index]
    key = perk["key"]
    level = save_data.get("perk_levels", {}).get(key, 0)
    if level >= perk["max"]:
        return i18n.L.t("dp_maxed")
    cost = config.perk_cost(level, perk.get("cost_scale", 1.0))
    if save_data["dp"] < cost:
        return i18n.L.t("dp_nofunds")
    save_data["dp"] -= cost
    save_data["perk_levels"][key] = level + 1
    save_manager.save_data(save_data)
    return i18n.L.t("dp_bought", i18n.L.perk_name(key), level + 1)


def _toggle_lang(save_data: dict):
    """Switch language between en/zh and persist."""
    i18n.L.LANG = "zh" if i18n.L.LANG == "en" else "en"
    save_data["lang"] = i18n.L.LANG
    save_manager.save_data(save_data)


def _clear_save_data(save_data: dict):
    """Reset all save data to defaults (DP, perks, equipment)."""
    lang = save_data.get("lang", "en")
    save_data.clear()
    save_data["lang"] = lang
    save_data["dp"] = 0
    save_data["total_dp_earned"] = 0
    save_data["perk_levels"] = {p["key"]: 0 for p in config.DIVINE_PERKS}
    save_data["equipped"] = {}
    save_manager.save_data(save_data)


def _fire_bullet(player, target: Enemy, bullet_list: list):
    """Fire bullet_count bullets in a spread toward *target*."""
    px, py = player.rect.center
    tx, ty = target.rect.center
    is_crit = random.random() < player.crit_rate
    dmg = player.attack_damage * (player.crit_damage if is_crit else 1.0)
    count = max(1, player.bullet_count)
    base_angle = math.atan2(ty - py, tx - px)
    step = 0.12
    for i in range(count):
        if i == 0:
            offset = 0.0
        elif i % 2 == 1:
            offset = -step * ((i + 1) // 2)
        else:
            offset = step * (i // 2)
        angle = base_angle + offset
        spread_tx = px + math.cos(angle) * 100
        spread_ty = py + math.sin(angle) * 100
        bullet = Bullet(px, py, spread_tx, spread_ty, dmg,
                        piercing=player.piercing, is_critical=is_crit)
        bullet_list.append(bullet)


def _try_equip_drop(save_data: dict, wave_manager) -> str:
    """Generate and auto-equip a better item.  Returns notification str."""
    item = generate_equipment(wave_manager.wave_number)
    slot = item.slot
    rarity = item.rarity
    tier_map = {r: i for i, r in enumerate(config.EQUIP_RARITIES)}
    new_tier = tier_map.get(rarity, 0)

    current = save_data["equipped"].get(slot)
    replace = False
    if current is None:
        replace = True
    else:
        try:
            cur_item = EquipmentItem.from_dict(current)
            replace = new_tier > tier_map.get(cur_item.rarity, 0)
        except (KeyError, TypeError, ValueError):
            replace = True

    if replace:
        save_data["equipped"][slot] = item.to_dict()
        save_manager.save_data(save_data)
        return i18n.L.t("equip_drop",
                        i18n.L.rarity_name(rarity).upper(),
                        i18n.L.slot_name(slot))
    return ""


if __name__ == "__main__":
    run_game()
