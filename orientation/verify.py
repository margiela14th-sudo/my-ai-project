"""生成した PPTX を検証し、PDF・一覧画像を作成する。

使い方:
    python3 verify.py [--skill-dir <pptx スキルのディレクトリ>]

実施内容:
 1. PPTX を再読み込みして 20 枚あることを確認
 2. ZIP 内部構造（破損チェック）と全 XML のパース確認、[Content_Types] とリレーションの参照先確認
 3. （任意）pptx スキルの validate.py による OOXML スキーマ検証
 4. LibreOffice で PDF に変換し、20 ページであること・フォント埋め込みを確認
 5. 全ページを PNG にレンダリング（build/render/）
 6. 図形がスライド外・安全余白外にはみ出していないか、テキストがボックスに収まるかを自動チェック
 7. 20 枚の一覧プレビュー画像を作成
"""
from __future__ import annotations

import argparse
import glob
import math
import os
import posixpath
import shutil
import subprocess
import sys
import zipfile

from lxml import etree
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Emu

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "output")
PPTX = os.path.join(OUT, "中学1年生_オリエンテーション_20枚.pptx")
PDF = os.path.join(OUT, "中学1年生_オリエンテーション_20枚.pdf")
OVERVIEW = os.path.join(OUT, "中学1年生_スライド一覧.png")
RENDER = os.path.join(HERE, "build", "render")
EXPECTED = 20
SAFE = 0.45  # 背景以外の要素に求める最低余白（インチ）

FONT_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

results = []


def check(ok, msg):
    results.append((ok, msg))
    print(("[OK]   " if ok else "[NG]   ") + msg)
    return ok


def zip_and_xml():
    with zipfile.ZipFile(PPTX) as z:
        bad = z.testzip()
        check(bad is None, f"ZIP 整合性（CRC）: {'問題なし' if bad is None else bad}")
        names = set(z.namelist())
        xml_err = []
        for n in names:
            if n.endswith(".xml") or n.endswith(".rels"):
                try:
                    etree.fromstring(z.read(n))
                except etree.XMLSyntaxError as e:
                    xml_err.append(f"{n}: {e}")
        check(not xml_err, f"全 XML/RELS パース（{sum(1 for n in names if n.endswith(('.xml', '.rels')))} ファイル）"
              + ("" if not xml_err else f": {xml_err[:3]}"))
        # リレーションの参照先が存在するか
        missing = []
        for n in names:
            if not n.endswith(".rels"):
                continue
            base = posixpath.dirname(posixpath.dirname(n))
            for rel in etree.fromstring(z.read(n)):
                if rel.get("TargetMode") == "External":
                    missing.append(f"外部リンク: {rel.get('Target')}")
                    continue
                tgt = posixpath.normpath(posixpath.join(base, rel.get("Target")))
                if tgt.lstrip("/") not in names:
                    missing.append(f"{n} -> {tgt}")
        check(not missing, "リレーション参照先がすべて存在・外部リンクなし" + ("" if not missing else f": {missing[:3]}"))
        ct = etree.fromstring(z.read("[Content_Types].xml"))
        exts = {e.get("Extension") for e in ct if e.get("Extension")}
        overrides = {e.get("PartName").lstrip("/") for e in ct if e.get("PartName")}
        untyped = [n for n in names if not n.endswith("/") and n != "[Content_Types].xml"
                   and n not in overrides and n.rsplit(".", 1)[-1] not in exts]
        check(not untyped, "全パーツに Content-Type 定義あり" + ("" if not untyped else f": {untyped[:3]}"))
        media = [n for n in names if n.startswith("ppt/media/")]
        size = sum(z.getinfo(n).file_size for n in media)
        print(f"       埋め込み画像 {len(media)} 点 / 合計 {size/1024/1024:.1f} MB")


