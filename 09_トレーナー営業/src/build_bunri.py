"""ソフトテニス：下半身は速く・上半身は繊細に（上下分離）メニュー集。A4横。"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_taiken import CSS, ACC, NAVY  # 体験メニューと同じ見た目（import時に体験メニューも再生成）
RED = "#e5484d"

def body_fig(top_label, bottom_label, extra=""):
    """上：静かなラケット、下：忙しい足の模式図"""
    return f'''<svg width="430" height="430" viewBox="0 0 430 430"><rect width="430" height="430" rx="16" fill="#f4f6f9"/>
<rect x="10" y="10" width="410" height="200" rx="12" fill="#eef4ff"/><rect x="10" y="220" width="410" height="200" rx="12" fill="#fff1e6"/>
<text x="24" y="38" font-size="17" fill="{NAVY}" font-weight="bold">上半身：繊細に</text><text x="24" y="248" font-size="17" fill="{RED}" font-weight="bold">下半身：速く</text>
<circle cx="215" cy="70" r="22" fill="{NAVY}"/><line x1="215" y1="92" x2="215" y2="250" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/>
<path d="M215 120 L280 150" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>
<line x1="280" y1="150" x2="312" y2="132" stroke="#5a6476" stroke-width="5"/><ellipse cx="340" cy="118" rx="34" ry="22" fill="none" stroke="{NAVY}" stroke-width="5" transform="rotate(-25 340 118)"/>
<circle cx="340" cy="100" r="12" fill="{ACC}"/>
<path d="M215 250 L175 330 L150 400 M215 250 L255 330 L285 400" stroke="{NAVY}" stroke-width="11" fill="none" stroke-linecap="round"/>
<g stroke="{RED}" stroke-width="4" stroke-linecap="round"><path d="M110 370 h-30 M110 385 h-40 M110 400 h-30"/><path d="M320 370 h30 M320 385 h40 M320 400 h30"/></g>
<text x="215" y="196" font-size="15" text-anchor="middle" fill="{NAVY}" stroke="#eef4ff" stroke-width="6" paint-order="stroke">{top_label}</text>
<text x="215" y="412" font-size="15" text-anchor="middle" fill="{RED}" stroke="#fff1e6" stroke-width="6" paint-order="stroke">{bottom_label}</text>{extra}</svg>'''

def page(n, kicker, h1, meta, fig, steps, up, measure, coach):
    st = "".join(f"<li>{s}</li>" for s in steps)
    mt = "".join(f"<span>{m}</span>" for m in meta)
    co = "".join(f"<li>{c}</li>" for c in coach)
    return f'''<section class="p"><p class="k">{kicker}</p><h1>{h1}</h1><div class="meta">{mt}</div>
<div class="row" style="margin-top:4mm"><div style="width:115mm">{fig}</div><div style="flex:1">
<div class="card"><h3>やり方</h3><ol class="st">{st}</ol><div class="up"><b>レベルアップ：</b>{up}</div></div>
<p style="margin-top:2.5mm"><b>記録すること：</b>{measure}</p>
<div class="memo"><b class="t">指導のポイント</b><ul style="padding-left:1.2em">{co}</ul></div></div></div><span class="n">{n}</span></section>'''

P = []
# 1 表紙
P.append(f'''<section class="p" style="background:{NAVY};color:#fff">
<div style="position:absolute;right:14mm;top:22mm">{body_fig("ラケット面は静かに・ていねいに","足は細かく・速く・止めない")}</div>
<div style="max-width:140mm;margin-top:20mm"><p class="k" style="color:{ACC}">ソフトテニス専用メニュー集</p>
<h1 style="color:#fff;font-size:32pt">足は<span style="color:{RED}">速く</span>、<br>ラケットは<span style="color:{ACC}">繊細に</span></h1>
<p style="font-size:14pt">上半身と下半身を「別々に動かす力」を鍛える<br>ライフキネティック式トレーニング 6種</p>
<p style="font-size:11pt;color:#c7d2e3;margin-top:8mm">足が忙しくなるほど、手元も雑になる。<br>その「つられ」を切り離すことが、このメニューのねらいです。</p></div>
<p style="position:absolute;left:14mm;bottom:10mm;font-size:11pt;color:#c7d2e3">フォロワーシップコーチ　〇〇 〇〇</p></section>''')

# 2 考え方と測り方
P.append(f'''<section class="p"><p class="k">考え方</p><h1>鍛えるのは<em>「上下の分離」</em>：足の忙しさに、手元をつられさせない</h1>
<div class="row"><div class="card" style="flex:1"><h3>試合で起きていること</h3><p>前衛は細かいステップでポジションを変えながら、ボレーでは面の角度とタッチを数ミリ単位で合わせます。後衛も、走りながらのロビングやつなぎで同じことが起きます。<br><br>足を速く動かすと、腕や手首にも力が入り、<b>面がぶれる・強く当たりすぎる</b>。これが「足は速いのにミスが多い」選手の正体であることがあります。</p></div>
<div class="card" style="flex:1"><h3>このメニューの3つの原則</h3><ol style="padding-left:1.2em"><li><b>上と下に違う課題を同時に</b>：足はリズム・方向・速さ、手元は高さ・角度・力加減</li><li><b>慣れる前に変える</b>：できたら、足のリズムか手元の課題のどちらかを変える</li><li><b>止めない</b>：ミスしても足は動かし続け、手元だけやり直す</li></ol></div></div>
<div class="card" style="margin-top:4mm;border-left:2mm solid {ACC}"><h3>分離力の測り方（毎回1分）</h3>
<p>① 足を止めた状態で、ラケットでボールを低くつく（30秒の回数・落とした回数）<br>② 同じことを、細かいステップ（または指示どおりのステップ）をしながら行う<br><b>分離力 ＝ ②の成功数 ÷ ①の成功数</b>（100%に近いほど、足につられていない）。足の速さ（ステップ数）も一緒に記録します。</p></div>
<p style="margin-top:2mm;font-size:9.5pt;color:#5a6476">「分離力」は、二つの課題を同時に行ったときの成績の落ち方（二重課題コスト）を、現場で測れるようにした本プログラム独自の指標です。効果はデータで確かめていきます。</p><span class="n">2</span></section>''')

acts = [
 dict(kicker="メニュー①　基本", h1="<em>速足・静面</em>（ボール乗せステップ）",
  meta=["約3分", "ラケット・ボール1個", "1人／2m四方"],
  fig=body_fig("面の上のボールを動かさない", "その場で細かいステップ"),
  steps=["ラケット面にボールを1個乗せ、面を水平に保つ", "その場で細かく速いステップ（10秒）→ 5秒休む、をくり返す", "コーチのコールで足だけ変える：「前」「後」「右」「左」へ1歩出て戻る"],
  up="面をフォア面→バック面に持ちかえながら／ボールを2個乗せる／目を閉じて5秒",
  measure="10秒で落とした回数、ステップ数",
  coach=["手首とひじの力を抜き、「面を浮かせて持つ」感覚を言葉にさせる", "足が止まったら失敗、ボールが落ちても足は止めない", "最初の1分は成功させる。成功率60〜80%になるよう課題を変える"]),
 dict(kicker="メニュー②　リズム", h1="<em>3拍の足・2拍の手</em>（ポリリズム）",
  meta=["約4分", "ラケット・ボール・メトロノームアプリ", "1人"],
  fig=body_fig("2拍に1回、低くつく", "3拍で「右・左・両足」", '<text x="215" y="226" font-size="13" text-anchor="middle" fill="#5a6476">足 3 ： 手 2</text>'),
  steps=["メトロノーム（90前後）に合わせ、足は「右・左・両足」の3拍をくり返す", "手はボールを低くつく。ついている間隔は足とずらし、2拍に1回", "合ったら、コールで入れかえ：足が2拍、手が3拍"],
  up="テンポを100→110に／つく高さをコールで変える（「低く」＝目の高さより下、「高く」＝頭の上）",
  measure="30秒間の、足と手のリズムが両方合っていた回数",
  coach=["上と下のリズムが「勝手にそろってしまう」のが普通。ずらせたら大成功", "スポーツリズムトレーニングの拍の取り方と組み合わせる", "できない選手には、まず手だけ・足だけで拍を言わせてから合わせる"]),
 dict(kicker="メニュー③　二つの指示", h1="<em>ナンバーは足、カラーは面</em>",
  meta=["約4分", "ラケット・ボール・色カード（赤・青・黄）", "コーチ1人に選手2〜4人"],
  fig=body_fig("色で面：赤フォア／青バック／黄止める", "数字で足：1前 2後 3右 4左"),
  steps=["選手はボールを低くつきながら、その場で細かいステップ", "コーチが数字をコール → その方向へ1歩出て戻る（足の指示）", "コーチが色カードを見せる → 面を変えて1回つく（赤＝フォア面、青＝バック面、黄＝面の上でボールを止める）"],
  up="数字と色を同時に出す／色の意味を途中で入れかえる／数字を足し算で出す（「1たす2」→3＝右）",
  measure="30秒で、足と面の両方が正しかった割合",
  coach=["数字は声（耳）、色はカード（目）。入ってくる感覚を分けるのがポイント", "「黄＝止める」は、ボールの勢いを吸収するタッチの練習。ドロップボレーにつながる", "ルールを入れかえた直後のミスは、脳が切りかえている証拠と伝える"]),
 dict(kicker="メニュー④　移動しながら", h1="<em>サイドステップ・ソフトキャッチ</em>",
  meta=["約4分", "ラケット・ボール・コーン2本（3m間）", "2人1組（球出し1人）"],
  fig=body_fig("面でボールを「止める」", "コーン間をサイドステップ"),
  steps=["選手は3mのコーン間を、サイドステップで往復し続ける", "球出しが軽くボールを投げる → ラケット面で受け、面の上でボールを止める（弾ませない）", "止めたら、ボールを球出しに軽く返し、すぐ往復を再開"],
  up="投げる高さ・速さを変える／止める前に、球出しがコールした色の面（フォア・バック）に変える／2球連続",
  measure="1分間の往復回数と、ボールを1回で止められた割合",
  coach=["足の速さを落として手元を合わせるのは失敗。往復のテンポは変えない", "ボールを「迎えに行く」と弾む。面を少し引いて吸収する感覚を言葉にさせる", "前衛のボレーの「当てるだけ・止めるだけ」の感覚につながる"]),
 dict(kicker="メニュー⑤　ネット前（段階2）", h1="<em>反応ステップ・タッチボレー</em>",
  meta=["約5分", "コート・コーン・的（フラフープ等）", "前衛／球出し1人"],
  fig=body_fig("小さな的へ、やわらかいタッチ", "合図でクロスステップ→スプリット"),
  steps=["前衛はネット前で、細かいステップを続ける", "球出しが左右どちらかを指さす → その方向へ2歩動いてスプリットステップ", "球出しのボールを、サービスライン手前の的（フラフープ）に、やわらかいボレーで落とす"],
  up="指さしと逆に動く（ルールの入れかえ）／的を小さく、ネットに近く／ボレーの直前に色をコールして、的を変える",
  measure="10球中、的に入った数（足の動き出しが遅れた球は別に数える）",
  coach=["足は全力、手元は5割の力。「足と手の力の配分」を数字で言わせる", "強く当たって的を越えるミスは「足につられた」サイン", "映像で、ステップ中のラケットの位置がぶれていないかを確認する"]),
 dict(kicker="メニュー⑥　本番の条件（段階3）", h1="<em>ラストポイント・タッチ</em>",
  meta=["約5分", "コート・ボール・応援音声（スマホ）", "前衛・後衛"],
  fig=body_fig("最後の1本も、タッチは変えない", "ダッシュ直後・応援の中で"),
  steps=["ベースライン⇔サービスラインのダッシュを2往復した直後に開始", "応援の音声を流し、「この1本で決まる」設定で、メニュー⑤のタッチボレー（前衛）／短いつなぎ球（後衛）を行う", "1本ごとに、ペアが「足」「手元」のどちらが崩れたかを伝える"],
  up="ダッシュを3往復に／音声を大きく／ペアのコールを入れる（コールがないと打てないルール）",
  measure="ダッシュ・音声ありとなしの成功率の差（本番の落ち幅）",
  coach=["判断の7つの輪のL7（本番で崩れない）と、上下の分離を同時に鍛えるメニュー", "疲れたときこそ手元をていねいに。息が上がっているときの深呼吸1回を習慣に", "ここでの成功率の差が小さくなっていくことを、6週・12週で確認する"])]
for i, a in enumerate(acts):
    P.append(page(i + 3, **a))

# 9 組み合わせ
P.append(f'''<section class="p"><p class="k">組み合わせ方</p><h1>1回20〜25分：<em>段階1→2→3</em>の順に</h1>
<table><tr><th style="width:18%">時期</th><th style="width:34%">メニュー</th><th>ねらい</th></tr>
<tr><td>1〜2週</td><td>① 速足・静面 ＋ ② 3拍の足・2拍の手</td><td>上下を分ける感覚をつくる（コート外でも可）</td></tr>
<tr><td>3〜4週</td><td>③ ナンバーは足、カラーは面 ＋ ④ サイドステップ・ソフトキャッチ</td><td>指示が二つになっても、上下を分けたまま判断する</td></tr>
<tr><td>5〜8週</td><td>④ ＋ ⑤ 反応ステップ・タッチボレー</td><td>コートで、ボレーのタッチにつなげる</td></tr>
<tr><td>9〜12週</td><td>⑤ ＋ ⑥ ラストポイント・タッチ</td><td>疲労と緊張の中でも、手元を崩さない</td></tr></table>
<div class="row" style="margin-top:4mm"><div class="card" style="flex:1"><h3>毎回の流れ（例）</h3><p>分離力の測定1分 → 段階1を5分 → 段階2を10分 → 段階3を5分 → ふりかえり2分</p></div>
<div class="card" style="flex:1"><h3>安全のために</h3><p>ラケットを持って動くので、選手どうしの間隔を2m以上あける。床・コートが滑りやすい日は、ステップの速さを落とす。</p></div>
<div class="card" style="flex:1"><h3>判断の診断とのつながり</h3><p>主に L3（同時に感じる）・L6（間を合わせる）・L7（本番で崩れない）。分離力の記録は診断ツールのメモ欄に残しておく。</p></div></div>
<p style="margin-top:3mm;font-size:9.5pt;color:#5a6476">※ライフキネティックとスポーツリズムトレーニングの考え方にもとづいて、ソフトテニス用に構成したオリジナルのメニューです。</p><span class="n">9</span></section>''')

out = os.path.join(os.path.dirname(__file__), "..", "メニュー集_足は速くラケットは繊細に.html")
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>足は速く、ラケットは繊細に</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print(len(P))
