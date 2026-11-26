import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import *
ACC, ACCD = "#c8e63c", "#6f8c00"
S = []

# 1 表紙：コートと神経ネットワークの図
net = "".join(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#c8e63c" stroke-opacity=".55" stroke-width="2"/>' for x1,y1,x2,y2 in
  [(820,140,980,260),(980,260,1120,170),(980,260,1040,420),(1040,420,880,470),(880,470,820,140),(1040,420,1200,520),(1120,170,1200,330),(1200,330,1040,420),(880,470,960,600),(960,600,1200,520)])
dots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#c8e63c"/>' for x,y,r in [(820,140,9),(980,260,14),(1120,170,8),(1040,420,12),(880,470,9),(1200,520,8),(1200,330,10),(960,600,7)])
S.append(f'''<section class="s dark">
<svg style="position:absolute;left:0;top:0" width="1280" height="720">
 <polygon points="700,720 1280,720 1280,360 960,360" fill="#16305a"/>
 <line x1="960" y1="360" x2="700" y2="720" stroke="#fff" stroke-opacity=".35" stroke-width="3"/>
 <line x1="1120" y1="360" x2="1100" y2="720" stroke="#fff" stroke-opacity=".35" stroke-width="3"/>
 <line x1="880" y1="470" x2="1280" y2="470" stroke="#fff" stroke-opacity=".6" stroke-width="5"/>
 {net}{dots}
 <circle cx="1060" cy="300" r="40" fill="#c8e63c"/><path d="M1028 280 Q1060 300 1028 325 M1092 275 Q1060 300 1092 322" stroke="#0f2340" stroke-width="3" fill="none"/>
</svg>
<div style="position:relative;margin-top:96px;max-width:720px">
 <p class="k" style="color:#c8e63c">ソフトテニス部 指導者の方へ ／ ご提案資料</p>
 <h1 style="font-size:58px;margin-top:16px">勝負の<span style="color:#c8e63c">0.39秒</span>を<br>鍛えるトレーニング</h1>
 <p style="font-size:25px">脳 × 感覚 × リズム ― 最強のNo.2「フォロワーシップコーチ」</p>
</div>
<p style="position:absolute;left:72px;bottom:56px;font-size:19px;color:#c7d2e3">2026年12月19日　｜　フォロワーシップコーチ　〇〇 〇〇</p>
</section>''')

# 2 0.39秒のタイムライン
tl = '''<svg width="1136" height="250" viewBox="0 0 1136 250">
 <rect x="20" y="110" width="1080" height="34" rx="17" fill="#e6eaf0"/>
 <rect x="20" y="110" width="1080" height="34" rx="17" fill="url(#g)"/>
 <defs><linearGradient id="g"><stop offset="0" stop-color="#c8e63c" stop-opacity=".25"/><stop offset="1" stop-color="#0f2340"/></linearGradient></defs>
 <g font-size="18" fill="#1d2433">
  <line x1="20" y1="90" x2="20" y2="160" stroke="#0f2340" stroke-width="3"/><text x="20" y="80">相手が打つ</text>
  <line x1="657" y1="90" x2="657" y2="170" stroke="#0f2340" stroke-width="3"/><text x="657" y="80" text-anchor="middle">約0.23秒</text><text x="657" y="196" text-anchor="middle" font-size="16" fill="#5a6476">筋肉が反応</text>
  <line x1="740" y1="150" x2="740" y2="230" stroke="#0f2340" stroke-width="3"/><text x="740" y="222" text-anchor="start" dx="8" font-size="16" fill="#5a6476">約0.26秒 関節が動き出す</text>
  <line x1="1100" y1="90" x2="1100" y2="170" stroke="#0f2340" stroke-width="3"/><text x="1100" y="80" text-anchor="end" font-weight="bold" font-size="22">約0.39秒 インパクト</text>
 </g></svg>'''
