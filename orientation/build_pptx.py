"""中学1年生 新年度オリエンテーションスライド（20枚）を python-pptx で生成する。

使い方:
    python3 build_pptx.py            # ../output/中学1年生_オリエンテーション_20枚.pptx を生成

方針:
- 日本語はすべて編集可能なテキストボックス（イラスト内に文字なし）
- 学校ごとに異なる情報は【…を入力】の点線ボックス（オブジェクト名「編集_…」）
- 共通デザインは関数（header, card, placeholder など）で統一
- 発表者ノートに「伝えたいこと／説明例／問いかけ／編集項目／所要時間」を記載
"""
from __future__ import annotations

import os
import re

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN, MSO_AUTO_SIZE
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt, Emu

import illustrations as il
from notes import NOTES

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(os.path.dirname(HERE), "output")
OUT_PPTX = os.path.join(OUT_DIR, "中学1年生_オリエンテーション_20枚.pptx")

FONT = "Meiryo"          # メイリオ（Windows 標準）。Mac/iPad では自動的に代替フォントで表示
SW, SH = 13.333, 7.5     # スライドサイズ（インチ）
M = 0.6                  # 安全余白

NAVY = "183153"
LIGHTBLUE = "DDEFFA"
YELLOW = "F5C84B"
WHITE = "FFFFFF"
MINT = "DCEFE5"
GRAY = "5B6577"
LIGHTGRAY = "EEF1F5"
PH_FILL = "FFF6D8"
PH_LINE = "C9971C"

# 章ごとのアクセントカラー（濃い色 / 薄い色 / 章チップの文字色）
CHAPTERS = {
    1: ("ようこそ中学校へ", "F5C84B", "FFF4D1", NAVY),
    2: ("小学校と中学校の違い", "2F7FC4", "DDEFFA", WHITE),
    3: ("中学校生活の基本", "26885B", "DCEFE5", WHITE),
    4: ("中学校の楽しみ", "D9622B", "FDE6D8", WHITE),
    5: ("人との関わりと成長", "7A52C7", "ECE4FA", WHITE),
    6: ("安心と未来", "17818E", "D7F1F3", WHITE),
}
TOTAL = 20


def rgb(h):
    return RGBColor.from_string(h)


# ---------------------------------------------------------------------------
# テキスト
# ---------------------------------------------------------------------------
def _set_font(run, size, bold=False, color=NAVY):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.name = FONT
    f.color.rgb = rgb(color)
    rPr = run._r.get_or_add_rPr()
    rPr.set("lang", "ja-JP")
    rPr.set("altLang", "en-US")
    latin = rPr.find(qn("a:latin"))
    for tag in ("a:ea", "a:cs"):
        old = rPr.find(qn(tag))
        if old is not None:
            rPr.remove(old)
    ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", FONT)
    latin.addnext(ea)


def fill_text(tf, paras, size=24, bold=False, color=NAVY, align=PP_ALIGN.LEFT,
              anchor=MSO_ANCHOR.TOP, spacing=1.25, margin=0.06, space_after=0):
    """paras: 文字列（\\n で段落）または [段落, ...]。段落は文字列か [(text, {opts}), ...]。"""
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    if isinstance(paras, str):
        paras = paras.split("\n")
    first = True
    for para in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        runs = para if isinstance(para, list) else [(para, {})]
        psize = max([o.get("size", size) for _, o in runs] or [size])
        p.line_spacing = Pt(round(psize * spacing))
        if space_after:
            p.space_after = Pt(space_after)
        for text, o in runs:
            r = p.add_run()
            r.text = text
            _set_font(r, o.get("size", size), o.get("bold", bold), o.get("color", color))


def text(slide, x, y, w, h, paras, name=None, **kw):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    fill_text(tb.text_frame, paras, **kw)
    if name:
        tb.name = name
    return tb


# ---------------------------------------------------------------------------
# 図形
# ---------------------------------------------------------------------------
def shape(slide, kind, x, y, w, h, fill=None, line=None, line_w=1.5, dash=False, name=None, radius=None):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(line_w)
        if dash:
            s.line.dash_style = MSO_LINE.DASH
    else:
        s.line.fill.background()
    if radius is not None and kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    # 影などのテーマ効果を使わない
    style = s._element.find(qn("p:style"))
    if style is not None:
        s._element.remove(style)
    if name:
        s.name = name
    return s


def box(slide, x, y, w, h, fill, paras=None, radius=0.12, line=None, name=None, **kw):
    s = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=fill, line=line, radius=radius, name=name)
    if paras is not None:
        kw.setdefault("margin", 0.12)
        fill_text(s.text_frame, paras, **kw)
    return s


def circle(slide, cx, cy, d, fill, paras=None, line=None, line_w=1.5, name=None, **kw):
    s = shape(slide, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d, fill=fill, line=line, line_w=line_w, name=name)
    if paras is not None:
        kw.setdefault("align", PP_ALIGN.CENTER)
        kw.setdefault("anchor", MSO_ANCHOR.MIDDLE)
        kw.setdefault("margin", 0.02)
        fill_text(s.text_frame, paras, **kw)
    return s


def placeholder(slide, x, y, w, h, label, size=20, name=None, align=PP_ALIGN.CENTER):
    """学校ごとに編集する欄（点線・薄い黄色）。"""
    s = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=PH_FILL, line=PH_LINE, line_w=1.75, dash=True,
              radius=0.18, name=name or "編集_" + re.sub(r"[【】]", "", label)[:20])
    fill_text(s.text_frame, label, size=size, bold=True, color="7A5A00", align=align,
              anchor=MSO_ANCHOR.MIDDLE, margin=0.08)
    return s


def img(slide, path, x, y, w=None, h=None, name=None):
    with Image.open(path) as im:
        iw, ih = im.size
    if w is None:
        w = h * iw / ih
    if h is None:
        h = w * ih / iw
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        pic.name = name
    return pic, w, h


def icon_circle(slide, cx, cy, d, icon_name, fill, icon_color="#FFFFFF", ratio=0.5):
    circle(slide, cx, cy, d, fill, name=f"アイコン背景_{icon_name}")
    s = d * ratio
    img(slide, il.icon(icon_name, icon_color), cx - s / 2, cy - s / 2, w=s, h=s, name=f"アイコン_{icon_name}")


def arrow(slide, x, y, w, h, fill, rot=0):
    s = shape(slide, MSO_SHAPE.RIGHT_ARROW, x, y, w, h, fill=fill)
    s.rotation = rot
    return s


