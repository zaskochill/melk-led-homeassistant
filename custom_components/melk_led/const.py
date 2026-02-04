"""Constants for MELK LED Strip - ALL 241 effects (213 effects + 28 scenes)."""
from enum import Enum

# =========================================================
# Основные константы
# =========================================================
DOMAIN = "melk_led"

CONF_RESET = "reset"
CONF_DELAY = "delay"

# =========================================================
# ВСЕ 213 ЭФФЕКТОВ
# =========================================================
class EFFECTS(Enum):
    """Все 213 эффектов RGB LED ленты."""
    
    # --- STATIC ---
    none = 0x00  # Static Color
    
    # --- BASIC GROUP (47 эффектов) ---
    # Special
    auto_play = 0  # 🎲 Auto Play
    magic_forward = 1  # ✨ Magic Forward
    magic_back = 2  # ✨ Magic Back
    
    # Jump
    jump_7_color = 193  # 🌈 7-Color Jump
    jump_rgb = 194  # ⚡ R-G-B Jump
    jump_ycp = 195  # 🎨 Y-C-P Jump
    
    # Strobe
    strobe_7_color = 196  # 🎇 7-Color Strobe
    strobe_rgb = 197  # ⚡ R-G-B Strobe
    strobe_ycp = 198  # 🎆 Y-C-P Strobe
    
    # Gradual
    gradual_7_color = 199  # 🌈 7-Color Gradual
    gradual_red_yellow = 200  # 🔴🟡 R-Y Gradual
    gradual_red_purple = 201  # 🔴💜 R-P Gradual
    gradual_green_cyan = 202  # 🟢💠 G-C Gradual
    gradual_green_yellow = 203  # 🟢🟡 G-Y Gradual
    gradual_blue_purple = 204  # 🔵💜 B-P Gradual
    
    # Marquee
    marquee_red = 205  # 🔴 Red Marquee
    marquee_green = 206  # 🟢 Green Marquee
    marquee_blue = 207  # 🔵 Blue Marquee
    marquee_yellow = 208  # 🟡 Yellow Marquee
    marquee_cyan = 209  # 💠 Cyan Marquee
    marquee_purple = 210  # 💜 Purple Marquee
    marquee_white = 211  # 🤍 White Marquee
    
    # Race
    race_7_color = 77  # 🏁 7-Color Race
    race_7_color_back = 78  # 🏁 7-Color Race Back
    race_rgb = 79  # 🏁 R-G-B Race
    race_rgb_back = 80  # 🏁 R-G-B Race Back
    race_ycp = 81  # 🏁 Y-C-P Race
    race_ycp_back = 82  # 🏁 Y-C-P Race Back
    
    # Wave
    wave_7_color = 83  # 🌊 7-Color Wave
    wave_7_color_back = 84  # 🌊 7-Color Wave Back
    wave_rgb = 85  # 🌊 R-G-B Wave
    wave_rgb_back = 86  # 🌊 R-G-B Wave Back
    wave_ycp = 87  # 🌊 Y-C-P Wave
    wave_ycp_back = 88  # 🌊 Y-C-P Wave Back
    
    # Flush
    flush_7_color = 181  # 💨 7-Color Flush
    flush_7_color_back = 182  # 💨 7-Color Flush Back
    flush_rgb = 183  # 💨 R-G-B Flush
    flush_rgb_back = 184  # 💨 R-G-B Flush Back
    flush_ycp = 185  # 💨 Y-C-P Flush
    flush_ycp_back = 186  # 💨 Y-C-P Flush Back
    flush_7_color_close = 187  # 💨 7-Color Flush Close
    flush_7_color_open = 188  # 💨 7-Color Flush Open
    flush_rgb_close = 189  # 💨 R-G-B Flush Close
    flush_rgb_open = 190  # 💨 R-G-B Flush Open
    flush_ycp_close = 191  # 💨 Y-C-P Flush Close
    flush_ycp_open = 192  # 💨 Y-C-P Flush Open
    
    # Energy
    energy_7_color = 212  # ⚡ 7-Color Energy
    
    # --- CURTAIN GROUP (20 эффектов) ---
    curtain_7_color_close = 57  # 🎭 7-Color Close
    curtain_7_color_open = 58  # 🎭 7-Color Open
    curtain_rgb_close = 59  # 🎭 R-G-B Close
    curtain_rgb_open = 60  # 🎭 R-G-B Open
    curtain_ycp_close = 61  # 🎭 Y-C-P Close
    curtain_ycp_open = 62  # 🎭 Y-C-P Open
    curtain_red_close = 63  # 🔴 Red Close
    curtain_red_open = 64  # 🔴 Red Open
    curtain_green_close = 65  # 🟢 Green Close
    curtain_green_open = 66  # 🟢 Green Open
    curtain_blue_close = 67  # 🔵 Blue Close
    curtain_blue_open = 68  # 🔵 Blue Open
    curtain_yellow_close = 69  # 🟡 Yellow Close
    curtain_yellow_open = 70  # 🟡 Yellow Open
    curtain_cyan_close = 71  # 💠 Cyan Close
    curtain_cyan_open = 72  # 💠 Cyan Open
    curtain_purple_close = 73  # 💜 Purple Close
    curtain_purple_open = 74  # 💜 Purple Open
    curtain_white_close = 75  # 🤍 White Close
    curtain_white_open = 76  # 🤍 White Open
    
    # --- TRANS GROUP (20 эффектов) ---
    trans_7_color = 3  # 🔄 7-Color Trans
    trans_7_color_back = 4  # 🔄 7-Color Trans Back
    trans_rgb = 5  # 🔄 R-G-B Trans
    trans_rgb_back = 6  # 🔄 R-G-B Trans Back
    trans_ycp = 7  # 🔄 Y-C-P Trans
    trans_ycp_back = 8  # 🔄 Y-C-P Trans Back
    trans_6_to_red = 9  # 🔴 6-Color to Red
    trans_6_to_red_back = 10  # 🔴 6-Color to Red Back
    trans_6_to_green = 11  # 🟢 6-Color to Green
    trans_6_to_green_back = 12  # 🟢 6-Color to Green Back
    trans_6_to_blue = 13  # 🔵 6-Color to Blue
    trans_6_to_blue_back = 14  # 🔵 6-Color to Blue Back
    trans_6_to_cyan = 15  # 💠 6-Color to Cyan
    trans_6_to_cyan_back = 16  # 💠 6-Color to Cyan Back
    trans_6_to_yellow = 17  # 🟡 6-Color to Yellow
    trans_6_to_yellow_back = 18  # 🟡 6-Color to Yellow Back
    trans_6_to_purple = 19  # 💜 6-Color to Purple
    trans_6_to_purple_back = 20  # 💜 6-Color to Purple Back
    trans_6_to_white = 21  # 🤍 6-Color to White
    trans_6_to_white_back = 22  # 🤍 6-Color to White Back
    
    # --- WATER GROUP (18 эффектов) ---
    water_7_color = 39  # 🌊 7-Color Water
    water_7_color_back = 40  # 🌊 7-Color Water Back
    water_rgb = 41  # 🌊 R-G-B Water
    water_rgb_back = 42  # 🌊 R-G-B Water Back
    water_ycp = 43  # 🌊 Y-C-P Water
    water_ycp_back = 44  # 🌊 Y-C-P Water Back
    water_rg = 45  # 🌊 R-G Water
    water_rg_back = 46  # 🌊 R-G Water Back
    water_gb = 47  # 🌊 G-B Water
    water_gb_back = 48  # 🌊 G-B Water Back
    water_yb = 49  # 🌊 Y-B Water
    water_yb_back = 50  # 🌊 Y-B Water Back
    water_yc = 51  # 🌊 Y-C Water
    water_yc_back = 52  # 🌊 Y-C Water Back
    water_cp = 53  # 🌊 C-P Water
    water_cp_back = 54  # 🌊 C-P Water Back
    water_white = 55  # 🌊 White Water
    water_white_back = 56  # 🌊 White Water Back
    
    # --- FLOW GROUP (24 эффекта) ---
    flow_wr_w = 143  # 💫 W-R-W Flow
    flow_wr_w_back = 144  # 💫 W-R-W Flow Back
    flow_wg_w = 145  # 💫 W-G-W Flow
    flow_wg_w_back = 146  # 💫 W-G-W Flow Back
    flow_wb_w = 147  # 💫 W-B-W Flow
    flow_wb_w_back = 148  # 💫 W-B-W Flow Back
    flow_wy_w = 149  # 💫 W-Y-W Flow
    flow_wy_w_back = 150  # 💫 W-Y-W Flow Back
    flow_wc_w = 151  # 💫 W-C-W Flow
    flow_wc_w_back = 152  # 💫 W-C-W Flow Back
    flow_wp_w = 153  # 💫 W-P-W Flow
    flow_wp_w_back = 154  # 💫 W-P-W Flow Back
    flow_rw_r = 155  # 💫 R-W-R Flow
    flow_rw_r_back = 156  # 💫 R-W-R Flow Back
    flow_gw_g = 157  # 💫 G-W-G Flow
    flow_gw_g_back = 158  # 💫 G-W-G Flow Back
    flow_bw_b = 159  # 💫 B-W-B Flow
    flow_bw_b_back = 160  # 💫 B-W-B Flow Back
    flow_yw_y = 161  # 💫 Y-W-Y Flow
    flow_yw_y_back = 162  # 💫 Y-W-Y Flow Back
    flow_cw_c = 163  # 💫 C-W-C Flow
    flow_cw_c_back = 164  # 💫 C-W-C Flow Back
    flow_pw_p = 165  # 💫 P-W-P Flow
    flow_pw_p_back = 166  # 💫 P-W-P Flow Back
    
    # --- TAIL GROUP (16 эффектов) ---
    tail_7_color = 23  # 🌟 7-Color Tail
    tail_7_color_back = 24  # 🌟 7-Color Tail Back
    tail_red = 25  # 🔴 Red Tail
    tail_red_back = 26  # 🔴 Red Tail Back
    tail_green = 27  # 🟢 Green Tail
    tail_green_back = 28  # 🟢 Green Tail Back
    tail_blue = 29  # 🔵 Blue Tail
    tail_blue_back = 30  # 🔵 Blue Tail Back
    tail_yellow = 31  # 🟡 Yellow Tail
    tail_yellow_back = 32  # 🟡 Yellow Tail Back
    tail_cyan = 33  # 💠 Cyan Tail
    tail_cyan_back = 34  # 💠 Cyan Tail Back
    tail_purple = 35  # 💜 Purple Tail
    tail_purple_back = 36  # 💜 Purple Tail Back
    tail_white = 37  # 🤍 White Tail
    tail_white_back = 38  # 🤍 White Tail Back
    
    # --- RUNNING GROUP (34 эффекта - нечетные ID) ---
    running_red = 89  # 🏃 Red Running
    running_red_2 = 109  # 🏃 Red Running 2
    running_red_3 = 111  # 🏃 Red Running 3
    running_red_4 = 113  # 🏃 Red Running 4
    running_red_5 = 115  # 🏃 Red Running 5
    running_green = 91  # 🏃 Green Running
    running_green_2 = 117  # 🏃 Green Running 2
    running_green_3 = 119  # 🏃 Green Running 3
    running_green_4 = 121  # 🏃 Green Running 4
    running_green_5 = 123  # 🏃 Green Running 5
    running_blue = 93  # 🏃 Blue Running
    running_blue_2 = 125  # 🏃 Blue Running 2
    running_blue_3 = 127  # 🏃 Blue Running 3
    running_blue_4 = 129  # 🏃 Blue Running 4
    running_blue_5 = 131  # 🏃 Blue Running 5
    running_yellow = 95  # 🏃 Yellow Running
    running_yellow_2 = 133  # 🏃 Yellow Running 2
    running_yellow_3 = 135  # 🏃 Yellow Running 3
    running_yellow_4 = 137  # 🏃 Yellow Running 4
    running_yellow_5 = 139  # 🏃 Yellow Running 5
    running_cyan = 97  # 🏃 Cyan Running
    running_cyan_2 = 141  # 🏃 Cyan Running 2
    running_cyan_3 = 167  # 🏃 Cyan Running 3
    running_cyan_4 = 169  # 🏃 Cyan Running 4
    running_cyan_5 = 171  # 🏃 Cyan Running 5
    running_purple = 99  # 🏃 Purple Running
    running_purple_2 = 173  # 🏃 Purple Running 2
    running_purple_3 = 175  # 🏃 Purple Running 3
    running_purple_4 = 177  # 🏃 Purple Running 4
    running_purple_5 = 179  # 🏃 Purple Running 5
    running_white = 101  # 🏃 White Running
    running_7_color = 103  # 🏃 7-Color Running
    running_rgb = 105  # 🏃 R-G-B Running
    running_ycp = 107  # 🏃 Y-C-P Running
    
    # --- RUN BACK GROUP (34 эффекта - четные ID) ---
    run_back_red = 90  # 🔙 Red Run Back
    run_back_red_2 = 110  # 🔙 Red Run Back 2
    run_back_red_3 = 112  # 🔙 Red Run Back 3
    run_back_red_4 = 114  # 🔙 Red Run Back 4
    run_back_red_5 = 116  # 🔙 Red Run Back 5
    run_back_green = 92  # 🔙 Green Run Back
    run_back_green_2 = 118  # 🔙 Green Run Back 2
    run_back_green_3 = 120  # 🔙 Green Run Back 3
    run_back_green_4 = 122  # 🔙 Green Run Back 4
    run_back_green_5 = 124  # 🔙 Green Run Back 5
    run_back_blue = 94  # 🔙 Blue Run Back
    run_back_blue_2 = 126  # 🔙 Blue Run Back 2
    run_back_blue_3 = 128  # 🔙 Blue Run Back 3
    run_back_blue_4 = 130  # 🔙 Blue Run Back 4
    run_back_blue_5 = 132  # 🔙 Blue Run Back 5
    run_back_yellow = 96  # 🔙 Yellow Run Back
    run_back_yellow_2 = 134  # 🔙 Yellow Run Back 2
    run_back_yellow_3 = 136  # 🔙 Yellow Run Back 3
    run_back_yellow_4 = 138  # 🔙 Yellow Run Back 4
    run_back_yellow_5 = 140  # 🔙 Yellow Run Back 5
    run_back_cyan = 98  # 🔙 Cyan Run Back
    run_back_cyan_2 = 142  # 🔙 Cyan Run Back 2
    run_back_cyan_3 = 168  # 🔙 Cyan Run Back 3
    run_back_cyan_4 = 170  # 🔙 Cyan Run Back 4
    run_back_cyan_5 = 172  # 🔙 Cyan Run Back 5
    run_back_purple = 100  # 🔙 Purple Run Back
    run_back_purple_2 = 174  # 🔙 Purple Run Back 2
    run_back_purple_3 = 176  # 🔙 Purple Run Back 3
    run_back_purple_4 = 178  # 🔙 Purple Run Back 4
    run_back_purple_5 = 180  # 🔙 Purple Run Back 5
    run_back_white = 102  # 🔙 White Run Back
    run_back_7_color = 104  # 🔙 7-Color Run Back
    run_back_rgb = 106  # 🔙 R-G-B Run Back
    run_back_ycp = 108  # 🔙 Y-C-P Run Back