S.append(slide(2, "前衛の現実", "考えてから動いたら、<em>もう間に合わない</em>",
 f'''<div class="row" style="align-items:center;margin-bottom:6px"><div class="stat">0.39<small>秒</small></div>
 <p style="font-size:22px">ソフトテニスのボレー動作を計測した研究では、反応からインパクトまで約0.39秒。<br>この一瞬の「見る→判断→動く」が勝敗を分けます。</p></div>{tl}''',
 "出典：畠山（北翔大学）ソフトテニスのスキル分析に関する論文。値は同論文の計測例。同論文は、ボールがネットを通過するまでの時間の方が反応より短い場面があることも示しています。"))

# 3 練習と試合の情報量
def burst(cx, items, big):
    center = f'<circle cx="{cx}" cy="190" r="{70 if big else 54}" fill="{"#0f2340" if big else "#9aa6b8"}"/><text x="{cx}" y="198" font-size="24" fill="#fff" text-anchor="middle" font-weight="bold">{"試合" if big else "練習"}</text>'
    out = ""
    import math
    for i, t in enumerate(items):
        a = -math.pi/2 + 2*math.pi*i/len(items)
        x, y = cx + 165*math.cos(a), 190 + 140*math.sin(a)
        out += f'<line x1="{cx}" y1="190" x2="{x}" y2="{y}" stroke="{"#c8e63c" if big else "#c3cad6"}" stroke-width="{4 if big else 2}"/>'
        out += f'<rect x="{x-62}" y="{y-20}" width="124" height="38" rx="19" fill="{"#c8e63c" if big else "#eef1f5"}"/><text x="{x}" y="{y+6}" font-size="16" text-anchor="middle" fill="#0f2340">{t}</text>'
    return out + center
S.append(slide(3, "なぜ試合で崩れるのか", "試合では、<em>情報が一度に押し寄せる</em>",
 f'''<svg width="1136" height="390" viewBox="0 0 1136 390">{burst(250, ["ボール","球出し"], False)}{burst(840, ["相手前衛","相手後衛","ボール","ペアの声","スコア","応援・緊張","風・日差し","監督の指示"], True)}
 <text x="545" y="200" font-size="46" fill="#6f8c00" text-anchor="middle">→</text></svg>''',
 "技術の差が小さい県上位レベルほど、最後は「多すぎる情報の中で判断を崩さない力」で差がつきます。"))

# 4 No.2
ic = lambda d: f'<svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="#c8e63c"/>{d}</svg>'
S.append(slide(4, "私の立ち位置", "主役は監督と選手。私は<em>最強のNo.2</em>",
 f'''<div class="row">
 <div class="card" style="flex:1">{ic('<path d="M18 34l9 9 19-21" stroke="#0f2340" stroke-width="6" fill="none"/>')}<h3 style="margin-top:12px">方針は変えない</h3><p>戦術・技術指導には口を出しません。監督の目標から逆算して土台づくりだけを担当。</p></div>
 <div class="card" style="flex:1">{ic('<circle cx="32" cy="32" r="16" stroke="#0f2340" stroke-width="5" fill="none"/><path d="M32 22v10l7 5" stroke="#0f2340" stroke-width="5" fill="none"/>')}<h3 style="margin-top:12px">練習時間を奪わない</h3><p>1回20〜30分。ウォームアップ枠や冬季の補強枠で、ラケットとボールを使って実施。</p></div>
 <div class="card" style="flex:1">{ic('<rect x="16" y="34" width="8" height="14" fill="#0f2340"/><rect x="28" y="24" width="8" height="24" fill="#0f2340"/><rect x="40" y="16" width="8" height="32" fill="#0f2340"/>')}<h3 style="margin-top:12px">数字で報告する</h3><p>開始時・6週・12週に測定してレポート。続けるかは監督が数字で判断できます。</p></div>
 </div><p style="margin-top:26px;font-size:22px">目標：<b>インターハイを本気で目指す選手の「判断の土台」を引き上げる</b></p>'''))