# ---------------------------------------------------------------------------
# 共通ヘッダー（章チップ・タイトル・冒険マップ型の進行表示・ページ番号）
# ---------------------------------------------------------------------------
def header(slide, no, ch, title):
    name, color, tint, chip_text = CHAPTERS[ch]
    label = f"第{ch}章　{name}"
    w = 0.3 * len(label) + 0.5
    box(slide, M, 0.38, w, 0.5, color, [[(label, {"bold": True, "color": chip_text})]], radius=0.5,
        size=20, anchor=MSO_ANCHOR.MIDDLE, margin=0.06, align=PP_ALIGN.CENTER, name="章ラベル")
    text(slide, M - 0.04, 0.98, SW - 2 * M, 0.85, [[(title, {"bold": True})]], size=36, anchor=MSO_ANCHOR.MIDDLE,
         margin=0.04, name="タイトル")
    progress(slide, no, ch)


def progress(slide, no, ch, dark=False):
    # 6章を「冒険の道しるべ」として表示（現在の章が大きく色付き）
    x0 = 9.55
    for i in range(1, 7):
        cx = x0 + (i - 1) * 0.36
        if i < ch:
            circle(slide, cx, 0.63, 0.2, CHAPTERS[i][1], name=f"進行_{i}")
        elif i == ch:
            circle(slide, cx, 0.63, 0.3, CHAPTERS[i][1], line=WHITE if dark else NAVY, line_w=2, name=f"進行_{i}")
        else:
            circle(slide, cx, 0.63, 0.2, "C9D2DD" if not dark else "5A6E8C", name=f"進行_{i}")
    text(slide, 11.68, 0.38, 1.05, 0.5, f"{no:02d} / {TOTAL}", size=20, color=WHITE if dark else GRAY,
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, margin=0, name="ページ番号")


def new_slide(prs, no):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(WHITE)
    s.notes_slide.notes_text_frame.text = NOTES[no]
    return s


# ---------------------------------------------------------------------------
# 各スライド
# ---------------------------------------------------------------------------
def s01(prs):
    s = new_slide(prs, 1)
    img(s, il.named("sky", il.sky_svg, width=1920), 0, 0, w=SW, h=SH, name="背景_空")
    img(s, il.named("school", il.school_svg, width=1800), 5.9, 2.75, w=7.43, name="背景_校舎と桜")
    shape(s, MSO_SHAPE.RECTANGLE, 0, 6.75, SW, 0.75, fill="9ED3A8", name="背景_地面")
    for nm, pose, x in (("mei", "wave", 6.9), ("haruto", "cheer", 8.55), ("sora", "wave", 10.3)):
        img(s, il.person(nm, pose, "open"), x, 3.95, h=3.3, name=f"イラスト_生徒_{nm}")
    placeholder(s, 0.7, 0.75, 5.6, 0.62, "【年度を入力】年度 オリエンテーション", size=20, name="編集_年度")
    text(s, 0.65, 1.6, 6.2, 2.3, [[("ようこそ！", {"bold": True})], [("中学校へ", {"bold": True})]], size=60,
         spacing=1.15, name="表紙タイトル")
    text(s, 0.7, 3.95, 6.2, 0.62, "ここから始まる、君たちの3年間", size=28, bold=True, color="2F7FC4", name="サブタイトル")
    placeholder(s, 0.7, 4.9, 5.0, 0.8, "【学校名を入力】", size=28, name="編集_学校名")
    text(s, 0.7, 5.85, 5.0, 0.5, "中学1年生 スタートガイド", size=20, color=GRAY, name="教材名")


def _road_point(x_px):
    # road_svg のパスと同じ 3 次ベジェ曲線上で、x に対応する y を求める
    segs = [((30, 250), (300, 250), (330, 175), (560, 165)),
            ((560, 165), (820, 155), (860, 115), (1130, 105)),
            ((1130, 105), (1400, 95), (1450, 55), (1680, 50))]
    best = None
    for p0, p1, p2, p3 in segs:
        for i in range(201):
            t = i / 200
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
            if best is None or abs(x - x_px) < abs(best[0] - x_px):
                best = (x, y)
    return best[1]


def road_svg():
    d = ("M30,250 C300,250 330,175 560,165 C820,155 860,115 1130,105 C1400,95 1450,55 1680,50")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1700 300">'
            f'<path d="{d}" fill="none" stroke="#C9D6E3" stroke-width="78" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#F3F6F9" stroke-width="64" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#F5C84B" stroke-width="6" stroke-dasharray="24 20" stroke-linecap="round"/>'
            f'</svg>')


def s02(prs):
    s = new_slide(prs, 2)
    header(s, 2, 1, "3年間の成長ロードマップ")
    rx, ry, rw = M, 1.95, SW - 2 * M
    scale = rw / 1700
    _, _, rh = img(s, il.render("road", road_svg(), width=1700), rx, ry, w=rw, name="イラスト_道")
    grades = [
        ("中学1年", "1年", YELLOW, NAVY, "新しい環境に慣れる", "いろいろ挑戦する", "D49A12"),
        ("中学2年", "2年", "2F7FC4", WHITE, "自分の強みを伸ばす", "仲間を支える", "2F7FC4"),
        ("中学3年", "3年", NAVY, YELLOW, "進路を考える", "未来へ進む", NAVY),
    ]
    cw = 3.7
    for i, (g, short, col, tcol, l1, l2, hcol) in enumerate(grades):
        cx = 2.6 + i * 4.067
        px = (cx - rx) / scale
        cy = ry + _road_point(px) * scale
        shape(s, MSO_SHAPE.RECTANGLE, cx - 0.02, cy, 0.04, 4.35 - cy, fill="AFC3D6", name="つなぎ線")
        circle(s, cx, cy, 0.95, col, [[(short, {"bold": True, "color": tcol})]], size=24, line=WHITE, line_w=3,
               name=f"目印_{short}")
        b = box(s, cx - cw / 2, 4.35, cw, 1.95, "F4F8FC", line="C9D6E3", name=f"カード_{g}")
        text(s, cx - cw / 2 + 0.25, 4.47, cw - 0.5, 0.6, [[(g, {"bold": True, "color": hcol})]], size=28,
             align=PP_ALIGN.CENTER)
        text(s, cx - cw / 2 + 0.15, 5.12, cw - 0.3, 1.05, [l1, l2], size=24, align=PP_ALIGN.CENTER)
    # ゴールの旗
    fx = rx + 1680 * scale
    img(s, il.icon("Flag", "#D9622B"), fx - 0.35, ry - 0.05, w=0.5, h=0.5, name="アイコン_ゴール")
    text(s, M, 6.42, SW - 2 * M, 0.55,
         [[("3年間かけて、", {}), ("自分のペースで成長", {"bold": True, "color": "2F7FC4"}), ("していこう", {})]],
         size=24, align=PP_ALIGN.CENTER)


