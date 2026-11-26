"""判断の診断・処方プログラム設計書（A4横）。仮説と既存の知見を区別して書くこと。"""
import os, math
ACC, NAVY, SOC = "#c8e63c", "#0f2340", "#3ddc84"
CSS = f"""
@page{{size:297mm 210mm;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"IPAPGothic","IPAGothic",sans-serif;color:#1d2433}}
.p{{width:297mm;height:210mm;padding:11mm 13mm;position:relative;page-break-after:always;overflow:hidden}}
.p:last-child{{page-break-after:auto}}
.k{{font-size:12pt;color:#6f8c00;font-weight:bold;letter-spacing:.06em}}
h1{{font-size:23pt;color:{NAVY};margin:1.5mm 0 4mm;line-height:1.3}}
h1 em{{font-style:normal;background:linear-gradient(transparent 62%,{ACC} 62%)}}
p,li{{font-size:11.5pt;line-height:1.55}}
.row{{display:flex;gap:6mm}}
.card{{background:#f4f6f9;border-radius:3.5mm;padding:4mm 5mm}}
.card h3{{font-size:13pt;color:{NAVY};margin-bottom:1.5mm}}
.card p,.card li{{font-size:10.5pt;line-height:1.5}}
table{{border-collapse:collapse;width:100%}}
td,th{{border-bottom:.3mm solid #d9dee7;padding:1.8mm 2.2mm;font-size:9.6pt;line-height:1.42;text-align:left;vertical-align:top}}
th{{background:{NAVY};color:#fff;font-size:9.6pt}}
td b{{color:{NAVY}}}
.L{{display:inline-block;min-width:8mm;text-align:center;border-radius:99px;background:{NAVY};color:#fff;font-size:9pt;padding:.4mm 1.5mm;margin-right:1mm}}
.h{{display:inline-block;font-size:8.5pt;border-radius:99px;padding:.3mm 2mm;background:#fff1e6;color:#b54708;margin-left:1mm}}
.e{{display:inline-block;font-size:8.5pt;border-radius:99px;padding:.3mm 2mm;background:#eef3d6;color:#3f5200;margin-left:1mm}}
.note{{position:absolute;left:13mm;right:24mm;bottom:5mm;font-size:8.5pt;color:#5a6476;line-height:1.4}}
.n{{position:absolute;right:9mm;bottom:5mm;font-size:9pt;color:#5a6476}}
svg text{{font-family:"IPAPGothic","IPAGothic",sans-serif}}
"""
P = []
def pg(k, h, body, note=""):
    P.append(f'<section class="p"><p class="k">{k}</p><h1>{h}</h1>{body}' + (f'<p class="note">{note}</p>' if note else "") + f'<span class="n">{len(P)+1}</span></section>')

LINKS = [("L1","予測する","相手の構え・体の向きから、打つ（蹴る）前に読む"),
         ("L2","探す","見るべき場所を、見るべき時に見る（首振り・相手前衛の確認）"),
         ("L3","同時に感じる","中心を見たまま周りを感じとる（周辺視・注意の配分）"),
         ("L4","選ぶ","選択肢が増えても速く正しく決める"),
         ("L5","止める・切り替える","動き出した後でも、状況が変われば取り消す（フェイク対応）"),
         ("L6","間を合わせる","動き出し・踏み込みのタイミングをそろえる（リズム）"),
         ("L7","本番で崩れない","緊張・疲労・騒音の中でも①〜⑥を保つ")]

