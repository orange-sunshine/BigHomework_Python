"""UI screens: menus, HUD, divine power, equipment, game over.

All draw functions that return button rects for mouse interaction.
"""

import pygame

import config
from entities import EquipmentItem
from i18n import L




# ═════════════════════════════════════════════════════════════════════════
#  Main menu  (returns clickable button rects)
# ═════════════════════════════════════════════════════════════════════════

def draw_menu(screen, font, save_data) -> dict:
    """Render main menu.  Returns {action_name: pygame.Rect} for mouse."""
    font_lg = L.create_font(42)

    title = font_lg.render(L.t("menu_title"), True, config.WHITE)
    dp_text = font.render(
        L.t("dp_available", save_data["dp"]), True, config.GOLD)

    screen.blit(title,
                (config.SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(dp_text,
                (config.SCREEN_WIDTH // 2 - dp_text.get_width() // 2, 155))

    items = [
        ("start",  L.t("start_game"),         config.WHITE),
        ("dp",     L.t("dp_perm"),            config.GOLD),
        ("equip",  L.t("equipment"),          config.ORANGE),
    ]
    buttons = {}
    y = 260
    for action, label, colour in items:
        surf = font.render(f"[ {label} ]", True, colour)
        rect = surf.get_rect(center=(config.SCREEN_WIDTH // 2, y))
        pygame.draw.rect(screen, (50, 50, 50),
                         rect.inflate(30, 8), border_radius=4)
        screen.blit(surf, rect)
        buttons[action] = rect.inflate(30, 8)
        y += 50

    # Language toggle
    lang_label = L.t("lang_label",
                     "EN" if L.LANG == "en" else "中文")
    lang_surf = font.render(lang_label, True, config.CYAN)
    lang_rect = lang_surf.get_rect(
        center=(config.SCREEN_WIDTH // 2, y))
    pygame.draw.rect(screen, (50, 50, 50),
                     lang_rect.inflate(30, 8), border_radius=4)
    screen.blit(lang_surf, lang_rect)
    buttons["lang"] = lang_rect.inflate(30, 8)
    y += 50

    # Clear Data button (red)
    clear_surf = font.render(f"[ {L.t('clear_data')} ]", True, config.RED)
    clear_rect = clear_surf.get_rect(
        center=(config.SCREEN_WIDTH // 2, y))
    pygame.draw.rect(screen, (50, 20, 20),
                     clear_rect.inflate(30, 8), border_radius=4)
    screen.blit(clear_surf, clear_rect)
    buttons["clear_data"] = clear_rect.inflate(30, 8)
    y += 50

    # Exit Game button
    exit_surf = font.render(f"[ {L.t('exit_game')} ]", True, config.RED)
    exit_rect = exit_surf.get_rect(
        center=(config.SCREEN_WIDTH // 2, y))
    pygame.draw.rect(screen, (50, 20, 20),
                     exit_rect.inflate(30, 8), border_radius=4)
    screen.blit(exit_surf, exit_rect)
    buttons["exit_game"] = exit_rect.inflate(30, 8)
    y += 30

    # Controls hint
    hint = font.render(L.t("controls_hint"), True, config.GREY)
    screen.blit(hint,
                (config.SCREEN_WIDTH // 2 - hint.get_width() // 2, y + 20))

    return buttons


# ═════════════════════════════════════════════════════════════════════════
#  Divine Power screen  (returns clickable perk row rects + back button)
# ═════════════════════════════════════════════════════════════════════════

def draw_divine_power_screen(screen, font, font_lg,
                              save_data, selected_index,
                              notification="",
                              scroll_offset=0) -> dict:
    """Render DP perk tree with a scrollable list container.

    Returns dict mapping action-name → clickable pygame.Rect.
    """
    overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    overlay.set_alpha(40)
    overlay.fill(config.BLACK)
    screen.blit(overlay, (0, 0))

    font_sm = L.create_font(20)
    perks = config.DIVINE_PERKS
    row_h = 55
    visible_rows = config.DP_VISIBLE_ROWS

    # ── Fixed top area ───────────────────────────────────────────────
    title = font_lg.render(L.t("dp_title"), True, config.GOLD)
    screen.blit(title,
                (config.SCREEN_WIDTH // 2 - title.get_width() // 2, 15))

    dp_text = font.render(L.t("dp_available", save_data["dp"]), True,
                          config.WHITE)
    screen.blit(dp_text,
                (config.SCREEN_WIDTH // 2 - dp_text.get_width() // 2, 58))

    # ── Scrollable list container ────────────────────────────────────
    container_h = visible_rows * row_h + 8
    container = pygame.Rect(40, 90, 720, container_h)
    pygame.draw.rect(screen, (30, 30, 30), container, border_radius=6)
    pygame.draw.rect(screen, (80, 80, 80), container, width=1,
                     border_radius=6)

    max_offset = max(0, len(perks) - visible_rows)
    scroll_offset = min(scroll_offset, max_offset)

    clip_rect = container.inflate(-8, -4)
    original_clip = screen.get_clip()
    screen.set_clip(clip_rect)

    clickable = {}

    for i in range(scroll_offset,
                   min(scroll_offset + visible_rows, len(perks))):
        perk = perks[i]
        key = perk["key"]
        level = save_data["perk_levels"].get(key, 0)
        max_lv = perk["max"]
        cost = config.perk_cost(level, perk.get("cost_scale", 1.0))
        can_afford = save_data["dp"] >= cost and level < max_lv
        is_selected = (i == selected_index)

        y = container.y + 4 + (i - scroll_offset) * row_h
        bg = (70, 70, 50) if is_selected else config.DARK_GREY
        row_rect = pygame.Rect(container.x + 8, y,
                               container.width - 16, row_h - 4)
        pygame.draw.rect(screen, bg, row_rect, border_radius=4)
        if is_selected:
            pygame.draw.rect(screen, config.YELLOW, row_rect, width=2,
                             border_radius=4)

        name_surf = font.render(L.perk_name(key), True, config.WHITE)
        screen.blit(name_surf, (row_rect.x + 10, y + 4))

        desc_surf = font_sm.render(L.perk_desc(key), True, config.GREY)
        screen.blit(desc_surf, (row_rect.x + 10, y + 28))

        bar_x = row_rect.x + 280
        bar_y = y + 8
        bar_w, bar_h = 160, 16
        if max_lv >= config.NO_MAX:
            fill_pct = 0
        else:
            fill_pct = level / max_lv if max_lv > 0 else 0
        pygame.draw.rect(screen, (60, 60, 60),
                         (bar_x, bar_y, bar_w, bar_h))
        if fill_pct > 0:
            pygame.draw.rect(screen, config.BAR_BLUE,
                             (bar_x, bar_y,
                              int(bar_w * fill_pct), bar_h))
        if max_lv >= config.NO_MAX:
            lv_text = font_sm.render(f"Lv.{level}", True, config.WHITE)
        else:
            lv_text = font_sm.render(f"{level}/{max_lv}", True, config.WHITE)
        screen.blit(lv_text, (bar_x + bar_w + 6, bar_y - 2))
        lv_w = lv_text.get_width()

        if level >= max_lv:
            status = font_sm.render(L.t("max"), True, config.GREEN)
        elif can_afford:
            status = font_sm.render(L.t("cost", cost), True, config.GOLD)
        else:
            status = font_sm.render(L.t("cost", cost), True, config.GREY)
        status_x = bar_x + bar_w + 6 + lv_w + 20
        screen.blit(status, (status_x, bar_y - 2))

        clickable[key] = row_rect

    screen.set_clip(original_clip)

    # ── Scroll arrows (overlaid on container edges) ──────────────────
    if scroll_offset > 0:
        up = font_sm.render("▲", True, config.CYAN)
        up_rect = up.get_rect(
            center=(container.centerx, container.y + 2))
        screen.blit(up, up_rect)
        clickable["scroll_up"] = up_rect.inflate(30, 6)
    if scroll_offset < max_offset:
        down = font_sm.render("▼", True, config.CYAN)
        down_rect = down.get_rect(
            center=(container.centerx, container.bottom - 2))
        screen.blit(down, down_rect)
        clickable["scroll_down"] = down_rect.inflate(30, 6)

    # ── Notification (below container, above buttons) ────────────────
    notification_y = container.bottom + 8
    if notification:
        notif = font.render(notification, True, config.GREEN)
        screen.blit(notif,
                    (config.SCREEN_WIDTH // 2 - notif.get_width() // 2,
                     notification_y))

    # ── Fixed bottom buttons ─────────────────────────────────────────
    btn_y = notification_y + 50
    buy_rect = pygame.Rect(0, 0, 180, 36)
    buy_rect.center = (config.SCREEN_WIDTH // 2 - 100, btn_y)
    pygame.draw.rect(screen, (60, 60, 60), buy_rect, border_radius=4)
    buy_text = font_sm.render(L.t("buy_btn"), True, config.WHITE)
    screen.blit(buy_text, buy_text.get_rect(center=buy_rect.center))

    back_rect = pygame.Rect(0, 0, 180, 36)
    back_rect.center = (config.SCREEN_WIDTH // 2 + 100, btn_y)
    pygame.draw.rect(screen, (60, 60, 60), back_rect, border_radius=4)
    back_text = font_sm.render(L.t("back_btn"), True, config.WHITE)
    screen.blit(back_text, back_text.get_rect(center=back_rect.center))

    clickable["buy"] = buy_rect
    clickable["back"] = back_rect
    return clickable


# ═════════════════════════════════════════════════════════════════════════
#  Equipment screen
# ═════════════════════════════════════════════════════════════════════════

def draw_equipment_screen(screen, font, font_lg, save_data):
    """Show currently equipped items.  Returns {'back': rect}."""
    overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    overlay.set_alpha(40)
    overlay.fill(config.BLACK)
    screen.blit(overlay, (0, 0))

    font_sm = L.create_font(20)

    title = font_lg.render(L.t("equip_title"), True, config.ORANGE)
    screen.blit(title,
                (config.SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    equipped = save_data.get("equipped", {})
    y = 80

    for slot in config.EQUIP_SLOTS:
        slot_name = L.slot_name(slot)
        s = font.render(f"[ {slot_name} ]", True, config.WHITE)
        screen.blit(s, (60, y))
        y += 35

        item_data = equipped.get(slot)
        if item_data is None:
            empty = font_sm.render(L.t("equip_empty"), True, config.GREY)
            screen.blit(empty, (80, y))
            y += 50
            continue

        try:
            item = EquipmentItem.from_dict(item_data)
        except (KeyError, TypeError):
            empty = font_sm.render(L.t("equip_invalid"), True, config.RED)
            screen.blit(empty, (80, y))
            y += 50
            continue

        rarity_color = config.EQUIP_RARITY_COLORS.get(item.rarity,
                                                       config.GREY)
        rt = font_sm.render(L.rarity_name(item.rarity).upper(), True,
                            rarity_color)
        screen.blit(rt, (80, y))
        y += 22

        for affix in item.affixes:
            label = L.affix_name(affix["name"])
            a = font_sm.render(
                f"  {label}: +{L.fmt(affix['value'])}",
                True, config.GREY)
            screen.blit(a, (100, y))
            y += 20
        y += 10

    # Back button
    hint = font_sm.render(L.t("equip_back"), True, config.GREY)
    back_rect = hint.get_rect(
        center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 40))
    pygame.draw.rect(screen, (60, 60, 60), back_rect.inflate(30, 8),
                     border_radius=4)
    screen.blit(hint, back_rect)
    return {"back": back_rect.inflate(30, 8)}


# ═════════════════════════════════════════════════════════════════════════
#  In-game HUD  (expanded stats)
# ═════════════════════════════════════════════════════════════════════════

def _render_fit(text, max_width, base_size=28, min_size=10):
    """Render *text* at the largest size that fits *max_width*."""
    for size in range(base_size, min_size - 1, -2):
        f = L.create_font(size)
        surf = f.render(text, True, config.WHITE)
        if surf.get_width() <= max_width:
            return surf
    f = L.create_font(min_size)
    return f.render(text, True, config.WHITE)


def draw_hud(screen, font, player, wave_manager, kills,
             gold=0, dp_earned=0, equip_notification="", notif_timer=0,
             time_scale=1.0, show_upgrade=False, upgrade_tab=0,
             gold_upgrades=None):
    """Render HUD with HP bar, gold display, stats panel, and action buttons.

    When *show_upgrade* is True, embeds the upgrade panel at the bottom.
    Returns dict of clickable button rects.
    """
    bar_w, bar_h = 260, 24
    bx, by = 12, 12
    inner_w = bar_w - 8
    buttons = {}

    # HP bar
    hp_ratio = player.hp / player.max_hp
    pygame.draw.rect(screen, config.GREY, (bx, by, bar_w, bar_h))
    fill = int(bar_w * hp_ratio)
    colour = config.HP_BAR_GREEN if hp_ratio > 0.3 else config.HP_BAR_RED
    if fill > 0:
        pygame.draw.rect(screen, colour, (bx, by, fill, bar_h))
    hp_text = L.t("hud_hp", int(player.hp), int(player.max_hp))
    hp_l = _render_fit(hp_text, inner_w)
    hp_l_rect = hp_l.get_rect(
        midleft=(bx + 4, by + bar_h // 2))
    screen.blit(hp_l, hp_l_rect)

    # Gold display (below HP bar)
    gold_y = by + bar_h + 10
    gold_text = L.t("hud_gold", gold)
    gold_surf = font.render(gold_text, True, config.GOLD)
    screen.blit(gold_surf, (bx, gold_y))

    # DP display (below gold)
    dp_text = L.t("hud_dp", dp_earned)
    dp_surf = font.render(dp_text, True, config.PURPLE)
    screen.blit(dp_surf, (bx, gold_y + 26))

    # Top-right: Wave, Kills, Bullets
    sx = config.SCREEN_WIDTH - 210
    sy = 10
    for text in (L.t("hud_wave", wave_manager.wave_number),
                 L.t("hud_kills", kills),
                 L.t("hud_bcount", player.bullet_count)):
        surf = font.render(text, True, config.GREY)
        screen.blit(surf, (sx, sy))
        sy += 22

    # Exit button (bottom-left)
    exit_text = L.t("hud_exit")
    exit_surf = font.render(exit_text, True, config.GREY)
    exit_rect = exit_surf.get_rect(
        bottomleft=(12, config.SCREEN_HEIGHT - 8))
    pygame.draw.rect(screen, (50, 50, 50),
                     exit_rect.inflate(12, 6), border_radius=4)
    screen.blit(exit_surf, exit_rect)
    buttons["exit"] = exit_rect.inflate(12, 6)

    # Speed button (next to exit)
    max_speed = getattr(player, "game_speed", 0)
    label = "x1" if max_speed == 0 else L.t("hud_speed_btn",
                                             L.fmt(time_scale))
    speed_surf = font.render(label, True,
                             config.CYAN if max_speed > 0 else config.GREY)
    speed_rect = speed_surf.get_rect(
        bottomleft=(exit_rect.right + 20, config.SCREEN_HEIGHT - 8))
    pygame.draw.rect(screen, (50, 50, 50),
                     speed_rect.inflate(12, 6), border_radius=4)
    screen.blit(speed_surf, speed_rect)
    buttons["speed"] = speed_rect.inflate(12, 6)

    # Upgrade button (next to speed)
    upg_text = L.t("hud_upgrade")
    upg_surf = font.render(upg_text, True, config.YELLOW)
    upg_rect = upg_surf.get_rect(
        bottomleft=(speed_rect.right + 20, config.SCREEN_HEIGHT - 8))
    pygame.draw.rect(screen, (50, 50, 50),
                     upg_rect.inflate(12, 6), border_radius=4)
    screen.blit(upg_surf, upg_rect)
    buttons["upgrade"] = upg_rect.inflate(12, 6)

    # Equipment drop notification
    if equip_notification and notif_timer > 0:
        n = font.render(equip_notification, True, config.ORANGE)
        nx = config.SCREEN_WIDTH // 2 - n.get_width() // 2
        ny = config.SCREEN_HEIGHT - 50
        screen.blit(n, (nx, ny))

    # ── Embedded upgrade panel ─────────────────────────────────────
    if show_upgrade:
        if gold_upgrades is None:
            gold_upgrades = {}
        font_sm = L.create_font(18)
        panel = pygame.Rect(80, 375, 640, 210)
        # backdrop
        backdrop = pygame.Surface((panel.width, panel.height))
        backdrop.set_alpha(200)
        backdrop.fill((20, 20, 30))
        screen.blit(backdrop, panel)
        pygame.draw.rect(screen, (80, 80, 80), panel, width=1,
                         border_radius=4)

        # ── Tab row ────────────────────────────────────────────────
        tab_keys = config.UPGRADE_TABS
        tab_w = (panel.width - 60) // 3
        tab_h = 26
        tab_y = panel.y + 6
        for i, tcfg in enumerate(tab_keys):
            tx = panel.x + 10 + i * (tab_w + 10)
            selected = i == upgrade_tab
            bg = (55, 55, 65) if selected else (40, 40, 40)
            tr = pygame.Rect(tx, tab_y, tab_w, tab_h)
            pygame.draw.rect(screen, bg, tr, border_radius=3)
            if selected:
                pygame.draw.rect(screen, config.GOLD, tr, width=1,
                                 border_radius=3)
            ts = font.render(L.t(tcfg["label_key"]), True,
                             config.GOLD if selected else config.GREY)
            screen.blit(ts, ts.get_rect(center=tr.center))
            buttons[f"tab_{i}"] = tr

        # Gold in top-right of panel
        gs = font_sm.render(L.t("hud_gold", gold), True, config.GOLD)
        screen.blit(gs, (panel.right - gs.get_width() - 10, tab_y + 2))

        # ── Upgrade buttons ───────────────────────────────────────
        tab_upgrades = tab_keys[upgrade_tab]["upgrades"]
        cols = 3 if len(tab_upgrades) > 4 else 2
        btn_w = (panel.width - 30 - (cols - 1) * 8) // cols
        btn_h = 50
        row0 = tab_y + tab_h + 8
        row_gap = 6

        def _val_str(key, raw):
            if key in ("crit_rate", "lifesteal"):
                return f"{int(raw*100)}%"
            if key == "crit_damage":
                return f"{int(raw*100)}%"
            if key == "dp_bonus":
                return f"+{int(raw*100)}%"
            if key == "gold_modifier":
                return f"+{int((raw-1)*100)}%"
            if key == "attack_cooldown":
                return f"{L.fmt(raw)}s"
            if isinstance(raw, float):
                return L.fmt(raw)
            return str(int(raw))

        for idx, key in enumerate(tab_upgrades):
            row = idx // cols
            col = idx % cols
            cfg = next(g for g in config.GOLD_UPGRADES
                       if g["key"] == key)
            level = gold_upgrades.get(key, 0)
            cost = int(cfg["base_cost"] * (cfg["cost_scale"] ** level))
            can_afford = gold >= cost

            bx = panel.x + 15 + col * (btn_w + 8)
            by = row0 + row * (btn_h + row_gap)
            br = pygame.Rect(bx, by, btn_w, btn_h)
            bg = (50, 60, 50) if can_afford else (40, 40, 40)
            pygame.draw.rect(screen, bg, br, border_radius=3)
            if can_afford:
                pygame.draw.rect(screen, config.DARK_GOLD, br,
                                 width=1, border_radius=3)

            nk = f"upg_{key}"
            ns = font_sm.render(L.t(nk), True, config.WHITE)
            screen.blit(ns, (bx + 6, by + 3))
            cs = font_sm.render(L.t("upg_buy", cost), True,
                                config.GOLD if can_afford
                                else config.GREY)
            screen.blit(cs, (bx + btn_w - cs.get_width() - 6, by + 3))

            raw = getattr(player, key)
            vs = font_sm.render(_val_str(key, raw), True, config.YELLOW)
            screen.blit(vs, (bx + 6, by + 26))

            buttons[f"buy_{key}"] = br

    return buttons


# ═════════════════════════════════════════════════════════════════════════
#  Game Over screen  (returns clickable rect)
# ═════════════════════════════════════════════════════════════════════════

def draw_game_over(screen, font, kills=0,
                   dp_earned=0) -> dict:
    """Render settlement screen.  Returns {'continue': rect}."""
    lines = [
        (L.t("go_title"), config.RED),
        (L.t("go_killed", kills), config.WHITE),
    ]
    if dp_earned > 0:
        lines.append((L.t("go_dp", dp_earned), config.GOLD))

    y = 200
    for text, colour in lines:
        r = font.render(text, True, colour)
        screen.blit(r,
                    (config.SCREEN_WIDTH // 2 - r.get_width() // 2, y))
        y += 55

    y += 10
    btn = pygame.Rect(0, 0, 260, 40)
    btn.center = (config.SCREEN_WIDTH // 2, y)
    pygame.draw.rect(screen, (60, 60, 60), btn, border_radius=6)
    pygame.draw.rect(screen, config.WHITE, btn, width=2, border_radius=6)
    go = font.render(L.t("go_continue"), True, config.WHITE)
    screen.blit(go, go.get_rect(center=btn.center))

    return {"continue": btn}
