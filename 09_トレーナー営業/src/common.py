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
.card p{font-size:20px;line-height:1.7}
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
    import re, itertools
    body = "\n".join(slides)
    c = itertools.count(1)
    # ページ番号は並び順で振り直す（表紙・クロージングは番号なし）
    body = "".join(re.sub(r'<span class="n">\d+</span>', lambda m: f'<span class="n">{i}</span>', sec) if 'class="n"' in sec else sec
                   for i, sec in ((next(c), sec) for sec in re.split(r'(?=<section )', body)))
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


def ai_slides(acc, accd, audio_uses, video_uses):
    """録音・録画×AI分析の2枚。効果は未検証であることを明示する。"""
    def dev(icon, name, sub, uses):
        li = "".join(f"<li>{u}</li>" for u in uses)
        return (f'<div class="card" style="flex:1"><div class="row" style="gap:14px;align-items:center">{icon}'
                f'<div><h3 style="margin:0">{name}</h3><p class="lbl" style="margin:0">{sub}</p></div></div>'
                f'<ul style="padding-left:1.2em;margin-top:14px;font-size:20px;line-height:1.8">{li}</ul></div>')
    mic = f'<svg width="60" height="60" viewBox="0 0 60 60"><circle cx="30" cy="30" r="30" fill="{acc}"/><rect x="23" y="12" width="14" height="24" rx="7" fill="#0f2340"/><path d="M17 30q0 13 13 13t13-13M30 43v7" stroke="#0f2340" stroke-width="4" fill="none"/></svg>'
    cam = f'<svg width="60" height="60" viewBox="0 0 60 60"><circle cx="30" cy="30" r="30" fill="{acc}"/><rect x="12" y="20" width="26" height="22" rx="4" fill="#0f2340"/><path d="M38 27l11-6v20l-11-6z" fill="#0f2340"/></svg>'
    flow = "".join(
        f'<div style="flex:1;text-align:center"><div style="background:{bg};color:{fg};border-radius:12px;padding:12px 8px;font-size:17px;font-weight:bold">{t}</div></div>'
        + ('<div style="font-size:24px;color:%s;align-self:center">→</div>' % accd if i < 3 else "")
        for i, (t, bg, fg) in enumerate([("録る", "var(--bg)", "var(--navy)"), ("匿名化", "var(--bg)", "var(--navy)"), ("AIで集計", "var(--bg)", "var(--navy)"), ("監督へレポート", "var(--navy)", "#fff")]))
    s1 = slide(1, "測定の新しい手段（試験導入）", "声と映像を<em>AIで数字に</em>する",
        f'<div class="row">{dev(mic, "音声：Plaud NotePin", "胸元につける小型の録音機", audio_uses)}{dev(cam, "映像：DJI のカメラ", "練習・試合を固定位置で撮影", video_uses)}</div>'
        f'<div class="row" style="gap:10px;margin-top:18px">{flow}</div>',
        "成果への効果はまだ分かりません。無料トライアルで試し、監督が「役に立つ」と判断した指標だけを本導入で使います。人の目での確認も必ず行います。")
    s1 = s1.replace('<span class="n">0</span>', '<span class="n">1</span>')
    steps = [("① 学校の許可", "校長・部の責任者に、目的・方法・保存期間を書面で説明"),
             ("② 保護者・本人の同意", "同意書で個別に確認。同意しない生徒は撮影・録音の対象にしない"),
             ("③ 撮影・録音の開始", "練習・試合のみ。更衣室や練習以外の場面は撮らない")]
    st = "".join(f'<div class="card" style="flex:1;border-top:6px solid {acc}"><h3>{a}</h3><p>{b}</p></div>' for a, b in steps)
    rules = ["目的は「選手の成長の測定」だけ。それ以外に使わない",
             "映像・音声・数値を外部に公開・提供しない（SNS掲載もしない）",
             "AIに渡す前に氏名を番号に置き換える。データを学習に使わない設定のサービスだけ使う",
             "保存はパスワード付きの専用の場所に限定。契約終了後は期限を決めて削除",
             "本人・保護者から求めがあれば、いつでもその生徒のデータを削除"]
    rl = "".join(f'<li>{r}</li>' for r in rules)
    s2 = slide(1, "データの取り扱いとお約束", "撮る前に、<em>許可と同意</em>をいただきます",
        f'<div class="row" style="gap:16px">{st}</div>'
        f'<div class="row" style="margin-top:18px"><div style="flex:1.6"><ul style="padding-left:1.2em">{"".join(f"<li style=\"font-size:20px;line-height:1.7\">{r}</li>" for r in rules)}</ul></div>'
        f'<div class="card" style="flex:1;background:var(--navy);color:#fff"><h3 style="color:{acc}">元教員として</h3><p style="color:#fff">学校で生徒の個人情報を扱ってきた立場から、学校と同じ水準でデータを管理します。ルールは書面にして、学校・保護者にお渡しします。</p></div></div>',
        "同意書・データ取り扱い方針のひな形は、学校の規程に合わせて事前にご確認いただきます。")
    s2 = s2.replace('<span class="n">0</span>', '<span class="n">1</span>')
    return [s1, s2]