# 1 表紙
P.append(f'''<section class="p" style="background:{NAVY};color:#fff">
<svg style="position:absolute;right:0;top:0" width="560" height="794">{''.join(f'<circle cx="{300+170*math.cos(2*math.pi*i/7-math.pi/2)}" cy="{400+170*math.sin(2*math.pi*i/7-math.pi/2)}" r="34" fill="{ACC if i<6 else SOC}"/><text x="{300+170*math.cos(2*math.pi*i/7-math.pi/2)}" y="{407+170*math.sin(2*math.pi*i/7-math.pi/2)}" font-size="18" text-anchor="middle" fill="{NAVY}" font-weight="bold">L{i+1}</text>' for i in range(7))}
<circle cx="300" cy="400" r="196" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="2"/><text x="300" y="392" font-size="22" fill="#fff" text-anchor="middle">判断の</text><text x="300" y="424" font-size="22" fill="#fff" text-anchor="middle">7つの輪</text></svg>
<div style="position:relative;max-width:150mm;margin-top:28mm"><p class="k" style="color:{ACC}">プログラム設計書　｜　ソフトテニス・サッカー共通</p>
<h1 style="color:#fff;font-size:32pt">判断を<span style="color:{ACC}">診断</span>し、<br><span style="color:{ACC}">処方</span>し、<br>データで<span style="color:{ACC}">結論</span>を出す</h1>
<p style="font-size:13pt;color:#c7d2e3">「これをやれば伸びる」から、「この選手の、この判断には、これが効く」へ。</p></div>
<p style="position:absolute;left:13mm;bottom:10mm;font-size:10pt;color:#c7d2e3">フォロワーシップコーチ　〇〇 〇〇　｜　内部資料（説明にも使用可）</p></section>''')

# 2 何を超えるか
pg("このプログラムが超えるもの", "一般的な導入の形と、<em>このプログラムの違い</em>",
 '''<table><tr><th style="width:17%">視点</th><th style="width:38%">一般的な導入の形</th><th>このプログラム</th></tr>
 <tr><td><b>対象</b></td><td>チーム全員に同じメニュー</td><td>選手ごとに「判断の7つの輪」のどこが弱いかを<b>診断</b>し、メニューを<b>処方</b>する</td></tr>
 <tr><td><b>ミスの見方</b></td><td>「判断ミス」「集中力不足」とひとまとめ</td><td>試合映像のミスを、<b>どの輪が切れたか</b>で分類（予測が遅い／見ていない／止められない…）</td></tr>
 <tr><td><b>負荷</b></td><td>決まった難易度・回数</td><td>成功率60〜80%に保つよう、選手ごとに難易度を毎回調整（<b>渋滞ゾーン</b>）</td></tr>
 <tr><td><b>競技とのつながり</b></td><td>机上・タブレットの脳トレと競技練習が別々</td><td>脳の課題を必ずラケット・ボール・相手・味方の声と組み合わせる（<b>競技の形</b>で鍛える）</td></tr>
 <tr><td><b>効果の確かめ方</b></td><td>「良くなった気がする」、チーム成績</td><td>選手ごとに<b>開始時期をずらして</b>比べ、伸びがトレーニングによるものかを判定。判定基準は<b>事前に決めて</b>おく</td></tr>
 <tr><td><b>データ</b></td><td>その場限り</td><td>診断→処方→結果を蓄積し、「この型の選手にはこの処方」の<b>当たり率</b>を更新し続ける</td></tr>
 <tr><td><b>声（音声）</b></td><td>使わない</td><td>ペア・味方へのコールの回数とタイミングを、<b>頭の渋滞を示すサイン</b>として記録（仮説として検証）</td></tr></table>''',
 "左の列はよく見られる導入の形を一般化したもので、特定のチームや団体の取り組みを評価したものではありません。")

# 3 7つの輪
SHORT = [(l, {"止める・切り替える":"止める","同時に感じる":"感じる","本番で崩れない":"本番","間を合わせる":"間"}.get(n, n), d) for l,n,d in LINKS]
cx, cy, R = 520, 300, 210
nodes = "".join(
 f'<line x1="{cx+R*math.cos(2*math.pi*i/7-math.pi/2)}" y1="{cy+R*math.sin(2*math.pi*i/7-math.pi/2)}" x2="{cx+R*math.cos(2*math.pi*(i+1)/7-math.pi/2)}" y2="{cy+R*math.sin(2*math.pi*(i+1)/7-math.pi/2)}" stroke="#c3cad6" stroke-width="6"/>' for i in range(7))