def s03(prs):
    s = new_slide(prs, 3)
    ch, col, tint = 2, CHAPTERS[2][1], CHAPTERS[2][2]
    header(s, 3, ch, "先生が変わる？　〜教科担任制〜")
    py, ph = 2.0, 4.2
    box(s, M, py, 5.85, ph, LIGHTGRAY, name="比較_小学校")
    box(s, 6.88, py, 5.85, ph, tint, name="比較_中学校")
    text(s, M, py + 0.15, 5.85, 0.6, [[("小学校", {"bold": True, "color": GRAY})]], size=28, align=PP_ALIGN.CENTER)
    text(s, 6.88, py + 0.15, 5.85, 0.6, [[("中学校", {"bold": True, "color": col})]], size=28, align=PP_ALIGN.CENTER)
    # 小学校：1人の先生＋多くの教科
    img(s, il.person("teacher_b", "stand", crop="bust"), 2.85, py + 0.8, h=1.9, name="イラスト_担任")
    for j, ic in enumerate(["Book", "Calculator", "Flask", "Music"]):
        cx = [1.4, 1.65, 5.0, 5.25][j]
        cy = [py + 1.25, py + 2.25, py + 1.25, py + 2.25][j]
        icon_circle(s, cx, cy, 0.62, ic, "8D99AE")
    text(s, M + 0.2, py + 2.85, 5.45, 1.2, [[("担任の先生が", {})], [("ほとんどの教科", {"bold": True}), ("を教える", {})]],
         size=24, align=PP_ALIGN.CENTER)
    # 中学校：教科ごとに先生
    for j, (nm, ic) in enumerate((("teacher_a", "Calculator"), ("counselor", "Book"), ("teacher_b", "Globe"))):
        x = 7.35 + j * 1.68
        img(s, il.person(nm, "stand", crop="bust"), x, py + 0.8, h=1.9, name=f"イラスト_教科の先生{j+1}")
        icon_circle(s, x + 1.15, py + 0.95, 0.5, ic, col)
    text(s, 7.08, py + 2.85, 5.45, 1.2, [[("教科ごとに", {})], [("専門の先生", {"bold": True, "color": col}), ("が教える", {})]],
         size=24, align=PP_ALIGN.CENTER)
    circle(s, 6.665, py + ph / 2, 0.75, col, line=WHITE, line_w=3, name="矢印背景")
    arrow(s, 6.44, py + ph / 2 - 0.17, 0.45, 0.34, WHITE)
    box(s, M, 6.38, SW - 2 * M, 0.62, "FFF4D1",
        [[("担任の先生は、", {}), ("クラスの相談役", {"bold": True}), ("。困ったことは何でも話してみよう", {})]],
        size=22, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, radius=0.5, name="まとめ")


def three_cards(s, ch, items, y=2.0, h=3.55, top_icon=True):
    col, tint = CHAPTERS[ch][1], CHAPTERS[ch][2]
    w, gap = 3.83, 0.305
    for i, (ic, head, body) in enumerate(items):
        x = M + i * (w + gap)
        box(s, x, y, w, h, tint, name=f"カード_{head}")
        icon_circle(s, x + w / 2, y + 0.75, 1.0, ic, col)
        text(s, x + 0.15, y + 1.4, w - 0.3, 0.6, [[(head, {"bold": True, "color": col})]], size=28, align=PP_ALIGN.CENTER)
        text(s, x + 0.15, y + 2.05, w - 0.3, 1.35, body, size=24, align=PP_ALIGN.CENTER)


def s04(prs):
    s = new_slide(prs, 4)
    header(s, 4, 2, "授業はどう変わる？")
    three_cards(s, 2, [
        ("BookOpen", "教科が増える", "教科が増え、\n内容も専門的に"),
        ("Comments", "進め方が変わる", "発表や話合いで\n考えを深める"),
        ("Lightbulb", "学びが深まる", "「なぜ？」を考え、\n知識をつなげる"),
    ])
    text(s, M, 5.85, 2.75, 0.7, [[("1時間の授業：", {"bold": True})]], size=24, anchor=MSO_ANCHOR.MIDDLE)
    placeholder(s, 3.3, 5.85, 3.6, 0.7, "【授業時間を入力】分", size=22, name="編集_授業時間")
    text(s, 7.2, 5.85, 5.53, 0.7, "※時間割は学校によって異なります", size=20, color=GRAY, anchor=MSO_ANCHOR.MIDDLE,
         align=PP_ALIGN.RIGHT)


def s05(prs):
    s = new_slide(prs, 5)
    ch, col, tint = 2, CHAPTERS[2][1], CHAPTERS[2][2]
    header(s, 5, ch, "定期テストって何？")
    cx, cy, r = 3.7, 4.45, 1.55
    rh = 2.0  # 横方向の半径（中央の文字が隠れないよう横長の輪にする）
    shape(s, MSO_SHAPE.OVAL, cx - rh, cy - r, 2 * rh, 2 * r, line="9CC3E6", line_w=5, name="サイクルの輪")
    circle(s, cx, cy, 1.75, tint, name="サイクル中心")
    text(s, cx - 0.8, cy - 0.45, 1.6, 0.9, ["くり返して", "力をのばす"], size=20, color=col, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0, spacing=1.2, name="サイクル中心_文字")
    nodes = [("計画", "CalendarCheck", 0, -r), ("学習", "Pencil", rh, 0), ("テスト", "PenToSquare", 0, r),
             ("振り返り", "MagnifyingGlass", -rh, 0)]
    # 矢じり（時計回り）
    import math
    for k in range(4):
        a = math.radians(-45 + 90 * k)
        ax, ay = cx + rh * math.cos(a), cy + r * math.sin(a)
        t = shape(s, MSO_SHAPE.ISOSCELES_TRIANGLE, ax - 0.2, ay - 0.2, 0.4, 0.4, fill="9CC3E6", name="矢じり")
        t.rotation = 45 + 90 * k + 90
    for lab, ic, dx, dy in nodes:
        w = 2.15
        b = box(s, cx + dx - w / 2, cy + dy - 0.38, w, 0.76, col, radius=0.5, name=f"ステップ_{lab}")
        img(s, il.icon(ic), cx + dx - w / 2 + 0.2, cy + dy - 0.2, w=0.4, h=0.4)
        text(s, cx + dx - w / 2 + 0.62, cy + dy - 0.38, w - 0.7, 0.76, [[(lab, {"bold": True, "color": WHITE})]],
             size=24, anchor=MSO_ANCHOR.MIDDLE, margin=0.02)
    x0 = 6.9
    text(s, x0, 2.15, 5.83, 0.6, [[("定期テストの目的", {"bold": True, "color": col})]], size=28)
    text(s, x0, 2.8, 5.83, 1.05, [[("学んだことが", {}), ("身についたか", {"bold": True})], [("を確かめ、次の学習に生かす", {})]],
         size=24)
    box(s, x0, 4.0, 5.83, 0.85, "FFF4D1", [[("点数だけでなく「", {}), ("振り返り", {"bold": True, "color": "C0392B"}),
                                           ("」が大切", {})]], size=24, anchor=MSO_ANCHOR.MIDDLE,
        align=PP_ALIGN.CENTER, name="ポイント")
    text(s, x0, 5.1, 5.83, 0.5, [[("本校の定期テスト", {"bold": True})]], size=20, color=GRAY)
    placeholder(s, x0, 5.6, 5.83, 0.9, "【テストの回数・時期を入力】", size=22, name="編集_定期テスト")