# =========================================================
# 28 СЦЕН (используют другую команду!)
# =========================================================
class SCENES(Enum):
    """28 специальных сцен (команда 7E 05 31 [ID] 07 FF FF 01 EF)."""
    
    sunrise = 1  # 🌅 Sunrise
    sunset = 2  # 🌇 Sunset
    birthday = 3  # 🎂 Birthday
    candlelight = 4  # 🕯️ Candlelight
    fireworks = 5  # 🎆 Fireworks
    party = 6  # 🎉 Party
    datiny = 7  # ✨ Datiny
    starry_sky = 8  # ⭐ Starry Sky
    romantic = 9  # 💕 Romantic
    disco = 10  # 🪩 Disco
    rainbow = 11  # 🌈 Rainbow
    movie = 12  # 🎬 Movie
    christmas = 13  # 🎄 Christmas
    flowing = 14  # 🌊 Flowing
    sleeping = 15  # 😴 Sleeping
    ocean = 16  # 🌊 Ocean
    forest = 17  # 🌲 Forest
    reading = 18  # 📖 Reading
    working = 19  # 💼 Working
    dazzle = 20  # ✨ Dazzle
    gentle = 21  # 🌸 Gentle
    wedding = 22  # 💒 Wedding
    snow = 23  # ❄️ Snow
    fire = 24  # 🔥 Fire
    lightning = 25  # ⚡ Lightning
    valentines_day = 26  # 💝 Valentine's Day
    hallowmas = 27  # 🎃 Hallowmas
    warning = 28  # ⚠️ Warning