nodes += "".join(
 f'<circle cx="{cx+R*math.cos(2*math.pi*i/7-math.pi/2)}" cy="{cy+R*math.sin(2*math.pi*i/7-math.pi/2)}" r="52" fill="{NAVY if i<6 else ACC}"/>'
 f'<text x="{cx+R*math.cos(2*math.pi*i/7-math.pi/2)}" y="{cy-6+R*math.sin(2*math.pi*i/7-math.pi/2)}" font-size="17" text-anchor="middle" fill="{ACC if i<6 else NAVY}" font-weight="bold">{l}</text>'
 f'<text x="{cx+R*math.cos(2*math.pi*i/7-math.pi/2)}" y="{cy+18+R*math.sin(2*math.pi*i/7-math.pi/2)}" font-size="15" text-anchor="middle" fill="{"#fff" if i<6 else NAVY}">{n}</text>' for i,(l,n,_) in enumerate(SHORT))
lk = "".join(f'<tr><td><span class="L">{l}</span><b>{n}</b></td><td>{d}</td></tr>' for l,n,d in LINKS)
pg("診断の枠組み", "「判断」を<em>7つの輪</em>に分けて見る",
 f'''<div class="row"><svg width="430" height="430" viewBox="250 30 540 540" style="flex:none">{nodes}<text x="{cx}" y="{cy+8}" font-size="20" text-anchor="middle" fill="{NAVY}" font-weight="bold">1か所切れると</text><text x="{cx}" y="{cy+34}" font-size="20" text-anchor="middle" fill="{NAVY}" font-weight="bold">判断が崩れる</text></svg>
 <div style="flex:1"><table>{lk}</table>
 <div class="card" style="margin-top:4mm"><p>「判断が遅い」という同じ症状でも、<b>どの輪が切れているかで処方はまったく違う</b>。例：読めていないのか（L1）、読めているのに動き出しが合わないのか（L6）。ここを分けることが、このプログラムの出発点です。</p></div></div></div>''',
 "7つの輪は、知覚・認知スポーツ心理学で扱われる要素（予測、視覚探索、注意、意思決定、抑制、タイミング、プレッシャー下の遂行）を、現場で使えるように〇〇が整理した枠組みです。")

# 4 診断：測り方
diag = [("L1","映像を打つ瞬間で止め、コースを答える（遮断テスト）の正答率","相手の打球（ソ：ストローク／サ：パス・シュート）に対する初動の向きが合っている割合"),
        ("L2","—（L3と合わせて実施）","サ：受ける前10秒の首振り回数／ソ：打つ前に相手前衛を確認した割合"),
        ("L3","周辺視フィンガーの正答率（中心課題あり／なし）","ソ：前衛の動きに気づいたか／サ：背後の相手に気づいたか（映像）"),
        ("L4","単純反応→2択→4択の反応時間。<b>選択肢が増えたときの遅れ幅</b>","選択肢が多い場面の判断時間・成功率"),
        ("L5","ストループ課題の干渉、Go/No-Go課題の誤反応","フェイクに引っかかった割合、動き出し後の修正の有無"),
        ("L6","メトロノーム同期のずれ（ミリ秒）と、テンポ変化への追従","ソ：スプリットステップの着地と相手の打球の時間差／サ：抜け出しのタイミング"),
        ("L7","上の課題を、騒音・時間制限・疲労（ダッシュ直後）で行ったときの<b>落ち幅</b>","重要な場面（デュース・終盤）と通常場面の成功率の<b>差</b>、コール回数の減り方")]
