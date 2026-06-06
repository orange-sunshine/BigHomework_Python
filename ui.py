"""UI screens: menus, HUD, and upgrade selection overlay."""

import pygame

import config

# Rarity colour mapping
_RARITY_COLORS = {
    "common": config.GREY,
    "rare": config.BLUE,
    "legendary": (255, 215, 0),          # gold
}

_RARITY_BG = {
    "common": (60, 60, 60),
    "rare": (20, 40, 80),
    "legendary": (60, 45, 10),
}


def draw_upgrade_screen(screen: pygame.Surface,
                         upgrades: list[dict],
                         player) -> None:
    """Draw the dimmed upgrade-selection overlay with three cards."""
    # Semi-transparent overlay
    overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(config.BLACK)
    screen.blit(overlay, (0, 0))

    font_lg = pygame.font.Font(None, 42)
    font_md = pygame.font.Font(None, 28)
    font_sm = pygame.font.Font(None, 20)

    # Title
    title = font_lg.render("LEVEL UP!", True, config.WHITE)
    screen.blit(title,
                (config.SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

    sub = font_md.render("Choose an upgrade", True, config.GREY)
    screen.blit(sub,
                (config.SCREEN_WIDTH // 2 - sub.get_width() // 2, 85))

    # Three cards
    card_w, card_h = 220, 300
    gap = 30
    total_w = 3 * card_w + 2 * gap
    start_x = (config.SCREEN_WIDTH - total_w) // 2
    card_y = (config.SCREEN_HEIGHT - card_h) // 2

    # An accent line to show current stats preview
    stats_preview = font_sm.render(
        f"HP {player.hp}/{player.max_hp}  "
        f"DMG {player.attack_damage:.0f}  "
        f"SPD {player.speed:.0f}",
        True, config.GREY
    )
    screen.blit(stats_preview,
                (config.SCREEN_WIDTH // 2 - stats_preview.get_width() // 2,
                 card_y - 30))

    for i, upg in enumerate(upgrades):
        x = start_x + i * (card_w + gap)
        y = card_y
        rarity = upg["rarity"]
        border_color = _RARITY_COLORS[rarity]
        bg_color = _RARITY_BG[rarity]

        # Card shadow
        pygame.draw.rect(screen, (20, 20, 20), (x + 4, y + 4, card_w, card_h),
                         border_radius=8)
        # Card background
        pygame.draw.rect(screen, bg_color, (x, y, card_w, card_h),
                         border_radius=8)
        # Card border (rarity colour)
        pygame.draw.rect(screen, border_color, (x, y, card_w, card_h),
                         width=3, border_radius=8)

        # Rarity label
        rarity_label = font_sm.render(rarity.upper(), True, border_color)
        screen.blit(rarity_label,
                    (x + card_w // 2 - rarity_label.get_width() // 2,
                     y + 18))

        # Upgrade name
        name_label = font_md.render(upg["name"], True, config.WHITE)
        screen.blit(name_label,
                    (x + card_w // 2 - name_label.get_width() // 2,
                     y + 50))

        # Description (word-wrap manually via splitting)
        desc_lines = _word_wrap(upg["desc"], font_sm, card_w - 24)
        line_y = y + 90
        for line in desc_lines:
            desc_surf = font_sm.render(line, True, config.GREY)
            screen.blit(desc_surf,
                        (x + card_w // 2 - desc_surf.get_width() // 2,
                         line_y))
            line_y += 22

        # Hotkey number at bottom
        key_surf = font_lg.render(f"[{i + 1}]", True, border_color)
        screen.blit(key_surf,
                    (x + card_w // 2 - key_surf.get_width() // 2,
                     y + card_h - 50))

    # Bottom hint
    hint = font_md.render("Press 1, 2, or 3 to select", True, config.GREY)
    screen.blit(hint,
                (config.SCREEN_WIDTH // 2 - hint.get_width() // 2,
                 card_y + card_h + 30))


def _word_wrap(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    """Split *text* into lines that fit *max_width*."""
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for w in words[1:]:
        test = current + " " + w
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = w
    lines.append(current)
    return lines
