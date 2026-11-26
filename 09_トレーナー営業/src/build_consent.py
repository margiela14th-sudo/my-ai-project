"""保護者・本人向け同意書と、データ取り扱い方針（Word）を作る。〇〇は後で差し替える。"""
import os
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

OUT = os.path.join(os.path.dirname(__file__), "..", "同意書")
os.makedirs(OUT, exist_ok=True)
NAVY = RGBColor(0x0F, 0x23, 0x40)

def new_doc():
    d = Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(20)
    sec.top_margin = sec.bottom_margin = Mm(18)
    st = d.styles["Normal"]
    st.font.name = "游明朝"; st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "游明朝")
    st.paragraph_format.space_after = Pt(3)
    st.paragraph_format.line_spacing = 1.25
    return d

def para(d, text="", bold=False, size=None, align=None, color=None, after=None):
    p = d.add_paragraph()
    r = p.add_run(text); r.bold = bold
    if size: r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    if align: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    return p

def head(d, text):
    p = para(d, text, bold=True, size=11.5, color=NAVY, after=2)
    p.paragraph_format.space_before = Pt(8)
    rr = p.runs[0]; rr.font.name = "游ゴシック"; rr._element.rPr.rFonts.set(qn("w:eastAsia"), "游ゴシック")

def items(d, lst, mark="・"):
    for t in lst:
        p = para(d, f"{mark}{t}", after=1)
        p.paragraph_format.left_indent = Mm(4); p.paragraph_format.first_line_indent = Mm(-4)

def title(d, text, sub=None):
    p = para(d, text, bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, color=NAVY, after=2)
    rr = p.runs[0]; rr.font.name = "游ゴシック"; rr._element.rPr.rFonts.set(qn("w:eastAsia"), "游ゴシック")
    if sub: para(d, sub, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, after=10)

def table(d, rows, widths, header=True):
    t = d.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for j, w in enumerate(widths):
        t.columns[j].width = Mm(w)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.width = Mm(widths[j]); c.text = ""
            r = c.paragraphs[0].add_run(v); r.font.size = Pt(10)
            if header and i == 0: r.bold = True
    return t

# ---------------- 1. データ取り扱い方針 ----------------
d = new_doc()
title(d, "トレーニング測定に関する映像・音声・測定データの取り扱い方針", "フォロワーシップコーチ　〇〇 〇〇　（制定：20〇〇年〇月〇日）")
para(d, "フォロワーシップコーチ 〇〇 〇〇（以下「私」）は、〇〇高等学校〇〇部（以下「部」）で行うトレーニングと効果測定において、生徒の皆さんの映像・音声・測定データを次のとおり取り扱います。")

head(d, "1　利用の目的")
para(d, "取得したデータは、次の目的だけに使います。これ以外の目的には使いません。")
items(d, ["トレーニングの効果を測定し、生徒本人と監督（顧問）にフィードバックすること",
          "トレーニングの内容を改善すること"])
para(d, "測定結果は指導の参考資料です。学校の成績評価、入試・推薦、進路の判断には使いません。")

head(d, "2　取得するデータと取得しないデータ")
table(d, [["区分", "内容"],
          ["測定データ", "反応時間、注意課題（ストループ課題など）、アジリティ、リズム再現、競技中の成功率など"],
          ["映像", "練習・試合の様子（DJI製カメラ等で、固定位置から撮影）"],
          ["音声", "練習・試合中の声かけ・コール（Plaud NotePin等の小型録音機を、同意した生徒・指導者が装着）"],
          ["アンケート", "試合時の緊張・集中などの自己評価"],
          ["取得しないもの", "学業成績、健康・病歴に関する情報、更衣室など練習・試合以外の場面の映像・音声"]], [35, 135])

head(d, "3　同意と、同意しない生徒への配慮")
items(d, ["撮影・録音の前に、学校の許可と、保護者・生徒本人の同意（別紙の同意書）をいただきます。",
          "同意の項目は「測定」「映像」「音声」「AI分析」に分かれており、一部だけ同意することもできます。",
          "同意しない生徒は、撮影・録音の対象にしません。映り込んだ場合は、ぼかしを入れるか、その部分を削除します。",
          "同意しないこと、または同意を取り消すことで、部活動での扱いに不利益が生じることはありません。"])

head(d, "4　AI（人工知能）サービスの利用")
items(d, ["文字起こしや映像の集計にAIサービスを使います。使うサービスの名前は、別表で学校・保護者にお知らせします。",
          "AIに渡す前に、生徒の氏名を番号に置き換えます（顔が映る映像を分析する場合は、事前に学校と方法を確認します）。",
          "入力したデータがAIの学習に使われない設定・契約になっているサービスだけを使います。",
          "AIが出した結果は、私が必ず目で確認してからレポートにします。"])

head(d, "5　保存と管理")
items(d, ["データは、パスワードと二段階認証を設定した専用の保存場所で管理し、私以外は扱いません。",
          "撮影・録音に使う機器と端末には画面ロックをかけ、紛失した場合はすぐに学校へ報告します。",
          "映像・音声（元データ）は、分析が終わりしだい、撮影・録音から〇〇日以内に削除します。",
          "測定の数値とレポートは、契約終了から〇年以内に削除します。"])

head(d, "6　外部への提供・公開")
items(d, ["データを第三者に提供したり、公開したりしません。SNS・ホームページ・広告にも使いません。",
          "ただし、法令にもとづく場合は除きます。",
          "学校説明会・保護者会などで部の取り組みを紹介する場合は、個人が特定できない集計の数値だけを使い、同意書で「紹介への利用」に同意をいただいた場合に限ります。"])

