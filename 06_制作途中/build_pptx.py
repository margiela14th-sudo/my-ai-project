# -*- coding: utf-8 -*-
"""県大会発表スライドを生成する（python-pptx）。
実行：python3 06_制作途中/build_pptx.py  → 07_完成資料/県大会発表_生成AI授業再構築.pptx
"""
import csv, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "07_完成資料", "県大会発表_生成AI授業再構築.pptx")
FONT = "Meiryo"
G = RGBColor(0x2E, 0x8B, 0x3A); LG = RGBColor(0xE8, 0xF3, 0xEA)
R = RGBColor(0xC0, 0x39, 0x2B); B = RGBColor(0x1F, 0x5F, 0xAD)
Y = RGBColor(0xFF, 0xF4, 0xB8); K = RGBColor(0x22, 0x22, 0x22)
GR = RGBColor(0x77, 0x77, 0x77); W = RGBColor(0xFF, 0xFF, 0xFF); LGR = RGBColor(0xF2, 0xF2, 0xF2)

TITLE = "生成AIを活用した数学科授業の改善と新たな授業モデルの提案"
SUB = "～関数分野における従来の授業実践を通して～"
FOOT = "山口県中学校数学教育研究協議会 発表資料　" + TITLE
DATE = "2026/11/26"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BL = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height


def tb(s, x, y, w, h, paras, size=20, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, fill=None, line=None):
    """paras: list of paragraphs; each paragraph is str or list of runs (text, {color,bold,size})."""
    shp = s.shapes.add_textbox(x, y, w, h) if fill is None and line is None else s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    if fill is not None or line is not None:
        shp.adjustments[0] = 0.06
        if fill is None: shp.fill.background()
        else:
            shp.fill.solid(); shp.fill.fore_color.rgb = fill
        if line is None: shp.line.fill.background()
        else:
            shp.line.color.rgb = line; shp.line.width = Pt(1.5)
        shp.shadow.inherit = False
    tf = shp.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.12); tf.margin_top = tf.margin_bottom = Inches(0.06)
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align; para.space_after = Pt(4)
        runs = [(p, {})] if isinstance(p, str) else p
        for t, o in runs:
            r = para.add_run(); r.text = t
            f = r.font; f.name = FONT; f.size = Pt(o.get("size", size)); f.bold = o.get("bold", False)
            f.color.rgb = o.get("color", K)
            rPr = r._r.get_or_add_rPr()
            for tag in ("a:ea",):
                pass
            r.font._element.get_or_add_latin().set("typeface", FONT)
            ea = rPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}ea")
            if ea is None:
                from lxml import etree
                ea = etree.SubElement(rPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}ea")
            ea.set("typeface", FONT)
    return shp


def base(title, notes, sec=None):
    s = prs.slides.add_slide(BL)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(0.3), Inches(0.14), Inches(0.62))
    bar.fill.solid(); bar.fill.fore_color.rgb = G; bar.line.fill.background()
    tb(s, Inches(0.6), Inches(0.22), Inches(10.6), Inches(0.8), [[(title, {"bold": True})]], size=28, anchor=MSO_ANCHOR.MIDDLE)
    if sec:
        tb(s, Inches(10.9), Inches(0.32), Inches(2.1), Inches(0.5), [[(sec, {"color": G, "bold": True})]], size=14, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    ln = s.shapes.add_connector(1, Inches(0.35), Inches(1.02), Inches(12.98), Inches(1.02)); ln.line.color.rgb = G; ln.line.width = Pt(1.25)
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.12), SW, Inches(0.38)); band.fill.solid(); band.fill.fore_color.rgb = G; band.line.fill.background()
    tb(s, Inches(0.3), Inches(7.12), Inches(10.5), Inches(0.38), [[(FOOT, {"color": W})]], size=10, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, Inches(10.8), Inches(7.12), Inches(2.3), Inches(0.38), [[(f"{DATE}　{len(prs.slides)}", {"color": W})]], size=10, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    s.notes_slide.notes_text_frame.text = notes
    return s


def font_chart(ch, size=12):
    ch.font.name = FONT; ch.font.size = Pt(size)


# ---------- 1 表紙 ----------
s = prs.slides.add_slide(BL)
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.45), Inches(0.14), Inches(0.45)); bar.fill.solid(); bar.fill.fore_color.rgb = G; bar.line.fill.background()
tb(s, Inches(0.75), Inches(0.38), Inches(9), Inches(0.6), ["令和8年度 山口県中学校数学教育研究協議会"], size=18, anchor=MSO_ANCHOR.MIDDLE)
tb(s, Inches(0.9), Inches(2.1), Inches(11.6), Inches(1.4), [[(TITLE, {"bold": True})]], size=36, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
tb(s, Inches(0.9), Inches(3.45), Inches(11.6), Inches(0.7), [SUB], size=24, align=PP_ALIGN.CENTER)
tb(s, Inches(2.2), Inches(4.5), Inches(9), Inches(0.9), [[("変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。", {"color": G, "bold": True})]], size=18, align=PP_ALIGN.CENTER, fill=LG)
tb(s, Inches(7.3), Inches(5.9), Inches(5.6), Inches(0.9), ["下関市立東部中学校　新田 正幸"], size=20, align=PP_ALIGN.RIGHT)
band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.12), SW, Inches(0.38)); band.fill.solid(); band.fill.fore_color.rgb = G; band.line.fill.background()
s.notes_slide.notes_text_frame.text = (
    "【0:20】今から、「生成AIを活用した数学科授業の改善と新たな授業モデルの提案 ～関数分野における従来の授業実践を通して～」という題で発表をします。"
    "下関市立東部中学校の新田です。よろしくお願いします。")