def s06(prs):
    s = new_slide(prs, 6)
    ch, col, tint = 2, CHAPTERS[2][1], CHAPTERS[2][2]
    header(s, 6, ch, "家庭学習のポイント")
    box(s, M, 2.0, 4.25, 3.85, tint, name="イラスト背景")
    img(s, il.person("yuto", "think", "calm", crop="bust"), 2.05, 1.95, h=2.15, name="イラスト_生徒")
    img(s, il.named("desk", il.desk_svg, width=900), 0.95, 3.55, w=3.55, name="イラスト_机")
    rows = [("BookOpen", "授業の復習", "その日の授業を、ノートで見直す"),
            ("MagnifyingGlass", "分からないことを整理", "どこが分からないかメモして質問する"),
            ("CalendarCheck", "計画を立てる", "テストや提出日から逆算して進める")]
    for i, (ic, head, body) in enumerate(rows):
        y = 2.0 + i * 1.3
        icon_circle(s, 5.55, y + 0.55, 0.95, ic, col)
        text(s, 6.25, y, 6.48, 0.55, [[(head, {"bold": True, "color": col})]], size=26, margin=0.02)
        text(s, 6.25, y + 0.55, 6.48, 0.55, body, size=22, margin=0.02)
    box(s, M, 6.1, SW - 2 * M, 0.82, "FFF4D1",
        [[("大切なのは「長い時間」より", {}), ("「中身」と「続けること」", {"bold": True, "color": "C0392B"})]],
        size=24, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, radius=0.5, name="まとめ")


def s07(prs):
    s = new_slide(prs, 7)
    ch, col, tint = 3, CHAPTERS[3][1], CHAPTERS[3][2]
    header(s, 7, ch, "中学校の1日")
    text(s, M, 1.95, SW - 2 * M, 0.55, "登校から下校まで、1日はこんな流れで進みます", size=24, color=GRAY)
    steps = [("PersonWalking", "登校"), ("Sun", "朝の活動"), ("BookOpen", "午前の\n授業"), ("Utensils", "昼食"),
             ("PenToSquare", "午後の\n授業"), ("Broom", "清掃"), ("DoorOpen", "帰りの会\n・下校")]
    pitch = (SW - 2 * M) / len(steps)
    ly = 3.4
    shape(s, MSO_SHAPE.RECTANGLE, M + pitch / 2, ly - 0.04, pitch * (len(steps) - 1), 0.08, fill="A9D6BF", name="時間の線")
    for i, (ic, lab) in enumerate(steps):
        cx = M + pitch * (i + 0.5)
        icon_circle(s, cx, ly, 0.95, ic, col)
        text(s, cx - pitch / 2, 4.0, pitch, 0.95, [[(l, {"bold": True})] for l in lab.split("\n")], size=24,
             align=PP_ALIGN.CENTER, spacing=1.1, margin=0.02)
        placeholder(s, cx - 0.78, 5.05, 1.56, 0.6, "【時刻】", size=20, name=f"編集_時刻_{lab.replace(chr(10), '')}")
    box(s, M, 6.05, SW - 2 * M, 0.85, tint, radius=0.5, name="問いかけ")
    img(s, il.icon("FaceSmile", "#26885B"), M + 0.3, 6.2, w=0.55, h=0.55)
    text(s, M + 1.0, 6.05, SW - 2 * M - 1.2, 0.85,
         [[("問い：", {"bold": True, "color": col}), ("中学校の1日で、いちばん楽しみな時間はどれ？", {"bold": True})]],
         size=24, anchor=MSO_ANCHOR.MIDDLE)