# 5 しくみ（サイクル図）
cyc = '''<svg width="560" height="400" viewBox="0 0 560 400">
<circle cx="280" cy="200" r="140" fill="none" stroke="#e1e5ec" stroke-width="28"/>
<path d="M280 60 A140 140 0 1 1 140 200" fill="none" stroke="#c8e63c" stroke-width="28"/>
<g font-size="19" font-weight="bold" fill="#0f2340" text-anchor="middle">
<rect x="195" y="22" width="170" height="54" rx="27" fill="#0f2340"/><text x="280" y="56" fill="#fff">① 同時に刺激</text>
<rect x="395" y="173" width="160" height="54" rx="27" fill="#0f2340"/><text x="475" y="207" fill="#fff">② 混乱・渋滞</text>
<rect x="195" y="324" width="170" height="54" rx="27" fill="#0f2340"/><text x="280" y="358" fill="#fff">③ 適応する</text>
<rect x="5" y="173" width="160" height="54" rx="27" fill="#c8e63c"/><text x="85" y="207">④ 課題を変える</text>
<text x="280" y="196" font-size="24">慣れる前に</text><text x="280" y="228" font-size="24">次の課題へ</text></g></svg>'''
S.append(slide(5, "トレーニングのしくみ", "わざと<em>「処理が追いつかない」</em>状態をつくる",
 f'''<div class="row" style="align-items:center">{cyc}<div style="flex:1">
 <div class="card" style="margin-bottom:14px"><h3>① ライフキネティック</h3><p>視覚・認知・協調運動の課題を同時に。色や数字のコール、2色ボール、利き手と逆の操作を組み合わせる。</p></div>
 <div class="card"><h3>② スポーツリズムトレーニング</h3><p>拍に合わせて身体を動かし、スプリットステップや動き出しの「間」をそろえる。</p></div></div></div>''',
 "脳の中で起きている変化（神経のつながり等）は研究途上です。本提案では、測定できる「反応・判断・動き」の変化で効果を確認します。"))

# 6 フェンシングRCT
ch = prepost([("ストループ課題（秒）", [("LK群", 26.83, 24.49, True), ("対照群", 26.81, 26.67, False)])], w=500, h=420, ymax=30)
ch2 = prepost([("アジリティ（秒）", [("LK群", 15.48, 13.73, True)])], w=260, h=420, ymax=18)
S.append(slide(6, "エビデンス ①　ライフキネティック × 競技者（ランダム化比較試験）", "8週間で、<em>判断もフットワークも速くなった</em>",
 f'''<div class="row" style="align-items:flex-end">{ch}{ch2}
 <div style="flex:1;padding-bottom:30px"><div class="stat">−11<small>%</small></div><p class="lbl">アジリティテストのタイム<br>（15.48秒 → 13.73秒）</p>
 <div class="stat" style="margin-top:20px;font-size:64px">p&lt;0.001</div><p class="lbl">LK群はストループ・アジリティ・垂直跳びが向上。<br>対照群は有意な変化なし</p></div></div>''',
 "Yarayan ほか（2025）BMC Sports Science, Medicine and Rehabilitation。フェンシング競技者22名（平均11.6歳）、週2回×60分×8週。グラフの数値はプレプリント版（Research Square）の表の値で、最終版と異なる可能性があります。タイムは短いほど良い。"))

# 7 バドミントン
S.append(slide(7, "エビデンス ②　ライフキネティック × ラケット競技", "バドミントンで<em>サービスの成績</em>まで向上",
 f'''<div class="row" style="align-items:center">
 <div style="width:380px"><div class="stat">6<small>週・18回</small></div><p class="lbl">通常練習にライフキネティックを追加<br>選手40名（ジュニア・中級）をランダムに割り付け</p>
 <div style="margin-top:22px"><span class="tag a">集中力</span><span class="tag a">作業記憶</span><br><span class="tag a" style="margin-top:8px">ショートサービス</span><span class="tag a" style="margin-top:8px">ロングサービス</span></div>
 <p class="lbl" style="margin-top:10px">すべて有意に向上（p&lt;0.001）</p></div>
 <div style="flex:1"><p style="font-size:19px;margin-bottom:6px"><b>効果の大きさ（偏η²）</b>　線＝「大きい効果」の目安 0.14</p>
 {meter("集中力（グリッド課題）", 0.80, 1.0, 0.14, "大きい効果の目安", 640, ACC)}
 {meter("作業記憶（数字の記憶）", 0.82, 1.0, 0.14, "大きい効果の目安", 640, ACC)}
 <div class="honest" style="margin-top:14px">ラケット競技で「競技動作そのもの」の改善が報告された点が、ソフトテニスに応用する根拠です。</div></div></div>''',
 "Life Kinetics Training as a Multimodal Neurocognitive Intervention…（Life, 16(5), 836, 2026）。偏η²の0.14は一般的な「大」の目安。ソフトテニス・高校生を対象にした研究はまだないため、貴校での測定で確かめながら進めます。"))