# ---------- 2 はじめに ----------
s = base("はじめに　これまでの研究の延長として", (
    "【0:30】まず、今回の研究の位置づけです。2021年は、関数y＝ax²の授業でGeoGebraを使い、ICTで「2乗に比例する関数とみなす」ことを支える授業を発表しました。"
    "2022年はジグソー法による協働的な学び、2023年はねじれの位置を説明する授業での教師の手立てを発表しました。"
    "どれも、良い授業を新しい手段で改善するという研究です。今回はその手段が生成AIです。授業の本質は変えずに、本質にたどり着くための手段を見直します。"), "はじめに")
items = [("2021", "ICT活用", "GeoGebra\n関数y＝ax²・振り子"), ("2022", "ジグソー法", "協働的な学び\n正負の数・文字式"), ("2023", "教師の手立て", "ねじれの位置を\n説明する授業"), ("2026", "生成AI", "関数分野の授業を\n再構築する")]
for i, (yr, means, th) in enumerate(items):
    x = Inches(0.6 + i * 3.15); last = i == 3
    tb(s, x, Inches(1.55), Inches(2.8), Inches(0.7), [[(yr, {"bold": True, "color": W})]], size=24, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=R if last else G)
    tb(s, x, Inches(2.35), Inches(2.8), Inches(2.4), [[(means, {"bold": True, "color": R if last else G})], th], size=20, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line=R if last else G)
    if i < 3:
        a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x + Inches(2.83), Inches(3.35), Inches(0.3), Inches(0.4)); a.fill.solid(); a.fill.fore_color.rgb = GR; a.line.fill.background()
tb(s, Inches(0.6), Inches(5.15), Inches(12.1), Inches(1.6), [[("共通する考え：", {"bold": True}), ("従来の良い授業を否定せず、", {}), ("新しい手段", {"color": R, "bold": True}), ("で改善する", {})],
   [("2021年の課題●「ICTの効果を計る項目」「ICTを扱うタイミング」を、今回の出発点にする", {"color": B})]], size=20, fill=Y)

# ---------- 3 現状① ----------
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "02_統計データ", "全国_教員採用選考_長期推移.csv"), encoding="utf-8-sig")) if int(r["西暦(採用年度)"]) >= 2000]
lab = [r["採用年度"].replace("年度", "").replace("平成", "H").replace("令和", "R").replace("元", "1") for r in rows]
s = base("教員を志望する人が減り、採用倍率は過去最低", (
    "【0:50】第1章、教育現場の現状です。左は公立中学校の教員採用選考の受験者数です。平成25年度の約6万3千人をピークに、令和7年度は約3万7千人に減っています。"
    "右は採用倍率で、平成12年度の17.9倍から、令和7年度は3.6倍と過去最低です。"
    "ただし、倍率の低下には、大量退職に伴って採用者数が増えたことも影響しています。また、これは受験者数の推移であり、教員の総数が減っているという意味ではありません。"
    "山口県の中学校数学は、令和7年度、受験者37人、採用者17人、2.2倍でした。"), "第1章")
cd = CategoryChartData(); cd.categories = lab; cd.add_series("中学校 受験者数（人）", [int(r["中学校_受験者数"]) for r in rows])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.4), Inches(1.2), Inches(6.3), Inches(4.9), cd); ch = gf.chart; font_chart(ch, 11)
ch.has_title = True; ch.chart_title.text_frame.text = "中学校 受験者数（人）"; ch.has_legend = False
ch.plots[0].series[0].format.fill.solid(); ch.plots[0].series[0].format.fill.fore_color.rgb = G; ch.plots[0].gap_width = 40
cd2 = CategoryChartData(); cd2.categories = lab; cd2.add_series("中学校 採用倍率（倍）", [float(r["中学校_競争率"]) for r in rows])
gf2 = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(6.8), Inches(1.2), Inches(6.2), Inches(4.9), cd2); ch2 = gf2.chart; font_chart(ch2, 11)
ch2.has_title = True; ch2.chart_title.text_frame.text = "中学校 採用倍率（倍）"; ch2.has_legend = False
sr = ch2.plots[0].series[0]; sr.format.line.color.rgb = R; sr.format.line.width = Pt(2.5); sr.smooth = False
for idx in (0, len(rows) - 1):
    pt = sr.points[idx]; pt.data_label.has_text_frame = False; pt.data_label.show_value = True; pt.data_label.position = XL_LABEL_POSITION.ABOVE
    pt.data_label.font.size = Pt(16); pt.data_label.font.bold = True; pt.data_label.font.color.rgb = R
tb(s, Inches(0.4), Inches(6.15), Inches(12.6), Inches(0.9), [
    [("H12：17.9倍 → R7：3.6倍（過去最低）　", {"color": R, "bold": True}), ("山口県 中学校数学 R7：受験37人・採用17人・2.2倍", {"bold": True})],
    [("出典：文部科学省「令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況等」参考資料1 第7表・第9表（単位：人、倍）。受験者数の推移であり、教員総数の推移ではない。", {"size": 10, "color": GR})]], size=16)

