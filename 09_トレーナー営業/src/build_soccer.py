import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from common import *
ACC, ACCD = "#3ddc84", "#12804a"
S = []

net = "".join(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ACC}" stroke-opacity=".55" stroke-width="2"/>' for x1,y1,x2,y2 in
  [(820,140,980,260),(980,260,1120,170),(980,260,1040,420),(1040,420,880,470),(880,470,820,140),(1040,420,1200,520),(1120,170,1200,330),(1200,330,1040,420),(880,470,960,600),(960,600,1200,520)])
dots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{ACC}"/>' for x,y,r in [(820,140,9),(980,260,14),(1120,170,8),(1040,420,12),(880,470,9),(1200,520,8),(1200,330,10),(960,600,7)])

# 1 表紙：ピッチ＋首振りの視野
S.append(f'''<section class="s dark">
<svg style="position:absolute;left:0;top:0" width="1280" height="720">
 <rect x="700" y="0" width="580" height="720" fill="#14365e"/>
 <circle cx="990" cy="360" r="90" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="3"/>
 <line x1="700" y1="360" x2="1280" y2="360" stroke="#fff" stroke-opacity=".3" stroke-width="3"/>
 <path d="M990 360 L760 120 A330 330 0 0 1 1220 120 Z" fill="{ACC}" fill-opacity=".18"/>
 <path d="M990 360 L1260 230 A300 300 0 0 1 1260 560 Z" fill="{ACC}" fill-opacity=".12"/>
 {net}{dots}
 <circle cx="990" cy="360" r="22" fill="{ACC}"/><circle cx="1030" cy="400" r="12" fill="#fff"/>
</svg>
<div style="position:relative;margin-top:96px;max-width:700px">
 <p class="k" style="color:{ACC}">サッカー部 指導者の方へ ／ ご提案資料</p>
 <h1 style="font-size:56px;margin-top:16px">ボールが来る前に<br><span style="color:{ACC}">「見て・決める」</span>選手へ</h1>
 <p style="font-size:25px">脳 × 感覚 × リズム ― 最強のNo.2「フォロワーシップコーチ」</p>
</div>
<p style="position:absolute;left:72px;bottom:56px;font-size:19px;color:#c7d2e3">2026年12月　｜　フォロワーシップコーチ　〇〇 〇〇</p>
</section>''')

# 2 スキャン研究
pitch = f'''<svg width="520" height="380" viewBox="0 0 520 380">
<rect x="10" y="10" width="500" height="360" rx="8" fill="#2c6e49"/><rect x="30" y="30" width="460" height="320" fill="none" stroke="#fff" stroke-width="3"/>
<line x1="260" y1="30" x2="260" y2="350" stroke="#fff" stroke-width="3"/><circle cx="260" cy="190" r="50" fill="none" stroke="#fff" stroke-width="3"/>
<path d="M230 220 L80 80 A210 210 0 0 1 200 40 Z" fill="{ACC}" fill-opacity=".45"/>
<path d="M230 220 L420 120 A210 210 0 0 1 440 290 Z" fill="{ACC}" fill-opacity=".45"/>
<path d="M230 220 L150 350 A140 140 0 0 1 90 300 Z" fill="{ACC}" fill-opacity=".3"/>
<circle cx="230" cy="220" r="16" fill="#0f2340" stroke="#fff" stroke-width="3"/>
<circle cx="120" cy="90" r="11" fill="#e5484d"/><circle cx="400" cy="160" r="11" fill="#e5484d"/><circle cx="330" cy="260" r="11" fill="#3b82f6"/><circle cx="170" cy="60" r="11" fill="#3b82f6"/><circle cx="130" cy="320" r="11" fill="#e5484d"/>
<circle cx="250" cy="236" r="7" fill="#fff"/>
<text x="260" y="374" font-size="14" fill="#fff" text-anchor="middle">受ける前に首を振り、周りの状況を取り込む（スキャン）</text></svg>'''
S.append(slide(2, "サッカーは「見る」競技", "トップ選手は、<em>パスの前ほど首を振っている</em>",
 f'''<div class="row" style="align-items:center">{pitch}<div style="flex:1">
 <div class="row" style="gap:18px;margin-bottom:16px"><div><div class="stat">21<small>試合</small></div><p class="lbl">プレミアリーグの試合を撮影</p></div>
 <div><div class="stat">9,574<small>回</small></div><p class="lbl">ボール保持の場面を分析</p></div></div>
 <div class="card"><p>・パスを出す前は、ドリブルやシュートの前よりスキャンが多い<br>・前方へのパスの前ほどスキャンが多い<br>・スキャンはパス成功に<b>小さいがプラス</b>の関連</p></div></div></div>''',
 "Jordet ほか（2020）Scanning, Contextual Factors, and Association With Performance in English Premier League Footballers. Frontiers in Psychology. 「見て判断する力」が競技力の一部であることを示す研究です。"))