def s08(prs):
    s = new_slide(prs, 8)
    ch, col, tint = 3, CHAPTERS[3][1], CHAPTERS[3][2]
    header(s, 8, ch, "学校生活のルール")
    box(s, M, 2.0, 4.4, 4.85, tint, name="問いのパネル")
    text(s, M + 0.3, 2.2, 3.9, 1.75, [[("ルールは", {"bold": True})], [("何のために", {"bold": True, "color": col})],
                                      [("ある？", {"bold": True})]], size=32, spacing=1.2)
    img(s, il.person("aoi", "think", "o", crop="bust"), M + 0.3, 3.95, h=2.0, name="イラスト_考える生徒")
    img(s, il.named("thought", il.thought_svg, width=600), M + 2.2, 3.95, w=1.9, name="イラスト_考え雲")
    text(s, M + 0.2, 6.0, 4.0, 0.8, [[("理由が分かると、", {})], [("自分から守れる", {"bold": True})]], size=20,
         align=PP_ALIGN.LEFT, spacing=1.15)
    cards = [("Clock", "時間"), ("Shirt", "服装"), ("Briefcase", "持ち物"), ("Building", "施設の使い方")]
    w, h = 3.6, 2.3
    for i, (ic, head) in enumerate(cards):
        x = 5.3 + (i % 2) * (w + 0.23)
        y = 2.0 + (i // 2) * (h + 0.25)
        box(s, x, y, w, h, WHITE, line="BFDCCB", name=f"ルール_{head}")
        icon_circle(s, x + 0.6, y + 0.6, 0.75, ic, col)
        text(s, x + 1.1, y + 0.28, w - 1.2, 0.65, [[(head, {"bold": True})]], size=26, anchor=MSO_ANCHOR.MIDDLE)
        placeholder(s, x + 0.2, y + 1.15, w - 0.4, 0.95, "【ルールを入力】", size=20, name=f"編集_ルール_{head}")


def s09(prs):
    s = new_slide(prs, 9)
    ch, col, tint = 3, CHAPTERS[3][1], CHAPTERS[3][2]
    header(s, 9, ch, "持ち物と提出物")
    # クリップボード
    box(s, M, 2.1, 7.4, 4.8, "C79A6B", radius=0.06, name="クリップボード")
    box(s, M + 0.15, 2.25, 7.1, 4.5, WHITE, radius=0.03, name="チェックリスト用紙")
    box(s, M + 2.7, 1.9, 2.0, 0.45, "8A8F99", radius=0.4, name="クリップ")
    items = ["前の日に、時間割を見て準備する", "提出物の期限を、メモに書く", "朝、もう一度カバンを確認する",
             "忘れたら、早めに先生に相談する"]
    for i, t in enumerate(items):
        y = 2.65 + i * 1.0
        last = i == len(items) - 1
        shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, M + 0.45, y + 0.08, 0.45, 0.45, fill=WHITE, line=col, line_w=2.5,
              name=f"チェック欄{i+1}")
        text(s, M + 1.1, y, 6.0, 0.62, [[(t, {"bold": last, "color": "C0392B" if last else NAVY})]], size=24,
             anchor=MSO_ANCHOR.MIDDLE, margin=0.02)
        if i < len(items) - 1:
            shape(s, MSO_SHAPE.RECTANGLE, M + 0.45, y + 0.82, 6.5, 0.015, fill="D5DCE4")
    img(s, il.person("mei", "hold", crop="bust"), 8.45, 1.95, h=2.75, name="イラスト_生徒")
    img(s, il.named("backpack", il.backpack_svg, width=500), 11.0, 2.75, h=1.8, name="イラスト_カバン")
    text(s, 8.4, 4.85, 4.33, 0.5, [[("本校の持ち物", {"bold": True})]], size=20, color=GRAY)
    placeholder(s, 8.4, 5.35, 4.33, 1.55, "【学校で必要な持ち物を入力】", size=20, name="編集_持ち物")