# ---------- 4 現状② ----------
s = base("在校時間は減ったが、授業準備の時間は減っていない", (
    "【0:50】次に勤務実態です。文部科学省の令和4年度の教員勤務実態調査では、中学校教諭の平日の在校等時間は11時間1分で、平成28年度より31分減りました。"
    "一方で、授業準備は1時間26分から1時間23分と、ほとんど変わっていません。授業そのものは増えています。"
    "教師不足も、令和3年度の始業日時点で、中学校で868人と報告されています。"
    "教職の大変さは以前からありましたが、SNSや報道で勤務の実態が見えるようになったことも、職業選択に影響しているのではないか、と私は考えています。ただし、これは私の仮説で、因果関係は確かめられていません。"
    "教員が増えることを待つだけでなく、今いる教員で教育の質をどう守るかを考えたいと思いました。"), "第1章")
items = [("授業（主担当）", 196), ("授業準備", 83), ("生徒指導（集団）", 54), ("朝の業務", 44), ("部活動・クラブ活動", 37), ("成績処理", 36), ("学年・学級経営", 27)]
cd = CategoryChartData(); cd.categories = [n for n, _ in items][::-1]; cd.add_series("令和4年度（分）", [v for _, v in items][::-1])
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.4), Inches(1.2), Inches(7.6), Inches(5.0), cd); ch = gf.chart; font_chart(ch, 12)
ch.has_title = True; ch.chart_title.text_frame.text = "中学校教諭 平日1日の業務別時間（分）R4"; ch.has_legend = False
pl = ch.plots[0]; pl.gap_width = 40; pl.has_data_labels = True; pl.data_labels.font.size = Pt(12)
sr = pl.series[0]; sr.format.fill.solid(); sr.format.fill.fore_color.rgb = RGBColor(0x9B, 0xBF, 0x9F)
p = sr.points[len(items) - 2]; p.format.fill.solid(); p.format.fill.fore_color.rgb = R
tb(s, Inches(8.3), Inches(1.3), Inches(4.7), Inches(1.7), [[("平日の在校等時間", {"bold": True})], [("11:32 → 11:01（−31分）", {"size": 22})]], size=18, line=G)
tb(s, Inches(8.3), Inches(3.15), Inches(4.7), Inches(1.7), [[("授業準備（平日）", {"bold": True, "color": R})], [("1:26 → 1:23（−3分）", {"size": 22, "color": R, "bold": True})]], size=18, fill=Y)
tb(s, Inches(8.3), Inches(5.0), Inches(4.7), Inches(1.2), [[("教師不足（R3始業日）", {"bold": True})], "中学校 868人（不足率0.40%）"], size=16, line=G)
tb(s, Inches(0.4), Inches(6.3), Inches(12.6), Inches(0.7), [[("出典：文部科学省「教員勤務実態調査（令和4年度）集計【確定値】」（10・11月、時間:分）、「『教師不足』に関する実態調査」（令和4年1月）。", {"size": 10, "color": GR})]], size=10)

# ---------- 5 数学で考える ----------
s = base("数学で考える：B ＝ W ÷（N × E）", (
    "【0:50】第2章です。この問題を数学で考えてみます。教員1人当たりの平均業務時間をB、学校全体の業務量をW、教員数をN、業務効率をEとすると、B＝W÷（N×E）と表せます。"
    "Wを一定とみれば、BはN×Eに反比例します。つまり、Bを減らす方法は、Nを増やす、Wを減らす、Eを高めるの三つです。"
    "これは実測値ではなく、業務を均等に分け、効率が一様に上がると仮定した簡易的なモデルです。個人差や精神的な負担は表せません。"), "第2章")