# 3 情報量
def burst(cx, items, big):
    out = ""
    for i, t in enumerate(items):
        a = -math.pi/2 + 2*math.pi*i/len(items)
        x, y = cx + 170*math.cos(a), 190 + 140*math.sin(a)
        out += f'<line x1="{cx}" y1="190" x2="{x}" y2="{y}" stroke="{ACC if big else "#c3cad6"}" stroke-width="{4 if big else 2}"/>'
        out += f'<rect x="{x-66}" y="{y-20}" width="132" height="38" rx="19" fill="{ACC if big else "#eef1f5"}"/><text x="{x}" y="{y+6}" font-size="16" text-anchor="middle" fill="#0f2340">{t}</text>'
    return out + f'<circle cx="{cx}" cy="190" r="{70 if big else 54}" fill="{"#0f2340" if big else "#9aa6b8"}"/><text x="{cx}" y="198" font-size="24" fill="#fff" text-anchor="middle" font-weight="bold">{"試合" if big else "練習"}</text>'
S.append(slide(3, "なぜ試合で判断が遅れるのか", "試合では、<em>22人とボールが同時に動く</em>",
 f'''<svg width="1136" height="390" viewBox="0 0 1136 390">{burst(250, ["コーン","パス相手"], False)}{burst(840, ["ボール","味方の位置","相手のプレス","背後のスペース","オフサイドライン","スコア・時間","声・指示","疲労・緊張"], True)}
 <text x="545" y="200" font-size="46" fill="{ACCD}" text-anchor="middle">→</text></svg>''',
 "技術が高い選手同士ほど、最後は「多すぎる情報の中で、早く正しく選ぶ力」で差がつきます。"))

# 4 No.2
ic = lambda d: f'<svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="{ACC}"/>{d}</svg>'
S.append(slide(4, "私の立ち位置", "主役は監督と選手。私は<em>最強のNo.2</em>",
 f'''<div class="row">
 <div class="card" style="flex:1">{ic('<path d="M18 34l9 9 19-21" stroke="#0f2340" stroke-width="6" fill="none"/>')}<h3 style="margin-top:12px">戦術は変えない</h3><p>チームの戦術・技術指導には口を出しません。監督の目標から逆算して土台づくりを担当。</p></div>
 <div class="card" style="flex:1">{ic('<circle cx="22" cy="28" r="7" fill="#0f2340"/><circle cx="42" cy="28" r="7" fill="#0f2340"/><path d="M10 50q12-14 24 0M30 50q12-14 24 0" stroke="#0f2340" stroke-width="5" fill="none"/>')}<h3 style="margin-top:12px">大人数でも回せる</h3><p>1回20〜30分、ボールを使ったグループ形式。カテゴリー（トップ・セカンド・1年生）ごとに実施できます。</p></div>
 <div class="card" style="flex:1">{ic('<rect x="16" y="34" width="8" height="14" fill="#0f2340"/><rect x="28" y="24" width="8" height="24" fill="#0f2340"/><rect x="40" y="16" width="8" height="32" fill="#0f2340"/>')}<h3 style="margin-top:12px">数字で報告する</h3><p>開始時・6週・12週に測定してレポート。続けるかは監督が数字で判断できます。</p></div>
 </div><p style="margin-top:26px;font-size:22px">目標：<b>全国を目指す選手の「見て・決める」土台を引き上げる</b></p>'''))