rows = "".join(f'<tr><td><span class="L">{l}</span></td><td>{a}</td><td>{b}</td></tr>' for l,a,b in diag)
pg("診断 ①　どう測るか", "同じ輪を、<em>テスト</em>と<em>試合</em>の両方から測る",
 f'''<table><tr><th style="width:6%">輪</th><th style="width:44%">テスト（10〜15分で全員実施）</th><th>試合・練習の指標（映像・音声からAIで集計→人が確認）</th></tr>{rows}</table>
 <div class="row" style="margin-top:3.5mm"><div class="card" style="flex:1"><p><b>ポイント1：</b>「選択肢が増えたときの遅れ幅」「緊張下の落ち幅」のように、<b>条件を変えたときの差</b>で測る。素の速さより、その選手の弱点がはっきり出ます。</p></div>
 <div class="card" style="flex:1"><p><b>ポイント2：</b>テストが伸びても試合が伸びなければ意味がない。<b>テスト・練習内・試合</b>の3段階を別々に記録し、どこまで効果が届いたかを正直に分けて報告します。</p></div></div>''',
 "ソ＝ソフトテニス、サ＝サッカー。遮断テスト、選択反応時間、ストループ、Go/No-Go、同期タッピングは研究で広く使われる課題です。試合指標の妥当性は、このプログラムの中で確かめていきます。")

# 5 ミスの型
mt = [("前衛がポーチに出たが、逆を突かれた","L1 予測 / L5 止める","読みの材料（相手の肩・面）を見ていない → L1。出た後に戻れない → L5"),
      ("ボレーに間に合わない（届かない）","L6 間 / L1 予測","スプリットの着地が遅い → L6。動き出しの方向は合っているか → L1"),
      ("後衛が相手前衛につかまる","L2 探す / L3 感じる","打つ前に前衛を見ていない → L2。見ているのに位置を覚えていない → L3"),
      ("受けた後に前を向けず、バックパスばかり","L2 探す","受ける前の首振りが少ない → L2"),
      ("フリーの味方がいるのに選べない・遅れる","L4 選ぶ","選択肢が増えると極端に遅くなる → L4"),
      ("1対1でフェイクに飛び込む","L5 止める","早く動きすぎて取り消せない → L5（速さはあるので L6 は強み）"),
      ("練習ではできるのに、終盤・大事な場面でミスが増える","L7 本番","通常場面と重要場面の差が大きい → L7。コールが減る・遅れるのも同じサイン")]
rows = "".join(f'<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>' for a,b,c in mt)
pg("診断 ②　ミスの型", "ミスを「判断ミス」で終わらせず、<em>切れた輪</em>を特定する",
 f'''<table><tr><th style="width:34%">試合で見えるミス（例）</th><th style="width:18%">疑う輪</th><th>見分け方（映像で確認するところ）</th></tr>{rows}</table>
 <div class="card" style="margin-top:4mm"><p>試合映像のミスを1本ずつこの型でタグ付けし（AIで候補を出し、〇〇が確認）、選手ごとに「どの輪で何回切れたか」を数えます。これが<b>試合から見た判断プロファイル</b>になります。</p></div>''')

# 6 選手の型
def radar(vals, col):
    pts = " ".join(f'{110+80*v*math.cos(2*math.pi*i/7-math.pi/2)},{100+80*v*math.sin(2*math.pi*i/7-math.pi/2)}' for i,v in enumerate(vals))
    grid = "".join(f'<polygon points="{" ".join(f"{110+80*r*math.cos(2*math.pi*i/7-math.pi/2)},{100+80*r*math.sin(2*math.pi*i/7-math.pi/2)}" for i in range(7))}" fill="none" stroke="#d9dee7"/>' for r in (0.33,0.66,1))
    lab = "".join(f'<text x="{110+96*math.cos(2*math.pi*i/7-math.pi/2)}" y="{104+96*math.sin(2*math.pi*i/7-math.pi/2)}" font-size="11" text-anchor="middle" fill="#5a6476">L{i+1}</text>' for i in range(7))
    return f'<svg width="220" height="200">{grid}<polygon points="{pts}" fill="{col}" fill-opacity=".55" stroke="{NAVY}" stroke-width="2"/>{lab}</svg>'
