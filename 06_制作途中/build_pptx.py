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
FOOT = "令和8年度山口県中学校数学教育第二地区研究協議会 発表資料　" + TITLE
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

# ===== 第2版のスライド本体（build_pptx.py のヘルパー部の後ろに連結して使う） =====
# スタンス：資料はすべてAIを活用して作成。土台は14年間の授業実践。賛否は受け取り方次第。AIと人間の共存。

def arrow(s, x, y, w=0.3, h=0.4):
    a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, y, Inches(w), Inches(h)); a.fill.solid(); a.fill.fore_color.rgb = GR; a.line.fill.background()


# ---------- 1 表紙 ----------
s = prs.slides.add_slide(BL)
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.45), Inches(0.14), Inches(0.45)); bar.fill.solid(); bar.fill.fore_color.rgb = G; bar.line.fill.background()
tb(s, Inches(0.75), Inches(0.38), Inches(9), Inches(0.6), ["令和8年度山口県中学校数学教育第二地区研究協議会"], size=18, anchor=MSO_ANCHOR.MIDDLE)
tb(s, Inches(0.9), Inches(1.9), Inches(11.6), Inches(1.4), [[(TITLE, {"bold": True})]], size=36, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
tb(s, Inches(0.9), Inches(3.25), Inches(11.6), Inches(0.7), [SUB], size=24, align=PP_ALIGN.CENTER)
tb(s, Inches(2.2), Inches(4.3), Inches(9), Inches(1.0), [[("14年間の授業実践を土台に、生成AIと一緒に作った発表です", {"color": G, "bold": True})]], size=20, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=LG)
tb(s, Inches(7.3), Inches(5.9), Inches(5.6), Inches(0.9), ["下関市立名陵中学校　新田正幸"], size=20, align=PP_ALIGN.RIGHT)
band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.12), SW, Inches(0.38)); band.fill.solid(); band.fill.fore_color.rgb = G; band.line.fill.background()
s.notes_slide.notes_text_frame.text = (
    "【0:20】今から、「生成AIを活用した数学科授業の改善と新たな授業モデルの提案 ～関数分野における従来の授業実践を通して～」という題で発表をします。"
    "下関市立名陵中学校の新田です。よろしくお願いします。")

# ---------- 2 この発表資料について ----------
s = base("はじめに　この発表資料について", (
    "【0:50】はじめに、お伝えしておきたいことがあります。今回の発表資料は、構成もスライドも原稿も、そして後でお見せする教材も、すべて生成AIを活用して作りました。"
    "AIで作った発表と聞くと、賛否両論あると思います。ただ、中身には、私がこの14年間、授業で大切にしてきた思いと、その蓄積を載せたつもりです。"
    "14年間の思いを、AIを活用して形にしてみました。どう受け取るかは、皆さんの受け取り方次第です。そのうえで、最後まで聞いていただけたらうれしいです。"), "はじめに")
tb(s, Inches(0.6), Inches(1.35), Inches(12.1), Inches(1.4), [[("この発表資料は、", {}), ("すべて生成AIを活用して", {"color": R, "bold": True}), ("作成しました。", {})],
   [("構成・スライド・発表原稿・グラフ・数学教材（振り子ラボ）", {"size": 18, "color": GR})]], size=26, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=Y)
tb(s, Inches(0.6), Inches(3.0), Inches(5.9), Inches(2.6), [[("AIが担ったこと", {"bold": True, "color": B})], "・資料の整理と構成案", "・統計資料の収集とグラフ化", "・スライド・原稿・教材の下書き"], size=20, line=B)
tb(s, Inches(6.8), Inches(3.0), Inches(5.9), Inches(2.6), [[("中身（土台）", {"bold": True, "color": G})], "・14年間の授業実践と研究発表", "・授業で大切にしてきた思い", "・何を残し、何を変えるかの判断"], size=20, line=G)
tb(s, Inches(0.6), Inches(5.85), Inches(12.1), Inches(0.9), [[("賛否両論あると思います。受け取り方は、皆さんにお任せします。", {"bold": True})]], size=20, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=LG)

