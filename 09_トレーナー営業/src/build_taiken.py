"""体験メニュー（A4横）。show=見せる用、memo=進行メモ付き。"""
import os, sys
ACC, NAVY = "#c8e63c", "#0f2340"
CSS = f"""
@page{{size:297mm 210mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"IPAPGothic","IPAGothic",sans-serif;color:#1d2433}}
.p{{width:297mm;height:210mm;padding:12mm 14mm;position:relative;page-break-after:always;overflow:hidden}}
.p:last-child{{page-break-after:auto}}
.k{{font-size:13pt;color:#6f8c00;font-weight:bold;letter-spacing:.06em}}
h1{{font-size:26pt;color:{NAVY};margin:2mm 0 4mm}}
h1 em{{font-style:normal;background:linear-gradient(transparent 62%,{ACC} 62%)}}
.meta span{{display:inline-block;background:#eef3d6;color:#3f5200;border-radius:99px;padding:1mm 4mm;font-size:11pt;margin-right:2mm}}
.row{{display:flex;gap:7mm}}
.card{{background:#f4f6f9;border-radius:4mm;padding:5mm 6mm}}
.card h3{{font-size:14pt;color:{NAVY};margin-bottom:2mm}}
ol.st{{list-style:none;counter-reset:s}}
ol.st li{{counter-increment:s;font-size:13pt;line-height:1.55;margin-bottom:2.5mm;padding-left:10mm;position:relative}}
ol.st li:before{{content:counter(s);position:absolute;left:0;top:.5mm;width:7mm;height:7mm;border-radius:50%;background:{NAVY};color:#fff;font-size:11pt;text-align:center;line-height:7mm}}
p,li{{font-size:12pt;line-height:1.6}}
.up{{border-left:2mm solid {ACC};padding:2mm 4mm;background:#fafbe9;margin-top:3mm}}
.memo{{border:.6mm dashed #b54708;border-radius:3mm;padding:3mm 5mm;background:#fff8f1;margin-top:4mm}}
.memo b.t{{color:#b54708}}
.memo li{{font-size:11pt;line-height:1.5}}
.n{{position:absolute;right:10mm;bottom:6mm;font-size:9pt;color:#5a6476}}
.foot{{position:absolute;left:14mm;bottom:6mm;font-size:9pt;color:#5a6476}}
table{{border-collapse:collapse;width:100%}}
td,th{{border-bottom:.3mm solid #d9dee7;padding:2.5mm 3mm;font-size:12pt;text-align:left}}
th{{background:{NAVY};color:#fff;font-size:11pt}}
svg text{{font-family:"IPAPGothic","IPAGothic",sans-serif}}
"""

def page(kicker, h1, meta, fig, steps, up, link, memo, n, show_memo):
    st = "".join(f"<li>{s}</li>" for s in steps)
    mt = "".join(f"<span>{m}</span>" for m in meta)
    mm = ""
    if show_memo:
        mm = '<div class="memo"><b class="t">進行メモ（〇〇用）</b><ul style="padding-left:1.2em">' + "".join(f"<li>{x}</li>" for x in memo) + "</ul></div>"
    return f'''<section class="p"><p class="k">{kicker}</p><h1>{h1}</h1><div class="meta">{mt}</div>
<div class="row" style="margin-top:5mm"><div style="width:115mm">{fig}</div>
<div style="flex:1"><div class="card"><h3>やり方</h3><ol class="st">{st}</ol>
<div class="up"><b>レベルアップ：</b>{up}</div></div>
<p style="margin-top:3mm"><b>競技につながるところ：</b>{link}</p>{mm}</div></div>
<span class="n">{n}</span></section>'''