types = [("A　読めるのに間に合わない", [.9,.7,.7,.7,.6,.3,.6], "L6 リズム系を中心に。予測は強みとして使う"),
         ("B　速いが、早まる", [.5,.6,.6,.7,.3,.9,.6], "L5 止める系。動き出し後の取り消し課題"),
         ("C　見ていない", [.6,.3,.4,.7,.6,.7,.6], "L2・L3 探す・感じる系。首振り・前衛チェック"),
         ("D　本番で崩れる", [.8,.7,.7,.8,.7,.7,.3], "L7 圧力下の課題。普段の練習に騒音・時間制限・疲労を足す")]
cards = "".join(f'<div class="card" style="flex:1;text-align:center"><h3>{t}</h3>{radar(v, ACC)}<p style="text-align:left"><b>処方：</b>{rx}</p></div>' for t,v,rx in types)
pg("診断 ③　選手の型", "プロファイルから、<em>4つの型</em>で処方の方向を決める",
 f'<div class="row" style="gap:4mm">{cards}</div><div class="card" style="margin-top:4mm"><p>型は出発点です。実際には一人ひとりのプロファイルで処方を組み、結果を見て更新します。型の分け方そのものも、データがたまるたびに見直します。</p></div>',
 "図は型の考え方を示す模式図で、実在の選手の測定値ではありません。4つの型は〇〇の仮説で、データで確かめていく対象です。")

# 7 処方マトリクス
rx = [("L1 予測する","<b>先読みカラー</b>：色の並びの規則を読み、次の色を先に言う","<b>面読みボレー</b>：球出しの面が見えた瞬間に「右/左」をコール→ボレー。徐々に見せる時間を短く","<b>体の向き読み</b>：パサーの踏み込み足が見えた瞬間に受ける方向を宣言"),
      ("L2 探す","<b>背中ナンバー</b>：前を向いたまま、合図で振り返って数字を読む","<b>前衛チェック・ラリー</b>：打つ前に相手前衛の位置をコールしてから打つ","<b>スキャン・ナンバー</b>：受ける前に背後の色・数字を答えてからトラップ"),
      ("L3 同時に感じる","<b>周辺視フィンガー</b>","<b>フィンガー・ラリー</b>：ラリー中、横で出す指の本数を答える","<b>周辺視ロンド</b>：ボールを見たまま、外側で上がった色のコーンへパス"),
      ("L4 選ぶ","<b>2択→4択カラー</b>：色と動きの対応を2つ→4つに増やす","<b>4コース・ボレー</b>：コール色で4方向に打ち分け。選択肢を段階的に増やす","<b>ゲート4択パス</b>：4色のゲートからコールされた所へ。数を増やす"),
      ("L5 止める・切り替える","<b>逆ルール</b>：慣れたルールを途中で反対にする","<b>ストップ・ボレー</b>：出た後に「ストップ」色が出たら止まって戻る","<b>フェイク1対1</b>：攻撃側のフェイクに対し、合図が出るまで重心を残す"),
      ("L6 間を合わせる","<b>リズム・スプリット</b>（一定→不規則なテンポ）","<b>拍スプリット</b>：相手の打球音に合わせて着地。メトロノームを相手の打球間隔に合わせる","<b>拍抜け出し</b>：パサーの踏み込みの拍に合わせて裏へ走る"),
      ("L7 本番で崩れない","上の課題に<b>騒音・時間制限</b>を足す","<b>ラストポイント課題</b>：「この1本で決まる」設定＋応援音声を流す＋ダッシュ直後に実施","<b>疲労下の判断</b>：インターバル走の直後に L2〜L5 の課題を行う")]
rows = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a,b,c,d in rx)
pg("処方　輪ごとの活動", "切れた輪に、<em>3段階</em>で処方する",
 f'''<table><tr><th style="width:13%">輪</th><th style="width:25%">段階1：脳の土台（ライフキネティック・リズム）</th><th style="width:31%">段階2：ソフトテニスの形</th><th>段階2：サッカーの形</th></tr>{rows}</table>
 <p style="margin-top:2.5mm;font-size:10pt"><b>段階3：</b>試合形式（ゲーム練習）の中に条件を1つだけ足す（例：ポイント間に必ず前衛の位置をコール）。段階1→2→3の順に「競技に近づける」ことで、試合まで効果を届けます。</p>''',
 "活動名は本プログラム用の名前です。段階1の一部はライフキネティック・スポーツリズムトレーニングの考え方にもとづきます。")

