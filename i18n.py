"""Multi-language support — English and Chinese.

Usage:
    from i18n import L
    L.t("key")          -> localized string
    L.perk_name("xp")   -> localized perk name
    L.perk_desc("xp")   -> localized perk description
    L.fmt(v)            -> number with at most 2 decimal places
"""


# ── String table ───────────────────────────────────────────────────────

_T = {
    # ── Menu ────────────────────────────────────────────────────────────
    "menu_title":          ("Survivor's Legacy", "幸存者生存"),
    "start_game":          ("Start Game", "开始游戏"),
    "dp_perm":             ("Divine Power (perm)", "神力 (永久)"),
    "equipment":           ("Equipment", "装备"),
    "controls_hint":       ("ENTER / click  to select", "回车 / 点击 选择"),
    "clear_data":          ("Clear Data", "清除数据"),
    "exit_game":           ("Exit Game", "退出游戏"),
    "lang_label":          ("Language: {} / 中文", "语言: EN / {}"),
    # ── Divine Power screen ─────────────────────────────────────────────
    "dp_title":            ("Divine Power", "神力系统"),
    "dp_available":        ("Available: {}", "可用神力: {}"),
    "max":                 ("MAX", "已达上限"),
    "cost":                ("Cost {}", "消耗 {}"),
    "buy_btn":             ("Buy [ENTER]", "购买 [回车]"),
    "back_btn":            ("Back [ESC]", "返回 [ESC]"),
    "dp_maxed":            ("Already maxed!", "已达上限！"),
    "dp_nofunds":          ("Not enough Divine Power!", "神力不足！"),
    "dp_bought":           ("{} Lv.{}", "{} 等级 {}"),
    # ── Equipment screen ────────────────────────────────────────────────
    "equip_title":         ("Equipment", "装备"),
    "equip_empty":         ("(empty)", "(空)"),
    "equip_invalid":       ("(invalid)", "(无效)"),
    "equip_back":          ("[ESC]  Back", "[ESC] 返回"),
    # ── HUD ──────────────────────────────────────────────────────────────
    "hud_hp":              ("HP {}/{}", "生命 {}/{}"),
    "hud_gold":            ("Gold: {}", "金币: {}"),
    "hud_dp":              ("Divine Power: {}", "神力: {}"),
    "hud_wave":            ("Wave {}", "波数 {}"),
    "hud_kills":           ("Kills {}", "击杀 {}"),
    "hud_atk":             ("ATK  {}", "攻击 {}"),
    "hud_cd":              ("CD   {}s", "冷却 {}秒"),
    "hud_crit":            ("Crit {}%", "暴击 {}%"),
    "hud_cdmg":            ("CDmg {}%", "暴伤 {}%"),
    "hud_pierce":          ("Pierce {}", "穿透 {}"),
    "hud_range":           ("Range {}", "范围 {}"),
    "hud_def":             ("DEF   {}", "防御 {}"),
    "hud_ls":              ("LS    {}%", "吸血 {}%"),
    "hud_regen":           ("Regen {}", "恢复 {}"),
    "hud_bcount":          ("Bullets {}", "子弹 {}"),
    "hud_speed":           ("Speed {}x", "倍速 {}x"),
    "hud_exit":            ("[M] Results", "[M] 结算"),
    "hud_speed_btn":       ("[TAB] {}", "[TAB] {}"),
    "hud_upgrade":         ("[U] Upgrade", "[U] 升级"),
    # ── Game Over ────────────────────────────────────────────────────────
    "go_title":            ("SETTLEMENT", "结算"),
    "go_killed":           ("Kills: {}", "击杀: {}"),
    "go_dp":               ("Divine Power: +{}", "神力: +{}"),
    "go_continue":         ("Continue [ENTER]", "继续 [回车]"),
    # ── Equipment notification ──────────────────────────────────────────
    "equip_drop":          ("!! {} {} !!", "!! {} {} !!"),
    # ── Upgrade screen ───────────────────────────────────────────────────
    "upg_title":           ("Upgrade", "升级"),
    "upg_lv":              ("Lv.{}", "等级 {}"),
    "upg_buy":             ("Buy {}g", "购买 {}金币"),
    "upg_maxed":           ("MAX", "已达上限"),
    "upg_nofunds":         ("Not enough gold!", "金币不足！"),
    "upg_bought":          ("{} Lv.{}", "{} 等级 {}"),
    "upg_close":           ("[ESC]  Close", "[ESC] 关闭"),
    # ── Upgrade tab labels ───────────────────────────────────────────────
    "upg_tab_attack":      ("Attack", "攻击"),
    "upg_tab_defense":     ("Defense", "防御"),
    "upg_tab_economy":     ("Economy", "经济"),
    # ── Upgrade stat labels ──────────────────────────────────────────────
    "upg_attack_damage":   ("Attack", "攻击力"),
    "upg_max_hp":          ("HP", "生命值"),
    "upg_defense":         ("Defense", "防御力"),
    "upg_lifesteal":       ("Lifesteal", "吸血"),
    "upg_hp_regen":        ("Regen", "生命恢复"),
    "upg_crit_rate":       ("Crit Rate", "暴击率"),
    "upg_crit_damage":     ("Crit Dmg", "暴击伤害"),
    "upg_attack_cooldown": ("Speed", "攻击速度"),
    "upg_piercing":        ("Pierce", "穿透"),
    "upg_gold_modifier":   ("Gold", "金币加成"),
    "upg_dp_bonus":        ("DP Boost", "神力加成"),
    # ── Slot names ──────────────────────────────────────────────────────
    "slot_weapon":         ("Weapon", "武器"),
    "slot_armor":          ("Armor", "护甲"),
    "slot_accessory":      ("Accessory", "饰品"),
}

