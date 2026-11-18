"""Instagram リール動画（1080x1920 / 30fps）を生成するスクリプト。

使い方:
    python3 reels/make_reel.py            # reels/out/study_tips_reel.mp4 を出力
    python3 reels/make_reel.py --preview  # 各シーンの静止画を reels/out/preview_*.png に出力

テキストを変えたいときは SCENES の中身を書き換えてください。
"""
import argparse
import math
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
W, H, FPS = 1080, 1920, 30

FONT_B = str(HERE / "fonts" / "mr800.ttf")
FONT_R = str(HERE / "fonts" / "mr400.ttf")

BOARD = (31, 61, 47)
CHALK = (246, 244, 236)
YELLOW = (255, 221, 87)
PINK = (255, 150, 160)
BLUE = (150, 210, 255)

# ---- 台本 ---------------------------------------------------------------
# kind: hook / tip / cta, dur: 秒
SCENES = [
    dict(kind="hook", dur=3.2,
         small="現役教員が教える",
         big=["テスト前に", "本当に効く", "勉強法 3選"]),
    dict(kind="tip", dur=4.6, num=1, color=YELLOW,
         title=["暗記より先に", "「問題を解く」"],
         body=["できない所が分かってから覚えると", "ムダな暗記がなくなります"]),
    dict(kind="tip", dur=4.6, num=2, color=PINK,
         title=["暗記は", "「寝る前10分」"],
         body=["寝ている間に記憶が整理されて", "翌朝まで残りやすくなります"]),
    dict(kind="tip", dur=4.6, num=3, color=BLUE,
         title=["友だちに", "「説明してみる」"],
         body=["説明できない所＝わかっていない所", "弱点がすぐに見つかります"]),
    dict(kind="cta", dur=3.4,
         big=["保存して", "テスト前に見返そう"],
         small="フォローで毎週 勉強のコツを発信中"),
]

# ---- 共通ユーティリティ ----------------------------------------------------
_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_back(t):
    t = clamp(t)
    c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def make_board():
    """チョークの粉っぽいムラのある黒板背景"""
    rnd = random.Random(7)
    img = Image.new("RGB", (W, H), BOARD)
    d = ImageDraw.Draw(img)
    for _ in range(260):  # 消し跡のムラ
        x, y = rnd.randint(-200, W), rnd.randint(-200, H)
        r = rnd.randint(80, 260)
        c = tuple(v + rnd.randint(-6, 9) for v in BOARD)
        d.ellipse([x, y, x + r * 2, y + r // 2], fill=c)
    img = img.filter(ImageFilter.GaussianBlur(40))
    noise = Image.effect_noise((W, H), 18).convert("RGB")
    img = Image.blend(img, noise, 0.06)
    # 木の枠
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 36], fill=(120, 82, 50))
    d.rectangle([0, H - 36, W, H], fill=(120, 82, 50))
    return img


def text_layer(lines, fnt, fill, spacing=1.25, stroke=0, stroke_fill=None):
    """複数行を中央揃えで描いた RGBA 画像を返す"""
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * spacing)
    widths = [fnt.getbbox(l)[2] for l in lines]
    w = max(widths) + stroke * 2 + 8
    h = lh * len(lines) + stroke * 2 + 8
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, l in enumerate(lines):
        x = (w - widths[i]) // 2
        d.text((x, stroke + 4 + i * lh), l, font=fnt, fill=fill,
               stroke_width=stroke, stroke_fill=stroke_fill)
    return layer


def paste(base, layer, cx, cy, alpha=1.0, scale=1.0, dy=0):
    if alpha <= 0:
        return
    if scale != 1.0:
        layer = layer.resize((max(1, int(layer.width * scale)),
                              max(1, int(layer.height * scale))), Image.LANCZOS)
    if alpha < 1:
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer = layer.copy()
        layer.putalpha(a)
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2 + dy)))


def underline(d, cx, y, width, color, progress, thick=14):
    """チョークで引いた手書き風アンダーライン（左から伸びる）"""
    if progress <= 0:
        return
    x0 = cx - width / 2
    x1 = x0 + width * ease_out(progress)
    pts = [(x, y + math.sin(x / 37) * 4) for x in range(int(x0), int(x1), 6)]
    if len(pts) > 1:
        d.line(pts, fill=color, width=thick, joint="curve")


def progress_bar(d, t_total, total):
    # 視聴維持のための上部プログレスバー（Reels UI に被らない位置）
    y = 70
    d.rounded_rectangle([80, y, W - 80, y + 10], 5, fill=(255, 255, 255, 50))
    d.rounded_rectangle([80, y, 80 + (W - 160) * (t_total / total), y + 10], 5, fill=YELLOW)


