"""読み上げ原稿（script.json）を、発表スライドの発表者ノートと 発表原稿.md に書き込む。
実行：cd 06_制作途中/deck && python3 set_notes.py   （build_deck.js の後に実行）
script.json は1スライド1要素：t=目安秒数、say=話すこと（15分版）、more=時間があれば、do=動き・注意
"""
import json, os
from pptx import Presentation

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PPTX = os.path.join(ROOT, "07_完成資料", "県大会発表_生成AI授業再構築.pptx")
MD = os.path.join(ROOT, "07_完成資料", "発表原稿.md")

S = json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8"))
prs = Presentation(PPTX)
assert len(prs.slides) == len(S), f"スライド {len(prs.slides)} 枚と原稿 {len(S)} 件が合いません"

def mmss(sec):
    return f"{sec // 60}:{sec % 60:02d}"

total = sum(x["t"] for x in S)
cum, md = 0, []
for i, (slide, x) in enumerate(zip(prs.slides, S), 1):
    cum += x["t"]
    head = f"【{i}/{len(S)}】目安 {mmss(x['t'])}（累計 {mmss(cum)}）" if x["t"] else f"【{i}/{len(S)}】補足（質疑用）"
    parts = [head, "", "▶ 話すこと", x["say"]]
    if x["more"]:
        parts += ["", "▷ 時間があれば", x["more"]]
    if x["do"]:
        parts += ["", "● 動き・注意", x["do"]]
    slide.notes_slide.notes_text_frame.text = "\n".join(parts)
    title = slide.shapes.title.text if slide.shapes.title is not None and slide.shapes.title.has_text_frame else ""
    if not title:
        texts = [sh.text_frame.text for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
        title = texts[1] if i == 1 and len(texts) > 1 else (texts[0] if texts else "")
    title = title.replace("\n", "")
    md += [f"## {i}　{title}", f"**{head}**", "", x["say"]]
    if x["more"]:
        md += ["", f"> 時間があれば：{x['more']}"]
    if x["do"]:
        md += ["", f"*動き・注意：{x['do']}*"]
    md.append("")
prs.save(PPTX)

chars = sum(len(x["say"]) for x in S if x["t"])
header = [
    "# 発表原稿（第8版：PowerPointの発表者ノートと同一）",
    "",
    f"全{len(S)}枚（本編{sum(1 for x in S if x['t'])}枚＋補足）。「話すこと」だけを読むと 目安 {mmss(total)}（{chars}字）。",
    "「時間があれば」は、時間に余裕があるときだけ足す。スライドの文字をそのまま読むのではなく、1枚に1つのことを自分の言葉で伝える。",
    "出典は各スライド下部と「補足① データの出典一覧」に記載。",
    "",
]
open(MD, "w", encoding="utf-8").write("\n".join(header + md))
print(f"notes written: {len(S)} slides, total {mmss(total)}, {chars} chars")