def schema_validate(skill_dir):
    v = os.path.join(skill_dir or "", "scripts", "office", "validate.py") if skill_dir else None
    if not v or not os.path.exists(v):
        print("[SKIP] OOXML スキーマ検証（validate.py が見つからないため未実施）")
        results.append((None, "OOXML スキーマ検証: 未実施"))
        return
    r = subprocess.run([sys.executable, v, PPTX], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    check(r.returncode == 0, "OOXML スキーマ・構造検証（validate.py）: " + out.splitlines()[-1] if out else "")


def to_pdf(skill_dir):
    tmp = os.path.join(HERE, "build", "pdf")
    os.makedirs(tmp, exist_ok=True)
    src = os.path.join(tmp, "deck.pptx")
    shutil.copy(PPTX, src)
    wrapper = os.path.join(skill_dir or "", "scripts", "office", "soffice.py")
    cmd = ([sys.executable, wrapper] if skill_dir and os.path.exists(wrapper) else ["soffice"]) + \
          ["--headless", "--convert-to", "pdf", "--outdir", tmp, src]
    subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=tmp)
    pdf = os.path.join(tmp, "deck.pdf")
    if not check(os.path.exists(pdf), "LibreOffice で PDF 変換"):
        return None
    shutil.copy(pdf, PDF)
    info = subprocess.run(["pdfinfo", PDF], capture_output=True, text=True).stdout
    pages = int([l for l in info.splitlines() if l.startswith("Pages:")][0].split()[-1])
    check(pages == EXPECTED, f"PDF ページ数 = {pages}")
    size = [l for l in info.splitlines() if l.startswith("Page size:")][0]
    print("       " + size.strip())
    fonts = subprocess.run(["pdffonts", PDF], capture_output=True, text=True).stdout.splitlines()[2:]
    not_emb = [f for f in fonts if f.split()[-5] != "yes"]
    check(fonts and not not_emb, f"PDF フォント埋め込み（{len(fonts)} 書体すべて埋め込み済み・iPhone で表示可）")
    return PDF


def render(pdf):
    if os.path.isdir(RENDER):
        shutil.rmtree(RENDER)
    os.makedirs(RENDER)
    subprocess.run(["pdftoppm", "-png", "-r", "144", pdf, os.path.join(RENDER, "slide")], check=True)
    files = sorted(glob.glob(os.path.join(RENDER, "slide-*.png")))
    w, h = Image.open(files[0]).size
    check(len(files) == EXPECTED, f"全ページを PNG にレンダリング（{len(files)} 枚, {w}×{h}px）")
    return files


_font_cache = {}


def _font(size_pt, bold):
    key = (size_pt, bold)
    if key not in _font_cache:
        # 1pt = 1/72 inch。100 px/inch で計測
        _font_cache[key] = ImageFont.truetype(FONT_B if bold else FONT_R, int(round(size_pt * 100 / 72)), index=0)
    return _font_cache[key]


def layout_checks(prs):
    sw, sh = prs.slide_width / 914400, prs.slide_height / 914400
    out_of_slide, unsafe, overflow, wraps = [], [], [], []
    for i, slide in enumerate(prs.slides, 1):
        for shp in slide.shapes:
            x, y = shp.left / 914400, shp.top / 914400
            w, h = shp.width / 914400, shp.height / 914400
            name = shp.name
            if x < -0.01 or y < -0.01 or x + w > sw + 0.01 or y + h > sh + 0.01:
                out_of_slide.append(f"{i:02d}:{name}")
            if not name.startswith("背景") and (x < SAFE - 0.01 or x + w > sw - SAFE + 0.01 or y < 0.3
                                                or y + h > sh - 0.05):
                unsafe.append(f"{i:02d}:{name}({x:.2f},{y:.2f},{w:.2f},{h:.2f})")
            if not shp.has_text_frame or not shp.text_frame.text.strip():
                continue
            tf = shp.text_frame
            ml = (tf.margin_left or 0) / 914400
            mr = (tf.margin_right or 0) / 914400
            mt = (tf.margin_top or 0) / 914400
            mb = (tf.margin_bottom or 0) / 914400
            avail = w - ml - mr
            if shp.shape_type == 1 and shp.auto_shape_type is not None and "OVAL" in str(shp.auto_shape_type):
                avail *= 0.70  # 楕円の内接領域
            total_h = 0.0
            for p in tf.paragraphs:
                txt = "".join(r.text for r in p.runs)
                if not p.runs:
                    continue
                width_in = 0.0
                maxsize = 0
                for r in p.runs:
                    sz = r.font.size.pt if r.font.size else 18
                    maxsize = max(maxsize, sz)
                    width_in += _font(sz, bool(r.font.bold)).getlength(r.text) / 100
                lines = max(1, math.ceil(width_in / avail - 0.02))
                if lines > 1:
                    wraps.append(f"{i:02d}:{name}「{txt[:18]}」 幅{width_in:.2f}/{avail:.2f}in")
                ls = p.line_spacing.pt / 72 if p.line_spacing is not None and hasattr(p.line_spacing, "pt") else maxsize * 1.2 / 72
                total_h += lines * ls
            if total_h > h - mt - mb + 0.08:
                overflow.append(f"{i:02d}:{name} 必要高さ{total_h:.2f}in > 枠{h - mt - mb:.2f}in")
    check(not out_of_slide, "スライド外へのはみ出しなし" + ("" if not out_of_slide else f": {out_of_slide}"))
    check(not unsafe, f"背景以外の要素が安全余白（左右 {SAFE}in）内" + ("" if not unsafe else f": {unsafe}"))
    check(not overflow, "テキストが枠の高さに収まる（Noto Sans CJK で計測）" + ("" if not overflow else f": {overflow}"))
    check(not wraps, "意図しない自動改行なし（改行位置はすべて明示）" + ("" if not wraps else f": {wraps}"))