# 8 メタ分析
S.append(slide(8, "エビデンス ③　22研究のメタ分析", "効果はある。だから<em>コートでやる</em>",
 f'''<div class="row" style="align-items:center">{effect_bars([("実験室のテスト", 1.51, False), ("コート上の実戦", 0.65, True)], 680, 280, 1.8, ACC)}
 <div style="flex:1"><div class="card" style="margin-bottom:14px"><h3>読み取れること</h3><p>知覚・認知トレーニングで予測・判断は改善。コート上でも「中程度以上」の効果。ただし実験室ほどは移らない。</p></div>
 <div class="card"><h3>本プログラムの設計</h3><p>机やタブレットの脳トレではなく、<b>ラケット・ボール・ペアの声・フットワーク</b>を必ず入れる競技特化型。</p></div></div></div>''',
 "Zhu ほか（2024）Behavioral Sciences 14(10):919（団体競技の22研究・45の効果量）。数値は効果量。一般的な脳トレの競技への転移には否定的な見解もあります（Fransen, 2024, Sports Medicine）。"))

# 9 リズム
S.append(slide(9, "エビデンス ④　リズム・タイミング", "タイミングが正確な選手ほど、<em>ステップが正確</em>",
 f'''<div class="row">
 <div class="card" style="flex:1.1"><h3>エリート女子サッカー選手24名</h3>
 {meter("タイミング能力と正確なステップ数の相関（|r|）", 0.59, 1.0, 0.5, "強い相関の目安 0.5", 560, ACC)}
 <p style="margin-top:8px">メトロノーム同期トレーニング（4週・12回）を行った群だけ、ステップ課題の正確さと速さが向上。</p></div>
 <div style="flex:1;display:flex;flex-direction:column;gap:16px">
 <div class="card"><h3>リズムジャンプ（小学生サッカー）</h3><p>週1回×8週で、8拍のリズム再現能力とアジリティが向上。</p></div>
 <div class="card"><h3>横浜市の全公立小学校</h3><p>スポーツリズムトレーニングを普及し、運動能力向上とけが予防の効果を評価。</p></div></div></div>''',
 "Rönnqvist ほか（2018）Frontiers in Psychology 9:2469（相関は事後テストで r = −0.588、反応のずれが小さいほど正確なステップが多い）。リズムジャンプ研究：Children（2025）。横浜市：津田ほか（CiNii）。競技者を対象にしたリズム研究はまだ少数です。"))