# ---------- 3 14年間の歩み ----------
s = base("14年間の歩み：良い授業を、新しい手段で改善してきた", (
    "【0:40】これまでの歩みを少しだけ振り返ります。2015年ごろから振り子の授業を続け、2017年には桜の開花日やバトンパスの授業もつくりました。"
    "2021年は、振り子の授業でGeoGebraを使い、全国大会で発表しました。2022年はジグソー法、2023年は教師の手立てを発表しました。"
    "振り返ると、どれも「良い授業を、新しい手段で改善する」ことでした。今回、その手段が生成AIです。"
    "14年間で学校も生徒も変わりましたが、現実の事象を数学で考える授業を大切にしたいという思いは、ずっと変わっていません。"), "はじめに")
items = [("2015〜", "振り子の授業\n（3年 y＝ax²）"), ("2017", "桜の開花日\nバトンパス"), ("2021", "ICT活用\nGeoGebra×振り子"), ("2022", "ジグソー法\n協働的な学び"), ("2023", "教師の手立て\nねじれの位置"), ("2026", "生成AI\n授業を再構築")]
for i, (yr, th) in enumerate(items):
    x = Inches(0.45 + i * 2.15); last = i == 5
    tb(s, x, Inches(1.5), Inches(1.9), Inches(0.65), [[(yr, {"bold": True, "color": W})]], size=22, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=R if last else G)
    tb(s, x, Inches(2.25), Inches(1.9), Inches(1.9), [th], size=17, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line=R if last else G, fill=Y if last else None)
    if i < 5: arrow(s, x + Inches(1.91), Inches(3.0), 0.22, 0.35)
tb(s, Inches(0.6), Inches(4.5), Inches(12.1), Inches(1.0), [[("共通する考え：", {"bold": True}), ("従来の良い授業を否定せず、", {}), ("新しい手段", {"color": R, "bold": True}), ("で改善する", {})]], size=22, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=LG)
tb(s, Inches(0.6), Inches(5.7), Inches(12.1), Inches(1.1), [[("2021年に残した課題●「ICTの効果を計る項目」「ICTを扱うタイミング」→ 今回の出発点", {"color": B})]], size=18, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 4 数値で見る教員不足 ----------
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "02_統計データ", "全国_教員採用選考_長期推移.csv"), encoding="utf-8-sig")) if int(r["西暦(採用年度)"]) >= 2000]
lab = [r["採用年度"].replace("年度", "").replace("平成", "H").replace("令和", "R").replace("元", "1") for r in rows]
s = base("数値で見てみる：ここ数年の教員不足", (
    "【0:50】まず、ここ数年の学校の教員不足を、数学的な数値で少し見てみたいと思いました。関数的な表現や、データの活用の部分です。ここは資料として載せておく、という意味合いですので、ご覧ください。"
    "中学校の教員採用の倍率は、平成12年度の17.9倍から、令和7年度は3.6倍まで下がっています。ただ、これは受験者数の推移で、教員の総数が減っているという意味ではありません。採用者数が増えたことも影響しています。"
    "勤務実態を見ると、在校時間は少し減りましたが、授業準備の時間はほとんど変わっていません。"
    "数学の授業で扱う、グラフから傾向を読み取る、変化の割合を考える、ということを、自分たちの職場のことにも当てはめてみた、というイメージです。"), "第1章")
cd2 = CategoryChartData(); cd2.categories = lab; cd2.add_series("中学校 採用倍率（倍）", [float(r["中学校_競争率"]) for r in rows])
gf2 = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.4), Inches(1.2), Inches(7.0), Inches(4.8), cd2); ch2 = gf2.chart; font_chart(ch2, 11)
ch2.has_title = True; ch2.chart_title.text_frame.text = "公立中学校 教員採用選考の採用倍率（倍）"; ch2.has_legend = False
sr = ch2.plots[0].series[0]; sr.format.line.color.rgb = R; sr.format.line.width = Pt(2.5); sr.smooth = False
for idx in (0, len(rows) - 1):
    pt = sr.points[idx]; pt.data_label.has_text_frame = False; pt.data_label.show_value = True; pt.data_label.position = XL_LABEL_POSITION.ABOVE
    pt.data_label.font.size = Pt(16); pt.data_label.font.bold = True; pt.data_label.font.color.rgb = R