tb(s, Inches(2.2), Inches(1.35), Inches(8.9), Inches(1.3), [[("B ＝ W ÷（N × E）", {"bold": True, "size": 48})]], size=48, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=LG)
defs = [("B", "教員1人当たりの平均業務時間"), ("W", "学校全体の業務量（従来の標準時間に換算）"), ("N", "教員数"), ("E", "業務効率（従来を1とする）")]
for i, (k, v) in enumerate(defs):
    tb(s, Inches(1.2 + (i % 2) * 5.6), Inches(2.95 + (i // 2) * 0.85), Inches(5.4), Inches(0.75), [[(k + "：", {"bold": True, "color": G}), (v, {})]], size=20)
sol = [("①　N を増やす", "採用・人材確保・復職支援・外部人材"), ("②　W を減らす", "業務の精選・会議削減・行事の再設計"), ("③　E を高める", "生成AI・教材の再利用・準備の効率化")]
for i, (h, d) in enumerate(sol):
    tb(s, Inches(0.6 + i * 4.15), Inches(4.75), Inches(3.95), Inches(1.45), [[(h, {"bold": True, "color": R if i == 2 else G})], [(d, {"size": 15})]], size=22, align=PP_ALIGN.CENTER, line=R if i == 2 else G, fill=Y if i == 2 else None)
tb(s, Inches(0.6), Inches(6.35), Inches(12.2), Inches(0.6), [[("※ 実測値ではなく仮定に基づく簡易モデル（業務の均等配分・一様な効率改善を仮定。個人差や精神的負担は表せない）", {"size": 13, "color": GR})]], size=13)

# ---------- 6 シミュレーション ----------
s = base("三つの解決策で、1人当たりの業務時間はどう変わるか", (
    "【0:40】仮の数値で計算してみます。教員20人、業務量200時間なら、1人10時間です。教員を25人にすると8時間、業務量を160時間にすると8時間、効率を125％にしても8時間です。"
    "面白いのは、教員数を25％増やしても、Bは20％しか減らないことです。反比例だからです。中学校1年の反比例が、そのまま学校の問題を考える道具になります。"
    "そして③は、人も業務も減らさずにBを減らせます。今回の研究は、この③、業務効率を高めることに焦点を当てます。"), "第2章")
cond = ["現状", "①N増", "②W減", "③E向上", "複合型"]; N = [20, 25, 20, 20, 20]; Wv = [200, 200, 160, 200, 180]; E = [1, 1, 1, 1.25, 1.2]
Bv = [w / (n * e) for w, n, e in zip(Wv, N, E)]
cd = CategoryChartData(); cd.categories = cond; cd.add_series("B（時間）", Bv)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.4), Inches(1.2), Inches(6.4), Inches(5.0), cd); ch = gf.chart; font_chart(ch, 13)
ch.has_legend = False; ch.has_title = True; ch.chart_title.text_frame.text = "1人当たりの業務時間 B（時間）"
pl = ch.plots[0]; pl.gap_width = 50; pl.has_data_labels = True; pl.data_labels.font.size = Pt(16); pl.data_labels.number_format = "0.0"; pl.data_labels.number_format_is_linked = False
cols = [GR, G, G, R, RGBColor(0xE6, 0xA2, 0x3C)]
for i, c in enumerate(cols):
    p = pl.series[0].points[i]; p.format.fill.solid(); p.format.fill.fore_color.rgb = c
tbl = s.shapes.add_table(6, 5, Inches(7.0), Inches(1.3), Inches(6.0), Inches(3.2)).table
hdr = ["条件", "N（人）", "W（時間）", "E", "B（時間）"]
data = [hdr] + [[c, str(n), str(w), f"{int(e*100)}%", f"{b:g}"] for c, n, w, e, b in zip(cond, N, Wv, E, Bv)]
for r_, row in enumerate(data):
    for c_, v in enumerate(row):
        cell = tbl.cell(r_, c_); cell.text = v
        para = cell.text_frame.paragraphs[0]; para.alignment = PP_ALIGN.CENTER
        f = para.runs[0].font; f.name = FONT; f.size = Pt(15); f.bold = r_ == 0 or (r_ == 4)
        f.color.rgb = W if r_ == 0 else (R if r_ == 4 else K)
        cell.fill.solid(); cell.fill.fore_color.rgb = G if r_ == 0 else (Y if r_ == 4 else W)
tb(s, Inches(7.0), Inches(4.7), Inches(6.0), Inches(1.5), [[("N を25%増やしても、B は20%減（反比例）", {"bold": True})], [("③は人も業務も減らさずに B を減らす → ", {}), ("本研究の焦点", {"color": R, "bold": True})]], size=17, fill=LG)
tb(s, Inches(0.4), Inches(6.35), Inches(12.6), Inches(0.6), [[("※ 数値はすべて仮定（実測値ではない）。", {"size": 13, "color": GR})]], size=13)

# ---------- 7 研究仮説 ----------
s = base("研究仮説と研究の内容・方法", (
    "【0:40】研究仮説です。従来の数学科授業実践における数学的な価値や教師の指導意図を継承しながら、生成AIを活用して授業を再構築することで、"
    "教師の授業準備に関わる負担を軽減するとともに、生徒の数学的な見方・考え方を働かせる授業の実現につながるのではないか。"
    "研究の内容は三つです。関数分野の過去の実践を振り返る。生成AIを使った授業再構築モデルをつくる。リメイク授業を提案し、検証の計画を立てる。"
    "今回はまだ実践前の段階なので、成果ではなく提案と検証計画としてお話しします。"), "第2章")
tb(s, Inches(0.6), Inches(1.3), Inches(12.1), Inches(2.4), [[("研究仮説", {"bold": True, "color": G, "size": 20})],
   "従来の数学科授業実践における数学的な価値や教師の指導意図を継承しながら、生成AIを活用して授業を再構築することで、教師の授業準備に関わる負担を軽減するとともに、生徒の数学的な見方・考え方を働かせる授業の実現につながるのではないか。"], size=21, line=G)
steps = [("①", "関数分野の過去の実践を振り返る", "1年 比例／2年 一次関数／3年 y＝ax²"), ("②", "授業再構築モデルをつくる", "AI LESSON REMAKE（7ステップ）"), ("③", "リメイク授業を提案し、検証計画を立てる", "実践前のため、成果ではなく計画を示す")]
for i, (n, h, d) in enumerate(steps):
    tb(s, Inches(0.6 + i * 4.15), Inches(4.0), Inches(3.95), Inches(2.3), [[(n + " " + h, {"bold": True})], [(d, {"size": 16, "color": B})]], size=19, fill=LG)

# ---------- 8 従来の実践 ----------
s = base("関数分野の三つの実践と、その数学的な価値", (
    "【0:50】第3章、従来の授業実践です。1年は、地震の初期微動継続時間と震源からの距離の関係を比例とみる授業です。"
    "2年は、山口県の2月の平均気温とソメイヨシノの開花日の関係を一次関数とみなし、開花日を予想する授業です。2015年の2月の気温7.5℃から3月27日ごろと予想し、実際も3月27日でした。"
    "3年は、巨大ブランコから始め、振り子の周期と長さの関係をy＝ax²とみなす授業です。"
    "三つに共通する数学的な価値は、現実の事象を関数とみなし、式・表・グラフを使って予測し、確かめることです。"), "第3章")
cards = [("1年　比例", "地震", "初期微動継続時間と\n震源からの距離", "比例とみなし、距離を求める"),
         ("2年　一次関数", "ソメイヨシノの開花日", "2月の平均気温と開花日\n（山口県・気象庁データ）", "一次関数とみなし、開花日を予想する"),
         ("3年　関数y＝ax²", "振り子・巨大ブランコ", "周期 x 秒と長さ y m\n（実測データ）", "y＝ax²とみなし、周期2秒の振り子をつくる")]
for i, (g_, t, d, v) in enumerate(cards):
    x = Inches(0.6 + i * 4.15)
    tb(s, x, Inches(1.3), Inches(3.95), Inches(0.65), [[(g_, {"bold": True, "color": W})]], size=20, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=G)
    tb(s, x, Inches(2.05), Inches(3.95), Inches(3.0), [[(t, {"bold": True, "size": 22})], [(d, {"size": 16})], [("→ " + v, {"color": R, "bold": True, "size": 16})]], size=18, align=PP_ALIGN.CENTER, line=G)
tb(s, Inches(0.6), Inches(5.35), Inches(12.1), Inches(1.0), [[("共通する数学的な価値：", {"bold": True}), ("現実の事象を", {}), ("関数とみなし", {"color": R, "bold": True}), ("、式・表・グラフで予測し、確かめる", {})]], size=21, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=Y)

# ---------- 9 良さと課題 ----------
s = base("2021年の振り子の授業：成果○と課題●", (
    "【0:50】3年の振り子の授業は、2021年の全国大会で発表しました。そのときの成果は、GeoGebraで「2乗に比例する関数とみなす」活動がしやすくなったこと、実測値を元に予想して解決できたこと、実物とICTを関連づけて主体的に取り組めたことです。"
    "課題は二つでした。ICTの効果を計る項目を振り返りシートに具体的に設けること、ICTを扱うタイミングを検討することです。実物の振り子を使う良さもあると書いています。"
    "また、教材をつくり直す準備の時間もかかっていました。この課題を、今回の出発点にしました。"), "第3章")
tb(s, Inches(0.6), Inches(1.3), Inches(6.0), Inches(4.6), [[("成果○（2021年 本人記述）", {"bold": True, "color": G})],
   "○ ICT（GeoGebra）で「2乗に比例する関数とみなす」活動がしやすくなった", "○ 実測値が元になり、予想し解決できたことで数学的活動が深まった", "○ 実物の振り子とICTを関連づけ、主体的に取り組んだ"], size=19, line=G)
tb(s, Inches(6.85), Inches(1.3), Inches(5.9), Inches(4.6), [[("課題●（2021年 本人記述）", {"bold": True, "color": R})],
   "● 振り返りシートで、ICTの効果を計る項目を具体的に設ける必要がある", "● ICTを扱う授業内のタイミングは検討の余地がある（実物の振り子を使う良さもある）",
   [("＋ 教材を毎年つくり直す準備の時間", {"color": B})]], size=19, fill=Y)
tb(s, Inches(0.6), Inches(6.1), Inches(12.1), Inches(0.8), [[("出典：第103回全国算数・数学教育研究（埼玉）大会 発表資料・大会誌原稿（新田・山本 2021）", {"size": 12, "color": GR})]], size=12)

# ---------- 10 AI LESSON REMAKE ----------
s = base("AI LESSON REMAKE（授業再構築モデル）", (
    "【1:00】第4章、今回提案する授業再構築モデル、AI LESSON REMAKEです。7つのステップがあります。"
    "ステップ1で、過去の授業資料を生成AIに入力します。生徒の名前などは入れません。ステップ2と3で、良かった点と課題を三つずつ整理します。ここに過去の研究の課題を必ず入れます。"
    "ステップ4で、生成AIに複数の改善案を出させます。大切なのはステップ5と6です。数学的に正しいか、教育的な価値があるかを教師が吟味し、残す・変える・削るの視点で授業を組み直します。"
    "ここは教師の判断で、AIに丸投げしません。ステップ7で実践し、評価し、また改善します。"), "第4章")
st = [("STEP1", "過去の授業資料を\n生成AIに入力"), ("STEP2", "良かった点を\n三つ整理"), ("STEP3", "課題を\n三つ整理"), ("STEP4", "AIに複数の\n改善案を提案させる"),
      ("STEP5", "教師が数学的妥当性と\n教育的価値を吟味"), ("STEP6", "残す・変える・削るで\n授業を再構築"), ("STEP7", "実践・評価・検証\n・再改善")]
for i, (h, d) in enumerate(st):
    teacher = i in (4, 5)
    x = Inches(0.45 + i * 1.83)
    tb(s, x, Inches(1.5), Inches(1.65), Inches(0.6), [[(h, {"bold": True, "color": W})]], size=17, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=R if teacher else G)
    tb(s, x, Inches(2.2), Inches(1.65), Inches(2.2), [d], size=15, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line=R if teacher else G, fill=Y if teacher else None)
    if i < 6:
        a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x + Inches(1.66), Inches(3.1), Inches(0.17), Inches(0.35)); a.fill.solid(); a.fill.fore_color.rgb = GR; a.line.fill.background()