# 図
fig1 = f'''<svg width="430" height="430" viewBox="0 0 430 430">
<rect width="430" height="430" rx="16" fill="#f4f6f9"/>
<circle cx="215" cy="80" r="34" fill="{NAVY}"/>
<line x1="215" y1="114" x2="215" y2="250" stroke="{NAVY}" stroke-width="14" stroke-linecap="round"/>
<path d="M215 140 L140 220 L180 290" stroke="{NAVY}" stroke-width="12" fill="none" stroke-linecap="round"/>
<path d="M215 140 L290 210 L250 280" stroke="#9aa6b8" stroke-width="12" fill="none" stroke-linecap="round"/>
<path d="M215 250 L170 330 L170 400" stroke="{NAVY}" stroke-width="13" fill="none" stroke-linecap="round"/>
<path d="M215 250 L255 300 L190 300" stroke="#9aa6b8" stroke-width="13" fill="none" stroke-linecap="round"/>
<circle cx="190" cy="300" r="14" fill="{ACC}"/>
<rect x="290" y="40" width="120" height="44" rx="22" fill="{ACC}"/><text x="350" y="70" font-size="22" text-anchor="middle" fill="{NAVY}">「1、2…」</text>
<text x="215" y="424" font-size="17" text-anchor="middle" fill="#5a6476">右手で左ひざ（奇数）／左手で右ひざ（偶数）</text></svg>'''
fig2 = f'''<svg width="430" height="430" viewBox="0 0 430 430">
<rect width="430" height="430" rx="16" fill="#f4f6f9"/>
<path d="M110 300 Q215 60 320 300" stroke="#9aa6b8" stroke-width="4" stroke-dasharray="10 8" fill="none"/>
<circle cx="215" cy="150" r="26" fill="{ACC}"/><path d="M196 138 Q215 150 196 164 M234 136 Q215 150 234 163" stroke="{NAVY}" stroke-width="3" fill="none"/>
<ellipse cx="105" cy="320" rx="40" ry="22" fill="{NAVY}"/><ellipse cx="325" cy="320" rx="40" ry="22" fill="{NAVY}"/>
<g font-size="20" font-weight="bold">
<rect x="20" y="30" width="120" height="44" rx="22" fill="#e5484d"/><text x="80" y="60" fill="#fff" text-anchor="middle">「赤」</text>
<text x="80" y="100" font-size="16" fill="#1d2433" text-anchor="middle">→ 1回手をたたく</text>
<rect x="290" y="30" width="120" height="44" rx="22" fill="#3b82f6"/><text x="350" y="60" fill="#fff" text-anchor="middle">「青」</text>
<text x="350" y="100" font-size="16" fill="#1d2433" text-anchor="middle">→ 上からつかむ</text></g>
<text x="215" y="400" font-size="17" text-anchor="middle" fill="#5a6476">ボールを左右の手で投げ渡しながら、コールに反応</text></svg>'''
fig3 = f'''<svg width="430" height="430" viewBox="0 0 430 430">
<rect width="430" height="430" rx="16" fill="#f4f6f9"/>
<path d="M215 380 L30 120 A280 280 0 0 1 400 120 Z" fill="{ACC}" fill-opacity=".35"/>
<circle cx="215" cy="380" r="22" fill="{NAVY}"/>
<circle cx="215" cy="150" r="40" fill="#fff" stroke="{NAVY}" stroke-width="4"/><circle cx="215" cy="150" r="7" fill="#e5484d"/>
<text x="215" y="215" font-size="16" text-anchor="middle" fill="{NAVY}">ここ（鼻）だけを見る</text>
<g fill="{NAVY}"><rect x="55" y="120" width="12" height="46" rx="6"/><rect x="72" y="114" width="12" height="52" rx="6"/><rect x="89" y="120" width="12" height="46" rx="6"/></g>
<g fill="{NAVY}"><rect x="340" y="120" width="12" height="46" rx="6"/><rect x="357" y="114" width="12" height="52" rx="6"/></g>
<text x="78" y="196" font-size="22" text-anchor="middle" fill="{NAVY}">3</text><text x="355" y="196" font-size="22" text-anchor="middle" fill="{NAVY}">2</text>
<rect x="140" y="250" width="150" height="44" rx="22" fill="{NAVY}"/><text x="215" y="280" font-size="20" text-anchor="middle" fill="#fff">答え「5」</text>
<text x="215" y="420" font-size="17" text-anchor="middle" fill="#5a6476">目を動かさず、左右の指の合計を答える</text></svg>'''
beats = "".join(f'<rect x="{40+i*92}" y="150" width="78" height="78" rx="12" fill="{ACC if i==3 else NAVY}"/><text x="{79+i*92}" y="200" font-size="22" fill="{NAVY if i==3 else "#fff"}" text-anchor="middle">{t}</text>' for i,t in enumerate(["右","左","右","スプリット"]))
fig4 = f'''<svg width="430" height="430" viewBox="0 0 430 430">
<rect width="430" height="430" rx="16" fill="#f4f6f9"/>
<text x="215" y="70" font-size="24" text-anchor="middle" fill="{NAVY}" font-weight="bold">メトロノーム 100 → 120</text>
<text x="215" y="110" font-size="18" text-anchor="middle" fill="#5a6476">1拍に1回、足ぶみ</text>
{''.join(f'<rect x="{40+i*92}" y="150" width="78" height="78" rx="12" fill="{ACC if i==3 else NAVY}"/>' for i in range(4))}
{''.join(f'<text x="{79+i*92}" y="198" font-size="{16 if i==3 else 24}" fill="{NAVY if i==3 else "#fff"}" text-anchor="middle">{t}</text>' for i,t in enumerate(["右","左","右","両足"]))}
{''.join(f'<text x="{79+i*92}" y="260" font-size="18" fill="#5a6476" text-anchor="middle">{i+1}</text>' for i in range(4))}
<path d="M60 320 h310" stroke="#9aa6b8" stroke-width="3"/>
<text x="215" y="360" font-size="18" text-anchor="middle" fill="{NAVY}">コール「チェンジ」→ 4拍目を「左右どちらかへ1歩」に</text>
<text x="215" y="410" font-size="17" text-anchor="middle" fill="#5a6476">4拍目にスプリットステップ（両足で軽く着地）</text></svg>'''