tb(s, Inches(7.7), Inches(1.3), Inches(5.3), Inches(1.4), [[("中学校の採用倍率", {"bold": True})], [("17.9倍（H12）→ 3.6倍（R7）", {"size": 22, "color": R, "bold": True})]], size=17, line=G)
tb(s, Inches(7.7), Inches(2.85), Inches(5.3), Inches(1.4), [[("山口県 中学校数学（R7）", {"bold": True})], [("受験37人・採用17人・2.2倍", {"size": 20})]], size=17, line=G)
tb(s, Inches(7.7), Inches(4.4), Inches(5.3), Inches(1.6), [[("中学校教諭 平日1日（R4）", {"bold": True})], "在校等時間 11:32 → 11:01", [("授業準備 1:26 → 1:23（−3分）", {"color": R, "bold": True})]], size=17, fill=Y)
tb(s, Inches(0.4), Inches(6.1), Inches(12.6), Inches(0.9), [[("※ 受験者数・倍率の推移であり、教員総数の推移ではない（採用者数の増加も影響）。", {"size": 12, "color": R})],
   [("出典：文部科学省「令和7年度公立学校教員採用選考試験の実施状況等」参考資料1 第7表・第9表、「教員勤務実態調査（令和4年度）集計【確定値】」", {"size": 10, "color": GR})]], size=12)

# ---------- 5 B=W/(NE) ----------
s = base("数学で考える：B ＝ W ÷（N × E）", (
    "【0:50】この問題を数学で考えると、教員1人当たりの業務時間Bは、業務量Wを、教員数Nと業務効率Eの積でわったもの、と表せます。"
    "教員を25％増やしても、Bは20％しか減りません。反比例だからです。一方で、効率Eを高めれば、人も業務も減らさずにBを減らせます。"
    "もちろん、これは仮定に基づく簡単なモデルで、実際の数値ではありません。今回はこの「効率を高める」部分に、生成AIを使ってみました。"), "第2章")
tb(s, Inches(0.5), Inches(1.3), Inches(6.3), Inches(1.2), [[("B ＝ W ÷（N × E）", {"bold": True, "size": 38})]], size=38, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=LG)
tb(s, Inches(0.5), Inches(2.6), Inches(6.3), Inches(1.8), ["B：教員1人当たりの平均業務時間", "W：学校全体の業務量", "N：教員数　E：業務効率（従来を1）"], size=17)
cond = ["現状", "①N増", "②W減", "③E向上", "複合型"]; N = [20, 25, 20, 20, 20]; Wv = [200, 200, 160, 200, 180]; E = [1, 1, 1, 1.25, 1.2]
Bv = [w / (n * e) for w, n, e in zip(Wv, N, E)]
cd = CategoryChartData(); cd.categories = cond; cd.add_series("B（時間）", Bv)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(7.0), Inches(1.2), Inches(6.0), Inches(3.9), cd); ch = gf.chart; font_chart(ch, 12)
ch.has_legend = False; ch.has_title = True; ch.chart_title.text_frame.text = "1人当たりの業務時間 B（時間）※仮定"
pl = ch.plots[0]; pl.gap_width = 50; pl.has_data_labels = True; pl.data_labels.font.size = Pt(14); pl.data_labels.number_format = "0.0"; pl.data_labels.number_format_is_linked = False
for i, c in enumerate([GR, G, G, R, RGBColor(0xE6, 0xA2, 0x3C)]):
    p = pl.series[0].points[i]; p.format.fill.solid(); p.format.fill.fore_color.rgb = c
tb(s, Inches(0.5), Inches(4.6), Inches(6.3), Inches(1.5), [[("N を25%増やしても B は20%減（反比例）", {"bold": True})], [("③ E を高める → 人も業務も減らさない", {"color": R, "bold": True})]], size=17, fill=Y)
tb(s, Inches(7.0), Inches(5.2), Inches(6.0), Inches(0.9), ["条件：N=20人・W=200時間 → ①N=25 ②W=160 ③E=125% 複合 W=180・E=120%"], size=13)
tb(s, Inches(0.5), Inches(6.3), Inches(12.4), Inches(0.6), [[("※ 実測値ではなく仮定に基づく簡易モデル（業務の均等配分・一様な効率改善を仮定。個人差や精神的負担は表せない）", {"size": 12, "color": GR})]], size=12)