tb(s, Inches(7.75), Inches(4.55), Inches(3.5), Inches(0.6), [[("教師の判断（AIに丸投げしない）", {"bold": True, "color": R})]], size=15, align=PP_ALIGN.CENTER)
tb(s, Inches(0.6), Inches(5.2), Inches(12.1), Inches(1.7), [[("既存のAIツールの位置づけ", {"bold": True, "color": G})],
   "STEP4：導入発問メーカー／数学教材生成ツール　STEP6：板書型指導案メーカー・学習指導案メーカー　STEP7：振り返り自動化（Forms→Sheets→GAS）",
   [("→ 他の先生も、自分の授業で同じ手順をたどれる（再現性）", {"color": B, "bold": True})]], size=16, fill=LG)

# ---------- 11 残す・変える・削る ----------
s = base("残す・変える・削る", (
    "【0:50】ステップ6の判断の基準です。残すのは授業の本質です。数学的な価値、中心発問、生徒が自分で考える時間、実物に触れる体験です。"
    "変えるのは、本質にたどり着くための手段です。教材の形、データの扱い方、支援の出し方です。"
    "削るのは、本質に役立たない作業です。手作業の転記や、毎年のデータの打ち直しなどです。"
    "変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。これが、このモデルの考え方です。"), "第4章")