# ---- シーン描画 -------------------------------------------------------------
def draw_hook(img, s, t):
    small = text_layer([s["small"]], font(FONT_B, 64), BOARD)
    pad = Image.new("RGBA", (small.width + 70, small.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(pad).rounded_rectangle([0, 0, pad.width - 1, pad.height - 1], 40, fill=YELLOW)
    pad.alpha_composite(small, (35, 15))
    paste(img, pad, W / 2, 560, alpha=ease_out(t / 0.3), scale=0.6 + 0.4 * ease_back(t / 0.4))

    big = font(FONT_B, 150)
    for i, line in enumerate(s["big"]):
        st = 0.35 + i * 0.3
        p = (t - st) / 0.45
        color = YELLOW if i == 2 else CHALK
        lay = text_layer([line], big, color, stroke=6, stroke_fill=(20, 40, 30))
        paste(img, lay, W / 2, 820 + i * 205, alpha=ease_out(p), dy=60 * (1 - ease_out(p)))
    d = ImageDraw.Draw(img)
    underline(d, W / 2, 1360, 760, PINK, (t - 1.4) / 0.5)


def draw_tip(img, s, t):
    d = ImageDraw.Draw(img)
    color = s["color"]
    # 番号バッジ
    p = ease_back(t / 0.45)
    r = 120 * max(p, 0.01)
    cx, cy = W / 2, 470
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=12)
    num = text_layer([str(s["num"])], font(FONT_B, 170), color)
    paste(img, num, cx, cy - 8, alpha=ease_out(t / 0.3), scale=max(p, 0.01))
    label = text_layer([f"POINT {s['num']}/3"], font(FONT_B, 46), CHALK)
    paste(img, label, cx, 650, alpha=ease_out((t - 0.2) / 0.3))

    # タイトル
    tf = font(FONT_B, 116)
    for i, line in enumerate(s["title"]):
        st = 0.35 + i * 0.25
        pr = (t - st) / 0.4
        lay = text_layer([line], tf, color if i == 1 else CHALK, stroke=5, stroke_fill=(20, 40, 30))
        paste(img, lay, W / 2, 830 + i * 165, alpha=ease_out(pr), dy=-50 * (1 - ease_out(pr)) if i == 0 else 50 * (1 - ease_out(pr)))
    underline(d, W / 2, 1090, 840, color, (t - 1.0) / 0.45, thick=10)

    # 説明（白いメモ用紙風カード）
    pr = (t - 1.3) / 0.5
    if pr > 0:
        body = text_layer(s["body"], font(FONT_B, 54), (45, 45, 45), spacing=1.5)
        card = Image.new("RGBA", (W - 140, body.height + 90), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, card.width - 1, card.height - 1], 36, fill=(250, 248, 240, 245))
        card.alpha_composite(body, ((card.width - body.width) // 2, 45))
        paste(img, card, W / 2, 1290, alpha=ease_out(pr), dy=80 * (1 - ease_out(pr)))


def draw_cta(img, s, t):
    d = ImageDraw.Draw(img)
    # しおり（保存）アイコン
    p = ease_back(t / 0.45)
    cx, cy, sc = W / 2, 560, max(p, 0.01)
    bw, bh = 150 * sc, 200 * sc
    pts = [(cx - bw / 2, cy - bh / 2), (cx + bw / 2, cy - bh / 2), (cx + bw / 2, cy + bh / 2),
           (cx, cy + bh / 2 - 60 * sc), (cx - bw / 2, cy + bh / 2)]
    d.polygon(pts, fill=YELLOW)

    big = font(FONT_B, 120)
    for i, line in enumerate(s["big"]):
        pr = (t - 0.3 - i * 0.25) / 0.45
        lay = text_layer([line], big if i == 0 else font(FONT_B, 96),
                         YELLOW if i == 0 else CHALK, stroke=5, stroke_fill=(20, 40, 30))
        paste(img, lay, W / 2, 830 + i * 170, alpha=ease_out(pr), dy=50 * (1 - ease_out(pr)))
    underline(d, W / 2, 1100, 820, PINK, (t - 1.0) / 0.45, thick=10)

    pr = (t - 1.3) / 0.5
    sm = text_layer([s["small"]], font(FONT_B, 54), CHALK)
    # 軽く脈打たせて目を引く
    pulse = 1 + 0.03 * math.sin(max(0, t - 1.8) * 6) if t > 1.8 else 1
    paste(img, sm, W / 2, 1260, alpha=ease_out(pr), scale=pulse)


DRAW = dict(hook=draw_hook, tip=draw_tip, cta=draw_cta)


def render_frame(board, t_total, total):
    acc = 0.0
    for s in SCENES:
        if t_total < acc + s["dur"] or s is SCENES[-1]:
            break
        acc += s["dur"]
    t = t_total - acc
    img = board.convert("RGBA")
    DRAW[s["kind"]](img, s, t)
    # シーン切替のフェード（終わり0.2秒）
    fade = clamp((s["dur"] - t) / 0.2) if s is not SCENES[-1] else 1.0
    if fade < 1:
        img = Image.blend(board.convert("RGBA"), img, fade)
    progress_bar(ImageDraw.Draw(img), t_total, total)
    return img.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--out", default=str(OUT / "study_tips_reel.mp4"))
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    board = make_board()
    total = sum(s["dur"] for s in SCENES)

    if args.preview:
        acc = 0.0
        for i, s in enumerate(SCENES):
            render_frame(board, acc + s["dur"] - 0.3, total).save(OUT / f"preview_{i}.png")
            acc += s["dur"]
        return

    n = int(total * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
           args.out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        proc.stdin.write(render_frame(board, i / FPS, total).tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"wrote {args.out} ({total:.1f}s, {n} frames)")


if __name__ == "__main__":
    main()