# Списки и мапы
EFFECTS_MAP = {e.name: e.value for e in EFFECTS}
SCENES_MAP = {s.name: s.value for s in SCENES}

# Объединенный список для UI (эффекты + сцены)
ALL_EFFECTS_MAP = {**EFFECTS_MAP, **{f"scene_{k}": v for k, v in SCENES_MAP.items()}}


# Красивые лейблы для UI
EFFECT_LABELS = {
    # Static
    "none": "💡 Static Color",
    
    # Basic - Special
    "auto_play": "🎲 Auto Play",
    "magic_forward": "✨ Magic Forward",
    "magic_back": "✨ Magic Back",
    
    # Basic - Jump
    "jump_7_color": "🌈 Jump: 7-Color",
    "jump_rgb": "⚡ Jump: RGB",
    "jump_ycp": "🎨 Jump: YCP",
    
    # Basic - Strobe
    "strobe_7_color": "🎇 Strobe: 7-Color",
    "strobe_rgb": "⚡ Strobe: RGB",
    "strobe_ycp": "🎆 Strobe: YCP",
    
    # Basic - Gradual
    "gradual_7_color": "🌈 Gradual: Rainbow",
    "gradual_red_yellow": "🔴🟡 Gradual: Red-Yellow",
    "gradual_red_purple": "🔴💜 Gradual: Red-Purple",
    "gradual_green_cyan": "🟢💠 Gradual: Green-Cyan",
    "gradual_green_yellow": "🟢🟡 Gradual: Green-Yellow",
    "gradual_blue_purple": "🔵💜 Gradual: Blue-Purple",
    
    # Basic - Marquee
    "marquee_red": "🔴 Marquee: Red",
    "marquee_green": "🟢 Marquee: Green",
    "marquee_blue": "🔵 Marquee: Blue",
    "marquee_yellow": "🟡 Marquee: Yellow",
    "marquee_cyan": "💠 Marquee: Cyan",
    "marquee_purple": "💜 Marquee: Purple",
    "marquee_white": "🤍 Marquee: White",
    
    # Basic - Race
    "race_7_color": "🏁 Race: 7-Color",
    "race_7_color_back": "🏁 Race: 7-Color Back",
    "race_rgb": "🏁 Race: RGB",
    "race_rgb_back": "🏁 Race: RGB Back",
    "race_ycp": "🏁 Race: YCP",
    "race_ycp_back": "🏁 Race: YCP Back",
    
    # Basic - Wave
    "wave_7_color": "🌊 Wave: 7-Color",
    "wave_7_color_back": "🌊 Wave: 7-Color Back",
    "wave_rgb": "🌊 Wave: RGB",
    "wave_rgb_back": "🌊 Wave: RGB Back",
    "wave_ycp": "🌊 Wave: YCP",
    "wave_ycp_back": "🌊 Wave: YCP Back",
    
    # Basic - Flush
    "flush_7_color": "💨 Flush: 7-Color",
    "flush_7_color_back": "💨 Flush: 7-Color Back",
    "flush_rgb": "💨 Flush: RGB",
    "flush_rgb_back": "💨 Flush: RGB Back",
    "flush_ycp": "💨 Flush: YCP",
    "flush_ycp_back": "💨 Flush: YCP Back",
    "flush_7_color_close": "💨 Flush: 7-Color Close",
    "flush_7_color_open": "💨 Flush: 7-Color Open",
    "flush_rgb_close": "💨 Flush: RGB Close",
    "flush_rgb_open": "💨 Flush: RGB Open",
    "flush_ycp_close": "💨 Flush: YCP Close",
    "flush_ycp_open": "💨 Flush: YCP Open",
    
    # Basic - Energy
    "energy_7_color": "⚡ Energy: 7-Color",
    
    # Curtain
    "curtain_7_color_close": "🎭 Curtain: 7-Color Close",
    "curtain_7_color_open": "🎭 Curtain: 7-Color Open",
    "curtain_rgb_close": "🎭 Curtain: RGB Close",
    "curtain_rgb_open": "🎭 Curtain: RGB Open",
    "curtain_ycp_close": "🎭 Curtain: YCP Close",
    "curtain_ycp_open": "🎭 Curtain: YCP Open",
    "curtain_red_close": "🔴 Curtain: Red Close",
    "curtain_red_open": "🔴 Curtain: Red Open",
    "curtain_green_close": "🟢 Curtain: Green Close",
    "curtain_green_open": "🟢 Curtain: Green Open",
    "curtain_blue_close": "🔵 Curtain: Blue Close",
    "curtain_blue_open": "🔵 Curtain: Blue Open",
    "curtain_yellow_close": "🟡 Curtain: Yellow Close",
    "curtain_yellow_open": "🟡 Curtain: Yellow Open",
    "curtain_cyan_close": "💠 Curtain: Cyan Close",
    "curtain_cyan_open": "💠 Curtain: Cyan Open",
    "curtain_purple_close": "💜 Curtain: Purple Close",
    "curtain_purple_open": "💜 Curtain: Purple Open",
    "curtain_white_close": "🤍 Curtain: White Close",
    "curtain_white_open": "🤍 Curtain: White Open",
    
    # Trans
    "trans_7_color": "🔄 Trans: 7-Color",
    "trans_7_color_back": "🔄 Trans: 7-Color Back",
    "trans_rgb": "🔄 Trans: RGB",
    "trans_rgb_back": "🔄 Trans: RGB Back",
    "trans_ycp": "🔄 Trans: YCP",
    "trans_ycp_back": "🔄 Trans: YCP Back",
    "trans_6_to_red": "🔴 Trans: 6→Red",
    "trans_6_to_red_back": "🔴 Trans: 6→Red Back",
    "trans_6_to_green": "🟢 Trans: 6→Green",
    "trans_6_to_green_back": "🟢 Trans: 6→Green Back",
    "trans_6_to_blue": "🔵 Trans: 6→Blue",
    "trans_6_to_blue_back": "🔵 Trans: 6→Blue Back",
    "trans_6_to_cyan": "💠 Trans: 6→Cyan",
    "trans_6_to_cyan_back": "💠 Trans: 6→Cyan Back",
    "trans_6_to_yellow": "🟡 Trans: 6→Yellow",
    "trans_6_to_yellow_back": "🟡 Trans: 6→Yellow Back",
    "trans_6_to_purple": "💜 Trans: 6→Purple",
    "trans_6_to_purple_back": "💜 Trans: 6→Purple Back",
    "trans_6_to_white": "🤍 Trans: 6→White",
    "trans_6_to_white_back": "🤍 Trans: 6→White Back",
    
    # Water
    "water_7_color": "🌊 Water: 7-Color",
    "water_7_color_back": "🌊 Water: 7-Color Back",
    "water_rgb": "🌊 Water: RGB",
    "water_rgb_back": "🌊 Water: RGB Back",
    "water_ycp": "🌊 Water: YCP",
    "water_ycp_back": "🌊 Water: YCP Back",
    "water_rg": "🌊 Water: RG",
    "water_rg_back": "🌊 Water: RG Back",
    "water_gb": "🌊 Water: GB",
    "water_gb_back": "🌊 Water: GB Back",
    "water_yb": "🌊 Water: YB",
    "water_yb_back": "🌊 Water: YB Back",
    "water_yc": "🌊 Water: YC",
    "water_yc_back": "🌊 Water: YC Back",
    "water_cp": "🌊 Water: CP",
    "water_cp_back": "🌊 Water: CP Back",
    "water_white": "🌊 Water: White",
    "water_white_back": "🌊 Water: White Back",
    
    # Flow
    "flow_wr_w": "💫 Flow: W-R-W",
    "flow_wr_w_back": "💫 Flow: W-R-W Back",
    "flow_wg_w": "💫 Flow: W-G-W",
    "flow_wg_w_back": "💫 Flow: W-G-W Back",
    "flow_wb_w": "💫 Flow: W-B-W",
    "flow_wb_w_back": "💫 Flow: W-B-W Back",
    "flow_wy_w": "💫 Flow: W-Y-W",
    "flow_wy_w_back": "💫 Flow: W-Y-W Back",
    "flow_wc_w": "💫 Flow: W-C-W",
    "flow_wc_w_back": "💫 Flow: W-C-W Back",
    "flow_wp_w": "💫 Flow: W-P-W",
    "flow_wp_w_back": "💫 Flow: W-P-W Back",
    "flow_rw_r": "💫 Flow: R-W-R",
    "flow_rw_r_back": "💫 Flow: R-W-R Back",
    "flow_gw_g": "💫 Flow: G-W-G",
    "flow_gw_g_back": "💫 Flow: G-W-G Back",
    "flow_bw_b": "💫 Flow: B-W-B",
    "flow_bw_b_back": "💫 Flow: B-W-B Back",
    "flow_yw_y": "💫 Flow: Y-W-Y",
    "flow_yw_y_back": "💫 Flow: Y-W-Y Back",
    "flow_cw_c": "💫 Flow: C-W-C",
    "flow_cw_c_back": "💫 Flow: C-W-C Back",
    "flow_pw_p": "💫 Flow: P-W-P",
    "flow_pw_p_back": "💫 Flow: P-W-P Back",
    
    # Tail
    "tail_7_color": "🌟 Tail: 7-Color",
    "tail_7_color_back": "🌟 Tail: 7-Color Back",
    "tail_red": "🔴 Tail: Red",
    "tail_red_back": "🔴 Tail: Red Back",
    "tail_green": "🟢 Tail: Green",
    "tail_green_back": "🟢 Tail: Green Back",
    "tail_blue": "🔵 Tail: Blue",
    "tail_blue_back": "🔵 Tail: Blue Back",
    "tail_yellow": "🟡 Tail: Yellow",
    "tail_yellow_back": "🟡 Tail: Yellow Back",
    "tail_cyan": "💠 Tail: Cyan",
    "tail_cyan_back": "💠 Tail: Cyan Back",
    "tail_purple": "💜 Tail: Purple",
    "tail_purple_back": "💜 Tail: Purple Back",
    "tail_white": "🤍 Tail: White",
    "tail_white_back": "🤍 Tail: White Back",
    
    # Running
    "running_red": "🏃 Running: Red",
    "running_red_2": "🏃 Running: Red 2",
    "running_red_3": "🏃 Running: Red 3",
    "running_red_4": "🏃 Running: Red 4",
    "running_red_5": "🏃 Running: Red 5",
    "running_green": "🏃 Running: Green",
    "running_green_2": "🏃 Running: Green 2",
    "running_green_3": "🏃 Running: Green 3",
    "running_green_4": "🏃 Running: Green 4",
    "running_green_5": "🏃 Running: Green 5",
    "running_blue": "🏃 Running: Blue",
    "running_blue_2": "🏃 Running: Blue 2",
    "running_blue_3": "🏃 Running: Blue 3",
    "running_blue_4": "🏃 Running: Blue 4",
    "running_blue_5": "🏃 Running: Blue 5",
    "running_yellow": "🏃 Running: Yellow",
    "running_yellow_2": "🏃 Running: Yellow 2",
    "running_yellow_3": "🏃 Running: Yellow 3",
    "running_yellow_4": "🏃 Running: Yellow 4",
    "running_yellow_5": "🏃 Running: Yellow 5",
    "running_cyan": "🏃 Running: Cyan",
    "running_cyan_2": "🏃 Running: Cyan 2",
    "running_cyan_3": "🏃 Running: Cyan 3",
    "running_cyan_4": "🏃 Running: Cyan 4",
    "running_cyan_5": "🏃 Running: Cyan 5",
    "running_purple": "🏃 Running: Purple",
    "running_purple_2": "🏃 Running: Purple 2",
    "running_purple_3": "🏃 Running: Purple 3",
    "running_purple_4": "🏃 Running: Purple 4",
    "running_purple_5": "🏃 Running: Purple 5",
    "running_white": "🏃 Running: White",
    "running_7_color": "🏃 Running: 7-Color",
    "running_rgb": "🏃 Running: RGB",
    "running_ycp": "🏃 Running: YCP",
    
    # Run Back
    "run_back_red": "🔙 Run Back: Red",
    "run_back_red_2": "🔙 Run Back: Red 2",
    "run_back_red_3": "🔙 Run Back: Red 3",
    "run_back_red_4": "🔙 Run Back: Red 4",
    "run_back_red_5": "🔙 Run Back: Red 5",
    "run_back_green": "🔙 Run Back: Green",
    "run_back_green_2": "🔙 Run Back: Green 2",
    "run_back_green_3": "🔙 Run Back: Green 3",
    "run_back_green_4": "🔙 Run Back: Green 4",
    "run_back_green_5": "🔙 Run Back: Green 5",
    "run_back_blue": "🔙 Run Back: Blue",
    "run_back_blue_2": "🔙 Run Back: Blue 2",
    "run_back_blue_3": "🔙 Run Back: Blue 3",
    "run_back_blue_4": "🔙 Run Back: Blue 4",
    "run_back_blue_5": "🔙 Run Back: Blue 5",
    "run_back_yellow": "🔙 Run Back: Yellow",
    "run_back_yellow_2": "🔙 Run Back: Yellow 2",
    "run_back_yellow_3": "🔙 Run Back: Yellow 3",
    "run_back_yellow_4": "🔙 Run Back: Yellow 4",
    "run_back_yellow_5": "🔙 Run Back: Yellow 5",
    "run_back_cyan": "🔙 Run Back: Cyan",
    "run_back_cyan_2": "🔙 Run Back: Cyan 2",
    "run_back_cyan_3": "🔙 Run Back: Cyan 3",
    "run_back_cyan_4": "🔙 Run Back: Cyan 4",
    "run_back_cyan_5": "🔙 Run Back: Cyan 5",
    "run_back_purple": "🔙 Run Back: Purple",
    "run_back_purple_2": "🔙 Run Back: Purple 2",
    "run_back_purple_3": "🔙 Run Back: Purple 3",
    "run_back_purple_4": "🔙 Run Back: Purple 4",
    "run_back_purple_5": "🔙 Run Back: Purple 5",
    "run_back_white": "🔙 Run Back: White",
    "run_back_7_color": "🔙 Run Back: 7-Color",
    "run_back_rgb": "🔙 Run Back: RGB",
    "run_back_ycp": "🔙 Run Back: YCP",
}