# 8 渋滞ゾーン
curve = "M60 300 C 180 300, 220 70, 330 70 C 440 70, 480 300, 600 300"
pg("処方の強さ", "成功率<em>60〜80%</em>の「渋滞ゾーン」に毎回合わせる",
 f'''<div class="row"><svg width="640" height="360" viewBox="0 0 640 360">
 <rect x="255" y="40" width="150" height="270" fill="{ACC}" fill-opacity=".35"/><text x="330" y="30" font-size="16" text-anchor="middle" fill="{NAVY}" font-weight="bold">渋滞ゾーン</text>
 <path d="{curve}" stroke="{NAVY}" stroke-width="5" fill="none"/><line x1="50" y1="310" x2="620" y2="310" stroke="#5a6476" stroke-width="2"/><line x1="50" y1="310" x2="50" y2="40" stroke="#5a6476" stroke-width="2"/>
 <text x="335" y="345" font-size="15" text-anchor="middle" fill="#5a6476">← 簡単すぎ（成功率90%以上）　　難しさ　　難しすぎ（50%未満） →</text>
 <text x="40" y="175" font-size="15" text-anchor="middle" fill="#5a6476" transform="rotate(-90 40 175)">学び（伸び）</text>
 <text x="330" y="260" font-size="15" text-anchor="middle" fill="{NAVY}">成功率 60〜80%</text></svg>
 <div style="flex:1"><div class="card" style="margin-bottom:3mm"><h3>毎回やること</h3><p>各活動の成功率を記録（タブレットで1タップ）。80%を超えたら1段階上げ、50%を下回ったら1段階下げる。</p></div>
 <div class="card"><h3>難しさを上げる5つのつまみ</h3><p>① 選択肢の数　② 見える時間の短さ　③ ルールの入れかえ　④ 同時に行う課題の数　⑤ 緊張・疲労・騒音</p></div></div></div>''',
 "課題の難しさを学ぶ人の力量に合わせると学習が最大になる、という考え方（Challenge Point Framework：Guadagnoli & Lee, 2004）にもとづきます。60〜80%という範囲は運用上の目安で、データで調整します。")

# 9 効果の確かめ方
def lane(y, start, name):
    return (f'<text x="10" y="{y+24}" font-size="15" fill="{NAVY}">{name}</text>'
            f'<rect x="110" y="{y}" width="{start*40}" height="36" rx="6" fill="#c3cad6"/>'
            f'<rect x="{110+start*40}" y="{y}" width="{(12-start)*40}" height="36" rx="6" fill="{ACC}"/>')
pg("効果の確かめ方", "選手ごとに<em>開始をずらして</em>、伸びの理由を見分ける",
 f'''<div class="row"><div style="width:150mm;flex:none"><svg width="560" height="230" viewBox="0 0 600 230">{lane(20,2,"選手グループ1")}{lane(80,4,"選手グループ2")}{lane(140,6,"選手グループ3")}
 {''.join(f'<text x="{110+i*40+20}" y="205" font-size="12" text-anchor="middle" fill="#5a6476">{i+1}</text>' for i in range(12))}<text x="350" y="225" font-size="13" text-anchor="middle" fill="#5a6476">週</text>
 <rect x="110" y="0" width="14" height="10" fill="#c3cad6"/><text x="130" y="10" font-size="12" fill="#5a6476">いつもの練習（基準づくり）</text><rect x="290" y="0" width="14" height="10" fill="{ACC}"/><text x="310" y="10" font-size="12" fill="#5a6476">処方を開始</text></svg>
 <div class="card" style="margin-top:2mm"><p>処方を始めた<b>直後に、始めた選手だけ</b>が伸びれば、季節や成長ではなくトレーニングの効果と判断しやすい（多層ベースライン法）。少人数のチームでも使える方法です。</p></div></div>
 <div style="flex:1"><div class="card" style="margin-bottom:3mm"><h3>判定のルールは事前に決める</h3><p>・「伸びた」の基準：開始前のばらつきを超える変化（目安：選手間の標準偏差の0.2倍以上）<br>・どの指標で判定するかを開始前に書面で決め、後から都合よく変えない</p></div>
 <div class="card"><h3>3段階で報告</h3><p>① テストの伸び　② 練習内の成功率　③ 試合の指標。<b>どこまで届いたか</b>を分けて正直に伝える。届かなければ処方を変える。</p></div></div></div>''',
 "多層ベースライン法は単一事例実験デザインの一つです。「意味のある最小の変化（0.2×SD）」はスポーツ科学で使われる目安（Hopkins ほか）。")

