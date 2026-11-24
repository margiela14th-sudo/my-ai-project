# -*- coding: utf-8 -*-
"""研究資料（Word, A4縦・1段組み）を生成する。
実行：python3 06_制作途中/build_docx.py → 07_完成資料/県大会研究資料_生成AI授業再構築.docx
"""
import os
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "07_完成資料", "県大会研究資料_生成AI授業再構築.docx")
MIN, GOT = "ＭＳ 明朝", "ＭＳ ゴシック"
G = RGBColor(0x2E, 0x8B, 0x3A); R = RGBColor(0xC0, 0x39, 0x2B)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Mm(210), Mm(297)
sec.top_margin = sec.bottom_margin = Mm(22); sec.left_margin = sec.right_margin = Mm(22)
st = doc.styles["Normal"]; st.font.name = "Century"; st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), MIN)
st.paragraph_format.space_after = Pt(2); st.paragraph_format.line_spacing = 1.15


def run(p, text, bold=False, color=None, size=None, font=None):
    r = p.add_run(text); r.bold = bold
    if color: r.font.color.rgb = color
    if size: r.font.size = Pt(size)
    if font:
        r.font.name = font; r._element.rPr.rFonts.set(qn("w:eastAsia"), font)
    return r


def para(text="", bold=False, align=None, size=None, font=None, color=None, indent=True):
    p = doc.add_paragraph()
    if align is not None: p.alignment = align
    if indent and align is None: p.paragraph_format.first_line_indent = Pt(10.5)
    if text: run(p, text, bold, color, size, font)
    return p


def h1(text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(3)
    run(p, text, True, G, 12, GOT)
    pPr = p._p.get_or_add_pPr(); bdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "1"), ("w:color", "2E8B3A")): b.set(qn(k), v)
    bdr.append(b); pPr.append(bdr)


def h2(text):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(4); run(p, text, True, None, 10.5, GOT)


def bullet(text, mark="・"):
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Pt(10.5); p.paragraph_format.first_line_indent = Pt(-10.5)
    run(p, mark + text); return p


def table(rows, widths, header=True, size=9):
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.width = Mm(widths[j]); c.text = ""
            p = c.paragraphs[0]; p.paragraph_format.first_line_indent = Pt(0)
            run(p, v, bold=header and i == 0, size=size, font=GOT if header and i == 0 else None)
            if header and i == 0:
                tcPr = c._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "E8F3EA"); tcPr.append(shd)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def fig(path, width_mm, cap):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(path, width=Mm(width_mm))
    c = doc.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER; run(c, cap, size=9)


# 表題
para("令和8年度 山口県中学校数学教育研究協議会", align=WD_ALIGN_PARAGRAPH.LEFT, size=9)
para("生成AIを活用した数学科授業の改善と新たな授業モデルの提案", True, WD_ALIGN_PARAGRAPH.CENTER, 15, GOT)
para("～関数分野における従来の授業実践を通して～", False, WD_ALIGN_PARAGRAPH.CENTER, 12, GOT)
para("下関市立名陵中学校　新田正幸", False, WD_ALIGN_PARAGRAPH.RIGHT, 10.5)

h1("１．研究主題設定の理由")
para("教員採用選考の受験者数は減少しており、公立中学校の採用倍率は平成12年度の17.9倍から令和7年度の3.6倍へと低下し、過去最低となった（文部科学省，2025）。ただし、この低下には大量退職に伴う採用者数の増加（平成12年度2,673人→令和7年度10,168人）も影響しており、受験者数の減少は教員総数の減少を意味するものではない。山口県の中学校数学は、令和7年度採用で受験者37人、採用者17人、2.2倍であった。")
para("また、令和4年度の教員勤務実態調査によると、中学校教諭の平日の在校等時間は11時間1分で、平成28年度より31分減少した一方、授業準備の時間は1時間26分から1時間23分とほとんど変わっていない（文部科学省，2024）。教師不足は、令和3年度始業日時点で中学校868人と報告されている（文部科学省，2022）。")
para("教職の大変さは近年に始まったことではない。SNSや報道によって勤務実態が可視化されたことも、教職の魅力や職業選択に影響しているのではないかと考えている。ただし、これは発表者の仮説であり、因果関係が確かめられたものではない。教員数が増えることだけに依存せず、今いる教員で教育の質を維持・向上させるための改善を考えたいと考え、本主題を設定した。")
fig(os.path.join(ROOT, "02_統計データ", "図1_中学校_受験者数と採用倍率.png"), 140, "図1　公立中学校 教員採用選考の受験者数と採用倍率の推移（文部科学省 参考資料1 第7表より作成）")