# 5 しくみ
cyc = f'''<svg width="560" height="400" viewBox="0 0 560 400">
<circle cx="280" cy="200" r="140" fill="none" stroke="#e1e5ec" stroke-width="28"/>
<path d="M280 60 A140 140 0 1 1 140 200" fill="none" stroke="{ACC}" stroke-width="28"/>
<g font-size="19" font-weight="bold" fill="#0f2340" text-anchor="middle">
<rect x="195" y="22" width="170" height="54" rx="27" fill="#0f2340"/><text x="280" y="56" fill="#fff">① 同時に刺激</text>
<rect x="395" y="173" width="160" height="54" rx="27" fill="#0f2340"/><text x="475" y="207" fill="#fff">② 混乱・渋滞</text>
<rect x="195" y="324" width="170" height="54" rx="27" fill="#0f2340"/><text x="280" y="358" fill="#fff">③ 適応する</text>
<rect x="5" y="173" width="160" height="54" rx="27" fill="{ACC}"/><text x="85" y="207">④ 課題を変える</text>
<text x="280" y="196" font-size="24">慣れる前に</text><text x="280" y="228" font-size="24">次の課題へ</text></g></svg>'''
S.append(slide(5, "トレーニングのしくみ", "わざと<em>「処理が追いつかない」</em>状態をつくる",
 f'''<div class="row" style="align-items:center">{cyc}<div style="flex:1">
 <div class="card" style="margin-bottom:14px"><h3>① ライフキネティック</h3><p>視覚・認知・協調運動の課題を同時に。色や数字のコール、2つのボール、利き足と逆の操作を組み合わせる。ドイツ発祥で、サッカー界でも導入が報じられています。</p></div>
 <div class="card"><h3>② スポーツリズムトレーニング</h3><p>拍に合わせて身体を動かし、ステップ・踏み切り・パスのタイミングをそろえる。</p></div></div></div>''',
 "脳の中で起きている変化は研究途上です。本提案では、測定できる「反応・判断・動き」の変化で効果を確認します。ドイツでの導入はÄrzte Zeitung等の報道によるもので、効果を示す研究ではありません。"))

# 6 メタ分析（団体競技）
S.append(slide(6, "エビデンス ①　団体競技の22研究をまとめた分析", "予測・判断の力は<em>トレーニングで伸びる</em>",
 f'''<div class="row" style="align-items:center">{effect_bars([("実験室のテスト", 1.51, False), ("ピッチ上の実戦", 0.65, True)], 680, 280, 1.8, ACC)}
 <div style="flex:1"><div class="card" style="margin-bottom:14px"><h3>読み取れること</h3><p>団体競技の選手で、知覚・認知トレーニングにより予測・判断が改善。ピッチ上でも「中程度以上」の効果。</p></div>
 <div class="card"><h3>本プログラムの設計</h3><p>実験室ほどは移らないため、<b>ボール・相手・味方の声・ステップ</b>を必ず入れたサッカー特化型で行います。</p></div></div></div>''',
 "Zhu ほか（2024）Behavioral Sciences 14(10):919（団体競技の22研究・45の効果量）。数値は効果量。一般的な脳トレの競技への転移には否定的な見解もあります（Fransen, 2024, Sports Medicine）。"))

# 7 リズム × サッカー
S.append(slide(7, "エビデンス ②　リズム × サッカー", "タイミングを鍛えると、<em>ステップが正確になる</em>",
 f'''<div class="row">
 <div class="card" style="flex:1.15"><h3>エリート女子サッカー選手24名</h3>
 {meter("タイミング能力と正確なステップ数の相関（|r|）", 0.59, 1.0, 0.5, "強い相関の目安 0.5", 600, ACC)}
 <p style="margin-top:8px">メトロノーム同期トレーニング（4週・12回）を行った群だけ、ステップ課題の正確さと速さが向上。</p></div>
 <div style="flex:1;display:flex;flex-direction:column;gap:16px">
 <div class="card"><h3>クロスの精度（同じトレーニング）</h3><p>サッカー選手のクロスで、狙いへの正確さが上がり、ばらつきが減ったと報告。</p></div>
 <div class="card"><h3>リズムジャンプ（小学生サッカー）</h3><p>週1回×8週で、リズム再現能力とアジリティが向上。</p></div></div></div>''',
 "Rönnqvist ほか（2018）Frontiers in Psychology 9:2469（事後テストで r = −0.588）。クロス：Sommer ほか（2018）。リズムジャンプ：Children（2025）。いずれも小規模な研究です。"))