# Лейблы для сцен
SCENE_LABELS = {
    "scene_sunrise": "🌅 Scene: Sunrise",
    "scene_sunset": "🌇 Scene: Sunset",
    "scene_birthday": "🎂 Scene: Birthday",
    "scene_candlelight": "🕯️ Scene: Candlelight",
    "scene_fireworks": "🎆 Scene: Fireworks",
    "scene_party": "🎉 Scene: Party",
    "scene_datiny": "✨ Scene: Datiny",
    "scene_starry_sky": "⭐ Scene: Starry Sky",
    "scene_romantic": "💕 Scene: Romantic",
    "scene_disco": "🪩 Scene: Disco",
    "scene_rainbow": "🌈 Scene: Rainbow",
    "scene_movie": "🎬 Scene: Movie",
    "scene_christmas": "🎄 Scene: Christmas",
    "scene_flowing": "🌊 Scene: Flowing",
    "scene_sleeping": "😴 Scene: Sleeping",
    "scene_ocean": "🌊 Scene: Ocean",
    "scene_forest": "🌲 Scene: Forest",
    "scene_reading": "📖 Scene: Reading",
    "scene_working": "💼 Scene: Working",
    "scene_dazzle": "✨ Scene: Dazzle",
    "scene_gentle": "🌸 Scene: Gentle",
    "scene_wedding": "💒 Scene: Wedding",
    "scene_snow": "❄️ Scene: Snow",
    "scene_fire": "🔥 Scene: Fire",
    "scene_lightning": "⚡ Scene: Lightning",
    "scene_valentines_day": "💝 Scene: Valentine's Day",
    "scene_hallowmas": "🎃 Scene: Hallowmas",
    "scene_warning": "⚠️ Scene: Warning",
}

