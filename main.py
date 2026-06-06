"""Entry point for the 2D roguelite survivor game.

Handles Pygame initialisation and the top-level state machine.
"""

import math

import pygame

import config
from entities import Player, Enemy, Bullet, XPPickup
from systems import WaveManager, UpgradeManager
from ui import draw_upgrade_screen


def run_game():
    """Initialise Pygame and run the main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH,
                                      config.SCREEN_HEIGHT))
    pygame.display.set_caption("Survivor's Legacy")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    # ── State machine ────────────────────────────────────────────────────
    MENU, PLAYING, UPGRADE, GAME_OVER = "MENU", "PLAYING", "UPGRADE", "GAME_OVER"
    state = MENU

    player = Player()
    enemies: list[Enemy] = []
    bullets: list[Bullet] = []
    pickups: list[XPPickup] = []
    wave_manager = WaveManager()
    upgrade_manager = UpgradeManager()
    pending_upgrades: list[dict] = []
    kills = 0
    score = 0

    running = True
    while running:
        dt = min(clock.tick(config.FPS) / 1000.0, 0.05)

        # ── Event handling ──────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == MENU and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = PLAYING

            if state == GAME_OVER and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player = Player()
                    enemies.clear()
                    bullets.clear()
                    pickups.clear()
                    wave_manager = WaveManager()
                    upgrade_manager = UpgradeManager()
                    pending_upgrades.clear()
                    kills = 0
                    score = 0
                    state = MENU

            if state == UPGRADE and event.type == pygame.KEYDOWN:
                index = None
                if event.key == pygame.K_1:
                    index = 0
                elif event.key == pygame.K_2:
                    index = 1
                elif event.key == pygame.K_3:
                    index = 2

                if index is not None and index < len(pending_upgrades):
                    upgrade_manager.apply_upgrade(player,
                                                  pending_upgrades[index])
                    pending_upgrades.clear()
                    state = PLAYING

        # ── Update ─────────────────────────────────────────────────────
        if state == PLAYING:
            # --- Player movement ---
            keys = pygame.key.get_pressed()
            dx = dy = 0.0
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy -= player.speed * dt
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy += player.speed * dt
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= player.speed * dt
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += player.speed * dt

            if dx != 0 and dy != 0:
                normal = (player.speed * dt) / (abs(dx) + abs(dy))
                dx *= normal
                dy *= normal

            player.move(dx, dy)

            # --- Auto-attack: fire at nearest enemy in range ---
            player.attack_timer -= dt
            if player.attack_timer <= 0:
                target = player.get_nearest_enemy(enemies)
                if target is not None:
                    _fire_bullets(player, target, bullets)
                    player.attack_timer = player.attack_cooldown

            # --- Update bullets ---
            for bullet in bullets[:]:
                bullet.update(dt)
                if not bullet.is_alive() or bullet.is_off_screen():
                    bullets.remove(bullet)

            # --- Enemy wave spawning ---
            wave_manager.update(dt, enemies)

            # --- Update enemies & contact damage ---
            for enemy in enemies[:]:
                enemy.move_towards(player.rect.center, dt)
                if player.rect.colliderect(enemy.rect):
                    player.take_damage(enemy.damage * dt)

            # --- Bullet ↔ enemy collisions ---
            for bullet in bullets[:]:
                hit_index = bullet.rect.collidelist(enemies)
                if hit_index != -1:
                    enemy = enemies[hit_index]
                    died = enemy.take_damage(bullet.damage)
                    if died:
                        pickups.append(
                            XPPickup(enemy.rect.centerx, enemy.rect.centery,
                                     enemy.xp_value)
                        )
                        enemies.remove(enemy)
                        kills += 1
                        wave_manager.on_enemy_killed()
                        score += enemy.xp_value * 10

                    # Piercing: keep flying if charges remain
                    if bullet.piercing > 0:
                        bullet.piercing -= 1
                    else:
                        bullets.remove(bullet)

            # --- Player ↔ pickup collisions ---
            for pickup in pickups[:]:
                pickup.update(dt)
                if not pickup.is_alive():
                    pickups.remove(pickup)
                    continue
                if player.rect.colliderect(pickup.rect):
                    levelled = player.gain_xp(pickup.value)
                    pickups.remove(pickup)
                    if levelled:
                        pending_upgrades = upgrade_manager.pick_upgrades(3)
                        state = UPGRADE

            # --- Player death ---
            if player.hp <= 0:
                state = GAME_OVER

        # ── Draw ────────────────────────────────────────────────────────
        screen.fill(config.DARK_GREY)

        if state == MENU:
            _draw_menu(screen, font)
        elif state == PLAYING:
            for pickup in pickups:
                pickup.draw(screen)
            for bullet in bullets:
                bullet.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            player.draw(screen)
            _draw_hud(screen, font, player, wave_manager, kills)
        elif state == UPGRADE:
            # Draw the frozen game scene underneath
            for pickup in pickups:
                pickup.draw(screen)
            for bullet in bullets:
                bullet.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            player.draw(screen)
            _draw_hud(screen, font, player, wave_manager, kills)
            # Overlay upgrade selection on top
            draw_upgrade_screen(screen, pending_upgrades, player)
        elif state == GAME_OVER:
            _draw_game_over(screen, font, score, wave_manager)

        pygame.display.flip()

    pygame.quit()


# ── Helper: fire bullet(s) ──────────────────────────────────────────────

_TRIPLE_SPREAD = math.radians(12)  # ±12 degrees


def _fire_bullets(player, target: Enemy, bullet_list: list):
    """Create one (or three, if triple-shot) bullets toward *target*."""
    px, py = player.rect.center
    tx, ty = target.rect.center

    # Base angle toward target
    angle = math.atan2(ty - py, tx - px)

    if player.triple_shot:
        # Fire three bullets in a spread
        offsets = (-_TRIPLE_SPREAD, 0, _TRIPLE_SPREAD)
        for off in offsets:
            a = angle + off
            bx = px + math.cos(a) * 20  # spawn slightly ahead
            by = py + math.sin(a) * 20
            # Calculate target point along this angle
            aim_x = px + math.cos(a) * 1000
            aim_y = py + math.sin(a) * 1000
            bullet = Bullet(bx, by, aim_x, aim_y, player.attack_damage,
                            piercing=player.piercing)
            bullet_list.append(bullet)
    else:
        bullet = Bullet(px, py, tx, ty, player.attack_damage,
                        piercing=player.piercing)
        bullet_list.append(bullet)


# ═════════════════════════════════════════════════════════════════════════
#  Drawing helpers
# ═════════════════════════════════════════════════════════════════════════

def _draw_menu(screen: pygame.Surface, font: pygame.font.Font):
    """Render the main menu screen."""
    title = font.render("Survivor's Legacy", True, config.WHITE)
    prompt = font.render("Press ENTER to play", True, config.WHITE)
    screen.blit(title,
                (config.SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(prompt,
                (config.SCREEN_WIDTH // 2 - prompt.get_width() // 2, 300))


def _draw_hud(screen: pygame.Surface, font: pygame.font.Font,
              player: Player, wave_manager: WaveManager, kills: int):
    """Render the in-game heads-up display with bars and stats."""
    bar_width, bar_height = 200, 16
    bar_x, bar_y = 12, 12

    # HP bar
    hp_ratio = player.hp / player.max_hp
    pygame.draw.rect(screen, config.GREY,
                     (bar_x, bar_y, bar_width, bar_height))
    fill_w = int(bar_width * hp_ratio)
    colour = config.HP_BAR_GREEN if hp_ratio > 0.3 else config.HP_BAR_RED
    if fill_w > 0:
        pygame.draw.rect(screen, colour,
                         (bar_x, bar_y, fill_w, bar_height))
    hp_label = font.render(f"HP {player.hp}/{player.max_hp}", True,
                           config.WHITE)
    screen.blit(hp_label, (bar_x, bar_y - 2))

    # XP bar (below HP)
    xp_y = bar_y + bar_height + 6
    needed = Player._xp_for_level(player.level)
    xp_ratio = player.xp / needed if needed > 0 else 0
    pygame.draw.rect(screen, config.GREY,
                     (bar_x, xp_y, bar_width, bar_height))
    if xp_ratio > 0:
        pygame.draw.rect(screen, config.XP_BAR_BLUE,
                         (bar_x, xp_y, int(bar_width * xp_ratio), bar_height))
    xp_label = font.render(f"Lv.{player.level}  XP {player.xp}/{needed}",
                           True, config.WHITE)
    screen.blit(xp_label, (bar_x, xp_y - 2))

    # Right-side stats
    stats_y = 12
    wave_text = font.render(f"Wave {wave_manager.wave_number}", True,
                            config.WHITE)
    kills_text = font.render(f"Kills: {kills}", True, config.WHITE)
    screen.blit(wave_text,
                (config.SCREEN_WIDTH - wave_text.get_width() - 12, stats_y))
    screen.blit(kills_text,
                (config.SCREEN_WIDTH - kills_text.get_width() - 12,
                 stats_y + 24))


def _draw_game_over(screen: pygame.Surface, font: pygame.font.Font,
                    score: int, wave_manager: WaveManager):
    """Render the game-over screen with final stats."""
    lines = [
        ("GAME OVER", config.RED),
        (f"Score: {score}", config.WHITE),
        (f"Wave reached: {wave_manager.wave_number}", config.WHITE),
        (f"Enemies killed: {wave_manager.enemies_killed}", config.WHITE),
        ("Press ENTER to return to menu", config.GREY),
    ]
    y = 220
    for text, colour in lines:
        rendered = font.render(text, True, colour)
        screen.blit(rendered,
                    (config.SCREEN_WIDTH // 2 - rendered.get_width() // 2, y))
        y += 36


if __name__ == "__main__":
    run_game()