# 8 LK フェンシング
ch = prepost([("ストループ課題（秒）", [("LK群", 26.83, 24.49, True), ("対照群", 26.81, 26.67, False)])], w=500, h=420, ymax=30)
ch2 = prepost([("アジリティ（秒）", [("LK群", 15.48, 13.73, True)])], w=260, h=420, ymax=18)
S.append(slide(8, "エビデンス ③　ライフキネティック × 競技者（ランダム化比較試験）", "8週間で、<em>判断もフットワークも速くなった</em>",
 f'''<div class="row" style="align-items:flex-end">{ch}{ch2}
 <div style="flex:1;padding-bottom:30px"><div class="stat">−11<small>%</small></div><p class="lbl">アジリティテストのタイム<br>（15.48秒 → 13.73秒）</p>
 <div class="stat" style="margin-top:20px;font-size:64px">p&lt;0.001</div><p class="lbl">LK群はストループ・アジリティ・垂直跳びが向上。対照群は有意な変化なし</p></div></div>''',
 "Yarayan ほか（2025）BMC Sports Sci Med Rehabil。フェンシング競技者22名（平均11.6歳）、週2回×60分×8週。数値はプレプリント版の表の値。タイムは短いほど良い。"))

# 9 バドミントン
S.append(slide(9, "エビデンス ④　ライフキネティック × 競技動作", "6週間で<em>競技の技術成績</em>まで向上",
 f'''<div class="row" style="align-items:center">
 <div style="width:380px"><div class="stat">40<small>名</small></div><p class="lbl">バドミントン選手をランダムに割り付け<br>通常練習＋ライフキネティック（6週・18回）</p>
 <div style="margin-top:22px"><span class="tag a">集中力</span><span class="tag a">作業記憶</span><span class="tag a">サービス成績</span></div>
 <p class="lbl" style="margin-top:10px">すべて有意に向上（p&lt;0.001）</p></div>
 <div style="flex:1"><p style="font-size:19px;margin-bottom:6px"><b>効果の大きさ（偏η²）</b>　線＝「大きい効果」の目安 0.14</p>
 {meter("集中力", 0.80, 1.0, 0.14, "大きい効果の目安", 640, ACC)}
 {meter("作業記憶", 0.82, 1.0, 0.14, "大きい効果の目安", 640, ACC)}
 <div class="honest" style="margin-top:14px">サッカー・高校生での研究はまだ少ないため、貴校での測定で確かめながら進めます。</div></div></div>''',
 "Life Kinetics Training as a Multimodal Neurocognitive Intervention…（Life, 16(5), 836, 2026）。偏η²の0.14は一般的な「大」の目安。"))

# 10 メニュー
pitch2 = f'''<svg width="500" height="400" viewBox="0 0 500 400">
<rect x="20" y="20" width="460" height="360" rx="8" fill="#2c6e49"/>
<rect x="60" y="60" width="380" height="280" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="8 6"/>
<g>{''.join(f'<rect x="{x-14}" y="{y-14}" width="28" height="28" rx="4" fill="{c}"/>' for x,y,c in [(60,60,"#e5484d"),(440,60,"#3b82f6"),(60,340,"#f5c518"),(440,340,"#fff")])}</g>
<circle cx="250" cy="200" r="16" fill="#0f2340" stroke="#fff" stroke-width="3"/>
<circle cx="250" cy="100" r="12" fill="{ACC}"/><text x="250" y="80" font-size="14" fill="#fff" text-anchor="middle">パサー（色コール）</text>
<path d="M250 112 L250 182" stroke="#fff" stroke-width="3" stroke-dasharray="6 5"/>
<path d="M262 210 L420 330" stroke="#fff" stroke-width="4"/><path d="M420 330 l-14 -2 l6 -10z" fill="#fff"/>
<text x="250" y="392" font-size="14" fill="#5a6476" text-anchor="middle">例：受ける直前のコール色のゲートへ、逆足でパス</text></svg>'''
S.append(slide(10, "サッカー版メニュー（例）", "ピッチで、<em>ボールを使って</em>行う",
 f'''<div class="row">{pitch2}<div style="flex:1"><table>
 <tr><th>ねらい</th><th>メニュー例</th></tr>
 <tr><td>スキャンの習慣</td><td>受ける前に後ろで示される色・数字を答えてからトラップ</td></tr>
 <tr><td>判断の切り替え</td><td>色コールでパスの方向を変える。慣れたらルールを逆に</td></tr>
 <tr><td>両足・逆側の処理</td><td>2つのボールの同時操作＋数字コール。できたら1つ変える</td></tr>
 <tr><td>動き出しの「間」</td><td>拍に合わせたステップ→不規則な拍で裏への抜け出し</td></tr>
 <tr><td>連携</td><td>3人組で交互にコールし、リズムをそろえてパス交換</td></tr></table></div></div>''',
 "1回20〜30分。ウォームアップ枠に組み込み、カテゴリー別に実施します。"))