# ---------- 6 研究仮説 ----------
s = base("研究仮説", (
    "【0:30】研究仮説です。従来の数学科授業実践における数学的な価値や教師の指導意図を継承しながら、生成AIを活用して授業を再構築することで、"
    "教師の授業準備に関わる負担を軽減するとともに、生徒の数学的な見方・考え方を働かせる授業の実現につながるのではないか、と考えました。"), "第2章")
tb(s, Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.0), ["従来の数学科授業実践における数学的な価値や教師の指導意図を継承しながら、生成AIを活用して授業を再構築することで、教師の授業準備に関わる負担を軽減するとともに、生徒の数学的な見方・考え方を働かせる授業の実現につながるのではないか。"], size=24, anchor=MSO_ANCHOR.MIDDLE, line=G)
for i, (n, h) in enumerate([("①", "過去の自分の実践を振り返る"), ("②", "AIでアレンジするモデルをつくる"), ("③", "リメイク授業と検証計画を示す")]):
    tb(s, Inches(0.8 + i * 3.95), Inches(5.0), Inches(3.75), Inches(1.0), [[(n + " " + h, {"bold": True})]], size=19, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=LG)
tb(s, Inches(0.8), Inches(6.2), Inches(11.7), Inches(0.6), [[("※ リメイク授業は未実践。成果ではなく、提案と検証計画として示す。", {"color": GR})]], size=14)

# ---------- 7 過去の実践 ----------
s = base("過去の自分の授業実践：関数分野の三つ", (
    "【0:50】ここからが中心です。過去の自分の授業実践を、AIを活用してアレンジしてみました。題材は関数分野の三つです。"
    "1年は、地震の初期微動継続時間と震源からの距離を比例とみる授業。2年は、山口県の2月の平均気温とソメイヨシノの開花日を一次関数とみなして予想する授業です。2015年の気温7.5℃から3月27日ごろと予想し、実際も3月27日でした。"
    "3年は、巨大ブランコから始めて、振り子の周期と長さをy＝ax²とみなす授業です。"
    "どれも、現実の事象を関数とみなし、予測し、確かめる授業です。ここが、私の授業の土台です。桜の授業は、当時の数学通信にも載せた、思い入れのある授業です。"), "第3章")
cards = [("1年　比例", "地震", "初期微動継続時間と\n震源からの距離", "比例とみなし、距離を求める"),
         ("2年　一次関数", "ソメイヨシノの開花日", "2月の平均気温と開花日\n（山口県・気象庁データ）", "一次関数とみなし、開花日を予想"),
         ("3年　関数y＝ax²", "振り子・巨大ブランコ", "周期 x 秒と長さ y m\n（実測データ）", "y＝ax²とみなし、周期2秒の振り子をつくる")]
for i, (g_, t, d, v) in enumerate(cards):
    x = Inches(0.6 + i * 4.15)
    tb(s, x, Inches(1.3), Inches(3.95), Inches(0.65), [[(g_, {"bold": True, "color": W})]], size=20, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=G)
    tb(s, x, Inches(2.05), Inches(3.95), Inches(3.0), [[(t, {"bold": True, "size": 22})], [(d, {"size": 16})], [("→ " + v, {"color": R, "bold": True, "size": 16})]], size=18, align=PP_ALIGN.CENTER, line=G)
tb(s, Inches(0.6), Inches(5.35), Inches(12.1), Inches(1.0), [[("土台：", {"bold": True}), ("現実の事象を", {}), ("関数とみなし", {"color": R, "bold": True}), ("、予測し、確かめる", {})]], size=22, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=Y)

# ---------- 8 2021年の成果と課題 ----------
s = base("2021年の振り子の授業：成果○と課題●", (
    "【0:40】3年の振り子は、2021年の全国大会で発表した授業です。GeoGebraで「2乗に比例する関数とみなす」活動がしやすくなった一方で、"
    "ICTの効果を計る項目がないこと、ICTを使うタイミング、という課題が残りました。実物の振り子を使う良さもある、とも書いています。この課題を、今回AIと一緒に考え直しました。"), "第3章")
tb(s, Inches(0.6), Inches(1.3), Inches(6.0), Inches(4.6), [[("成果○", {"bold": True, "color": G})],
   "○ GeoGebraで「2乗に比例する関数とみなす」活動がしやすくなった", "○ 実測値をもとに予想し解決でき、数学的活動が深まった", "○ 実物の振り子とICTを関連づけ、主体的に取り組んだ"], size=19, line=G)