# Объединенные лейблы
ALL_EFFECT_LABELS = {**EFFECT_LABELS, **SCENE_LABELS}


# =========================================================
# Режимы микрофона
# =========================================================
class MIC_MODES(Enum):
    """Режимы эквалайзера для микрофона."""
    energic = 0x80  # 128
    rhythm = 0x81  # 129
    spectrum = 0x82  # 130
    rolling = 0x83  # 131
    rhythm_spectrum = 0x84  # 132
    rhythm_rolling = 0x85  # 133
    spectrum_rolling = 0x86  # 134
    energic_rolling = 0x87  # 135


MIC_MODE_LABELS = {
    "energic": "⚡ Energic",
    "rhythm": "🎵 Rhythm",
    "spectrum": "🌈 Spectrum",
    "rolling": "🌊 Rolling",
    "rhythm_spectrum": "🎵🌈 Rhythm+Spectrum",
    "rhythm_rolling": "🎵🌊 Rhythm+Rolling",
    "spectrum_rolling": "🌈🌊 Spectrum+Rolling",
    "energic_rolling": "⚡🌊 Energic+Rolling",
}


# =========================================================
# Экспорт
# =========================================================
__all__ = [
    "DOMAIN",
    "CONF_RESET",
    "CONF_DELAY",
    "EFFECTS",
    "SCENES",
    "EFFECTS_MAP",
    "SCENES_MAP",
    "ALL_EFFECTS_MAP",
    "EFFECT_LABELS",
    "SCENE_LABELS",
    "ALL_EFFECT_LABELS",
    "MIC_MODES",
    "MIC_MODE_LABELS",
]