# 11 レポート見本
def blank_chart(title):
    bars = "".join(f'<rect x="{40+i*70}" y="40" width="44" height="130" rx="4" fill="none" stroke="#9aa6b8" stroke-dasharray="5 5"/><text x="{62+i*70}" y="192" font-size="13" text-anchor="middle" fill="#5a6476">{t}</text>' for i,t in enumerate(["開始","6週","12週"]))
    return f'<div class="card" style="padding:14px 16px"><p style="font-size:16px;font-weight:bold;color:#0f2340">{title}</p><svg width="250" height="200">{bars}<text x="125" y="115" font-size="14" text-anchor="middle" fill="{ACCD}">貴校の実測値</text></svg></div>'
S.append(slide(11, "結果へのコミット ＝ 測って、見せる", "12週後、このレポートを<em>数字で</em>お渡しします",
 f'''<div class="row" style="gap:16px">{blank_chart("選択反応時間")}{blank_chart("ストループ課題")}{blank_chart("アジリティ")}{blank_chart("試合映像のスキャン回数")}</div>
 <div class="row" style="margin-top:18px;gap:16px"><div class="honest" style="flex:1">測定：反応時間（アプリ）・ストループ・アジリティ・リズム再現・試合映像の首振り回数とパス成功率・緊張の自己評価</div>
 <div class="honest" style="flex:1">約束：測定と報告を必ず行う／伸びない項目はメニューを組み替える／個人データは学校外に出さない</div></div>''',
 "レポートの見本（枠のみ）です。数値は実施後の実測値のみを記入します。勝敗・大会成績を保証するものではなく、土台となる能力の変化を数字で示すことにコミットします。"))

S.extend(ai_slides(ACC, ACCD, ['選手同士のコーチング（声）の回数とタイミング', 'ハーフタイム・試合中の声の質（指示・励まし）', '監督の指示がどう伝わったかの振り返り'], ['受ける前の首振り（スキャン）の回数', 'パスの成功率・前方へのパスの割合', '奪われた後の切り替えの速さ']))

# 12 私立高校にとっての価値
S.append(slide(12, "私立高校のチームにとっての価値", "<em>「科学的に鍛える部」</em>を、数字で示せる",
 '''<div class="row">
 <div class="card" style="flex:1"><h3>大人数・複数カテゴリー</h3><p>トップ・セカンド・1年生など、カテゴリーごとにグループ形式で実施。全員に同じ土台をつくれます。</p></div>
 <div class="card" style="flex:1"><h3>学校説明・保護者向け</h3><p>測定データ（個人が特定できない形）を使い、部の取り組みを学校説明会や保護者会で紹介できます。</p></div>
 <div class="card" style="flex:1"><h3>監督の負担を増やさない</h3><p>メニュー作成・測定・集計・レポートは私が担当。監督は結果を見て判断するだけ。</p></div></div>
 <p style="margin-top:26px">外部の専門スタッフとして、<b>コーチ陣の一員</b>のように動きます。</p>''',
 "生徒募集などへの効果を約束するものではありません。データの外部公開は、学校・保護者の同意の範囲で行います。"))

# 13 スケジュール
S.append(slide(13, "導入スケジュール", "冬は<em>無料</em>で確かめ、4月から本格導入",
 timeline([("12月〜1月","無料","体験セッション<br>初回測定・メニュー設計",False),("1月〜3月","無料","トライアル6週<br>中間測定・結果のご報告",False),
           ("4月","契約開始","導入をご判断<br>ここから料金発生",False),("5月〜7月","","6週・12週で測定<br>インターハイ予選へ",False),("秋〜冬","","選手権予選・<br>リーグ戦へ",True)], ACC)
 + '<p style="margin-top:28px">トライアルの数字を見てから決められます。<b>導入しない場合、費用は一切かかりません。</b></p>'))