cols3 = [("残す", "授業の本質", ["数学的な価値", "中心発問", "生徒が考える時間", "実物に触れる体験"], G),
         ("変える", "本質にたどり着く手段", ["教材の形（動的教材）", "データの扱い方", "支援の出し方（段階的ヒント）"], B),
         ("削る", "本質に寄与しない作業", ["手作業の転記・計算", "毎年のデータ打ち直し", "教材の作り直し"], R)]
for i, (h, sub, li, c) in enumerate(cols3):
    x = Inches(0.6 + i * 4.15)
    tb(s, x, Inches(1.3), Inches(3.95), Inches(1.1), [[(h, {"bold": True, "color": W, "size": 30})], [(sub, {"color": W, "size": 15})]], size=30, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=c)
    tb(s, x, Inches(2.5), Inches(3.95), Inches(2.8), ["・" + t for t in li], size=19, line=c)
tb(s, Inches(0.6), Inches(5.6), Inches(12.1), Inches(1.1), [[("変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。", {"bold": True, "color": G})]], size=22, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=Y)

# ---------- 12 Before/After ----------
s = base("重点事例：3年「振り子」Before／After", (
    "【1:20】第5章、具体的なリメイク授業です。重点事例は3年の振り子です。"
    "巨大ブランコの導入、「ひもの長さと1往復の時間にはどんな関係があるか」という中心発問、そして実物の振り子を測る体験は残します。"
    "変えるのは三つです。一つ目、GeoGebraで見た目を比べていた場面を、関数ごとの「ずれ」を数値で比べられる教材にします。見た目だけでなく、根拠をもって「みなす」ためです。"
    "二つ目、ヒントを3段階にして、つまずいている生徒に合わせて出します。正解はすぐには見せません。"
    "三つ目、生成AIの答えを検証する活動を入れます。"
    "そして2021年の課題に応えて、振り返りにICTの効果を計る項目を入れます。"), "第5章")
rows12 = [("", "Before（2021年の実践）", "After（提案）"),
          ("導入・中心発問", "巨大ブランコ／長さと1往復の時間の関係は？", "同じ（残す）"),
          ("自力解決", "実物の振り子を測る → 点をとる", "実物で測る（残す）→ 振り子ラボに入力"),
          ("練り上げ", "GeoGebraで関数を重ね、見た目で比べる", "関数ごとの「ずれ」を数値で比べ、根拠をもってみなす"),
          ("個別の支援", "机間指導", "3段階のヒント（正解はすぐに見せない）"),
          ("数学的考察", "y＝0.25x²、周期2秒 → 1m", "＋「AIの答え」を検証する／成立条件にふれる"),
          ("振り返り", "わかったこと・理解度", "＋ ICTの効果を計る項目（2021年の課題）"),
          ("教材研究・準備", "教材を個人で作成・修正", "AIで案を作り、教師が検証（時間を記録）")]
t = s.shapes.add_table(len(rows12), 3, Inches(0.5), Inches(1.25), Inches(12.3), Inches(5.6)).table
t.columns[0].width = Inches(2.2); t.columns[1].width = Inches(4.7); t.columns[2].width = Inches(5.4)
for r_, row in enumerate(rows12):
    for c_, v in enumerate(row):
        cell = t.cell(r_, c_); cell.text = v; cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        para = cell.text_frame.paragraphs[0]; f = para.runs[0].font if para.runs else None
        if f is None: continue
        f.name = FONT; f.size = Pt(16); f.bold = r_ == 0 or c_ == 0
        changed = c_ == 2 and r_ > 0 and "残す" not in v and "同じ" not in v
        f.color.rgb = W if r_ == 0 else (R if changed else K)
        cell.fill.solid(); cell.fill.fore_color.rgb = (G if c_ != 2 else R) if r_ == 0 else (LG if c_ == 0 else (Y if changed else W))

# ---------- 13 振り子ラボ ----------
s = base("振り子ラボ：数値で「みなす」・AIの答えを確かめる", (
    "【1:30】これが、生成AIと一緒に作った「振り子ラボ」です。ブラウザで動き、インストールは不要です。"
    "実物で測ったデータを入れると、表とグラフに点が出ます。生徒は、比例、一次関数、反比例、y＝ax²の中から関数を選び、aを動かして点に近づけます。"
    "「ずれを確かめる」を押すと、点とグラフのずれの大きさが出ます。2021年の授業データでは、y＝0.25x²のときずれは0.025m、比例だと0.138mでした。見た目だけでなく、数値で「y＝ax²とみなす」根拠を説明できます。"
    "次に、「ある生成AIは、振り子の長さは周期に比例すると答えた。正しいか」と問います。AIの答えをうのみにせず、データで確かめる活動です。"
    "最後は、周期2秒の振り子の長さを式から求め、シミュレーションと実物で確かめます。y＝0.25×2²で1m、理論でも約0.99mです。"
    "なお、この関係はふれはばが小さいときに成り立つ近似です。教材ではふれはばを変えて、ずれ方も確かめられるようにしました。"), "第5章")