# 10 データの蓄積
loop = [("診断","7つの輪のテスト＋ミスの型"),("処方","輪×段階で活動を選ぶ"),("実施・記録","成功率・難易度を毎回"),("判定","事前に決めた基準で"),("更新","型と処方の当たり率を更新")]
cyc = "".join(f'<div style="flex:1;background:{NAVY if i==4 else "#f4f6f9"};color:{"#fff" if i==4 else "#1d2433"};border-radius:3mm;padding:3mm;text-align:center"><b style="font-size:13pt;color:{ACC if i==4 else NAVY}">{a}</b><p style="font-size:10pt">{b}</p></div>' + ('<div style="align-self:center;font-size:18pt;color:#6f8c00">→</div>' if i<4 else "") for i,(a,b) in enumerate(loop))
pg("データの蓄積と分析", "チームをまたいで、<em>「誰に何が効くか」</em>を学習し続ける",
 f'''<div class="row" style="gap:2mm">{cyc}</div>
 <div class="row" style="margin-top:4mm"><div class="card" style="flex:1"><h3>ためるデータ（1回ごと）</h3><p>選手番号・型・輪ごとのテスト値／活動名・段階・成功率・難易度のつまみ／試合のミスの型の回数／重要場面と通常場面の差／コールの回数とタイミング</p></div>
 <div class="card" style="flex:1"><h3>分析でわかるようにすること</h3><p>・「型Aの選手に拍スプリットを6週」→ L6 が伸びた割合（<b>処方の当たり率</b>）<br>・どの段階1の活動が、どの試合指標と一緒に動くか<br>・ソフトテニスとサッカーで共通に効く活動／競技別に効く活動</p></div>
 <div class="card" style="flex:1"><h3>使い方の原則</h3><p>・最初は仮説。チーム・選手が増えるほど当たり率の精度が上がる<br>・新しい選手には、近い型の過去の結果から最初の処方を選ぶ<br>・データは匿名化し、同意の範囲でだけ使う</p></div></div>''',
 "当たり率は、データがたまるたびに更新していく推定値です（ベイズ的な更新の考え方）。少ないデータの段階では、結論ではなく「次に試す候補」として扱います。")

# 11 12週
wk = [("0週","診断","7つの輪のテスト、試合映像のミスの型、型の決定、判定基準を書面化"),
      ("1〜2週","基準づくり","全員のいつもの練習を記録（処方開始前の基準）"),
      ("3〜7週","処方を順に開始","グループ1は3週、2は5週、3は7週から処方開始（段階1→2）。成功率で毎回難易度を調整"),
      ("6週","中間診断","テストと試合指標を再測定。当たり率を見て処方を更新"),
      ("7〜11週","段階2→3","試合形式に条件を足す。L7（緊張・疲労）を重点的に"),
      ("12週","最終診断・報告","3段階（テスト・練習・試合）で結果を報告。次の12週の処方案")]
rows = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a,b,c in wk)
pg("12週のロードマップ", "診断から結論まで、<em>12週で1サイクル</em>",
 f'<table><tr><th style="width:12%">時期</th><th style="width:20%">段階</th><th>内容</th></tr>{rows}</table>'
 '<div class="card" style="margin-top:4mm"><p>無料トライアル（6週）は、このうち0〜6週分（診断・基準づくり・処方の開始・中間診断）にあたります。</p></div>')