ACTS = [
 dict(kicker="体験 ①　ライフキネティック（体だけ・道具なし）", h1="<em>クロス・タッチ</em>カウント",
      meta=["約3分", "道具なし", "立ったまま・スーツでもOK"], fig=fig1,
      steps=["「1、2、3…」と声に出して数を数える", "奇数のときは右手で左ひざ、偶数のときは左手で右ひざにタッチ", "慣れてきたら、3の倍数のときだけ「手をたたく」に変える"],
      up="数を逆から数える（20→1）／3の倍数を「4の倍数」に変える",
      link="声（言葉）と体の左右の動きを同時に処理する。ペアのコールを聞きながら動くプレーの土台。",
      memo=["最初に「間違えてOKです。間違えたときに脳が一番働いています」と伝える", "できるようになったら、すぐにルールを変える（慣れる前に変えるのがポイント）", "相手が笑ったら成功のサイン。笑いながら止まった瞬間が「情報の渋滞」の体験"]),
 dict(kicker="体験 ②　ライフキネティック（ボール1個）", h1="<em>カラー</em>・トス＆キャッチ",
      meta=["約4分", "テニスボール等1個", "1〜2m四方の場所"], fig=fig2,
      steps=["ボールを右手→左手→右手と、顔の高さで投げ渡す", "コーチが色をコール：「赤」→キャッチ前に1回手をたたく、「青」→上からつかむ", "コールがないときは、そのまま投げ渡しを続ける"],
      up="「赤」と「青」の意味を入れかえる／ボールを2個にする",
      link="ボールを目で追いながら、言葉の指示で動きを切りかえる。試合中に作戦や状況が変わったときの判断の速さ。",
      memo=["色はリズムを崩すタイミングで不規則に言う（2回続けて同じ色も入れる）", "ルールを入れかえた直後のミスを一緒に楽しむ", "ボールが落ちても拾ってすぐ再開。止めない"]),
 dict(kicker="体験 ③　ライフキネティック（視野）", h1="<em>周辺視</em>フィンガー",
      meta=["約3分", "道具なし", "向かい合って1.5mほど"], fig=fig3,
      steps=["体験する人は、コーチの鼻だけを見る（目を動かさない）", "コーチが顔の横あたりで、左右の手の指を何本か出す", "左右の指の本数を足して、答えを声に出す"],
      up="指を出す位置を外側に広げる／答えるときに片足立ちになる",
      link="正面のボールを見たまま、横の相手や味方を感じとる力。ソフトテニスなら前衛の動き、サッカーなら首振り（スキャン）に近い。",
      memo=["目が指の方に動いたら「今、目が動きました」とやさしく伝える", "最初は顔の近く→少しずつ外側へ", "体験後に「試合では、これを動きながらやっています」と一言そえる"]),
 dict(kicker="体験 ④　スポーツリズムトレーニング", h1="<em>リズム</em>・スプリットステップ",
      meta=["約3分", "メトロノームアプリ（スマホ）", "その場で足ぶみ"], fig=fig4,
      steps=["メトロノームを100にして、1拍に1回、右・左・右と足ぶみ", "4拍目に両足で軽く着地（スプリットステップ）", "コーチの「チェンジ」の合図で、4拍目を左右どちらかへの1歩に変える"],
      up="テンポを120に上げる／4拍目の方向を色のコールで決める",
      link="動き出しのタイミング（間）をそろえる。ソフトテニスのスプリットステップ、サッカーの裏への抜け出しのタイミング。",
      memo=["最初の30秒は音に合わせるだけ。ずれていても指摘しない", "テンポを上げた瞬間に足が合わなくなる → 「これが試合の緊張で起きること」とつなげる", "最後は「12週間で、ここを数字で見ていきます」と提案資料の測定ページへつなぐ"]),
]

