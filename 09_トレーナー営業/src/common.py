"""営業資料の共通パーツ（CSS・SVGグラフ）。数値は必ず出典のあるものだけを渡すこと。"""
CSS = """
@page{size:1280px 720px;margin:0}
:root{--navy:#0f2340;--ink:#1d2433;--sub:#5a6476;--acc:ACC;--accD:ACCD;--line:#d9dee7;--bg:#f4f6f9;--ctl:#a9b3c3}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"IPAPGothic","IPAGothic",sans-serif;color:var(--ink)}
.s{width:1280px;height:720px;position:relative;overflow:hidden;page-break-after:always;background:#fff;padding:52px 72px 44px}
.s:last-child{page-break-after:auto}
.k{font-size:18px;color:var(--accD);font-weight:bold;letter-spacing:.08em}
h1{font-size:38px;line-height:1.3;margin:6px 0 22px;color:var(--navy)}
h1 em{font-style:normal;background:linear-gradient(transparent 62%,var(--acc) 62%)}
p,li{font-size:21px;line-height:1.6}
.n{position:absolute;right:40px;bottom:20px;font-size:14px;color:var(--sub)}
.note{position:absolute;left:72px;bottom:20px;right:120px;font-size:13px;color:var(--sub);line-height:1.5}
.dark{background:var(--navy);color:#fff}.dark h1{color:#fff}.dark .n{color:#9fb0c8}
.row{display:flex;gap:28px;align-items:stretch}
.card{background:var(--bg);border-radius:14px;padding:20px 24px}
.card h3{font-size:22px;color:var(--navy);margin-bottom:8px}
.card p{font-size:18px;line-height:1.55}
.stat{font-size:84px;font-weight:bold;color:var(--navy);line-height:1;letter-spacing:-.02em}
.stat small{font-size:30px}
.lbl{font-size:17px;color:var(--sub);margin-top:6px;line-height:1.4}
.tag{display:inline-block;font-size:14px;padding:3px 12px;border-radius:99px;background:var(--navy);color:#fff;margin-right:6px;vertical-align:middle}
.tag.a{background:var(--acc);color:var(--navy)}
table{border-collapse:collapse;width:100%}
th,td{border-bottom:1px solid var(--line);padding:9px 12px;text-align:left;font-size:17px;line-height:1.45;vertical-align:top}
th{background:var(--navy);color:#fff;font-size:15px}
.ref li{font-size:13.5px;line-height:1.45;margin-bottom:5px}
.honest{border-left:6px solid var(--acc);background:var(--bg);padding:10px 16px;font-size:16px;line-height:1.5;border-radius:0 10px 10px 0}
svg text{font-family:"IPAPGothic","IPAGothic",sans-serif}
"""

def css(acc, accd):
    return CSS.replace("ACCD", accd).replace("ACC", acc)

def page(title, acc, accd, slides):
    body = "\n".join(slides)
    return f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>{title}</title><style>{css(acc,accd)}</style></head><body>{body}</body></html>'

def slide(n, kicker, h1, inner, note="", cls=""):
    nt = f'<p class="note">{note}</p>' if note else ""
    num = f'<span class="n">{n}</span>' if n else ""
    return f'<section class="s {cls}"><p class="k">{kicker}</p><h1>{h1}</h1>{inner}{nt}{num}</section>'