h1("２．数学的な視点からの問題解決")
para("教員の業務負担を、次の簡易的な数学的モデルで表す。")
para("B ＝ W ÷（N × E）", True, WD_ALIGN_PARAGRAPH.CENTER, 13, GOT)
para("B：教員1人当たりの平均業務時間、W：学校全体の業務量（従来の標準作業時間に換算）、N：教員数、E：業務効率（従来を1とする）。Wを一定とみれば、BはN×Eに反比例する。したがって、Bを減らす方法は、①Nを増やす、②Wを減らす、③Eを高める、の三つである。")
table([["条件", "教員数N", "標準業務量W", "業務効率E", "1人当たりB"], ["現状", "20人", "200時間", "100％", "10時間"], ["解決策①", "25人", "200時間", "100％", "8時間"],
       ["解決策②", "20人", "160時間", "100％", "8時間"], ["解決策③", "20人", "200時間", "125％", "8時間"], ["複合型", "20人", "180時間", "120％", "7.5時間"]], [28, 28, 32, 28, 32])
para("この表の値は実測値ではなく、仮定に基づくモデルである。業務の均等配分や一様な効率改善を仮定しており、個人差や精神的な負担は表現できない。Nを25％増やしてもBは20％しか減らない（反比例）ことなど、比例・反比例・百分率といった中学校数学の内容で学校の課題を考察できる。③は人員も業務量も減らさずにBを減らす方法であり、本研究はこの③に焦点を当て、生成AIを活用した数学科授業の改善へとつなげる。")

h1("３．研究仮説")
p = para("従来の数学科授業実践における数学的な価値や教師の指導意図を継承しながら、生成AIを活用して授業を再構築することで、教師の授業準備に関わる負担を軽減するとともに、生徒の数学的な見方・考え方を働かせる授業の実現につながるのではないか。", True)

h1("４．研究の内容と方法")
for t in ["（１）関数分野における過去の授業実践（1年 比例、2年 一次関数、3年 関数y＝ax²）を振り返り、数学的な価値と課題を整理する。",
          "（２）生成AIを活用した授業再構築モデル「AI LESSON REMAKE」を作成する。",
          "（３）リメイク授業と動的教材を提案し、教師側・生徒側の検証計画を立てる。なお、本発表の時点ではリメイク授業は未実践であり、成果ではなく、期待される効果と検証計画として示す。"]:
    bullet(t, "")

h1("５．従来の関数分野の授業実践")
table([["学年・単元", "題材・中心発問", "数学的な価値"],
       ["1年 比例", "地震：初期微動継続時間と震源からの距離", "比例とみなし、距離を求める"],
       ["2年 一次関数", "山口県の2月の平均気温とソメイヨシノの開花日「さくらの開花には何が影響しているのか」", "一次関数とみなし、開花日を予想する（2015年の2月の平均気温7.5℃から3月27日頃と予想し、実際の開花日も3月27日であった）"],
       ["3年 関数y＝ax²", "巨大ブランコ・振り子「ひもの長さと1往復にかかる時間にはどのような関係があるだろうか」", "実測データをy＝ax²とみなし、周期2秒の振り子をつくる（y＝0.25x²）"]], [30, 70, 66])
para("3年の振り子の授業は、2021年の第103回全国算数・数学教育研究（埼玉）大会で発表した（新田・山本，2021）。成果として、○ICT（GeoGebra）で「2乗に比例する関数とみなす」活動がしやすくなった、○実測値をもとに予想し解決できたことで数学的活動が深まった、○実物の振り子とICTを関連づけて主体的に取り組んだ、の3点を挙げた。課題として、●振り返りシートでICTの効果を計る項目を具体的に設ける必要がある、●ICTを扱う授業内のタイミングは検討の余地がある（実物の振り子を使う良さもある）、の2点を挙げた。本研究はこの課題を出発点とする。")

h1("６．AI LESSON REMAKE（生成AIを活用した数学科授業再構築モデル）")
table([["STEP", "内容", "主体"], ["1", "過去の授業資料を生成AIに入力する（生徒の個人情報は入力しない）", "教師"], ["2", "従来の授業の良かった点を三つ整理する", "AI案→教師"],
       ["3", "従来の授業の課題を三つ整理する（過去の研究の課題を入力する）", "AI案→教師"], ["4", "生成AIに複数の改善案を提案させる", "AI"],
       ["5", "教師が数学的な妥当性と教育的価値を吟味する", "教師"], ["6", "「残す・変える・削る」の三つの視点から授業を再構築する", "教師"], ["7", "授業実践、評価、検証、再改善を行う", "教師・生徒"]], [14, 120, 32])
para("STEP5・6は教師の判断であり、生成AIに判断を丸投げしない。「残す」は授業の本質（数学的な価値、中心発問、生徒が考える時間、実物に触れる体験）、「変える」は本質にたどり着くための手段（教材の形、データの扱い方、支援の出し方）、「削る」は本質に寄与しない作業（手作業の転記、毎年のデータ打ち直し、教材の作り直し）である。既存のAIツールは、導入発問メーカー・数学教材生成ツール（STEP4）、板書型指導案メーカー・学習指導案メーカー（STEP6）、振り返り自動化（STEP7）として位置づける。")