head(d, "7　確認・訂正・削除・同意の取り消し")
para(d, "生徒本人・保護者は、いつでも自分（お子さま）のデータの確認、訂正、削除、同意の取り消しを求めることができます。下の連絡先にお申し出ください。〇〇日以内に対応し、結果をお知らせします。")

head(d, "8　漏えいなどが起きたとき")
para(d, "データの漏えい・紛失のおそれがあるときは、すぐに学校と該当する保護者へ報告し、被害を広げないための対応を行います。法令で必要な場合は、個人情報保護委員会へ報告します。")

head(d, "9　この方針の変更")
para(d, "この方針を変更するときは、事前に学校と保護者にお知らせします。")

head(d, "お問い合わせ先")
para(d, "フォロワーシップコーチ　〇〇 〇〇　　電話：〇〇〇-〇〇〇〇-〇〇〇〇　　メール：〇〇〇〇@〇〇〇〇")

head(d, "別表　利用する機器・サービス（予定）")
table(d, [["用途", "機器・サービス", "データの扱い（確認事項）"],
          ["音声の録音・文字起こし", "Plaud NotePin／〇〇", "保存場所：〇〇　学習への利用：なし（規約を確認済み）"],
          ["映像の撮影", "DJI製カメラ（〇〇）", "保存場所：〇〇"],
          ["映像・データの分析", "〇〇", "保存場所：〇〇　学習への利用：なし（規約を確認済み）"]], [42, 50, 78])
d.save(os.path.join(OUT, "データ取り扱い方針.docx"))

# ---------------- 2. 同意書 ----------------
d = new_doc()
para(d, "20〇〇年〇月〇日", align=WD_ALIGN_PARAGRAPH.RIGHT, after=0)
para(d, "保護者の皆さま・部員の皆さんへ", after=0)
para(d, "フォロワーシップコーチ　〇〇 〇〇", align=WD_ALIGN_PARAGRAPH.RIGHT, after=8)
title(d, "トレーニングの効果測定（映像・音声の記録を含む）についてのお願い")
para(d, "〇〇高等学校〇〇部では、学校の許可を得て、脳と感覚のトレーニング（ライフキネティック、スポーツリズムトレーニング）を行います。トレーニングの効果を確かめるため、次の測定と記録を行いたいと考えています。")
table(d, [["項目", "内容"],
          ["測定", "反応時間・注意課題・アジリティなどを、開始時・6週・12週ごろに測ります（1回20分程度）"],
          ["映像", "練習・試合の様子を、固定したカメラで撮影します"],
          ["音声", "練習・試合中の声かけを、小型の録音機（胸元につけるもの）で録音します"],
          ["AI分析", "氏名を番号に置き換えたうえで、AIサービスで文字起こしや集計をします"]], [30, 140])
para(d, "")
para(d, "記録したデータは、効果の測定と指導の改善だけに使い、外部への提供・公開はしません。くわしくは別紙「データ取り扱い方針」をご覧ください。同意は項目ごとに選べます。同意しなくても、部活動で不利益になることは一切ありません。また、同意はいつでも取り消せます。")

para(d, "同意書（次のページ）は、〇月〇日までに部の顧問の先生へ提出してください。", bold=True)
d.add_page_break()
title(d, "同　意　書")
para(d, "フォロワーシップコーチ　〇〇 〇〇　様", after=4)
para(d, "「データ取り扱い方針」の説明を受け、内容を理解しました。各項目の「同意する」「同意しない」のどちらかに、レ点をつけて回答します。")
rows = [["項目", "同意する", "同意しない"],
        ["① 測定（反応時間・アジリティ等）に参加すること", "□", "□"],
        ["② 練習・試合の映像を撮影すること", "□", "□"],
        ["③ 練習・試合中の音声を録音すること（録音機を装着することを含む）", "□", "□"],
        ["④ 氏名を番号に置き換えたデータを、AIサービスで分析すること", "□", "□"],
        ["⑤（任意）個人が特定できない集計の数値を、学校説明会・保護者会での部の紹介に使うこと", "□", "□"]]
t = table(d, rows, [126, 22, 22])
for r in t.rows[1:]:
    for c in r.cells[1:]: c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
para(d, "")
table(d, [["学年・組", "　　年　　組", "生徒氏名（自署）", ""],
          ["保護者氏名（自署）", "", "記入日", "　　年　　月　　日"]], [32, 45, 38, 55], header=False)
para(d, "※生徒本人も内容を確認し、氏名を自分で記入してください。", size=9)

d.add_page_break()
title(d, "同意の取り消し・データ削除の申出書")
para(d, "フォロワーシップコーチ　〇〇 〇〇　様", after=4)
para(d, "先に提出した同意書について、次の項目の同意を取り消します。あわせて、該当するデータの削除を求めます。")
table(d, [["取り消す項目（□にレ点）"],
          ["□ ① 測定　　□ ② 映像　　□ ③ 音声　　□ ④ AI分析　　□ ⑤ 部の紹介への利用"]], [170], header=False)
para(d, "")
table(d, [["学年・組", "　　年　　組", "生徒氏名", ""],
          ["保護者氏名", "", "記入日", "　　年　　月　　日"]], [32, 45, 38, 55], header=False)
para(d, "受け付けてから〇〇日以内に対応し、結果をお知らせします。", size=9)
d.save(os.path.join(OUT, "同意書_保護者・生徒用.docx"))
print("ok")