# ── Rarity names ───────────────────────────────────────────────────────

_RARITY_NAMES = {
    "white":  ("White",  "普通"),
    "blue":   ("Blue",   "精良"),
    "purple": ("Purple", "史诗"),
    "orange": ("Orange", "传说"),
    "red":    ("Red",    "神话"),
}

# ── Affix names (equipment stat labels) ────────────────────────────────

_AFFIX_NAMES = {
    "Atk":     ("ATK",      "攻击"),
    "HP":      ("HP",       "生命"),
    "Def":     ("DEF",      "防御"),
    "LS":      ("LS",       "吸血"),
    "Regen":   ("Regen",    "恢复"),
    "CritRt":  ("Crit Rt",  "暴击率"),
    "CritDmg": ("Crit Dmg", "暴伤"),
    "Gold":    ("Gold",     "金币"),
    "Range":   ("Range",    "范围"),
}

# ── Perk names & descriptions ──────────────────────────────────────────

_PERK_NAMES = {
    "gold_modifier":   ("Gold Boost", "金币加成"),
    "attack_damage":   ("Attack", "攻击力"),
    "max_hp":          ("HP", "生命值"),
    "defense":         ("Defense", "防御力"),
    "lifesteal":       ("Lifesteal", "吸血"),
    "hp_regen":        ("Regen", "生命恢复"),
    "bullet_count":    ("Bullets", "子弹数量"),
    "crit_rate":       ("Crit Rate", "暴击率"),
    "crit_damage":     ("Crit Dmg", "暴击伤害"),
    "attack_cooldown": ("Speed", "攻击速度"),
    "piercing":        ("Pierce", "穿透"),
    "game_speed":      ("Game Speed", "游戏速度"),
    "dp_bonus":        ("DP Boost", "神力加成"),
}

_PERK_DESCS = {
    "gold_modifier":   ("+5% gold", "+5% 金币"),
    "attack_damage":   ("+2% damage", "+2% 伤害"),
    "max_hp":          ("+2% max HP", "+2% 最大生命"),
    "defense":         ("+2% defense", "+2% 防御"),
    "lifesteal":       ("+0.2% lifesteal", "+0.2% 吸血"),
    "hp_regen":        ("+0.1 HP/sec", "+0.1 生命/秒"),
    "bullet_count":    ("+1 bullet", "+1 子弹"),
    "crit_rate":       ("+0.5% crit rate", "+0.5% 暴击率"),
    "crit_damage":     ("+3% crit dmg", "+3% 暴击伤害"),
    "attack_cooldown": ("-1% cooldown", "-1% 冷却"),
    "piercing":        ("+1 pierce", "+1 穿透"),
    "game_speed":      ("+1 max speed tier", "+1 最高倍速"),
    "dp_bonus":        ("+5% DP earned", "+5% 神力获取"),
}


# ── Public lookup helpers ──────────────────────────────────────────────

class L:
    """Static localisation helper."""

    LANG = "en"

    @staticmethod
    def create_font(size):
        """Create a pygame Font that supports both EN and ZH.

        Always tries Microsoft YaHei first (handles both languages),
        falls back to the default pygame font.
        """
        import os
        import pygame
        windir = os.environ.get("WINDIR", "C:\\Windows")
        candidates = [
            os.path.join(windir, "Fonts", "msyh.ttc"),
            os.path.join(windir, "Fonts", "msyh.ttf"),
            os.path.join(windir, "Fonts",
                         "Microsoft YaHei.ttf"),
        ]
        for path in candidates:
            if os.path.isfile(path):
                try:
                    return pygame.font.Font(path, size)
                except pygame.error:
                    continue
        return pygame.font.Font(None, size)

    @staticmethod
    def fmt(value, max_decimals=2):
        """Format a number with at most *max_decimals* decimal places."""
        return f"{value:.{max_decimals}f}".rstrip("0").rstrip(".")

    @staticmethod
    def t(key, *args):
        """Return localized string for *key*, formatted with *args."""
        pair = _T.get(key)
        if pair is None:
            return key
        text = pair[0] if L.LANG == "en" else pair[1]
        if args:
            return text.format(*args)
        return text

    @staticmethod
    def perk_name(key):
        """Return localized perk name for *key*."""
        pair = _PERK_NAMES.get(key)
        return pair[0] if L.LANG == "en" else (pair[1] if pair else key)

    @staticmethod
    def perk_desc(key):
        """Return localized perk description for *key*."""
        pair = _PERK_DESCS.get(key)
        return pair[0] if L.LANG == "en" else (pair[1] if pair else key)

    @staticmethod
    def slot_name(key):
        """Return localized equipment-slot name for *key*."""
        pair = _T.get(f"slot_{key}")
        return pair[0] if L.LANG == "en" else (pair[1] if pair else key)

    @staticmethod
    def rarity_name(key):
        """Return localized rarity name for *key* (white/blue/...)."""
        pair = _RARITY_NAMES.get(key)
        return pair[0] if L.LANG == "en" else (pair[1] if pair else key)

    @staticmethod
    def affix_name(key):
        """Return localized affix display name (Atk/HP/...)."""
        pair = _AFFIX_NAMES.get(key)
        return pair[0] if L.LANG == "en" else (pair[1] if pair else key)