img = os.path.join(ROOT, "05_数学教材", "振り子ラボ_画面.png")
s.shapes.add_picture(img, Inches(0.45), Inches(1.2), height=Inches(4.75))
tb(s, Inches(9.05), Inches(1.2), Inches(3.95), Inches(5.7), [
    [("① 実物のデータを入力", {"bold": True, "color": G})], [("表・グラフ・式が連動", {"size": 15})],
    [("② 関数を選び a を動かす", {"bold": True, "color": G})], [("ずれ：y＝0.25x² 0.025m／比例 0.138m", {"size": 15, "color": R})],
    [("③ AIの答えを検証", {"bold": True, "color": G})], [("「長さは周期に比例する」は正しい？", {"size": 15})],
    [("④ 周期2秒の振り子", {"bold": True, "color": G})], [("y＝0.25×2²＝1（m）→ 実物で確認", {"size": 15})],
    [("単一HTML・インストール不要", {"size": 14, "color": B})]], size=18, line=G)
tb(s, Inches(0.45), Inches(6.05), Inches(8.5), Inches(0.9), [[("成立条件：", {"bold": True}), ("T＝2π√(L/g) より L＝(g/4π²)T²、g/4π²≒0.248。ふれはばが小さいときの近似。", {})]], size=14, fill=LG)

# ---------- 14 1年・2年 ----------
s = base("1年「地震」・2年「桜の開花日」のリメイク", (
    "【1:10】1年と2年のリメイクです。2年の桜の授業では、2017年までのデータを使っていました。生成AIを使えば、気象庁のデータを最新の年まで整える作業を補助できます。ただし、数値は必ず教師が原典と照合します。"
    "生徒は散布図の上で自分で直線を引き、2点から式を求めて開花日を予想します。グラフを手で描く時間を、考える時間に回せます。"
    "ここでも「AIは、気温が1℃上がると開花は10日早くなると答えた。正しいか」とデータで確かめさせます。資料のデータでは、1℃でおよそ3日早まる程度です。"
    "1年の地震の授業では、初期微動継続時間と震源からの距離の比例関係を、観測点のデータで確かめる教材を構想しています。理科との関連も大切にします。"), "第5章")
for i, (g_, bf, af) in enumerate([("2年　桜の開花日（一次関数）", ["2017年までの表データ", "グラフは手描き", "「何が影響しているか」を考える"], ["データを最新年まで更新（AIが補助・教師が原典照合）", "散布図に自分で直線を引く動的教材", "「AIの答え」をデータで確かめる"]),
                                   ("1年　地震（比例）", ["初期微動継続時間と震源からの距離を比例とみる"], ["観測点のデータで比例を確かめる教材（構想）", "比例定数＝1秒あたり何kmか、の意味を考える", "理科との関連"])]):
    y0 = Inches(1.3 + i * 2.85)
    tb(s, Inches(0.5), y0, Inches(3.0), Inches(2.55), [[(g_, {"bold": True, "color": W})]], size=19, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=G)
    tb(s, Inches(3.65), y0, Inches(4.0), Inches(2.55), [[("Before", {"bold": True})]] + ["・" + x for x in bf], size=16, line=G)
    a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(7.75), y0 + Inches(1.0), Inches(0.4), Inches(0.5)); a.fill.solid(); a.fill.fore_color.rgb = GR; a.line.fill.background()
    tb(s, Inches(8.25), y0, Inches(4.6), Inches(2.55), [[("After（提案）", {"bold": True, "color": R})]] + ["・" + x for x in af], size=16, fill=Y)

# ---------- 15 期待される効果・限界・検証 ----------
s = base("期待される効果と研究の限界、今後の検証", (
    "【1:10】第6章、まとめです。今回は実践前のため、成果ではなく、期待される効果として示します。"
    "教師側では、教材作成や指導案、板書計画の準備時間の短縮が期待されます。生徒側では、つまずきに応じたヒントで基礎の理解を支え、数値の根拠をもって関数とみなす説明ができることが期待されます。"
    "研究の限界として、業務時間のモデルは簡易的な仮定に基づくこと、時間短縮や理解の向上はまだ測っていないこと、AIの出力の確認と修正には時間がかかることがあげられます。"
    "今後は、準備時間を改善の前後で記録し、時間削減率をこの式で求めます。生徒の到達度や振り返りの内容も比べ、効果を確かめていきます。"), "第6章")
tb(s, Inches(0.5), Inches(1.3), Inches(6.1), Inches(2.6), [[("期待される効果（未検証）", {"bold": True, "color": G})],
   "○ 教材・指導案・板書計画の準備時間の短縮", "○ 段階的ヒントによる基礎の理解の支援", "○ 数値の根拠をもって「みなす」説明", "○ AIの答えを数学的に検証する力"], size=17, line=G)
tb(s, Inches(6.8), Inches(1.3), Inches(6.0), Inches(2.6), [[("研究の限界●", {"bold": True, "color": R})],
   "● B＝W÷(N×E) は簡易的な仮定のモデル", "● 時間短縮・理解の向上は未測定", "● AI出力の確認・修正にも時間がかかる", "● 生徒の個人情報を入力しない運用が前提"], size=17, fill=Y)
tb(s, Inches(0.5), Inches(4.1), Inches(12.3), Inches(2.85), [[("今後の検証", {"bold": True, "color": B})],
   [("教師：", {"bold": True}), ("授業準備・教材作成・指導案・板書計画・AI出力の確認修正の時間、心理的負担", {})],
   [("生徒：", {"bold": True}), ("基礎の到達率、数学的な説明、つまずく生徒への支援、得点分布、振り返りの内容", {})],
   [("時間削減率（％）＝（改善前の時間 − 改善後の時間）÷ 改善前の時間 × 100", {"bold": True, "color": R})]], size=17, fill=LG)