# 10 メニュー（コート図）
court = '''<svg width="500" height="400" viewBox="0 0 500 400">
<rect x="40" y="20" width="420" height="360" fill="#2c6e49" rx="6"/>
<rect x="70" y="40" width="360" height="320" fill="none" stroke="#fff" stroke-width="3"/>
<line x1="70" y1="200" x2="430" y2="200" stroke="#fff" stroke-width="6"/>
<line x1="250" y1="110" x2="250" y2="290" stroke="#fff" stroke-width="3"/>
<line x1="70" y1="110" x2="430" y2="110" stroke="#fff" stroke-width="3"/><line x1="70" y1="290" x2="430" y2="290" stroke="#fff" stroke-width="3"/>
<circle cx="250" cy="70" r="16" fill="#fff"/><text x="250" y="76" font-size="15" text-anchor="middle" fill="#0f2340">C</text>
<circle cx="210" cy="240" r="18" fill="#c8e63c"/><text x="210" y="246" font-size="15" text-anchor="middle" fill="#0f2340">前</text>
<path d="M250 86 L214 220" stroke="#fff" stroke-dasharray="6 6" stroke-width="2"/>
<path d="M210 222 L110 130" stroke="#e5484d" stroke-width="4" marker-end="url(#a)"/><path d="M210 222 L330 130" stroke="#3b82f6" stroke-width="4" marker-end="url(#a)"/>
<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#fff"/></marker></defs>
<rect x="84" y="140" width="70" height="30" rx="15" fill="#e5484d"/><text x="119" y="161" font-size="15" text-anchor="middle" fill="#fff">赤＝右</text>
<rect x="320" y="140" width="70" height="30" rx="15" fill="#3b82f6"/><text x="355" y="161" font-size="15" text-anchor="middle" fill="#fff">青＝左</text>
<text x="250" y="396" font-size="15" text-anchor="middle" fill="#5a6476">例：色コールでボレーの方向を切り替える（途中でルールを逆に）</text></svg>'''
S.append(slide(10, "ソフトテニス版メニュー（例）", "コートで、<em>ラケットを持って</em>行う",
 f'''<div class="row">{court}<div style="flex:1"><table>
 <tr><th>ねらい</th><th>メニュー例</th></tr>
 <tr><td>判断の切り替え</td><td>色コール→ボレーの方向を変える。慣れたらルールを逆にする</td></tr>
 <tr><td>周辺視</td><td>ボールを見たまま、横で示す指の本数を答えながらラリー</td></tr>
 <tr><td>動き出しの「間」</td><td>拍に合わせたスプリットステップ→不規則な拍へ</td></tr>
 <tr><td>情報の渋滞</td><td>2色ボール＋数字コール＋ステップを同時に。できたら1つ変える</td></tr>
 <tr><td>ペアの連携</td><td>交互のコールとリズムでフットワークをそろえる</td></tr></table></div></div>''',
 "1回20〜30分。監督の練習計画に合わせて組み込みます。"))

# 11 レポート見本（空欄）
def blank_chart(title):
    bars = "".join(f'<rect x="{40+i*70}" y="40" width="44" height="130" rx="4" fill="none" stroke="#9aa6b8" stroke-dasharray="5 5"/><text x="{62+i*70}" y="192" font-size="13" text-anchor="middle" fill="#5a6476">{t}</text>' for i,t in enumerate(["開始","6週","12週"]))
    return f'<div class="card" style="padding:14px 16px"><p style="font-size:16px;font-weight:bold;color:#0f2340">{title}</p><svg width="250" height="200">{bars}<text x="125" y="115" font-size="14" text-anchor="middle" fill="#6f8c00">貴校の実測値</text></svg></div>'
S.append(slide(11, "結果へのコミット ＝ 測って、見せる", "12週後、このレポートを<em>数字で</em>お渡しします",
 f'''<div class="row" style="gap:16px">{blank_chart("選択反応時間")}{blank_chart("ストループ課題")}{blank_chart("アジリティ")}{blank_chart("ボレー・ポーチ成功率")}</div>
 <div class="row" style="margin-top:18px;gap:16px"><div class="honest" style="flex:1">測定：反応時間（アプリ）・ストループ・反復横跳び・リズム再現・練習試合のボレー成功率・緊張の自己評価</div>
 <div class="honest" style="flex:1">約束：測定と報告を必ず行う／伸びない項目はメニューを組み替える／個人データは学校外に出さない</div></div>''',
 "レポートの見本（枠のみ）です。数値は実施後の実測値のみを記入します。勝敗・大会成績を保証するものではなく、土台となる能力の変化を数字で示すことにコミットします。"))

# 12 スケジュール
S.append(slide(12, "導入スケジュール", "冬は<em>無料</em>で確かめ、4月から本格導入",
 timeline([("12月〜1月","無料","体験セッション<br>初回測定・メニュー設計",False),("1月〜3月","無料","トライアル6週<br>中間測定・結果のご報告",False),
           ("4月","契約開始","導入をご判断<br>ここから料金発生",False),("5月〜7月","","6週・12週で測定<br>大会前は短時間の調整",False),("夏","","インターハイ・<br>上位大会へ",True)], ACC)
 + '<p style="margin-top:28px">トライアルの数字を見てから決められます。<b>導入しない場合、費用は一切かかりません。</b></p>'))