h1("７．リメイク授業の提案")
h2("（１）重点事例：3年「振り子」")
table([["比較項目", "Before（2021年の実践）", "After（提案）"], ["導入・中心発問", "巨大ブランコ／長さと1往復の時間の関係は？", "同じ（残す）"],
       ["自力解決", "実物の振り子を測る→点をとる", "実物で測る（残す）→振り子ラボに入力"], ["練り上げ", "GeoGebraで関数を重ね、見た目で比べる", "関数ごとの「ずれ」を数値で比べ、根拠をもってみなす"],
       ["個別の支援", "机間指導", "3段階のヒント（正解はすぐに見せない）"], ["数学的考察", "y＝0.25x²、周期2秒→1m", "「AIの答え」を検証する、成立条件にふれる"],
       ["振り返り", "わかったこと・理解度", "ICTの効果を計る項目を追加（2021年の課題）"], ["教材研究・準備", "教材を個人で作成・修正", "AIで案を作り、教師が検証（時間を記録）"]], [30, 64, 72])
para("生成AIと協働して、ブラウザで動く単一HTMLの教材「振り子ラボ」を作成した。実物で測定したデータを入力すると表とグラフが連動し、生徒は比例・一次関数・反比例・y＝ax²から関数を選び、係数を動かして点に近づける。2021年の授業データでは、y＝0.25x²のときの点とグラフのずれ（平均）は0.025m、比例y＝0.45xでは0.138mであり、見た目だけでなく数値を根拠に「y＝ax²とみなす」ことを説明できる。また、「ある生成AIは『振り子の長さは周期に比例する』と答えた。正しいか」と問い、AIの回答をデータで検証させる。")
para("数学的な妥当性として、単振り子の周期T＝2π√(L/g)よりL＝(g/4π²)T²であり、g/4π²≒0.248である。授業のa≒0.25はこれとよく一致し、周期2秒の長さは約0.99mとなる。この関係は振れ幅が小さいときの近似であり、教材では振れ幅を変えて確かめられるようにした。")
fig(os.path.join(ROOT, "05_数学教材", "振り子ラボ_画面.png"), 130, "図2　振り子ラボ（2021年の授業データを入力し、y＝0.25x²を当てはめた画面）")
h2("（２）2年「ソメイヨシノの開花日」")
para("2017年までのデータを、生成AIの補助で最新年まで整える（数値は教師が気象庁の原典と照合する）。生徒は散布図に自分で直線を引き、2点から式を求めて開花日を予想する。資料のデータでは、2月の平均気温が1℃上がると開花日はおよそ3日早まる程度であり、「気温が1℃上がると開花は10日早くなる」というAIの誤った回答をデータで検証させる。")
h2("（３）1年「地震と比例」")
para("初期微動継続時間と震源からの距離の比例関係を、観測点のデータで確かめる教材を構想している。比例定数を「1秒あたり何kmか」と解釈させ、理科との関連を図る。")

h1("８．期待される効果と研究の限界、今後の検証")
para("期待される効果（未検証）：○教材・指導案・板書計画の準備時間の短縮、○段階的ヒントによる基礎の理解の支援、○数値の根拠をもって関数とみなす説明、○AIの回答を数学的に検証する力。")
para("研究の限界：●B＝W÷(N×E)は簡易的な仮定に基づくモデルである。●時間短縮や理解の向上は未測定である。●AIの出力の確認・修正にも時間がかかる。●生徒の個人情報を入力しない運用が前提である。")
para("今後の検証：教師側は授業準備・教材作成・指導案・板書計画・AI出力の確認修正の時間と心理的負担を、生徒側は基礎的な内容の到達率、数学的な説明、つまずく生徒への支援、得点分布、振り返りの内容を、改善の前後で比較する。時間削減率は次式で求める。")
para("時間削減率（％）＝（改善前の時間－改善後の時間）÷改善前の時間×100", True, WD_ALIGN_PARAGRAPH.CENTER)

h1("９．おわりに")
para("本研究で伝えたいことは、過去の教育実践を否定することではない。これまでの優れた実践を継承しながら、生成AIを手段として活用し、より良い数学科授業を実現することである。変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。教育の質を守るために、教師の時間を守る。")

h1("参考・引用文献")
for t in ["文部科学省（2017）中学校学習指導要領（平成29年告示）解説 数学編",
          "文部科学省（2022）「教師不足」に関する実態調査 https://www.mext.go.jp/content/20220128-mxt_kyoikujinzai01-000020293-1.pdf",
          "文部科学省（2024）教員勤務実態調査（令和4年度）集計【確定値】 https://www.mext.go.jp/content/20240404-mxt_zaimu01-100003067-1.pdf",
          "文部科学省（2025）令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況等 参考資料1 https://www.mext.go.jp/content/20261001-kyoikushokuin-000046447_2.pdf",
          "新田正幸・山本剛（2021）「主体的・対話的で深い学び」の視点からの授業改善 ～関数y＝ax²におけるICT活用をとおして～，第103回全国算数・数学教育研究（埼玉）大会",
          "啓林館「未来へひろがる数学3」",
          "気象庁「過去の気象データ」"]:
    bullet(t, "◆")

doc.save(OUT); print("saved", OUT)