# 12 約束と限界
pg("コミットすること・正直に言うこと", "「結果にコミット」の<em>中身</em>",
 '''<div class="row"><div class="card" style="flex:1;border-top:2mm solid #c8e63c"><h3>コミットすること</h3><ul style="padding-left:1.2em">
 <li>全員の「判断の7つの輪」を診断し、選手ごとの処方を出す</li><li>毎回の記録と、6週・12週の再診断を必ず行う</li>
 <li>判定基準を事前に決め、伸びた・伸びなかったを隠さず報告する</li><li>伸びない輪には、処方を変えて再挑戦する</li>
 <li>データは同意の範囲で匿名化して扱い、外に出さない</li></ul></div>
 <div class="card" style="flex:1;border-top:2mm solid #b54708"><h3>正直に言うこと</h3><ul style="padding-left:1.2em">
 <li>7つの輪・4つの型・処方の組み合わせは、既存の研究をもとにした<b>仮説</b>で、このプログラムで確かめていく</li>
 <li>テストの伸びが試合の伸びに届くとは限らない。だから3段階で分けて測る</li>
 <li>勝敗は監督の指導と選手の努力の結果。私が約束するのは、判断の土台の変化を<b>数字で示し、結論を出すこと</b></li></ul></div></div>
 <p style="margin-top:5mm;font-size:13pt;text-align:center"><b>最強のNo.2とは、監督の判断を「データで支える」存在です。</b></p>''')

# 13 参考
pg("このプログラムの土台にある考え方・研究", "参考文献",
 '''<ol style="padding-left:1.4em">
 <li style="font-size:10pt">Guadagnoli, M. A., & Lee, T. D. (2004). Challenge Point: A framework for conceptualizing the effects of various practice conditions in motor learning. Journal of Motor Behavior, 36(2), 212–224.</li>
 <li style="font-size:10pt">Pinder, R. A., Davids, K., Renshaw, I., & Araújo, D. (2011). Representative learning design and functionality of research and practice in sport. Journal of Sport & Exercise Psychology, 33(1), 146–155.（競技の形で鍛える考え方）</li>
 <li style="font-size:10pt">Hopkins, W. G. ほか. 意味のある最小の変化（smallest worthwhile change）に関する一連の論文・解説.（正式書誌は原典で確認）</li>
 <li style="font-size:10pt">Zhu ほか (2024). Effects of Perceptual-Cognitive Training on Anticipation and Decision-Making Skills in Team Sports: A Systematic Review and Meta-Analysis. Behavioral Sciences, 14(10), 919.</li>
 <li style="font-size:10pt">Fransen (2024). There is No Supporting Evidence for a Far Transfer of General Perceptual or Cognitive Training to Sports Performance. Sports Medicine.</li>
 <li style="font-size:10pt">Jordet ほか (2020). Scanning, Contextual Factors, and Association With Performance in English Premier League Footballers. Frontiers in Psychology.</li>
 <li style="font-size:10pt">Rönnqvist ほか (2018). Influences of Synchronized Metronome Training on Soccer Players' Timing Ability, Performance Accuracy, and Lower-Limb Kinematics. Frontiers in Psychology, 9, 2469.</li>
 <li style="font-size:10pt">ライフキネティックの研究：Yarayan ほか (2025) BMC Sports Sci Med Rehabil／Life, 16(5), 836 (2026)（営業資料の参考文献を参照）</li></ol>
 <p style="margin-top:3mm;font-size:10pt">遮断テスト（予測）、選択反応時間、ストループ、Go/No-Go、同期タッピング、多層ベースライン法は、心理学・スポーツ科学で一般的に使われる課題・方法です。</p>''')

out = os.path.join(os.path.dirname(__file__), "..", "プログラム設計書_判断の診断と処方.html")
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>判断の診断と処方</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print(len(P))