tb(s, Inches(6.85), Inches(1.3), Inches(5.9), Inches(4.6), [[("課題●", {"bold": True, "color": R})],
   "● ICTの効果を計る項目を振り返りに設ける必要がある", "● ICTを扱うタイミングは検討の余地がある（実物の振り子を使う良さもある）", [("＋ 教材を毎年つくり直す準備の時間", {"color": B})]], size=19, fill=Y)
tb(s, Inches(0.6), Inches(6.1), Inches(12.1), Inches(0.7), [[("出典：第103回全国算数・数学教育研究（埼玉）大会 発表資料・大会誌原稿（新田・山本 2021）", {"size": 12, "color": GR})]], size=12)

# ---------- 9 AI LESSON REMAKE ----------
s = base("AI LESSON REMAKE（授業再構築モデル）", (
    "【0:50】アレンジの手順を、7つのステップにまとめました。過去の資料をAIに入れ、良かった点と課題を整理し、AIに改善案を出させます。"
    "大事なのはステップ5と6です。数学的に正しいか、生徒にとって価値があるかを判断し、何を残して何を変えるかを決めるのは、教師です。ここはAIに任せません。"), "第4章")
st = [("STEP1", "過去の授業資料を\n生成AIに入力"), ("STEP2", "良かった点を\n三つ整理"), ("STEP3", "課題を\n三つ整理"), ("STEP4", "AIに複数の\n改善案を提案させる"),
      ("STEP5", "教師が数学的妥当性と\n教育的価値を吟味"), ("STEP6", "残す・変える・削るで\n授業を再構築"), ("STEP7", "実践・評価・検証\n・再改善")]
for i, (h, d) in enumerate(st):
    teacher = i in (4, 5); x = Inches(0.45 + i * 1.83)
    tb(s, x, Inches(1.5), Inches(1.65), Inches(0.6), [[(h, {"bold": True, "color": W})]], size=17, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=R if teacher else G)
    tb(s, x, Inches(2.2), Inches(1.65), Inches(2.2), [d], size=15, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line=R if teacher else G, fill=Y if teacher else None)
    if i < 6: arrow(s, x + Inches(1.66), Inches(3.1), 0.17, 0.35)
tb(s, Inches(7.75), Inches(4.55), Inches(3.5), Inches(0.6), [[("人間の判断（AIに任せない）", {"bold": True, "color": R})]], size=15, align=PP_ALIGN.CENTER)
tb(s, Inches(0.6), Inches(5.2), Inches(12.1), Inches(1.6), [[("既存のAIツールの位置づけ", {"bold": True, "color": G})],
   "STEP4：導入発問メーカー／数学教材生成ツール　STEP6：板書型指導案メーカー・学習指導案メーカー　STEP7：振り返り自動化",
   [("→ 他の先生も、自分の得意な授業で同じ手順をたどれる", {"color": B, "bold": True})]], size=16, fill=LG)

# ---------- 10 残す・変える・削る ----------
s = base("残す・変える・削る", (
    "【0:40】判断の基準は三つです。残すのは授業の本質。変えるのは、本質にたどり着くための手段。削るのは、本質に役立たない作業です。"
    "変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。これが今回の考え方です。"), "第4章")
cols3 = [("残す", "授業の本質", ["数学的な価値", "中心発問", "生徒が考える時間", "実物に触れる体験"], G),
         ("変える", "本質にたどり着く手段", ["教材の形（動的教材）", "データの扱い方", "支援の出し方（段階的ヒント）"], B),
         ("削る", "本質に寄与しない作業", ["手作業の転記・計算", "毎年のデータ打ち直し", "教材の作り直し"], R)]
for i, (h, sub, li, c) in enumerate(cols3):
    x = Inches(0.6 + i * 4.15)
    tb(s, x, Inches(1.3), Inches(3.95), Inches(1.1), [[(h, {"bold": True, "color": W, "size": 30})], [(sub, {"color": W, "size": 15})]], size=30, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=c)
    tb(s, x, Inches(2.5), Inches(3.95), Inches(2.8), ["・" + t for t in li], size=19, line=c)
tb(s, Inches(0.6), Inches(5.6), Inches(12.1), Inches(1.1), [[("変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。", {"bold": True, "color": G})]], size=22, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=Y)