# ---------- 16 結び ----------
s = base("おわりに", (
    "【1:00】最後に、この研究で伝えたいことです。これまでの優れた教育実践を否定するのではありません。"
    "振り子の授業で大切にしてきた、現実の事象を関数とみなし、予想し、確かめるという本質は、これからも残します。"
    "生成AIは目的ではなく、その本質にたどり着くための手段です。そして、教師がAIに判断を丸投げしないことが前提です。"
    "変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。教育の質を守るために、教師の時間を守る。"
    "みなさんも、ご自身の得意な授業をAI LESSON REMAKEでリメイクしてみてください。ご清聴ありがとうございました。"), "第6章")
tb(s, Inches(1.0), Inches(1.5), Inches(11.3), Inches(1.6), [[("変えるべきは、授業の本質ではない。", {"bold": True})], [("その本質にたどり着くための手段である。", {"bold": True})]], size=30, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=LG)
tb(s, Inches(1.0), Inches(3.35), Inches(11.3), Inches(1.1), [[("教育の質を守るために、教師の時間を守る。", {"bold": True, "color": R})]], size=30, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=Y)
tb(s, Inches(1.0), Inches(4.75), Inches(11.3), Inches(1.0), ["過去の実践を継承し、生成AIは手段として使う。判断するのは教師。"], size=20, align=PP_ALIGN.CENTER)
tb(s, Inches(1.0), Inches(5.8), Inches(11.3), Inches(0.9), [[("ご清聴ありがとうございました。", {"bold": True})]], size=26, align=PP_ALIGN.CENTER)

# ---------- 補足 ----------
s = base("補足① 統計データの出典", "【補足・質疑用】統計の出典です。", "補足")
tb(s, Inches(0.5), Inches(1.3), Inches(12.3), Inches(5.6), [
    "・文部科学省「令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況等」参考資料1 第7表（長期推移）・第2表-1・第9表-1（山口県・教科別）",
    [("　https://www.mext.go.jp/content/20261001-kyoikushokuin-000046447_2.pdf", {"size": 13, "color": B})],
    "・文部科学省「教員勤務実態調査（令和4年度）集計【確定値】」",
    [("　https://www.mext.go.jp/content/20240404-mxt_zaimu01-100003067-1.pdf", {"size": 13, "color": B})],
    "・文部科学省「『教師不足』に関する実態調査」（令和4年1月）",
    [("　https://www.mext.go.jp/content/20220128-mxt_kyoikujinzai01-000020293-1.pdf", {"size": 13, "color": B})],
    "・気象庁「過去の気象データ」（2月の平均気温・ソメイヨシノの開花日、山口）",
    [("注意：採用選考の受験者数の推移であり、教員総数の推移ではない。教師不足の全国調査は令和3年度の1回。", {"color": R})]], size=17)
s = base("補足② 振り子モデルの成立条件と過去のデータ", "【補足・質疑用】振り子の式の根拠と、2021年の実測データです。", "補足")
tb(s, Inches(0.5), Inches(1.3), Inches(6.2), Inches(5.6), [
    [("単振り子の周期", {"bold": True})], "T＝2π√(L/g) → L＝(g/4π²)T²", "g＝9.80665 m/s² のとき g/4π²≒0.248", "周期2秒 → L≒0.99 m（秒振り子）",
    [("成り立つ条件", {"bold": True})], "・ふれはばが小さい（30°で周期は約1.7%長くなる）", "・長さはおもりの重心まで", "・糸の質量・空気抵抗が小さい",
    [("巨大ブランコは人の重心・大きなふれはばで近似が粗くなる", {"color": R})]], size=16, line=G)
t = s.shapes.add_table(11, 3, Inches(7.0), Inches(1.3), Inches(5.8), Inches(5.4)).table
d21 = [(0.65, 0.10), (0.90, 0.19), (1.01, 0.27), (1.08, 0.31), (1.14, 0.38), (1.39, 0.50), (1.59, 0.64), (1.70, 0.72), (1.72, 0.78), (1.81, 0.84)]
for r_, row in enumerate([("周期x（秒）", "長さy（m）", "y÷x²")] + [(f"{x:.2f}", f"{y:.2f}", f"{y/x/x:.3f}") for x, y in d21]):
    for c_, v in enumerate(row):
        cell = t.cell(r_, c_); cell.text = v; para = cell.text_frame.paragraphs[0]; para.alignment = PP_ALIGN.CENTER
        f = para.runs[0].font; f.name = FONT; f.size = Pt(13); f.bold = r_ == 0; f.color.rgb = W if r_ == 0 else K
        cell.fill.solid(); cell.fill.fore_color.rgb = G if r_ == 0 else W
s = base("補足③ 理想的なバトンパス（2017年・3年）", "【補足・質疑用】2017年に実践したバトンパスの授業です。今回は本編では扱いません。", "補足")
tb(s, Inches(0.5), Inches(1.3), Inches(12.3), Inches(5.5), [
    "・運動会のリレー練習の場面設定（バトンが渡せない会話文）から問題をつくる",
    "・加速して走り出す次走者（y＝ax²）と、一定の速さで走る前走者（一次関数）のグラフで考える",
    [("今後のリメイク候補：", {"bold": True}), ("スタート位置やタイミングを動かしてグラフの交点を確かめる動的教材", {})],
    [("※ 本編では、資料が最もそろっている振り子を重点事例とした", {"color": GR})]], size=19)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
