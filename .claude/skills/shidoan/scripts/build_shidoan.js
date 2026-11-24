// 学習指導案（文字ベース）を JSON から Word（.docx）で作る
// 使い方: node build_shidoan.js 指導案.json 出力.docx
// 見出し＝ＭＳ ゴシック、本文＝ＭＳ 明朝、A4縦。JSON の形は ../examples/sample_shidoan.json を参照。
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType,
  BorderStyle, ShadingType, VerticalAlign, TableLayoutType, ImageRun, Footer, PageNumber, LineRuleType,
} = require("docx");

const [, , inFile, outFile] = process.argv;
if (!inFile || !outFile) { console.error("使い方: node build_shidoan.js 指導案.json 出力.docx"); process.exit(1); }
const J = JSON.parse(fs.readFileSync(inFile, "utf8"));
const baseDir = path.dirname(path.resolve(inFile));

const GOT = "ＭＳ ゴシック", MIN = "ＭＳ 明朝";
const mm = v => Math.round(v * 56.7);
const PAGE_W = 11906, ML = mm(20), MR = mm(20), W = PAGE_W - ML - MR;
const C = { head: "2C5F2D", tint: "EEF4EA", line: "8A9A86", ink: "222222" };

const r = (t, o = {}) => new TextRun({ text: String(t ?? ""), font: { name: o.got ? GOT : MIN, eastAsia: o.got ? GOT : MIN }, size: o.size || 21, bold: !!o.bold, color: o.color || C.ink });
// 「◆」「☆」などで始まる行を太字にせず、そのまま書く。改行(\n)は段落に分ける
const paras = (text, o = {}) => String(text ?? "").split("\n").map(line => new Paragraph({
  spacing: { after: o.after ?? 0, line: o.line || 300, lineRule: LineRuleType.AUTO },
  indent: o.hang ? { left: 210, hanging: 210 } : undefined,
  alignment: o.align || AlignmentType.LEFT,
  children: [r(line, o)],
}));

const kids = [];
const H1 = t => kids.push(new Paragraph({ keepNext: true, spacing: { before: 200, after: 80 }, children: [r(t, { got: true, bold: true, size: 23 })] }));
const H2 = t => kids.push(new Paragraph({ keepNext: true, spacing: { before: 100, after: 40 }, indent: { left: 210 }, children: [r(t, { got: true, size: 21 })] }));
const P = (t, indent = 420) => String(t ?? "").split("\n").forEach(line => kids.push(new Paragraph({ indent: { left: indent, firstLine: 210 }, spacing: { after: 40, line: 320, lineRule: LineRuleType.AUTO }, alignment: AlignmentType.BOTH, children: [r(line)] })));
const LI = (t, indent = 420) => kids.push(new Paragraph({ indent: { left: indent + 210, hanging: 210 }, spacing: { after: 30, line: 300, lineRule: LineRuleType.AUTO }, children: [r(t)] }));

const line = { style: BorderStyle.SINGLE, size: 4, color: C.line };
function TABLE(rows, ratios, o = {}) {
  const tot = ratios.reduce((a, b) => a + b, 0), cw = ratios.map(x => Math.floor(x / tot * W));
  cw[cw.length - 1] += W - cw.reduce((a, b) => a + b, 0);
  kids.push(new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: cw, layout: TableLayoutType.FIXED,
    borders: { top: line, bottom: line, left: line, right: line, insideHorizontal: line, insideVertical: line },
    rows: rows.map((row, ri) => new TableRow({
      tableHeader: ri === 0, cantSplit: !!o.cantSplit,
      children: row.map((v, ci) => new TableCell({
        width: { size: cw[ci], type: WidthType.DXA }, verticalAlign: ri === 0 ? VerticalAlign.CENTER : VerticalAlign.TOP,
        margins: { top: 50, bottom: 50, left: 80, right: 80 },
        shading: { type: ShadingType.CLEAR, color: "auto", fill: ri === 0 ? C.tint : (o.firstColTint && ci === 0 ? "F7F9F6" : "FFFFFF") },
        children: paras(v, { got: ri === 0, size: ri === 0 ? 19 : 19, align: ri === 0 || (o.centerFirst && ci === 0) ? AlignmentType.CENTER : AlignmentType.LEFT, hang: ri > 0 && !(o.centerFirst && ci === 0) }),
      })),
    })),
  }));
  kids.push(new Paragraph({ spacing: { after: 60 }, children: [] }));
}

