"""オリジナルイラスト（SVG）を生成し、PNG に変換するモジュール。

- すべて自作の図形で描いたオリジナルキャラクター・背景です（既存作品の模倣はしていません）。
- イラストの中には文字を一切描きません（日本語はすべて PowerPoint のテキストボックスで配置）。
- 生成した PNG は build/png/ にキャッシュされ、PPTX に埋め込まれます。
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field, replace

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, "assets", "icons")
PNG_DIR = os.path.join(HERE, "build", "png")
os.makedirs(PNG_DIR, exist_ok=True)

LINE = "#3A2E3A"  # 線画の色


# ---------------------------------------------------------------------------
# 人物
# ---------------------------------------------------------------------------
@dataclass
class Person:
    hair: str = "short"          # short / spiky / bob / long / pony / adult_short / adult_bun
    hair_color: str = "#3B2B25"
    skin: str = "#FBDCC4"
    eye: str = "#4A3228"
    bottom: str = "pants"        # pants / skirt
    outfit: str = "blazer"       # blazer / suit / cardigan / whitecoat / jersey
    outfit_color: str = "#2C3E66"
    tie: str = "#C8424B"         # ネクタイ・リボンの色
    tie_style: str = "tie"       # tie / ribbon / none
    pose: str = "stand"          # stand / wave / cheer / hold / raise / think / point
    mouth: str = "smile"         # smile / open / calm / o
    glasses: bool = False
    adult: bool = False
    extra: list = field(default_factory=list)


def _arm(points, color, hand_skin, width=21):
    (x1, y1), (x2, y2), (x3, y3) = points
    d = f"M{x1},{y1} L{x2},{y2} L{x3},{y3}"
    s = (f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{width+5}" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
    # 手（親指つき）
    s += _hand(x3, y3, hand_skin, x3 - x2, y3 - y2)
    return s


def _hand(x, y, skin, dx, dy):
    # 進行方向に少し出した手のひら＋親指
    import math
    ang = math.atan2(dy, dx)
    hx, hy = x + math.cos(ang) * 6, y + math.sin(ang) * 6
    tx, ty = hx + math.cos(ang - 1.4) * 10, hy + math.sin(ang - 1.4) * 10
    return (f'<ellipse cx="{tx:.1f}" cy="{ty:.1f}" rx="5" ry="6.5" fill="{skin}" stroke="{LINE}" stroke-width="2.2" transform="rotate({math.degrees(ang):.0f} {tx:.1f} {ty:.1f})"/>'
            f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="11" fill="{skin}" stroke="{LINE}" stroke-width="2.5"/>')


ARM_POSES = {
    # (左腕[画面左], 右腕[画面右]) 各 3 点: 肩→肘→手
    "stand": (((70, 168), (58, 218), (62, 262)), ((130, 168), (142, 218), (138, 262))),
    "wave": (((70, 168), (58, 218), (62, 262)), ((130, 168), (166, 150), (170, 104))),
    "cheer": (((70, 168), (40, 136), (36, 90)), ((130, 168), (160, 136), (164, 90))),
    "hold": (((70, 168), (60, 216), (88, 236)), ((130, 168), (140, 216), (112, 236))),
    "raise": (((70, 168), (58, 218), (62, 262)), ((130, 168), (150, 118), (152, 70))),
    "think": (((70, 168), (58, 218), (62, 262)), ((130, 168), (150, 210), (118, 150))),
    "point": (((70, 168), (58, 218), (62, 262)), ((130, 168), (170, 190), (196, 172))),
}


def _hair_back(p: Person):
    c = p.hair_color
    h = p.hair
    if h in ("short", "spiky", "adult_short"):
        return f'<ellipse cx="100" cy="84" rx="50" ry="48" fill="{c}" stroke="{LINE}" stroke-width="2.5"/>'
    if h == "bob":
        return (f'<path d="M48,88 C46,30 154,30 152,88 L154,140 Q134,150 122,138 L78,138 Q66,150 46,140 Z" '
                f'fill="{c}" stroke="{LINE}" stroke-width="2.5"/>')
    if h == "long":
        return (f'<path d="M48,88 C46,28 154,28 152,88 L160,212 Q130,226 100,214 Q70,226 40,212 Z" '
                f'fill="{c}" stroke="{LINE}" stroke-width="2.5"/>')
    if h == "pony":
        return (f'<path d="M138,62 C176,62 184,118 170,168 C164,186 150,190 152,170 C160,130 156,96 134,84 Z" '
                f'fill="{c}" stroke="{LINE}" stroke-width="2.5"/>'
                f'<ellipse cx="100" cy="84" rx="50" ry="48" fill="{c}" stroke="{LINE}" stroke-width="2.5"/>'
                f'<circle cx="140" cy="66" r="7" fill="#F5C84B" stroke="{LINE}" stroke-width="2"/>')
    if h == "adult_bun":
        return (f'<circle cx="100" cy="36" r="20" fill="{c}" stroke="{LINE}" stroke-width="2.5"/>'
                f'<ellipse cx="100" cy="84" rx="50" ry="48" fill="{c}" stroke="{LINE}" stroke-width="2.5"/>')
    return ""


def _hair_front(p: Person):
    c = p.hair_color
    h = p.hair
    if h == "short":
        d = ("M54,98 C50,50 76,34 102,34 C128,34 152,50 146,98 L140,80 L130,72 L122,84 L112,68 "
             "L100,84 L88,68 L78,86 L68,74 L60,92 Z")
    elif h == "spiky":
        d = ("M52,100 C46,58 62,40 80,34 L84,20 L96,32 L106,16 L114,32 L128,22 L128,38 C148,48 154,70 148,100 "
             "L140,82 L132,90 L124,74 L114,88 L102,72 L92,88 L80,74 L72,90 L62,80 Z")
    elif h in ("bob", "long", "pony"):
        d = ("M52,104 C46,52 74,34 102,34 C130,34 156,52 148,104 L142,86 L136,76 L124,86 "
             "L118,70 L104,84 L96,70 L84,86 L74,74 L64,90 L58,108 Z")
    elif h == "adult_short":
        d = ("M54,96 C50,50 76,36 102,36 C128,36 152,50 146,96 L140,74 C120,70 104,58 96,52 "
             "C88,64 70,72 60,76 Z")
    elif h == "adult_bun":
        d = ("M54,100 C50,52 76,38 102,38 C128,38 152,52 146,100 L140,78 C124,70 108,60 100,56 "
             "C92,62 74,74 60,78 Z")
    else:
        d = ""
    s = f'<path d="{d}" fill="{c}" stroke="{LINE}" stroke-width="2.5" stroke-linejoin="round"/>' if d else ""
    if h in ("bob", "long"):
        # 顔の横に垂れる髪
        s += (f'<path d="M54,90 C48,110 50,130 56,146 L66,142 C62,124 62,106 64,92 Z" fill="{c}" stroke="{LINE}" stroke-width="2.2"/>'
              f'<path d="M146,90 C152,110 150,130 144,146 L134,142 C138,124 138,106 136,92 Z" fill="{c}" stroke="{LINE}" stroke-width="2.2"/>')
    # ハイライト
    if s:
        s += '<path d="M72,52 Q100,40 128,52" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="5" stroke-linecap="round"/>'
    return s


def _eyes(p: Person):
    ry = 9.5 if p.adult else 12
    rx = 8 if p.adult else 9.5
    s = ""
    for cx, side in ((82, -1), (118, 1)):
        cy = 101
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.2"/>'
        s += f'<ellipse cx="{cx}" cy="{cy+1.5}" rx="{rx-1.8}" ry="{ry-1.8}" fill="{p.eye}"/>'
        s += f'<ellipse cx="{cx}" cy="{cy+3}" rx="{rx-5}" ry="{ry-6}" fill="#1E1418"/>'
        s += f'<circle cx="{cx-2.8}" cy="{cy-3.5}" r="3" fill="#FFFFFF"/>'
        s += f'<circle cx="{cx+3}" cy="{cy+5}" r="1.4" fill="#FFFFFF" fill-opacity="0.85"/>'
        # 上まぶた（目の上端に沿う太線＋目尻の小さなはね）
        x1, x2 = cx - rx - 1, cx + rx + 1
        s += (f'<path d="M{x1},{cy-2} Q{cx},{cy-ry-5} {x2},{cy-2}" fill="none" '
              f'stroke="{LINE}" stroke-width="3.6" stroke-linecap="round"/>')
        ex = x2 if side > 0 else x1
        s += f'<path d="M{ex},{cy-2} L{ex + side*4},{cy-5}" stroke="{LINE}" stroke-width="2.6" stroke-linecap="round"/>'
    # 眉（やわらかい弧）
    s += f'<path d="M72,80 Q81,75 90,78" fill="none" stroke="{LINE}" stroke-width="2.2" stroke-linecap="round"/>'
    s += f'<path d="M110,78 Q119,75 128,80" fill="none" stroke="{LINE}" stroke-width="2.2" stroke-linecap="round"/>'
    if p.glasses:
        s += (f'<g fill="none" stroke="#5A4A5A" stroke-width="2.4"><rect x="68" y="88" width="28" height="25" rx="8"/>'
              f'<rect x="104" y="88" width="28" height="25" rx="8"/><path d="M96,98 L104,98"/></g>')
    return s


def _mouth(p: Person):
    m = p.mouth
    if m == "open":
        return (f'<path d="M90,121 Q100,121 110,121 Q108,134 100,134 Q92,134 90,121 Z" fill="#9C3A44" stroke="{LINE}" stroke-width="2"/>'
                f'<path d="M94,129 Q100,126 106,129 Q103,133 100,133 Q97,133 94,129 Z" fill="#E9848C"/>')
    if m == "calm":
        return f'<path d="M93,124 Q100,128 107,124" fill="none" stroke="{LINE}" stroke-width="2.4" stroke-linecap="round"/>'
    if m == "o":
        return f'<ellipse cx="100" cy="125" rx="4" ry="5" fill="#9C3A44" stroke="{LINE}" stroke-width="2"/>'
    return f'<path d="M91,121 Q100,130 109,121" fill="none" stroke="{LINE}" stroke-width="2.6" stroke-linecap="round"/>'


def _torso(p: Person):
    oc = p.outfit_color
    s = ""
    if p.outfit == "whitecoat":
        s += f'<path d="M66,162 Q100,152 134,162 L148,300 L52,300 Z" fill="#FFFFFF" stroke="{LINE}" stroke-width="2.5"/>'
        s += f'<path d="M88,158 L100,200 L112,158 Z" fill="{oc}" stroke="{LINE}" stroke-width="2"/>'
        s += f'<path d="M100,200 L100,298" stroke="{LINE}" stroke-width="2"/>'
        s += f'<rect x="112" y="214" width="20" height="16" rx="3" fill="#DDEFFA" stroke="{LINE}" stroke-width="2"/>'
        return s
    if p.outfit == "jersey":
        s += f'<path d="M66,162 Q100,152 134,162 L142,282 L58,282 Z" fill="{oc}" stroke="{LINE}" stroke-width="2.5"/>'
        s += f'<path d="M88,158 L100,176 L112,158" fill="none" stroke="#FFFFFF" stroke-width="4"/>'
        s += f'<path d="M100,176 L100,280" stroke="#FFFFFF" stroke-width="3"/>'
        s += f'<path d="M64,170 L58,282 M136,170 L142,282" stroke="#FFFFFF" stroke-width="4"/>'
        return s
    if p.outfit == "cardigan":
        s += f'<path d="M66,162 Q100,152 134,162 L142,286 L58,286 Z" fill="{oc}" stroke="{LINE}" stroke-width="2.5"/>'
        s += f'<path d="M86,158 L100,214 L114,158 Z" fill="#FFFFFF" stroke="{LINE}" stroke-width="2"/>'
        s += f'<path d="M100,214 L100,284" stroke="{LINE}" stroke-width="2"/>'
        for y in (232, 254):
            s += f'<circle cx="94" cy="{y}" r="3" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.5"/>'
        return s
    # blazer / suit
    s += f'<path d="M66,162 Q100,152 134,162 L142,282 L58,282 Z" fill="{oc}" stroke="{LINE}" stroke-width="2.5"/>'
    s += f'<path d="M86,158 L100,206 L114,158 Z" fill="#FFFFFF" stroke="{LINE}" stroke-width="2"/>'
    if p.tie_style == "tie":
        s += f'<path d="M96,166 L104,166 L107,200 L100,210 L93,200 Z" fill="{p.tie}" stroke="{LINE}" stroke-width="1.8"/>'
    elif p.tie_style == "ribbon":
        s += (f'<path d="M100,172 L84,163 L84,183 Z M100,172 L116,163 L116,183 Z" fill="{p.tie}" stroke="{LINE}" stroke-width="1.8"/>'
              f'<circle cx="100" cy="172" r="5" fill="{p.tie}" stroke="{LINE}" stroke-width="1.8"/>')
    # 襟（ラペル）
    s += f'<path d="M86,158 L94,190 L84,186 L78,166 Z M114,158 L106,190 L116,186 L122,166 Z" fill="{oc}" stroke="{LINE}" stroke-width="1.8" stroke-opacity="0.8"/>'
    s += f'<path d="M100,208 L100,280" stroke="{LINE}" stroke-width="1.8" stroke-opacity="0.6"/>'
    for y in (232, 258):
        s += f'<circle cx="106" cy="{y}" r="3.2" fill="#E8C766" stroke="{LINE}" stroke-width="1.2"/>'
    # 胸ポケットの校章（無地の図形）
    if not p.adult:
        s += f'<circle cx="124" cy="190" r="5" fill="#F5C84B" stroke="{LINE}" stroke-width="1.2"/>'
    return s


def _lower(p: Person):
    s = ""
    skin = p.skin
    if p.bottom == "skirt":
        s += f'<rect x="78" y="330" width="16" height="44" fill="{skin}" stroke="{LINE}" stroke-width="2.2"/>'
        s += f'<rect x="106" y="330" width="16" height="44" fill="{skin}" stroke="{LINE}" stroke-width="2.2"/>'
        s += f'<rect x="77" y="364" width="18" height="24" fill="#FFFFFF" stroke="{LINE}" stroke-width="2.2"/>'
        s += f'<rect x="105" y="364" width="18" height="24" fill="#FFFFFF" stroke="{LINE}" stroke-width="2.2"/>'
        skirt = "#5A6E9A" if p.outfit == "blazer" else "#6A5A7A"
        s += f'<path d="M60,276 L140,276 L156,338 L44,338 Z" fill="{skirt}" stroke="{LINE}" stroke-width="2.5"/>'
        for x in (66, 82, 100, 118, 134):
            s += f'<path d="M{x+ (x-100)*0.05:.0f},280 L{x + (x-100)*0.22:.0f},336" stroke="{LINE}" stroke-width="1.5" stroke-opacity="0.5"/>'
        s += '<path d="M52,308 L148,308" stroke="#C8424B" stroke-width="2" stroke-opacity="0.5"/>'
    else:
        pc = "#3E4A63" if p.outfit in ("blazer", "suit") else ("#2C3E66" if p.outfit == "jersey" else "#5B5B6B")
        s += f'<path d="M62,276 L138,276 L136,386 L104,386 L100,318 L96,386 L64,386 Z" fill="{pc}" stroke="{LINE}" stroke-width="2.5" stroke-linejoin="round"/>'
    # 靴
    s += f'<ellipse cx="82" cy="392" rx="17" ry="8" fill="#5A3B2E" stroke="{LINE}" stroke-width="2.2"/>'
    s += f'<ellipse cx="118" cy="392" rx="17" ry="8" fill="#5A3B2E" stroke="{LINE}" stroke-width="2.2"/>'
    return s


def person_svg(p: Person, crop: str = "full") -> str:
    left, right = ARM_POSES[p.pose]
    sleeve = "#FFFFFF" if p.outfit == "whitecoat" else p.outfit_color
    parts = []
    parts.append(_hair_back(p))
    parts.append(_lower(p))
    parts.append(f'<rect x="91" y="132" width="18" height="30" fill="{p.skin}" stroke="{LINE}" stroke-width="2.2"/>')
    parts.append(_torso(p))
    # 腕は胴体の上に描く
    parts.append(_arm(left, sleeve, p.skin))
    parts.append(_arm(right, sleeve, p.skin))
    if p.pose == "hold":
        parts.append(f'<rect x="76" y="214" width="48" height="36" rx="3" fill="#F5C84B" stroke="{LINE}" stroke-width="2.4" transform="rotate(-4 100 232)"/>'
                     f'<path d="M100,214 L100,250" stroke="{LINE}" stroke-width="2" transform="rotate(-4 100 232)"/>')
        parts.append(_hand(88, 238, p.skin, 1, 0.4) + _hand(112, 238, p.skin, -1, 0.4))
    # 顔
    parts.append(f'<ellipse cx="57" cy="104" rx="7" ry="10" fill="{p.skin}" stroke="{LINE}" stroke-width="2.2"/>')
    parts.append(f'<ellipse cx="143" cy="104" rx="7" ry="10" fill="{p.skin}" stroke="{LINE}" stroke-width="2.2"/>')
    parts.append(f'<path d="M58,92 C58,56 78,44 100,44 C122,44 142,56 142,92 C142,118 124,140 100,144 C76,140 58,118 58,92 Z" '
                 f'fill="{p.skin}" stroke="{LINE}" stroke-width="2.5"/>')
    parts.append('<ellipse cx="74" cy="117" rx="8" ry="4.5" fill="#F29A9A" fill-opacity="0.45"/>'
                 '<ellipse cx="126" cy="117" rx="8" ry="4.5" fill="#F29A9A" fill-opacity="0.45"/>')
    parts.append(_eyes(p))
    parts.append(f'<path d="M100,108 L98,114" stroke="{LINE}" stroke-width="1.8" stroke-linecap="round" stroke-opacity="0.6"/>')
    parts.append(_mouth(p))
    parts.append(_hair_front(p))
    parts.extend(p.extra)
    vb = {"full": "0 0 210 408", "bust": "20 0 170 250"}[crop]
    if p.pose in ("cheer", "point", "wave", "raise"):
        vb = {"full": "0 0 210 408", "bust": "10 0 200 250"}[crop]
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{"".join(parts)}</svg>'


# 登場人物（服装・髪型を全スライドで統一）
CAST = {
    "haruto": Person(hair="short", hair_color="#3B2B25", skin="#F6D2B8", bottom="pants", tie_style="tie"),
    "mei": Person(hair="pony", hair_color="#5A3A2A", skin="#FBDCC4", bottom="skirt", tie_style="ribbon", eye="#6A4A30"),
    "sora": Person(hair="bob", hair_color="#2A2430", skin="#F3CDB0", bottom="pants", tie_style="ribbon", eye="#3A4A6A"),
    "yuto": Person(hair="spiky", hair_color="#6B4A32", skin="#E9BC98", bottom="pants", tie_style="tie", glasses=True),
    "aoi": Person(hair="long", hair_color="#2E2228", skin="#FBE0CC", bottom="skirt", tie_style="ribbon", eye="#4A3A5A"),
}
STAFF = {
    "teacher_a": Person(hair="adult_short", hair_color="#2E2A2A", skin="#F3CFB3", outfit="suit", outfit_color="#4A5568",
                        tie="#2E7D9A", tie_style="tie", adult=True, glasses=True, bottom="pants"),
    "teacher_b": Person(hair="adult_bun", hair_color="#4A3428", skin="#FADBC4", outfit="cardigan", outfit_color="#5FA383",
                        tie_style="none", adult=True, bottom="skirt"),
    "nurse": Person(hair="adult_short", hair_color="#5A4030", skin="#FADBC4", outfit="whitecoat", outfit_color="#F29AAE",
                    tie_style="none", adult=True, bottom="pants"),
    "counselor": Person(hair="adult_bun", hair_color="#3A2E2A", skin="#EFC8A8", outfit="cardigan", outfit_color="#E0A34A",
                        tie_style="none", adult=True, bottom="pants", glasses=True),
}


def person(name: str, pose: str = "stand", mouth: str = "smile", crop: str = "full", **kw) -> str:
    base = CAST.get(name) or STAFF[name]
    p = replace(base, pose=pose, mouth=mouth, **kw)
    path = render(f"person_{name}_{pose}_{mouth}_{crop}" + "".join(f"_{k}{v}" for k, v in sorted(kw.items())),
                  person_svg(p, crop), width=600)
    _trim(path)
    return path


def _trim(path, pad=6):
    """透明な余白を切り詰め、配置枠と見た目の大きさを一致させる。"""
    from PIL import Image
    im = Image.open(path)
    l, t, r, b = im.getchannel("A").getbbox()
    im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad))).save(path)


# ---------------------------------------------------------------------------
# 背景・小物
# ---------------------------------------------------------------------------
def _sakura_tree(x, y, s=1.0):
    blobs = [(-60, -40, 52), (-10, -70, 60), (50, -40, 54), (-40, 10, 46), (30, 14, 50), (80, 0, 40), (-85, 0, 36)]
    g = f'<g transform="translate({x},{y}) scale({s})">'
    g += f'<path d="M-12,140 L-8,20 L-34,-10 L-26,-16 L-4,8 L0,-30 L10,-30 L10,10 L34,-14 L42,-8 L14,24 L14,140 Z" fill="#8A5A44" stroke="{LINE}" stroke-width="2.5"/>'
    for (bx, by, r) in blobs:
        g += f'<circle cx="{bx}" cy="{by}" r="{r}" fill="#F7B6C8" stroke="#E58FA9" stroke-width="2"/>'
    for (bx, by, r) in blobs:
        g += f'<circle cx="{bx - r*0.25}" cy="{by - r*0.3}" r="{r*0.45}" fill="#FCD3DE"/>'
    for i, (px, py) in enumerate([(-50, -60), (10, -90), (60, -50), (-20, 0), (40, 20), (-70, 10), (90, -10)]):
        g += _flower(px, py, 7)
    return g + "</g>"


def _flower(x, y, r):
    import math
    s = ""
    for k in range(5):
        a = math.radians(k * 72 - 90)
        s += f'<ellipse cx="{x + math.cos(a)*r:.1f}" cy="{y + math.sin(a)*r:.1f}" rx="{r*0.62:.1f}" ry="{r*0.8:.1f}" fill="#FFFFFF" transform="rotate({k*72} {x + math.cos(a)*r:.1f} {y + math.sin(a)*r:.1f})"/>'
    s += f'<circle cx="{x}" cy="{y}" r="{r*0.35:.1f}" fill="#F5C84B"/>'
    return s


def _petals(n, w, h, seed=3):
    import random
    rnd = random.Random(seed)
    s = ""
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.uniform(5, 10)
        a = rnd.uniform(0, 180)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.1f}" ry="{r*0.6:.1f}" fill="#F7B6C8" fill-opacity="0.9" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>'
    return s


def school_svg():
    w, h = 900, 560
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
    # 校舎
    s += f'<rect x="150" y="190" width="600" height="300" rx="6" fill="#FFFFFF" stroke="{LINE}" stroke-width="3"/>'
    s += f'<rect x="380" y="110" width="140" height="100" fill="#FFFFFF" stroke="{LINE}" stroke-width="3"/>'
    s += f'<path d="M370,112 L450,64 L530,112 Z" fill="#183153" stroke="{LINE}" stroke-width="3"/>'
    s += f'<circle cx="450" cy="160" r="30" fill="#FFFFFF" stroke="{LINE}" stroke-width="3"/>'
    s += f'<path d="M450,160 L450,140 M450,160 L464,166" stroke="{LINE}" stroke-width="3.5" stroke-linecap="round"/>'
    s += f'<rect x="140" y="180" width="620" height="18" rx="4" fill="#183153" stroke="{LINE}" stroke-width="2.5"/>'
    for row in range(3):
        for col in range(8):
            if 3 <= col <= 4 and row == 2:
                continue
            x = 178 + col * 70
            y = 218 + row * 86
            s += f'<rect x="{x}" y="{y}" width="48" height="56" rx="3" fill="#BFE0F5" stroke="{LINE}" stroke-width="2.2"/>'
            s += f'<path d="M{x+24},{y} L{x+24},{y+56} M{x},{y+28} L{x+48},{y+28}" stroke="#FFFFFF" stroke-width="2.5"/>'
            s += f'<path d="M{x+6},{y+20} L{x+16},{y+8}" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>'
    s += f'<rect x="400" y="390" width="100" height="100" fill="#A7C8E0" stroke="{LINE}" stroke-width="3"/>'
    s += f'<path d="M450,390 L450,490" stroke="{LINE}" stroke-width="2.5"/>'
    # 地面
    s += _sakura_tree(110, 360, 1.25)
    s += _sakura_tree(800, 370, 1.15)
    s += _petals(28, w, 420, seed=7)
    s += "</svg>"
    return s


def sky_svg(w=1920, h=1080, dark=False):
    """表紙・エンディング用の背景（空のグラデーション）。文字なし。"""
    if dark:
        top, bottom = "#0F2240", "#2B4C7E"
    else:
        top, bottom = "#BFE3F7", "#FFFFFF"
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
         f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
         f'<rect width="{w}" height="{h}" fill="url(#g)"/>')
    if dark:
        import random
        rnd = random.Random(11)
        for _ in range(70):
            x, y, r = rnd.uniform(0, w), rnd.uniform(0, h * 0.7), rnd.uniform(1.5, 4)
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#FFFFFF" fill-opacity="{rnd.uniform(0.4, 0.95):.2f}"/>'
        # 朝日
        s += f'<circle cx="{w*0.5}" cy="{h*1.05}" r="{h*0.42}" fill="#F5C84B" fill-opacity="0.25"/>'
        s += f'<circle cx="{w*0.5}" cy="{h*1.05}" r="{h*0.3}" fill="#F5C84B" fill-opacity="0.35"/>'
        s += f'<path d="M0,{h*0.9} Q{w*0.5},{h*0.8} {w},{h*0.9} L{w},{h} L0,{h} Z" fill="#1B3A5E"/>'
    else:
        for (cx, cy, k) in [(260, 170, 1.0), (1500, 120, 0.8), (980, 230, 0.6)]:
            s += (f'<g fill="#FFFFFF" fill-opacity="0.9"><ellipse cx="{cx}" cy="{cy}" rx="{110*k}" ry="{42*k}"/>'
                  f'<circle cx="{cx-40*k}" cy="{cy-26*k}" r="{44*k}"/><circle cx="{cx+34*k}" cy="{cy-34*k}" r="{54*k}"/></g>')
    s += "</svg>"
    return s


def road_svg(color="#DDEFFA"):
    """ロードマップ用の曲がった道（文字なし）"""
    w, h = 1700, 520
    d = "M40,450 C360,450 380,250 700,250 C1020,250 1040,80 1360,80 C1480,80 1560,80 1660,80"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
            f'<path d="{d}" fill="none" stroke="#C9D6E3" stroke-width="86" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#F3F6F9" stroke-width="70" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#F5C84B" stroke-width="7" stroke-dasharray="26 22" stroke-linecap="round"/>'
            f'</svg>')


def phone_svg():
    w, h = 260, 460
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
    s += f'<rect x="10" y="10" width="240" height="440" rx="34" fill="#2A3550" stroke="{LINE}" stroke-width="3"/>'
    s += f'<rect x="24" y="44" width="212" height="372" rx="12" fill="#F4F8FC"/>'
    s += '<rect x="100" y="24" width="60" height="8" rx="4" fill="#4A5670"/>'
    # 吹き出し（文字なし・線で表現）
    bubbles = [(40, 70, 130, "#DDEFFA", "l"), (90, 140, 130, "#DCEFE5", "r"), (40, 210, 110, "#DDEFFA", "l"), (70, 280, 150, "#FCE8B5", "r")]
    for (x, y, bw, c, side) in bubbles:
        s += f'<rect x="{x}" y="{y}" width="{bw}" height="52" rx="16" fill="{c}" stroke="#AFC3D6" stroke-width="1.5"/>'
        s += f'<rect x="{x+14}" y="{y+14}" width="{bw-40}" height="7" rx="3.5" fill="#9BB0C6"/>'
        s += f'<rect x="{x+14}" y="{y+30}" width="{bw-64}" height="7" rx="3.5" fill="#9BB0C6"/>'
    s += f'<circle cx="208" cy="372" r="18" fill="#F5C84B"/><path d="M200,372 L214,372 M208,365 L214,372 L208,379" stroke="#183153" stroke-width="3" fill="none" stroke-linecap="round"/>'
    return s + "</svg>"


def blackboard_svg():
    w, h = 520, 300
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
    s += f'<rect x="10" y="10" width="500" height="250" rx="8" fill="#8A6244" stroke="{LINE}" stroke-width="3"/>'
    s += f'<rect x="26" y="26" width="468" height="218" rx="4" fill="#2F6B55"/>'
    # 図形だけ（文字なし）
    s += '<circle cx="120" cy="110" r="40" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-opacity="0.85"/>'
    s += '<path d="M210,160 L270,70 L330,160 Z" fill="none" stroke="#F5C84B" stroke-width="4"/>'
    s += '<path d="M370,150 Q400,70 440,120 T470,90" fill="none" stroke="#F7B6C8" stroke-width="4"/>'
    s += '<path d="M60,200 L460,200" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.5" stroke-dasharray="12 10"/>'
    s += f'<rect x="60" y="250" width="400" height="12" rx="4" fill="#B08868" stroke="{LINE}" stroke-width="2"/>'
    s += '<rect x="120" y="244" width="30" height="8" rx="2" fill="#FFFFFF"/><rect x="170" y="244" width="30" height="8" rx="2" fill="#F5C84B"/>'
    return s + "</svg>"


def desk_svg():
    w, h = 360, 220
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
    s += f'<rect x="20" y="70" width="320" height="22" rx="4" fill="#D9A877" stroke="{LINE}" stroke-width="2.5"/>'
    s += f'<rect x="40" y="92" width="14" height="120" fill="#9AA6B8" stroke="{LINE}" stroke-width="2"/>'
    s += f'<rect x="306" y="92" width="14" height="120" fill="#9AA6B8" stroke="{LINE}" stroke-width="2"/>'
    s += f'<rect x="70" y="40" width="110" height="32" rx="3" fill="#FFFFFF" stroke="{LINE}" stroke-width="2.2"/>'
    s += f'<path d="M125,40 L125,72" stroke="{LINE}" stroke-width="2"/>'
    for i in range(3):
        s += f'<path d="M80,{50+i*7} L118,{50+i*7} M132,{50+i*7} L170,{50+i*7}" stroke="#9BB0C6" stroke-width="2"/>'
    s += f'<rect x="200" y="30" width="22" height="42" rx="2" fill="#E8743B" stroke="{LINE}" stroke-width="2"/>'
    s += f'<rect x="224" y="24" width="22" height="48" rx="2" fill="#3A8FD6" stroke="{LINE}" stroke-width="2"/>'
    s += f'<rect x="248" y="34" width="22" height="38" rx="2" fill="#2E9E6B" stroke="{LINE}" stroke-width="2"/>'
    s += f'<path d="M280,66 L322,40" stroke="#F5C84B" stroke-width="8" stroke-linecap="round"/>'
    return s + "</svg>"


def backpack_svg():
    w, h = 220, 240
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
    s += f'<path d="M70,40 Q110,0 150,40" fill="none" stroke="{LINE}" stroke-width="10"/>'
    s += f'<rect x="40" y="36" width="140" height="190" rx="36" fill="#183153" stroke="{LINE}" stroke-width="3"/>'
    s += f'<rect x="62" y="120" width="96" height="80" rx="16" fill="#2D4C7A" stroke="{LINE}" stroke-width="2.5"/>'
    s += f'<path d="M62,140 L158,140" stroke="#F5C84B" stroke-width="4"/>'
    s += f'<circle cx="110" cy="84" r="12" fill="#F5C84B" stroke="{LINE}" stroke-width="2"/>'
    return s + "</svg>"


def stairs_svg(color="#8A63D2"):
    w, h = 520, 360
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
    for i in range(4):
        x = 20 + i * 120
        y = 280 - i * 70
        s += f'<rect x="{x}" y="{y}" width="{w-20-x}" height="{h-y-10}" fill="{["#EFE7FA","#E2D5F6","#D3C0F0","#C2A8EA"][i]}" stroke="#B9A2E0" stroke-width="2"/>'
    s += f'<path d="M470,20 L470,70" stroke="{LINE}" stroke-width="4"/><path d="M470,22 L510,34 L470,48 Z" fill="#F5C84B" stroke="{LINE}" stroke-width="2"/>'
    return s + "</svg>"


def thought_svg():
    """考えごとの雲（文字なし）"""
    w, h = 300, 220
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
    for (x, y, r) in [(90, 90, 60), (160, 70, 66), (220, 100, 56), (130, 130, 56), (190, 140, 50)]:
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="#AFC3D6" stroke-width="3"/>'
    for (x, y, r) in [(90, 90, 58), (160, 70, 64), (220, 100, 54), (130, 130, 54), (190, 140, 48)]:
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF"/>'
    s += '<circle cx="70" cy="186" r="12" fill="#FFFFFF" stroke="#AFC3D6" stroke-width="3"/><circle cx="44" cy="206" r="7" fill="#FFFFFF" stroke="#AFC3D6" stroke-width="3"/>'
    s += '<path d="M120,96 L140,116 L180,76" fill="none" stroke="#F5C84B" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    return s + "</svg>"


# ---------------------------------------------------------------------------
# アイコン（Font Awesome 6 Free, CC BY 4.0）
# ---------------------------------------------------------------------------
def icon(name: str, color: str = "#FFFFFF", size: int = 256) -> str:
    path = os.path.join(ICON_DIR, f"{name}.svg")
    with open(path, encoding="utf-8") as f:
        svg = f.read()
    svg = svg.replace("currentColor", color)
    svg = re.sub(r'color="[^"]*"', "", svg)
    svg = re.sub(r'style="[^"]*"', "", svg)
    return render(f"icon_{name}_{color.strip('#')}_{size}", svg, width=size)


def render(key: str, svg: str, width: int = 800) -> str:
    out = os.path.join(PNG_DIR, re.sub(r"[^A-Za-z0-9_.-]", "_", key) + ".png")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out, output_width=width)
    return out


def named(key: str, svg_func, width=1200, **kw) -> str:
    return render(key, svg_func(**kw), width=width)


if __name__ == "__main__":
    # 動作確認用：キャラクター一覧を書き出す
    from PIL import Image
    paths = [person(n, pose=pp) for n in CAST for pp in ("stand", "wave")] + [person(n) for n in STAFF]
    ims = [Image.open(x).convert("RGBA") for x in paths]
    W = sum(i.width for i in ims)
    H = max(i.height for i in ims)
    sheet = Image.new("RGBA", (W, H), "white")
    x = 0
    for i in ims:
        sheet.paste(i, (x, 0), i)
        x += i.width
    sheet.save(os.path.join(PNG_DIR, "_cast_sheet.png"))
    named("school", school_svg)
    print("ok")