# ---------- 11 Before/After ----------
s = base("振り子の授業を、AIでアレンジ：Before／After", (
    "【1:10】では、振り子の授業をどうアレンジしたかです。巨大ブランコの導入、「ひもの長さと1往復の時間にはどんな関係があるか」という問い、そして実物の振り子を測る体験は、そのまま残しました。ここは譲れない部分です。"
    "変えたのは、見た目で比べていた場面を、数値の「ずれ」で比べられるようにしたこと。ヒントを3段階にして、つまずいている生徒に合わせて出せるようにしたこと。"
    "そして、生成AIの答えを生徒が確かめる活動を入れたことです。2021年の課題だった振り返りの項目も加えました。"
    "実物の振り子を測るのは時間がかかります。AIを使えば、全部シミュレーションで済ませることもできます。でも、それはしませんでした。自分の手で測って、ばらつきに悩む経験こそ、数学で現実を考える出発点だと思うからです。"), "第5章")
rows12 = [("", "Before（2021年の実践）", "After（AIでアレンジ）"),
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
        para = cell.text_frame.paragraphs[0]
        if not para.runs: continue
        f = para.runs[0].font; f.name = FONT; f.size = Pt(16); f.bold = r_ == 0 or c_ == 0
        changed = c_ == 2 and r_ > 0 and "残す" not in v and "同じ" not in v
        f.color.rgb = W if r_ == 0 else (R if changed else K)
        cell.fill.solid(); cell.fill.fore_color.rgb = (G if c_ != 2 else R) if r_ == 0 else (LG if c_ == 0 else (Y if changed else W))

# ---------- 12 振り子ラボ ----------
s = base("AIと作った教材「振り子ラボ」", (
    "【1:20】これが、生成AIと一緒に作った「振り子ラボ」です。ブラウザで動き、インストールはいりません。"
    "実物で測ったデータを入れると、表とグラフに点が出ます。生徒は関数を選び、aを動かして点に近づけます。2021年の授業のデータでは、y＝0.25x²のときのずれは0.025m、比例だと0.138mでした。見た目だけでなく、数値を根拠に「y＝ax²とみなす」と説明できます。"
    "そして、「ある生成AIは、振り子の長さは周期に比例すると答えた。本当か」と問います。AIの答えをうのみにせず、データで確かめる。これからの時代に必要な力だと思っています。"
    "最後に、周期2秒の振り子の長さを式で求め、実物で確かめます。"
    "この教材のプログラムも、AIが作ったものです。使う前に、数学的に正しいかを自分で確かめる。ここでも、判断するのは人間です。"), "第5章")
img = os.path.join(ROOT, "05_数学教材", "振り子ラボ_画面.png")
s.shapes.add_picture(img, Inches(0.45), Inches(1.2), height=Inches(4.75))
tb(s, Inches(9.05), Inches(1.2), Inches(3.95), Inches(5.7), [
    [("① 実物のデータを入力", {"bold": True, "color": G})], [("表・グラフ・式が連動", {"size": 15})],
    [("② 関数を選び a を動かす", {"bold": True, "color": G})], [("ずれ：y＝0.25x² 0.025m／比例 0.138m", {"size": 15, "color": R})],
    [("③ AIの答えを検証", {"bold": True, "color": G})], [("「長さは周期に比例する」は本当？", {"size": 15})],
    [("④ 周期2秒の振り子", {"bold": True, "color": G})], [("y＝0.25×2²＝1（m）→ 実物で確認", {"size": 15})],
    [("単一HTML・インストール不要", {"size": 14, "color": B})]], size=18, line=G)
tb(s, Inches(0.45), Inches(6.05), Inches(8.5), Inches(0.9), [[("成立条件：", {"bold": True}), ("T＝2π√(L/g) より L＝(g/4π²)T²、g/4π²≒0.248。ふれはばが小さいときの近似。", {})]], size=14, fill=LG)

# ---------- 13 1年・2年 ----------
s = base("1年「地震」・2年「桜の開花日」のアレンジ", (
    "【0:50】1年と2年も同じ手順でアレンジしました。2年の桜は、2017年までのデータを使っていましたが、AIの補助で最新の年まで整えます。数値は必ず原典と照らし合わせます。"
    "生徒は散布図に自分で直線を引いて開花日を予想し、「AIの答え」もデータで確かめます。"
    "1年の地震は、観測点のデータで比例を確かめる教材を構想しているところです。"), "第5章")
for i, (g_, bf, af) in enumerate([("2年　桜の開花日（一次関数）", ["2017年までの表データ", "グラフは手描き", "「何が影響しているか」を考える"], ["データを最新年まで更新（AIが補助・教師が原典照合）", "散布図に自分で直線を引く動的教材", "「AIの答え」をデータで確かめる"]),
                                   ("1年　地震（比例）", ["初期微動継続時間と震源からの距離を比例とみる"], ["観測点のデータで比例を確かめる教材（構想）", "比例定数＝1秒あたり何kmか", "理科との関連"])]):
    y0 = Inches(1.3 + i * 2.85)
    tb(s, Inches(0.5), y0, Inches(3.0), Inches(2.55), [[(g_, {"bold": True, "color": W})]], size=19, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=G)
    tb(s, Inches(3.65), y0, Inches(4.0), Inches(2.55), [[("Before", {"bold": True})]] + ["・" + x for x in bf], size=16, line=G)
    arrow(s, Inches(7.75), y0 + Inches(1.0), 0.4, 0.5)
    tb(s, Inches(8.25), y0, Inches(4.6), Inches(2.55), [[("After（AIでアレンジ）", {"bold": True, "color": R})]] + ["・" + x for x in af], size=16, fill=Y)

# ---------- 14 AIと共存する ----------
s = base("AIと共存する：人間にしかできない部分", (
    "【1:00】今回、AIと一緒に資料を作ってみて感じたことがあります。AIは、案を出すこと、作業をすること、教材のプログラムを書くことは、とても速いです。"
    "でも、何を残すかを決めること、目の前の生徒の表情を見て問い返すこと、授業に思いを込めること、そして結果に責任を持つことは、人間にしかできません。"
    "そもそも、土台がなければ、AIでアレンジすることもできません。私自身、土台があると言い切れるものではありませんが、14年間の授業がなければ、今回の資料は作れませんでした。"
    "これからの世の中で、AIは必ず必要になってきます。それを学校教育にどう取り入れ、人間らしさでどう扱い、人間にしかできない部分でどう共存していくか。それがとても大事なのではないかと考えています。便利だからこそ、使う側の人間の考えが問われるのだと思います。"), "第6章")
tb(s, Inches(0.6), Inches(1.3), Inches(5.9), Inches(3.4), [[("AIが得意なこと", {"bold": True, "color": B})], "・案をたくさん出す", "・資料の整理・作業", "・教材のプログラムを書く", "・データを集めて形にする"], size=20, line=B)
tb(s, Inches(6.8), Inches(1.3), Inches(5.9), Inches(3.4), [[("人間にしかできないこと", {"bold": True, "color": R})], "・何を残すかを決める", "・生徒の表情を見て問い返す", "・授業に思いを込める", "・結果に責任をもつ"], size=20, fill=Y)
tb(s, Inches(0.6), Inches(4.95), Inches(12.1), Inches(1.9), [[("土台（14年間の授業実践）があってこそ、AIでアレンジできる", {"bold": True, "color": G})],
   [("AIを学校教育にどう取り入れ、人間らしさでどう扱い、", {}), ("人間にしかできない部分でどう共存するか", {"bold": True, "color": R})]], size=20, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=LG)

# ---------- 15 期待される効果・限界・検証 ----------
s = base("期待される効果と研究の限界、今後の検証", (
    "【0:50】今回は実践前なので、成果ではなく、期待される効果としてお示しします。準備時間の短縮、段階的なヒントによる基礎の理解、数値を根拠にした説明、AIの答えを確かめる力です。"
    "一方で、業務時間のモデルは簡単な仮定であること、時間短縮や理解の向上はまだ測っていないこと、AIの出力を確かめる時間もかかることが限界です。今後、時間を記録し、この式で確かめていきます。"), "第6章")
tb(s, Inches(0.5), Inches(1.3), Inches(6.1), Inches(2.6), [[("期待される効果（未検証）", {"bold": True, "color": G})],
   "○ 教材・指導案・板書計画の準備時間の短縮", "○ 段階的ヒントによる基礎の理解の支援", "○ 数値の根拠をもって「みなす」説明", "○ AIの答えを数学的に検証する力"], size=17, line=G)
tb(s, Inches(6.8), Inches(1.3), Inches(6.0), Inches(2.6), [[("研究の限界●", {"bold": True, "color": R})],
   "● B＝W÷(N×E) は簡易的な仮定のモデル", "● 時間短縮・理解の向上は未測定", "● AI出力の確認・修正にも時間がかかる", "● 生徒の個人情報を入力しない運用が前提"], size=17, fill=Y)
tb(s, Inches(0.5), Inches(4.1), Inches(12.3), Inches(2.85), [[("今後の検証", {"bold": True, "color": B})],
   [("教師：", {"bold": True}), ("授業準備・教材作成・指導案・板書計画・AI出力の確認修正の時間、心理的負担", {})],
   [("生徒：", {"bold": True}), ("基礎の到達率、数学的な説明、つまずく生徒への支援、得点分布、振り返りの内容", {})],
   [("時間削減率（％）＝（改善前の時間 − 改善後の時間）÷ 改善前の時間 × 100", {"bold": True, "color": R})]], size=17, fill=LG)

# ---------- 16 おわりに ----------
s = base("おわりに　14年間の蓄積を込めて", (
    "【1:10】最後になります。今回の発表には、いろいろな賛否があると思います。それでも、私の14年間分の蓄積を込めました。私にとっては、最後の発表という部分もあると思っています。"
    "変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。そして、教育の質を守るために、教師の時間を守る。"
    "AIは目的ではなく手段です。判断し、思いを込めるのは人間です。14年間、たくさんの生徒と一緒に授業をつくってきました。その一つ一つが、今回の資料の土台になっています。その部分を、少しでも感じ取っていただけたらと思います。ご清聴ありがとうございました。"), "第6章")
tb(s, Inches(1.0), Inches(1.35), Inches(11.3), Inches(1.5), [[("変えるべきは、授業の本質ではない。", {"bold": True})], [("その本質にたどり着くための手段である。", {"bold": True})]], size=28, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=LG)
tb(s, Inches(1.0), Inches(3.05), Inches(11.3), Inches(1.0), [[("教育の質を守るために、教師の時間を守る。", {"bold": True, "color": R})]], size=28, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fill=Y)
tb(s, Inches(1.0), Inches(4.3), Inches(11.3), Inches(1.4), ["14年間の授業実践の蓄積を、生成AIを活用して形にしました。", "賛否はあると思います。受け取り方は、皆さんにお任せします。"], size=20, align=PP_ALIGN.CENTER)
tb(s, Inches(1.0), Inches(5.9), Inches(11.3), Inches(0.9), [[("ご清聴ありがとうございました。", {"bold": True})]], size=26, align=PP_ALIGN.CENTER)

# ---------- 補足 ----------
s = base("補足① 統計データの出典と詳細", "【補足・質疑用】統計の出典と詳細です。", "補足")
tb(s, Inches(0.5), Inches(1.3), Inches(12.3), Inches(5.6), [
    "・中学校 受験者数：H25 62,998人 → R7 36,621人　採用者数：H12 2,673人 → R7 10,168人",
    "・教師不足（R3始業日）：中学校868人（0.40%）、全体2,558人（0.31%）※全国調査はこの1回",
    "・文部科学省「令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況等」参考資料1 第7表・第2表-1・第9表-1",
    [("　https://www.mext.go.jp/content/20261001-kyoikushokuin-000046447_2.pdf", {"size": 13, "color": B})],
    "・文部科学省「教員勤務実態調査（令和4年度）集計【確定値】」",
    [("　https://www.mext.go.jp/content/20240404-mxt_zaimu01-100003067-1.pdf", {"size": 13, "color": B})],
    "・文部科学省「『教師不足』に関する実態調査」（令和4年1月）",
    [("　https://www.mext.go.jp/content/20220128-mxt_kyoikujinzai01-000020293-1.pdf", {"size": 13, "color": B})],
    [("注意：採用選考の受験者数の推移であり、教員総数の推移ではない。", {"color": R})]], size=16)
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
    [("今後のアレンジ候補：", {"bold": True}), ("スタート位置やタイミングを動かしてグラフの交点を確かめる動的教材", {})]], size=19)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