// ===== 表題 =====
kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [r(J.title || `第${J.grade}学年　数学科学習指導案`, { got: true, bold: true, size: 30 })] }));
for (const [k, v] of Object.entries(J.header || {})) {
  kids.push(new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [r(`${k}　${v}`, { size: 21 })] }));
}

let n = 0;
const sec = t => H1(`${++n}　${t}`);

if (J.unit) { sec("単元名"); P(J.unit); }
if (J.unitGoals) { sec("単元の目標"); (Array.isArray(J.unitGoals) ? J.unitGoals : [J.unitGoals]).forEach((g, i, a) => a.length > 1 ? LI(`(${i + 1}) ${g}`) : P(g)); }
if (J.criteria) {
  sec("単元の評価規準");
  TABLE([["知識・技能", "思考・判断・表現", "主体的に学習に取り組む態度"], [J.criteria.knowledge, J.criteria.thinking, J.criteria.attitude]], [1, 1, 1]);
}
if (J.about) {
  sec("単元について");
  const lab = { students: "生徒観", material: "教材観", teaching: "指導観" };
  let k = 0;
  for (const key of ["students", "material", "teaching"]) if (J.about[key]) { H2(`（${++k}）${lab[key]}`); P(J.about[key]); }
}
if (J.plan) {
  sec(`指導計画（全${J.plan.reduce((a, p) => a + (+p.hours || 0), 0)}時間）`);
  TABLE([["次", "時", "学習内容", "評価規準（観点・方法）"]].concat(J.plan.map(p => [p.stage || "", `${p.hours}${p.current ? "\n（本時）" : ""}`, p.content, p.eval || ""])), [8, 10, 46, 36], { centerFirst: true });
}
if (J.lesson) {
  const L = J.lesson;
  sec("本時の学習");
  if (L.goal) { H2("（１）本時の目標"); P(L.goal); }
  if (L.eval) { H2("（２）本時の評価規準"); P(L.eval); }
  if (L.flow) {
    H2(`（${L.eval ? "３" : "２"}）本時の展開`);
    if (L.problem) kids.push(new Paragraph({ spacing: { before: 40, after: 80 }, indent: { left: 210 }, border: { top: line, bottom: line, left: line, right: line }, children: [r("課題　" + L.problem, { got: true, size: 21 })] }));
    TABLE([["段階\n（時間）", "学習活動　○主な発問　・予想される生徒の反応", "指導上の留意点　◆評価　☆ICT・AI"]]
      .concat(L.flow.map(f => [`${f.stage}\n（${f.min}分）`, f.activity, f.notes])), [12, 50, 38], { centerFirst: true, firstColTint: true });
  }
}
async function addBoard() {
  if (!J.boardImage) return;
  sec("板書計画");
  const fp = path.resolve(baseDir, J.boardImage);
  const buf = fs.readFileSync(fp);
  let w = 1600, h = 900;
  try { const sharp = require("sharp"); const m = await sharp(buf).metadata(); w = m.width; h = m.height; } catch (e) { /* sharp が無ければ 16:9 とみなす */ }
  const pw = Math.round(W / 15), ph = Math.round(pw * h / w);
  kids.push(new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({ type: fp.toLowerCase().endsWith(".jpg") ? "jpg" : "png", data: buf, transformation: { width: pw, height: ph }, altText: { title: "板書計画", description: "板書計画", name: "board" } })] }));
}

(async () => {
  await addBoard();
  if (J.sources && J.sources.length) {
    H1("＜参考・引用文献＞");
    J.sources.forEach(s => LI("・" + s, 0));
  }
  const footer = new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ["－ ", PageNumber.CURRENT, " －"], size: 18, font: MIN })] })] });
  const doc = new Document({
    creator: J.author || "", title: J.title || "学習指導案",
    styles: { default: { document: { run: { font: { name: MIN, eastAsia: MIN }, size: 21 } } } },
    sections: [{ properties: { page: { size: { width: PAGE_W, height: 16838 }, margin: { top: mm(18), bottom: mm(18), left: ML, right: MR } } }, footers: { default: footer }, children: kids }],
  });
  fs.writeFileSync(outFile, await Packer.toBuffer(doc));
  console.log("saved", outFile);
})();