# 13 料金（控えめ）
S.append(slide(13, "導入プラン（案）", "2027年4月からのプラン",
 '''<table style="margin-top:6px"><tr><th>プラン</th><th>内容</th><th style="width:22%">料金（税込・交通費別）</th></tr>
 <tr><td><b>ライト</b></td><td>月2回訪問（各90分）・測定3回・レポート</td><td>月額 30,000円</td></tr>
 <tr><td><b>スタンダード</b></td><td>月4回訪問（各90分）・測定3回・レポート・自主練メニュー</td><td>月額 55,000円</td></tr>
 <tr><td><b>年間サポート</b></td><td>スタンダード×12か月・大会前の個別調整</td><td>年額 580,000円</td></tr></table>
 <p style="margin-top:22px">12月〜3月の<b>無料トライアル6週＋初回・中間測定</b>の結果を見てからお選びいただけます。</p>''',
 "金額は案です。支払い元（後援会・保護者会など）、訪問距離、人数に応じて調整します。"))

# 14 参考文献
S.append(slide(14, "参考文献", "本資料で引用した研究",
 '''<ol class="ref" style="padding-left:1.4em">
 <li>Yarayan ほか. Impact of life kinetik training on balance, agility, jumping, proprioception, and cognitive function in preadolescent recreational fencing athletes: a randomized controlled trial. BMC Sports Sci Med Rehabil, 17, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12145597/（グラフの値はプレプリント https://www.researchsquare.com/article/rs-5463104/v1）</li>
 <li>Life Kinetics Training as a Multimodal Neurocognitive Intervention: Enhances Cognitive and Motor Performance in Badminton Athletes. Life, 16(5), 836, 2026. https://doi.org/10.3390/life16050836</li>
 <li>Zhu ほか. Effects of Perceptual-Cognitive Training on Anticipation and Decision-Making Skills in Team Sports: A Systematic Review and Meta-Analysis. Behavioral Sciences, 14(10), 919, 2024. https://www.mdpi.com/2076-328X/14/10/919</li>
 <li>Fransen. There is No Supporting Evidence for a Far Transfer of General Perceptual or Cognitive Training to Sports Performance. Sports Medicine, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11560981/</li>
 <li>Rönnqvist ほか. Influences of Synchronized Metronome Training on Soccer Players' Timing Ability, Performance Accuracy, and Lower-Limb Kinematics. Frontiers in Psychology, 9, 2469, 2018. https://www.frontiersin.org/articles/10.3389/fpsyg.2018.02469/full</li>
 <li>The Effects of Rhythm Jump Training on the Rhythmic Reproduction Ability in Jumping and Agility in Elementary School Soccer Players. Children, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC11854900/</li>
 <li>津田幸保ほか. 横浜市の全公立小学校におけるスポーツリズムトレーニング普及の取り組みに関する報告（正式題名は原典で確認）. https://cir.nii.ac.jp/crid/1390851398293246336</li>
 <li>畠山. ソフトテニスのスキル分析に関する論文（正式題名は原典で確認）. 北翔大学. https://hokusho.repo.nii.ac.jp/record/1635/files/JHWC30115.pdf</li></ol>'''))

# 15 クロージング
S.append(f'''<section class="s dark"><svg style="position:absolute;left:0;top:0" width="1280" height="720">{net}{dots}</svg>
<div style="position:relative;margin-top:150px;max-width:700px"><p class="k" style="color:#c8e63c">次の一歩</p>
<h1 style="font-size:50px">まずは無料トライアルで、<br>選手の反応と数字を見てください</h1>
<p style="font-size:22px">体験セッション → 6週トライアル → 中間測定</p>
<p style="margin-top:36px;font-size:19px;color:#c7d2e3">フォロワーシップコーチ　〇〇 〇〇<br>連絡先：〇〇〇〇（メール／電話）</p></div></section>''')

out = os.path.join(os.path.dirname(__file__), "..", "提案資料_ソフトテニス.html")
open(out, "w", encoding="utf-8").write(page("フォロワーシップコーチ提案", ACC, ACCD, S))
print("written", len(S))