# 14 料金
S.append(slide(14, "導入プラン（案）", "2027年4月からのプラン",
 '''<table style="margin-top:6px"><tr><th>プラン</th><th>内容</th><th style="width:22%">料金（税込・交通費別）</th></tr>
 <tr><td><b>ライト</b></td><td>月2回訪問（各90分・1カテゴリー）・測定3回・レポート</td><td>月額 40,000円</td></tr>
 <tr><td><b>スタンダード</b></td><td>月4回訪問（各90分・2カテゴリーまで）・測定3回・レポート・自主練メニュー</td><td>月額 70,000円</td></tr>
 <tr><td><b>年間サポート</b></td><td>スタンダード×12か月・大会前の調整・映像からのスキャン分析</td><td>年額 750,000円</td></tr></table>
 <p style="margin-top:22px">12月〜3月の<b>無料トライアル6週＋初回・中間測定</b>の結果を見てからお選びいただけます。</p>''',
 "金額は案です。部員数・カテゴリー数・訪問距離に応じて調整します。"))

# 15 参考文献
S.append(slide(15, "参考文献", "本資料で引用した研究",
 '''<ol class="ref" style="padding-left:1.4em">
 <li>Jordet ほか. Scanning, Contextual Factors, and Association With Performance in English Premier League Footballers: An Investigation Across a Season. Frontiers in Psychology, 2020. https://doi.org/10.3389/fpsyg.2020.553813</li>
 <li>Zhu ほか. Effects of Perceptual-Cognitive Training on Anticipation and Decision-Making Skills in Team Sports: A Systematic Review and Meta-Analysis. Behavioral Sciences, 14(10), 919, 2024. https://www.mdpi.com/2076-328X/14/10/919</li>
 <li>Fransen. There is No Supporting Evidence for a Far Transfer of General Perceptual or Cognitive Training to Sports Performance. Sports Medicine, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11560981/</li>
 <li>Rönnqvist ほか. Influences of Synchronized Metronome Training on Soccer Players' Timing Ability, Performance Accuracy, and Lower-Limb Kinematics. Frontiers in Psychology, 9, 2469, 2018. https://www.frontiersin.org/articles/10.3389/fpsyg.2018.02469/full</li>
 <li>Sommer ほか. Synchronized metronome training and soccer cross-pass performance, 2018（正式書誌は原典で確認）.</li>
 <li>The Effects of Rhythm Jump Training on the Rhythmic Reproduction Ability in Jumping and Agility in Elementary School Soccer Players. Children, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC11854900/</li>
 <li>Yarayan ほか. Impact of life kinetik training on … preadolescent recreational fencing athletes: a randomized controlled trial. BMC Sports Sci Med Rehabil, 17, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12145597/（数値はプレプリント https://www.researchsquare.com/article/rs-5463104/v1）</li>
 <li>Life Kinetics Training as a Multimodal Neurocognitive Intervention: Enhances Cognitive and Motor Performance in Badminton Athletes. Life, 16(5), 836, 2026. https://doi.org/10.3390/life16050836</li>
 <li>Ärzte Zeitung「Neurobiologie bahnt den Weg zum Erfolg」（ライフキネティックの導入に関する報道）. https://www.aerztezeitung.de/Panorama/Neurobiologie-bahnt-den-Weg-zum-Erfolg-231827.html</li></ol>'''))

# 16 クロージング
S.append(f'''<section class="s dark"><svg style="position:absolute;left:0;top:0" width="1280" height="720">{net}{dots}</svg>
<div style="position:relative;margin-top:150px;max-width:700px"><p class="k" style="color:{ACC}">次の一歩</p>
<h1 style="font-size:50px">まずは無料トライアルで、<br>選手の反応と数字を見てください</h1>
<p style="font-size:22px">体験セッション → 6週トライアル → 中間測定</p>
<p style="margin-top:36px;font-size:19px;color:#c7d2e3">フォロワーシップコーチ　〇〇 〇〇<br>連絡先：〇〇〇〇（メール／電話）</p></div></section>''')

out = os.path.join(os.path.dirname(__file__), "..", "提案資料_サッカー.html")
open(out, "w", encoding="utf-8").write(page("フォロワーシップコーチ提案（サッカー）", ACC, ACCD, S))
print("written", len(S))
