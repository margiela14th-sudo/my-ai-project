"""コンディション管理（睡眠・食事・練習負荷・スケジュール）×AI の提案書（A4横）。"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import build_program as BP  # CSS を再利用（import 時に設計書も再生成される）
NAVY, ACC = BP.NAVY, BP.ACC
P = []
def pg(k, h, body, note=""):
    P.append(f'<section class="p"><p class="k">{k}</p><h1>{h}</h1>{body}' + (f'<p class="note">{note}</p>' if note else "") + f'<span class="n">{len(P)+1}</span></section>')

# 1 表紙
P.append(f'''<section class="p" style="background:{NAVY};color:#fff">
<svg style="position:absolute;right:30px;top:120px" width="460" height="460">
 <circle cx="230" cy="230" r="200" fill="none" stroke="#fff" stroke-opacity=".2" stroke-width="2"/>
 <circle cx="230" cy="230" r="80" fill="{ACC}"/><text x="230" y="222" font-size="22" text-anchor="middle" fill="{NAVY}" font-weight="bold">判断の</text><text x="230" y="252" font-size="22" text-anchor="middle" fill="{NAVY}" font-weight="bold">7つの輪</text>
 {''.join(f'<circle cx="{x}" cy="{y}" r="56" fill="#16305a" stroke="{ACC}" stroke-width="3"/><text x="{x}" y="{y+7}" font-size="20" text-anchor="middle" fill="#fff">{t}</text>' for x,y,t in [(230,40,"睡眠"),(420,230,"食事"),(230,420,"練習負荷"),(40,230,"予定")])}
</svg>
<div style="position:relative;max-width:150mm;margin-top:30mm"><p class="k" style="color:{ACC}">追加提案　｜　コンディション管理 × AI</p>
<h1 style="color:#fff;font-size:30pt">判断は、<br><span style="color:{ACC}">体の内側</span>から崩れる</h1>
<p style="font-size:13pt;color:#c7d2e3">睡眠・食事・練習負荷・予定を毎日1分で記録し、<br>判断の診断と同じデータの上で見える化する。</p></div>
<p style="position:absolute;left:13mm;bottom:10mm;font-size:10pt;color:#c7d2e3">フォロワーシップコーチ　〇〇 〇〇　｜　提案書（案）</p></section>''')

# 2 なぜ
pg("なぜコンディションなのか", "どんなに鍛えても、<em>寝不足の日の判断</em>は崩れる",
 f'''<div class="row" style="align-items:stretch">
 <div class="card" style="flex:1;text-align:center"><p style="font-size:11pt">13〜18歳に推奨される睡眠時間</p><p style="font-size:52pt;font-weight:bold;color:{NAVY};line-height:1.1">8〜10<span style="font-size:20pt">時間</span></p><p class="note" style="position:static">米国睡眠医学会の合意声明（Paruthi ほか, 2016）</p></div>
 <div class="card" style="flex:1;text-align:center"><p style="font-size:11pt">睡眠8時間未満の高校生アスリートのけがのリスク</p><p style="font-size:52pt;font-weight:bold;color:{NAVY};line-height:1.1">1.7<span style="font-size:20pt">倍</span></p><p class="note" style="position:static">8時間以上の選手との比較（Milewski ほか, 2014）</p></div>
 <div class="card" style="flex:1.3"><h3>判断の7つの輪とのつながり</h3><p>睡眠不足や疲労は、反応の速さ・注意・切り替え（L3〜L5）や、緊張下での安定（L7）に影響すると考えられています。<br><br>だから<b>判断のテストの日の睡眠・疲労も一緒に記録</b>し、「判断が伸びない理由」が練習内容なのか、コンディションなのかを分けて見ます。</p></div></div>''',
 "睡眠時間とけがの関係は観察研究で、因果関係を示したものではありません。数値は各論文の要旨にもとづき、提示前に原典で確認してください。")

# 3 毎日の記録
items = [("睡眠","寝た時刻・起きた時刻／ぐっすり度（1〜5）"),("体の状態","疲れ・筋肉痛・ストレス・気分（各1〜5）"),
         ("練習の強度と時間","きつさ（0〜10）× 練習時間（分）＝練習負荷"),("食事","朝食をとったか／主食・主菜・副菜・乳製品・果物がそろった回数／補食の回数"),
         ("予定","テスト・大会・遠征・行事（月の初めにまとめて入力）")]
rows = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a,b in items)
pg("毎日1分の記録", "スマホで<em>1分</em>。続けられる項目だけにしぼる",
 f'''<div class="row"><div style="flex:1.4"><table><tr><th style="width:25%">項目</th><th>入力すること</th></tr>{rows}</table>
 <p style="margin-top:3mm;font-size:10.5pt">体重・体脂肪・月経などの体の情報は、<b>このプログラムでは集めません</b>（必要な場合は医師・専門家が扱います）。</p></div>
 <div class="card" style="flex:1"><h3>続けるための工夫</h3><ul style="padding-left:1.2em"><li>入力は朝練前・寝る前の決まった時間に</li><li>選択式とスライダーが中心。文章は書かなくてよい</li><li>週1回、本人に「自分のグラフ」を返す（記録の意味を実感させる）</li><li>監督には個人の細かい記録ではなく、<b>気をつけたい選手の合図</b>だけを渡す</li></ul></div></div>''',
 "練習負荷（きつさ×時間）は、セッションRPE法（Foster ほか, 2001）として広く使われる方法です。")

# 4 見る指標
ind = [("睡眠","平均睡眠時間（目安8〜10時間）／寝る時刻のばらつき","8時間未満が3日以上続く"),
       ("体の状態","5項目の合計を、本人のふだんの値と比べる","ふだんより大きく下がった日が続く"),
       ("練習負荷","1週間の合計と、前の週からの増え方／毎日の負荷の変化の少なさ（単調さ）","急に増えた週、休みなく同じ強さが続く週"),
       ("食事","朝食をとった日の割合／基本形（5つ）がそろった回数／補食","朝食抜きが続く、練習量に対して食事の回数が少ない"),
       ("組み合わせ","テスト期間・大会前後の睡眠と負荷の重なり","睡眠が減る時期に負荷が上がる")]
rows = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a,b,c in ind)
pg("見る指標", "他人と比べず、<em>その選手の「ふだん」</em>と比べる",
 f'''<table><tr><th style="width:13%">分野</th><th style="width:47%">見る指標</th><th>声をかける合図（例）</th></tr>{rows}</table>
 <div class="card" style="margin-top:4mm"><p>高校生は成長の時期と体格の差が大きく、プロの数値をそのまま当てはめるのは適切ではありません。だから<b>その選手自身のふだんの値</b>を基準にし、そこから外れたときに気づける仕組みにします。合図の具体的な線は、最初の4週の記録を見てから監督と決めます。</p></div>''',
 "単調さ・負担度（monotony / strain）は Foster（1998）が提案した指標です。")

# 5 AI分析
ai = [("毎日","記録の抜けと合図のチェック","合図が出た選手を監督・本人に一言で知らせる（例：「睡眠が3日8時間未満。今日の練習の強さを相談」）"),
      ("毎週","1週間のまとめ","睡眠・負荷・体の状態のグラフを本人に返す。監督にはチーム全体の傾向"),
      ("月1回","予定と重ねた見通し","テスト・大会・遠征と過去の記録を重ね、「睡眠が減りやすい時期」「負荷が重なる週」を先に示す"),
      ("6週・12週","判断の診断と重ねる","判断の輪のスコアと、睡眠・負荷・体の状態の関係を個人ごとに確認（例：寝不足の週に L7 が下がる選手）")]
rows = "".join(f'<tr><td><b>{a}</b></td><td><b>{b}</b></td><td>{c}</td></tr>' for a,b,c in ai)
pg("AIでの分析", "記録を、<em>先回りの一言</em>に変える",
 f'''<table><tr><th style="width:11%">頻度</th><th style="width:22%">分析</th><th>出てくるもの</th></tr>{rows}</table>
 <div class="row" style="margin-top:4mm"><div class="card" style="flex:1"><h3>このプログラムならではの点</h3><p>判断の診断（7つの輪）と同じ選手番号でデータがつながるので、「判断が伸びない理由」をトレーニング・睡眠・疲労のどれにあるかで分けて考えられます。</p></div>
 <div class="card" style="flex:1"><h3>AIの使い方の約束</h3><p>AIには番号と数値だけを渡します。AIの出した結果は必ず人が確認し、<b>医学的な判断や診断はしません</b>。気になる変化は専門家につなぎます。</p></div></div>''')

# 6 役割の線引き
pg("役割の線引き", "私がやること、<em>専門家につなぐこと</em>、やらないこと",
 f'''<div class="row">
 <div class="card" style="flex:1;border-top:2mm solid {ACC}"><h3>私がやること</h3><ul style="padding-left:1.2em"><li>記録の仕組みづくりと見える化</li><li>睡眠・食事の<b>基本の習慣</b>についての声かけ・ミニ講座（朝食、寝る時刻、補食のタイミング）</li><li>練習負荷の推移を監督と共有</li><li>合図が出たときの声かけと連絡</li></ul></div>
 <div class="card" style="flex:1;border-top:2mm solid #3b82f6"><h3>専門家につなぐこと</h3><ul style="padding-left:1.2em"><li><b>個別の食事指導・献立</b> → 管理栄養士・公認スポーツ栄養士と連携</li><li>体重の大きな変化、疲れが抜けない、月経の乱れ、貧血の疑い → 保護者・養護教諭を通じて医師へ</li><li>気持ちの落ち込みが続く → スクールカウンセラー等</li></ul></div>
 <div class="card" style="flex:1;border-top:2mm solid #b54708"><h3>やらないこと</h3><ul style="padding-left:1.2em"><li>体重・体脂肪の目標設定や減量の指導</li><li>サプリメントの勧め</li><li>病気やけがの診断</li><li>食事の量を減らす指導</li></ul></div></div>
 <p style="margin-top:4mm;font-size:11pt">成長期の選手は、練習量に対して食事が足りないと、体の成長・骨・ホルモン・パフォーマンスに影響が出ることが知られています（スポーツにおける相対的エネルギー不足：REDs）。<b>「減らす」方向の指導はせず、気づいたら専門家につなぐ</b>のが、この線引きの理由です。</p>''',
 "REDs：国際オリンピック委員会の合意声明（Mountjoy ほか, 2023）。")

# 7 予定の管理
pg("スケジュール管理", "大会から<em>逆算</em>して、睡眠と負荷の山をずらす",
 f'''<svg width="1080" height="270" viewBox="0 0 1080 270">
 {''.join(f'<rect x="{40+i*82}" y="{220-h}" width="60" height="{h}" rx="5" fill="{c}"/><text x="{70+i*82}" y="245" font-size="14" text-anchor="middle" fill="#5a6476">{i+1}週</text>' for i,(h,c) in enumerate([(110,"#c3cad6"),(130,"#c3cad6"),(150,"#c3cad6"),(170,"#e5484d"),(100,"#c3cad6"),(140,"#c3cad6"),(160,"#c3cad6"),(150,"#c3cad6"),(110,ACC),(80,ACC),(60,ACC),(40,NAVY)]))}
 <text x="356" y="40" font-size="15" text-anchor="middle" fill="#e5484d">定期テスト（睡眠が減りやすい）</text><path d="M356 48 v118" stroke="#e5484d" stroke-dasharray="5 5"/>
 <text x="1010" y="155" font-size="15" text-anchor="middle" fill="{NAVY}" font-weight="bold">大会</text>
 <text x="840" y="110" font-size="14" text-anchor="middle" fill="#5c7500">大会前は負荷を下げ、睡眠を確保</text>
 <text x="40" y="20" font-size="13" fill="#5a6476">棒＝練習負荷の計画（模式図）</text></svg>
 <div class="row" style="margin-top:2mm"><div class="card" style="flex:1"><p><b>月の初め：</b>テスト・大会・遠征・行事を入力。AIが「負荷と睡眠不足が重なりやすい週」を示し、監督が練習計画を調整する材料にします。</p></div>
 <div class="card" style="flex:1"><p><b>大会前：</b>寝る時刻・起きる時刻を試合の時間に合わせていく、遠征時の食事と補食の準備など、<b>習慣の準備</b>を本人と一緒に確認します。</p></div></div>''',
 "図は考え方を示す模式図で、特定のチームの計画ではありません。練習計画を決めるのは監督です。")

# 8 進め方とプラン
pg("進め方とプラン（案）", "判断のトレーニングに<em>オプションとして追加</em>",
 '''<table><tr><th style="width:16%">時期</th><th>内容</th></tr>
 <tr><td><b>開始前</b></td><td>学校・保護者への説明、同意書（コンディション記録の項目を追加）、管理栄養士など連携先の確認</td></tr>
 <tr><td><b>1〜4週</b></td><td>毎日1分の記録を習慣にする。各選手の「ふだん」の値をつくる。睡眠・食事のミニ講座（各15分）</td></tr>
 <tr><td><b>5〜12週</b></td><td>合図の運用開始。週1回の本人へのグラフ返却、監督へのチームの傾向報告。6週・12週に判断の診断と重ねて分析</td></tr></table>
 <div class="row" style="margin-top:4mm"><div class="card" style="flex:1"><h3>オプション料金（案）</h3><p>判断トレーニングのプランに<b>月額 〇〇,〇〇〇円</b>を追加（部員数に応じて調整）。管理栄養士の個別指導は別途。</p></div>
 <div class="card" style="flex:1"><h3>まずは試しに</h3><p>無料トライアルの6週のうち、後半の3週で睡眠と練習負荷の記録だけを試すこともできます。</p></div></div>''',
 "料金は空欄にしてあります。連携する専門家の費用も含めて設定してください。")

# 9 参考文献
pg("参考文献", "本資料で引用した研究・指針",
 '''<ol style="padding-left:1.4em">
 <li style="font-size:10pt">Paruthi, S. ほか (2016). Recommended amount of sleep for pediatric populations: a consensus statement of the American Academy of Sleep Medicine. Journal of Clinical Sleep Medicine, 12(6), 785–786.</li>
 <li style="font-size:10pt">Milewski, M. D. ほか (2014). Chronic lack of sleep is associated with increased sports injuries in adolescent athletes. Journal of Pediatric Orthopaedics, 34(2), 129–133.</li>
 <li style="font-size:10pt">Foster, C. ほか (2001). A new approach to monitoring exercise training. Journal of Strength and Conditioning Research, 15(1), 109–115.（セッションRPE法）</li>
 <li style="font-size:10pt">Foster, C. (1998). Monitoring training in athletes with reference to overtraining syndrome. Medicine & Science in Sports & Exercise, 30(7), 1164–1168.（単調さ・負担度）</li>
 <li style="font-size:10pt">Mountjoy, M. ほか (2023). 2023 International Olympic Committee's (IOC) consensus statement on Relative Energy Deficiency in Sport (REDs). British Journal of Sports Medicine, 57(17), 1073–1097.</li>
 <li style="font-size:10pt">Desbrow, B. ほか (2014). Sports Dietitians Australia position statement: sports nutrition for the adolescent athlete. International Journal of Sport Nutrition and Exercise Metabolism, 24(5), 570–584.</li>
 <li style="font-size:10pt">厚生労働省「日本人の食事摂取基準（2025年版）」（年齢・身体活動レベル別の基準。具体の数値は原典で確認）</li></ol>
 <p style="margin-top:3mm;font-size:10pt">巻号・ページは記憶にもとづく記載を含みます。提示前に原典で確認してください。</p>''')

out = os.path.join(os.path.dirname(__file__), "..", "提案書_コンディション管理.html")
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>コンディション管理の提案</title><style>{BP.CSS}</style></head><body>{"".join(P)}</body></html>')
print(len(P))
