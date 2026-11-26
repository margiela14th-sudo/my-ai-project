// 想定質疑応答（発表者用）を Word で作る。実行：cd 06_制作途中/deck && NODE_PATH=$PWD/node_modules node build_qa.js
const fs = require("fs"), path = require("path");
const { Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle, ShadingType, Footer, PageNumber, LineRuleType } = require("docx");
const ROOT = path.resolve(__dirname, "..", "..");
const PUB = process.argv[2] === "public";
const OUT = path.join(ROOT, "07_完成資料", PUB ? "想定質疑応答_配布用.docx" : "想定質疑応答_発表者用.docx");
const D = JSON.parse(fs.readFileSync(path.join(__dirname, "qa.json"), "utf8"));
const MIN = "ＭＳ 明朝", GOT = "ＭＳ ゴシック", FOREST = "2C5F2D", SAKURA = "B8405F", GRAY = "666666";
const r = (text, o = {}) => new TextRun(Object.assign({ text, font: { name: o.got ? GOT : MIN, eastAsia: o.got ? GOT : MIN } }, o));
const kids = [];
kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [r(PUB ? "想定される質疑と回答" : D.title, { got: true, bold: true, size: 32, color: FOREST })] }));
kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [r(D.sub, { size: 18, color: GRAY })] }));
if (!PUB) D.howto.forEach(t => kids.push(new Paragraph({ indent: { left: 220, hanging: 220 }, spacing: { after: 20 }, children: [r("・" + t, { size: 19 })] })));
let n = 0;
for (const g of D.groups) {
  kids.push(new Paragraph({ keepNext: true, spacing: { before: 280, after: 100 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: FOREST, space: 2 } }, children: [r(g.name, { got: true, bold: true, size: 24, color: FOREST })] }));
  for (const it of g.items) {
    n++;
    kids.push(new Paragraph({ keepNext: true, spacing: { before: 140, after: 40 }, shading: { type: ShadingType.CLEAR, color: "auto", fill: "EEF4EA" },
      children: [r(`Q${n}${it.star && !PUB ? " ★" : ""}　`, { got: true, bold: true, size: 21, color: it.star ? SAKURA : FOREST }), r(it.q, { got: true, bold: true, size: 21 })] }));
    kids.push(new Paragraph({ keepNext: true, indent: { left: 200 }, spacing: { after: 40, line: 330, lineRule: LineRuleType.AUTO }, children: [r(PUB ? "回答　" : "答え（話す）　", { got: true, bold: true, size: 19, color: SAKURA }), r(it.a, { size: 21 })] }));
    const sx = PUB ? it.s : [it.s, it.sp].filter(Boolean).join("　");
    if (sx) kids.push(new Paragraph({ keepNext: !!it.ref, indent: { left: 200 }, spacing: { after: 20 }, children: [r("根拠・補足　", { got: true, size: 17, color: GRAY }), r(sx, { size: 17, color: GRAY })] }));
    if (it.ref) kids.push(new Paragraph({ indent: { left: 200 }, spacing: { after: 40 }, children: [r("関連スライド　" + it.ref, { got: true, size: 17, color: GRAY })] }));
  }
}
const doc = new Document({ creator: "新田正幸", title: D.title,
  styles: { default: { document: { run: { font: { name: MIN, eastAsia: MIN }, size: 21 } } } },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ["－ ", PageNumber.CURRENT, " －"], size: 18 })] })] }) },
    children: kids }] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log("saved", OUT, "Q", n); });