def build(show_memo):
    flow_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a,b,c in [
        ("1分","はじめに","「間違えてOKの体験です」と伝える"),
        ("3分","① クロス・タッチ カウント","声と体の左右を同時に"),
        ("4分","② カラー・トス＆キャッチ","ボール＋言葉の指示"),
        ("3分","③ 周辺視フィンガー","見ないで感じとる"),
        ("3分","④ リズム・スプリットステップ","動き出しの間"),
        ("1分","ふりかえり","どこで「頭が渋滞」したかを聞く")])
    memo = ('<div class="memo" style="margin-top:4mm"><b class="t">進行メモ（〇〇用）</b><ul style="padding-left:1.2em">'
            '<li>相手の服装・場所に合わせて、①③は必ず実施、②④は場所があれば実施（最短6分）</li>'
            '<li>体験のあとは「どこで頭が渋滞しましたか？」と聞き、その答えを提案資料の「しくみ」のページにつなげる</li>'
            '<li>相手がやる気になったら、最後に「生徒さんでも試してみませんか」と無料トライアルの話へ</li></ul></div>') if show_memo else ""
    cover = f'''<section class="p" style="background:{NAVY};color:#fff">
<p class="k" style="color:{ACC};margin-top:14mm">体験メニュー</p>
<h1 style="color:#fff;font-size:34pt">15分でわかる<br>「脳 × 感覚 × リズム」トレーニング</h1>
<p style="font-size:14pt">ライフキネティックの考え方による体験3つ ＋ スポーツリズムトレーニング1つ</p>
<div class="row" style="margin-top:10mm">{"".join(f'<div style="flex:1;background:#16305a;border-radius:4mm;padding:5mm"><p style="color:{ACC};font-size:11pt">{a["kicker"].split("　")[0]}</p><p style="font-size:15pt;font-weight:bold">{a["h1"].replace("<em>","").replace("</em>","")}</p><p style="font-size:10.5pt;color:#c7d2e3">{a["meta"][0]}・{a["meta"][1]}</p></div>' for a in ACTS)}</div>
<p style="position:absolute;left:14mm;bottom:12mm;font-size:12pt;color:#c7d2e3">フォロワーシップコーチ　〇〇 〇〇　｜　できなくてOK。できないときに、脳がいちばん働いています。</p></section>'''
    flow = f'''<section class="p"><p class="k">進め方</p><h1>体験の流れ（<em>約15分</em>）</h1>
<table><tr><th style="width:14%">時間</th><th style="width:38%">内容</th><th>ねらい</th></tr>{flow_rows}</table>
<div class="row" style="margin-top:5mm"><div class="card" style="flex:1"><h3>大事なルールは1つだけ</h3><p>間違えてOK。むしろ「頭が追いつかない」「体が止まる」瞬間が、このトレーニングの中心です。できるようになったら、すぐにルールを変えます。</p></div>
<div class="card" style="flex:1"><h3>安全のために</h3><p>周りに1〜2mの空間をとってください。足ぶみは軽く。体調がすぐれないときは見学だけでも大丈夫です。</p></div></div>{memo}<span class="n">2</span></section>'''
    pages = [cover, flow] + [page(**a, n=i+3, show_memo=show_memo) for i, a in enumerate(ACTS)]
    end = f'''<section class="p"><p class="k">体験してみて</p><h1>「頭が渋滞した」瞬間は<em>どこ</em>でしたか？</h1>
<div class="row"><div class="card" style="flex:1"><h3>ふりかえり</h3><p>□ 数とタッチ（①）　□ 色のコール（②）　□ 周辺視（③）　□ テンポの変化（④）</p><p style="margin-top:3mm">いちばん難しかったところ：<br><span style="display:inline-block;width:100%;border-bottom:.3mm solid #9aa6b8;height:9mm"></span></p></div>
<div class="card" style="flex:1"><h3>選手で行うときは</h3><p>この体験を、ラケット・ボールを使った競技の形にして、1回20〜30分で行います。開始時・6週・12週に反応時間やアジリティなどを測り、変化を数字でお伝えします。</p></div></div>
<p style="margin-top:8mm;font-size:14pt"><b>まずは無料トライアル（6週）で、選手の反応と数字を見てください。</b></p>
<p class="foot">※体験メニューは、ライフキネティックとスポーツリズムトレーニングの考え方にもとづいて構成した入門用の内容です。</p><span class="n">7</span></section>'''
    pages.append(end)
    return f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>体験メニュー</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'

base = os.path.join(os.path.dirname(__file__), "..")
open(os.path.join(base, "体験メニュー_見せる用.html"), "w", encoding="utf-8").write(build(False))
open(os.path.join(base, "体験メニュー_進行メモ付き.html"), "w", encoding="utf-8").write(build(True))
print("ok")