def font_sizes(prs):
    small = []
    for i, slide in enumerate(prs.slides, 1):
        for shp in slide.shapes:
            if shp.has_text_frame:
                for p in shp.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.size and r.font.size.pt < 20 and r.text.strip():
                            small.append(f"{i:02d}:{r.text[:10]}({r.font.size.pt})")
    check(not small, "スライド上の文字はすべて 20pt 以上" + ("" if not small else f": {small}"))


def overview(files):
    thumbs = [Image.open(f).convert("RGB") for f in files]
    tw = 640
    th = int(thumbs[0].height * tw / thumbs[0].width)
    cols, rows, pad, lab = 4, 5, 28, 44
    W = cols * tw + (cols + 1) * pad
    H = rows * (th + lab) + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), (236, 241, 246))
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype(FONT_B, 26, index=0)
    for k, im in enumerate(thumbs):
        r, c = divmod(k, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + lab + pad)
        d.text((x, y), f"{k + 1:02d}", font=f, fill=(24, 49, 83))
        t = im.resize((tw, th), Image.LANCZOS)
        d.rectangle([x - 1, y + lab - 1, x + tw, y + lab + th], outline=(190, 200, 214), width=2)
        sheet.paste(t, (x, y + lab))
    sheet.save(OVERVIEW, optimize=True)
    check(os.path.exists(OVERVIEW), f"一覧プレビュー画像を作成（{W}×{H}px）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill-dir", default=os.environ.get("PPTX_SKILL_DIR"))
    a = ap.parse_args()
    print("== 1. 再読み込み")
    prs = Presentation(PPTX)
    check(len(prs.slides) == EXPECTED, f"スライド枚数 = {len(prs.slides)}")
    check(abs(prs.slide_width / 914400 - 13.333) < 0.01 and abs(prs.slide_height / 914400 - 7.5) < 0.01,
          f"スライドサイズ {prs.slide_width/914400:.3f} × {prs.slide_height/914400:.3f} in（16:9）")
    notes = sum(1 for s in prs.slides if s.has_notes_slide and "【5 想定所要時間】" in s.notes_slide.notes_text_frame.text)
    check(notes == EXPECTED, f"発表者ノート（5項目）あり: {notes} 枚")
    print("== 2. ZIP / XML")
    zip_and_xml()
    print("== 3. スキーマ検証")
    schema_validate(a.skill_dir)
    print("== 4. レイアウト自動チェック")
    layout_checks(prs)
    font_sizes(prs)
    print("== 5. PDF 変換・レンダリング")
    pdf = to_pdf(a.skill_dir)
    if pdf:
        files = render(pdf)
        overview(files)
    ng = [m for ok, m in results if ok is False]
    print(f"\n結果: OK {sum(1 for ok, _ in results if ok)} / NG {len(ng)} / 未実施 {sum(1 for ok, _ in results if ok is None)}")
    return 1 if ng else 0


if __name__ == "__main__":
    sys.exit(main())