def prepost(groups, w=560, h=330, unit="", ymax=None, lower_better=False, acc="#c8e63c"):
    """groups: [(ラベル, [(系列名, 前, 後, 強調bool)]...)] 前後の棒グラフ"""
    vals = [v for _, ser in groups for _, a, b, _ in ser for v in (a, b) if v is not None]
    ymax = ymax or max(vals) * 1.15
    left, bottom, top = 50, 50, 20
    ph = h - bottom - top
    nbars = sum(len(s) * 2 for _, s in groups)
    gap = 26
    bw = (w - left - 20 - gap * (len(groups) - 1) - 12 * (nbars // 2)) / nbars
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for i in range(5):
        y = top + ph * i / 4
        out.append(f'<line x1="{left}" x2="{w-10}" y1="{y}" y2="{y}" stroke="#e3e7ee"/>')
        out.append(f'<text x="{left-8}" y="{y+5}" font-size="13" fill="#5a6476" text-anchor="end">{ymax*(1-i/4):.0f}</text>')
    x = left + 6
    for gl, ser in groups:
        gx0 = x
        for name, a, b, hi in ser:
            for j, v in enumerate((a, b)):
                if v is None:
                    out.append(f'<text x="{x+bw/2}" y="{top+ph-6}" font-size="12" fill="#5a6476" text-anchor="middle">—</text>')
                else:
                    bh = ph * v / ymax
                    col = ("#0f2340" if j else "#9aa6b8") if hi else ("#c3cad6" if j else "#e1e5ec")
                    out.append(f'<rect x="{x}" y="{top+ph-bh}" width="{bw}" height="{bh}" rx="4" fill="{col}"/>')
                    out.append(f'<text x="{x+bw/2}" y="{top+ph-bh-6}" font-size="14" font-weight="bold" fill="#1d2433" text-anchor="middle">{v:g}</text>')
                out.append(f'<text x="{x+bw/2}" y="{top+ph+18}" font-size="12" fill="#5a6476" text-anchor="middle">{"後" if j else "前"}</text>')
                x += bw
            out.append(f'<text x="{x-bw}" y="{top+ph+36}" font-size="14" fill="#1d2433" text-anchor="middle">{name}</text>')
            x += 12
        out.append(f'<text x="{(gx0+x-12)/2}" y="{top-4}" font-size="15" font-weight="bold" fill="#0f2340" text-anchor="middle">{gl}</text>')
        x += gap
    if unit:
        out.append(f'<text x="{left-8}" y="{top-6}" font-size="12" fill="#5a6476" text-anchor="end">{unit}</text>')
    out.append('</svg>')
    return "".join(out)

def effect_bars(items, w=600, h=260, xmax=1.8, acc="#c8e63c"):
    """items: [(ラベル, 値, 強調色bool)] 効果量の横棒（目安線つき）"""
    left, top = 170, 30
    pw = w - left - 40
    rowh = (h - top - 40) / len(items)
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for v, t in ((0.2, "小"), (0.5, "中"), (0.8, "大")):
        x = left + pw * v / xmax
        out.append(f'<line x1="{x}" x2="{x}" y1="{top-8}" y2="{h-30}" stroke="#9aa6b8" stroke-dasharray="4 4"/>')
        out.append(f'<text x="{x}" y="{top-14}" font-size="13" fill="#5a6476" text-anchor="middle">効果{t} {v}</text>')
    for i, (lab, v, hi) in enumerate(items):
        y = top + rowh * i + 10
        bw = pw * v / xmax
        out.append(f'<text x="{left-12}" y="{y+rowh/2}" font-size="17" fill="#1d2433" text-anchor="end">{lab}</text>')
        out.append(f'<rect x="{left}" y="{y}" width="{bw}" height="{rowh-22}" rx="6" fill="{acc if hi else "#0f2340"}"/>')
        out.append(f'<text x="{left+bw+10}" y="{y+(rowh-22)/2+9}" font-size="26" font-weight="bold" fill="#0f2340">{v}</text>')
    out.append('</svg>')
    return "".join(out)

def meter(label, v, vmax, mark, mark_lbl, w=520, acc="#c8e63c"):
    """1本のゲージ。mark=目安値"""
    pw = w - 20
    mx = 10 + pw * mark / vmax
    return (f'<svg width="{w}" height="78" viewBox="0 0 {w} 78"><text x="10" y="18" font-size="16" fill="#1d2433">{label}</text>'
            f'<rect x="10" y="28" width="{pw}" height="24" rx="12" fill="#e6eaf0"/>'
            f'<rect x="10" y="28" width="{pw*v/vmax}" height="24" rx="12" fill="{acc}"/>'
            f'<line x1="{mx}" x2="{mx}" y1="22" y2="58" stroke="#0f2340" stroke-width="2"/>'
            f'<text x="{mx}" y="74" font-size="13" fill="#5a6476" text-anchor="middle">{mark_lbl}</text>'
            f'<text x="{10+pw*v/vmax-8}" y="46" font-size="16" font-weight="bold" fill="#0f2340" text-anchor="end">{v}</text></svg>')

def timeline(steps, acc):
    """steps: [(期間, タグ, 本文, 強調)]"""
    n = len(steps)
    cells = []
    for i, (when, tag, body, hi) in enumerate(steps):
        bg = "var(--navy)" if hi else "var(--bg)"
        fg = "#fff" if hi else "var(--ink)"
        t = f'<span class="tag a">{tag}</span>' if tag else ""
        cells.append(f'<div style="flex:1;background:{bg};color:{fg};border-radius:12px;padding:18px 16px;position:relative">'
                     f'<div style="font-size:22px;font-weight:bold;color:{acc if hi else "var(--navy)"};margin-bottom:6px">{when}</div>{t}'
                     f'<div style="font-size:17px;line-height:1.5;margin-top:8px">{body}</div></div>')
    bar = (f'<div style="height:10px;border-radius:5px;margin:0 0 16px;background:linear-gradient(90deg,#c3cad6 0%,#c3cad6 {100*2/n:.0f}%,{acc} {100*2/n:.0f}%)"></div>')
    return bar + '<div class="row" style="gap:14px">' + "".join(cells) + '</div>'