def s10(prs):
    s = new_slide(prs, 10)
    ch, col, tint = 3, CHAPTERS[3][1], CHAPTERS[3][2]
    header(s, 10, ch, "スマホ・SNSとの付き合い方")
    cards = [("Lock", "個人情報を守る", "名前・学校・住所などを\n公開しない"),
             ("Camera", "写真の共有", "人が写った写真は\n許可なく載せない"),
             ("CommentDots", "言葉の使い方", "送る前に読み返す\n相手が傷つかない？"),
             ("HandHoldingHeart", "困ったときは", "一人で抱えず、\nすぐ大人に相談")]
    w, h = 4.75, 2.25
    for i, (ic, head, body) in enumerate(cards):
        x = M if i % 2 == 0 else SW - M - w
        y = 2.0 + (i // 2) * (h + 0.3)
        box(s, x, y, w, h, tint, name=f"事例_{head}")
        icon_circle(s, x + 0.6, y + 0.6, 0.8, ic, col if i < 3 else "D9622B")
        text(s, x + 1.15, y + 0.3, w - 1.3, 0.6, [[(head, {"bold": True, "color": col if i < 3 else "D9622B"})]],
             size=26, anchor=MSO_ANCHOR.MIDDLE)
        text(s, x + 0.3, y + 1.1, w - 0.45, 1.0, body, size=22, spacing=1.2)
    img(s, il.named("phone", il.phone_svg, width=520), 5.72, 2.0, h=3.65, name="イラスト_スマホ")
    text(s, 5.45, 5.75, 2.45, 1.2, [[("使い方のルールを", {})], [("家族と決めよう", {"bold": True})]], size=20,
         align=PP_ALIGN.CENTER, spacing=1.2)


def s11(prs):
    s = new_slide(prs, 11)
    ch, col, tint = 4, CHAPTERS[4][1], CHAPTERS[4][2]
    header(s, 11, ch, "部活動・地域クラブ活動")
    box(s, M, 2.0, 3.0, 4.2, tint, name="イラスト背景")
    img(s, il.person("haruto", "cheer", "open", outfit="jersey", outfit_color="#D9622B", tie_style="none"),
        M + 0.4, 2.1, h=4.0, name="イラスト_ジャージの生徒")
    rows = [("Futbol", "運動系", "体を動かし、きたえる", "【運動部の名前を入力】"),
            ("Music", "文化系", "表現する・つくる", "【文化部の名前を入力】"),
            ("PeopleGroup", "地域クラブ", "地域で活動する", "【地域クラブ名を入力】")]
    for i, (ic, head, sub, ph) in enumerate(rows):
        y = 2.0 + i * 1.42
        box(s, 3.85, y, SW - M - 3.85, 1.28, WHITE, line="F2C3A8", name=f"活動_{head}")
        icon_circle(s, 4.55, y + 0.64, 0.9, ic, col)
        text(s, 5.2, y + 0.12, 3.2, 0.55, [[(head, {"bold": True, "color": col})]], size=26, margin=0.02)
        text(s, 5.2, y + 0.67, 3.3, 0.5, sub, size=20, margin=0.02)
        placeholder(s, 8.5, y + 0.19, 4.05, 0.9, ph, size=20)
    box(s, M, 6.38, SW - 2 * M, 0.58, "F4F5F7",
        "※活動の形（部活動・地域クラブ）は、学校や地域によって異なります", size=20, color=GRAY,
        anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, radius=0.5, name="注記")


def s12(prs):
    s = new_slide(prs, 12)
    ch, col, tint = 4, CHAPTERS[4][1], CHAPTERS[4][2]
    header(s, 12, ch, "学校行事")
    a = shape(s, MSO_SHAPE.PENTAGON, M, 2.0, SW - 2 * M, 0.75, fill=tint, name="1年間の流れ")
    text(s, M + 0.2, 2.0, 2.0, 0.75, [[("4月", {"bold": True, "color": col})]], size=24, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M + 3.0, 2.0, 6.0, 0.75, "1年間の主な行事", size=22, color=GRAY, anchor=MSO_ANCHOR.MIDDLE,
         align=PP_ALIGN.CENTER)
    text(s, SW - M - 2.4, 2.0, 1.6, 0.75, [[("3月", {"bold": True, "color": col})]], size=24, anchor=MSO_ANCHOR.MIDDLE,
         align=PP_ALIGN.RIGHT)
    events = [("Bus", "校外学習", "学校の外で学ぶ"), ("PersonRunning", "体育祭", "力を合わせる"),
              ("MasksTheater", "文化祭", "表現・発表の場"), ("Star", None, "")]
    w, gap = 2.85, (SW - 2 * M - 4 * 2.85) / 3
    for i, (ic, name, sub) in enumerate(events):
        x = M + i * (w + gap)
        y = 3.05
        box(s, x, y, w, 3.05, WHITE, line="F2C3A8", name=f"行事カード{i+1}")
        icon_circle(s, x + w / 2, y + 0.65, 0.9, ic, col if name else "C9971C")
        if name:
            text(s, x + 0.1, y + 1.2, w - 0.2, 0.6, [[(name, {"bold": True})]], size=26, align=PP_ALIGN.CENTER,
                 name=f"行事名_{name}")
            text(s, x + 0.1, y + 1.78, w - 0.2, 0.5, sub, size=20, color=GRAY, align=PP_ALIGN.CENTER)
        else:
            placeholder(s, x + 0.15, y + 1.22, w - 0.3, 1.0, "【行事名を入力】", size=20, name="編集_学校行事")
        placeholder(s, x + 0.25, y + 2.33, w - 0.5, 0.55, "【時期を入力】", size=20, name=f"編集_行事時期{i+1}")
    text(s, M, 6.32, SW - 2 * M, 0.6,
         [[("問い：", {"bold": True, "color": col}), ("どの行事が楽しみ？　となりの人と話してみよう", {"bold": True})]],
         size=24, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def s13(prs):
    s = new_slide(prs, 13)
    ch, col, tint = 4, CHAPTERS[4][1], CHAPTERS[4][2]
    header(s, 13, ch, "生徒会・委員会活動")
    box(s, M, 2.0, 8.85, 1.6, col, name="キャッチコピー")
    text(s, M + 0.35, 2.0, 8.3, 1.6, [[("自分たちの学校は、", {"bold": True, "color": WHITE})],
                                      [("自分たちでもつくる", {"bold": True, "color": "FFE9A8"})]], size=34,
         anchor=MSO_ANCHOR.MIDDLE, spacing=1.15)
    cards = [("Bullhorn", "生徒会", "行事などを\n企画・運営する", None),
             ("ClipboardList", "委員会", "仕事を分担して\n学校を支える", "【委員会を入力】"),
             ("Lightbulb", "提案する", "アイデアを\n出し合い、形に", None)]
    w = 2.85
    for i, (ic, head, body, ph) in enumerate(cards):
        x = M + i * (w + 0.15)
        y = 3.85
        box(s, x, y, w, 3.05, tint, name=f"活動_{head}")
        icon_circle(s, x + 0.6, y + 0.6, 0.8, ic, col)
        text(s, x + 1.1, y + 0.3, w - 1.15, 0.6, [[(head, {"bold": True, "color": col})]], size=26,
             anchor=MSO_ANCHOR.MIDDLE, margin=0.02)
        text(s, x + 0.15, y + 1.15, w - 0.3, 1.0, body, size=22, spacing=1.2)
        if ph:
            placeholder(s, x + 0.12, y + 2.2, w - 0.24, 0.7, ph, size=20, name="編集_委員会")
    p2 = il.person("yuto", "raise", "open")
    p1 = il.person("aoi", "raise", "open")
    w2 = 4.4 * Image.open(p2).width / Image.open(p2).height
    w1 = 4.6 * Image.open(p1).width / Image.open(p1).height
    x2 = SW - M - w2
    img(s, p1, max(9.65, x2 - w1 + 0.25), 2.25, h=4.6, name="イラスト_手を挙げる生徒1")
    img(s, p2, x2, 2.45, h=4.4, name="イラスト_手を挙げる生徒2")


def s14(prs):
    s = new_slide(prs, 14)
    ch, col, tint = 4, CHAPTERS[4][1], CHAPTERS[4][2]
    header(s, 14, ch, "学級活動　〜クラスをつくる時間〜")
    items = [("Comments", "話合い", "意見を出し合い、\nクラスで決める"),
             ("ClipboardCheck", "係活動", "一人一人が役割を\n担って支える"),
             ("FaceSmile", "レクリエーション", "楽しみながら\n仲を深める"),
             ("MagnifyingGlass", "課題解決", "クラスの困りごとを\nみんなで考える")]
    w, h = 5.9, 2.3
    for i, (ic, head, body) in enumerate(items):
        x = M if i % 2 == 0 else SW - M - w
        y = 2.0 + (i // 2) * (h + 0.25)
        box(s, x, y, w, h, tint, name=f"学級活動_{head}")
        tx = x + 0.3 if i % 2 == 0 else x + 1.25
        icon_circle(s, tx + 0.5, y + 0.75, 0.95, ic, col)
        text(s, tx + 1.15, y + 0.4, 3.55, 0.65, [[(head, {"bold": True, "color": col})]], size=26, margin=0.02)
        text(s, tx + 1.15, y + 1.05, 3.55, 1.05, body, size=22, margin=0.02, spacing=1.2)
    circle(s, SW / 2, 2.0 + h + 0.125, 1.75, WHITE, line=col, line_w=4, name="中心_協力")
    img(s, il.icon("Handshake", "#" + col), SW / 2 - 0.33, 2.0 + h + 0.125 - 0.62, w=0.66, h=0.66)
    text(s, SW / 2 - 0.8, 2.0 + h + 0.125 + 0.05, 1.6, 0.55, [[("協力", {"bold": True, "color": col})]], size=26,
         align=PP_ALIGN.CENTER, margin=0)


def s15(prs):
    s = new_slide(prs, 15)
    ch, col, tint = 5, CHAPTERS[5][1], CHAPTERS[5][2]
    header(s, 15, ch, "友達との関わり方")
    cols = [(("haruto", "stand", "smile"), ("sora", "wave", "open"), "違いを認める", "考え方や好きなことは\n人それぞれ"),
            (("mei", "stand", "open"), ("yuto", "stand", "calm"), "相手の話を聞く", "最後まで聞いてから\n自分の考えを話す"),
            (("aoi", "stand", "calm"), ("teacher_b", "stand", "smile"), "困ったら相談する", "一人で悩まず、\n信頼できる人に")]
    w = 3.83
    for i, (a, b, head, body) in enumerate(cols):
        x = M + i * (w + 0.305)
        box(s, x, 2.0, w, 3.75, tint, name=f"関わり_{head}")
        img(s, il.person(a[0], a[1], a[2], crop="bust"), x + 0.55, 2.12, h=1.75)
        img(s, il.person(b[0], b[1], b[2], crop="bust"), x + 1.95, 2.12, h=1.75)
        text(s, x + 0.1, 3.95, w - 0.2, 0.6, [[(head, {"bold": True, "color": col})]], size=26, align=PP_ALIGN.CENTER)
        text(s, x + 0.15, 4.55, w - 0.3, 1.1, body, size=22, align=PP_ALIGN.CENTER, spacing=1.2)
    box(s, M, 5.98, SW - 2 * M, 0.95, "FFF4D1", radius=0.3, name="メッセージ")
    img(s, il.icon("Heart", "#E25C7A"), M + 0.35, 6.18, w=0.55, h=0.55)
    text(s, M + 1.1, 5.98, SW - 2 * M - 1.3, 0.95,
         [[("全員と同じように仲良くしなくても大丈夫。", {})],
          [("お互いを大切にすることが、いちばん大事", {"bold": True, "color": col})]], size=22,
         anchor=MSO_ANCHOR.MIDDLE, spacing=1.2)


def s16(prs):
    s = new_slide(prs, 16)
    ch, col, tint = 5, CHAPTERS[5][1], CHAPTERS[5][2]
    header(s, 16, ch, "自分で考えて行動する")
    box(s, M, 2.0, 4.6, 1.05, LIGHTGRAY, [[("言われたからやる", {"bold": True, "color": GRAY})]], size=26,
        anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, radius=0.5, name="これまで")
    arrow(s, 5.4, 2.2, 1.2, 0.65, "F5C84B")
    box(s, 6.8, 2.0, SW - M - 6.8, 1.05, col, [[("必要だと考えて行動する", {"bold": True, "color": WHITE})]],
        size=28, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, radius=0.5, name="これから")
    scenes = [("Book", "授業の前", "次の授業の準備を\n自分から始める"),
              ("Recycle", "教室で", "落ちているごみに\n気づいて拾う"),
              ("HandHoldingHeart", "友達が困っていたら", "「どうしたの？」と\n声をかける")]
    w = 3.83
    for i, (ic, scene, body) in enumerate(scenes):
        x = M + i * (w + 0.305)
        y = 3.35
        box(s, x, y, w, 3.55, tint, name=f"場面_{scene}")
        box(s, x + 0.3, y + 0.25, w - 0.6, 0.55, WHITE, [[(scene, {"bold": True, "color": col})]], size=20,
            anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, radius=0.5)
        icon_circle(s, x + w / 2, y + 1.55, 1.05, ic, col)
        text(s, x + 0.15, y + 2.3, w - 0.3, 1.1, body, size=22, align=PP_ALIGN.CENTER, spacing=1.2)


def s17(prs):
    s = new_slide(prs, 17)
    ch, col, tint = 5, CHAPTERS[5][1], CHAPTERS[5][2]
    header(s, 17, ch, "失敗は成長のチャンス")
    sx, sy, sw = M, 2.15, 6.5
    k = sw / 520
    img(s, il.named("stairs", il.stairs_svg, width=1040), sx, sy, w=sw, name="イラスト_階段")
    labels = ["挑戦", "失敗", "振り返り", "改善"]
    icons = ["Flag", "TriangleExclamation", "MagnifyingGlass", "Seedling"]
    for i, lab in enumerate(labels):
        x = sx + (20 + i * 120) * k
        y = sy + (280 - i * 70) * k
        icon_circle(s, x + 0.75, y - 0.45, 0.7, icons[i], col)
        text(s, x, y + 0.12, 1.5, 0.55, [[(lab, {"bold": True, "color": "4A2F8A"})]], size=24, align=PP_ALIGN.CENTER,
             margin=0)
    x0 = 7.45
    text(s, x0, 2.1, SW - M - x0, 0.7, [[("失敗は、次の一歩のヒント", {"bold": True, "color": col})]], size=28)
    text(s, x0, 2.9, SW - M - x0, 1.1, [[("うまくいかなかった理由を考え、", {})], [("やり方を変えて、もう一度。", {})]],
         size=24)
    box(s, x0, 4.2, SW - M - x0, 1.35, tint,
        [[("失敗した人を責めない", {"bold": True})], [("「次はどうする？」を一緒に考える", {})]], size=22,
        anchor=MSO_ANCHOR.MIDDLE, spacing=1.25, name="クラスの約束")
    img(s, il.person("sora", "cheer", "open", crop="bust"), x0 + 0.1, 5.65, h=1.3, name="イラスト_生徒")
    text(s, x0 + 1.3, 5.75, SW - M - x0 - 1.3, 1.1, [[("このサイクルを", {})], [("くり返して成長しよう", {"bold": True})]],
         size=22, anchor=MSO_ANCHOR.MIDDLE, spacing=1.2)


def s18(prs):
    s = new_slide(prs, 18)
    ch, col, tint = 6, CHAPTERS[6][1], CHAPTERS[6][2]
    header(s, 18, ch, "困ったときは相談しよう")
    rows = [("ChalkboardUser", "担任の先生", "毎日会える、身近な相談相手"),
            ("Users", "学年の先生・教科の先生", "話しやすい先生に相談してOK"),
            ("KitMedical", "保健室の先生（養護教諭）", "体や心の調子が悪いときに"),
            ("Comments", "スクールカウンセラー", "心の専門家　来校日：【入力】"),
            ("HouseUser", "家の人・地域の相談窓口", "【地域の相談窓口を入力】")]
    for i, (ic, name, sub) in enumerate(rows):
        y = 2.0 + i * 0.99
        box(s, M, y, 6.2, 0.88, tint, radius=0.2, name=f"相談先_{name}")
        icon_circle(s, M + 0.5, y + 0.44, 0.66, ic, col)
        text(s, M + 1.0, y + 0.02, 5.1, 0.45, [[(name, {"bold": True})]], size=22, margin=0.02, spacing=1.1,
             name=f"相談先名_{i+1}")
        text(s, M + 1.0, y + 0.45, 5.1, 0.42, sub, size=20, color="2E4A5E" if "【" not in sub else "7A5A00",
             margin=0.02, spacing=1.1, name=f"相談先説明_{i+1}")
    x0, w0 = 7.1, SW - M - 7.1
    box(s, x0, 2.0, w0, 1.85, col, [[("学校に行きづらいときも、", {"bold": True, "color": WHITE})],
                                   [("相談していいんだよ", {"bold": True, "color": "FFE9A8"})]],
        size=28, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, spacing=1.25, name="メッセージ")
    img(s, il.person("counselor", "stand", "smile", crop="bust"), x0 + 1.05, 4.0, h=1.85, name="イラスト_先生")
    img(s, il.person("sora", "stand", "calm", crop="bust"), x0 + 2.75, 4.0, h=1.85, name="イラスト_生徒")
    placeholder(s, x0, 6.0, w0, 0.88, "【学校の相談窓口・連絡方法を入力】", size=20, name="編集_相談窓口")


def s19(prs):
    s = new_slide(prs, 19)
    ch, col, tint = 6, CHAPTERS[6][1], CHAPTERS[6][2]
    header(s, 19, ch, "3年後の自分を想像しよう")
    qs = ["どんなことに挑戦したい？", "どんな自分になりたい？", "仲間とどんな3年間を過ごしたい？"]
    w = 7.75
    for i, q in enumerate(qs):
        y = 2.0 + i * 1.38
        box(s, M, y, w, 1.25, tint, radius=0.15, name=f"問い{i+1}")
        circle(s, M + 0.55, y + 0.62, 0.75, col, [[(str(i + 1), {"bold": True, "color": WHITE})]], size=28)
        text(s, M + 1.15, y + 0.1, w - 1.35, 0.6, [[(q, {"bold": True})]], size=26, margin=0.02)
        line = shape(s, MSO_SHAPE.RECTANGLE, M + 1.17, y + 0.98, w - 1.5, 0.02, fill="8FBFC6")
    img(s, il.named("thought", il.thought_svg, width=600), 10.55, 1.95, w=2.15, name="イラスト_考え雲")
    img(s, il.person("aoi", "think", "smile"), 8.75, 2.35, h=3.7, name="イラスト_未来を考える生徒")
    box(s, M, 6.2, SW - 2 * M, 0.75, "FFF4D1", radius=0.5, name="活動の流れ")
    img(s, il.icon("Clock", "#17818E"), M + 0.3, 6.33, w=0.5, h=0.5)
    text(s, M + 0.95, 6.2, 2.5, 0.75, [[("ひとりで考える", {"bold": True})]], size=22, anchor=MSO_ANCHOR.MIDDLE)
    placeholder(s, 3.85, 6.29, 1.85, 0.57, "【　】分", size=20, name="編集_考える時間")
    arrow(s, 5.95, 6.4, 0.6, 0.35, col)
    text(s, 6.75, 6.2, 2.7, 0.75, [[("となりの人と話す", {"bold": True})]], size=22, anchor=MSO_ANCHOR.MIDDLE)
    placeholder(s, 9.55, 6.29, 1.85, 0.57, "【　】分", size=20, name="編集_話す時間")


def s20(prs):
    s = new_slide(prs, 20)
    s.background.fill.fore_color.rgb = rgb("0F2240")
    img(s, il.named("sky_dark", il.sky_svg, width=1920, dark=True), 0, 0, w=SW, h=SH, name="背景_夜明け")
    progress(s, 20, 6, dark=True)
    text(s, M, 0.95, SW - 2 * M, 0.95, [[("中学校生活、スタート！", {"bold": True, "color": WHITE})]], size=44,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 2.05, SW - 2 * M, 0.7, [[("比べるのは、", {"color": WHITE}), ("昨日の自分。", {"bold": True, "color": "9FD3F5"})]],
         size=34, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 2.8, SW - 2 * M, 0.7, [[("自分のペースで、", {"color": WHITE}), ("一歩ずつ。", {"bold": True, "color": "A8E6C4"})]],
         size=34, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, M, 3.6, SW - 2 * M, 0.85, [[("ここから、君たちの物語が始まる。", {"bold": True, "color": YELLOW})]], size=40,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    cast = [("aoi", "wave"), ("yuto", "cheer"), ("mei", "cheer"), ("haruto", "cheer"), ("sora", "wave")]
    for i, (nm, pose) in enumerate(cast):
        x = 1.7 + i * 2.1
        img(s, il.person(nm, pose, "open"), x, 4.65, h=2.75, name=f"イラスト_生徒_{nm}")


SLIDES = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20]


# ---------------------------------------------------------------------------
# テーマ（フォント・配色）をメイリオ／指定配色に設定
# ---------------------------------------------------------------------------
def set_theme(prs):
    theme_part = prs.slide_master.part.part_related_by(RT.THEME)
    root = etree.fromstring(theme_part.blob)
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    root.find(".//a:themeElements", ns).getparent()
    root.set("name", "中学1年オリエンテーション")
    for tag in ("majorFont", "minorFont"):
        f = root.find(f".//a:fontScheme/a:{tag}", ns)
        f.find("a:latin", ns).set("typeface", FONT)
        f.find("a:ea", ns).set("typeface", FONT)
        for jp in f.findall("a:font", ns):
            if jp.get("script") == "Jpan":
                jp.set("typeface", FONT)
    clr = root.find(".//a:clrScheme", ns)
    clr.set("name", "オリエンテーション")
    colors = {"dk2": NAVY, "lt2": LIGHTBLUE, "accent1": NAVY, "accent2": YELLOW, "accent3": "2F7FC4",
              "accent4": "26885B", "accent5": "D9622B", "accent6": "7A52C7"}
    for k, v in colors.items():
        el = clr.find(f"a:{k}", ns)
        for c in list(el):
            el.remove(c)
        etree.SubElement(el, qn("a:srgbClr")).set("val", v)
    theme_part._blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def build():
    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)
    set_theme(prs)
    for f in SLIDES:
        f(prs)
    cp = prs.core_properties
    cp.title = "中学1年生 スタートガイド｜中学校生活オリエンテーション"
    cp.subject = "新年度オリエンテーション（20枚）"
    cp.author = ""
    cp.last_modified_by = ""
    cp.keywords = "中学1年生, オリエンテーション, 学級活動"
    os.makedirs(OUT_DIR, exist_ok=True)
    prs.save(OUT_PPTX)
    print("saved:", OUT_PPTX, "slides:", len(prs.slides))


if __name__ == "__main__":
    build()
