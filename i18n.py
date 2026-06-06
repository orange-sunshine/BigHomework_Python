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
    "hud_xp":              ("Lv.{}  XP {}/{}", "等级 {}  经验 {}/{}"),
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
    "hud_level_up":        ("LEVEL UP!", "升级！"),
    "hud_speed":           ("Speed {}x", "倍速 {}x"),
    "hud_exit":            ("[M] Results", "[M] 结算"),
    "hud_speed_btn":       ("[TAB] {}", "[TAB] {}"),
    # ── Game Over ────────────────────────────────────────────────────────
    "go_title":            ("GAME OVER", "游戏结束"),
    "go_score":            ("Score: {}", "得分: {}"),
    "go_wave":             ("Wave reached: {}", "到达波数: {}"),
    "go_killed":           ("Enemies killed: {}", "击杀敌人: {}"),
    "go_dp":               ("Divine Power earned: +{}", "获得神力: +{}"),
    "go_continue":         ("Continue [ENTER]", "继续 [回车]"),
    # ── Equipment notification ──────────────────────────────────────────
    "equip_drop":          ("!! {} {} !!", "!! {} {} !!"),
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
    "XP":      ("XP",       "经验"),
    "Range":   ("Range",    "范围"),
}

# ── Perk names & descriptions ──────────────────────────────────────────

_PERK_NAMES = {
    "xp_modifier":     ("XP Boost", "经验加成"),
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
    "dp_bonus":        ("DP Boost", "神力获取加成"),
}

_PERK_DESCS = {
    "xp_modifier":     ("+10% XP", "+10% 经验"),
    "attack_damage":   ("+8% damage", "+8% 伤害"),
    "max_hp":          ("+5% max HP", "+5% 最大生命"),
    "defense":         ("+8% defense", "+8% 防御"),
    "lifesteal":       ("+1% lifesteal", "+1% 吸血"),
    "hp_regen":        ("+0.5 HP/sec", "+0.5 生命/秒"),
    "bullet_count":    ("+1 bullet", "+1 子弹"),
    "crit_rate":       ("+2% crit rate", "+2% 暴击率"),
    "crit_damage":     ("+10% crit dmg", "+10% 暴击伤害"),
    "attack_cooldown": ("-3% cooldown", "-3% 冷却"),
    "piercing":        ("+1 pierce, less dmg loss", "+1 穿透, 减少伤害衰减"),
    "game_speed":      ("+0.5x max speed", "+0.5 最高倍速"),
    "dp_bonus":        ("+15% DP earned", "+15% 神力获取"),
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
