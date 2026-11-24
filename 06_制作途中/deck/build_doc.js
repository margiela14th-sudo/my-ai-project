// 研究資料（Word）— 公式 docx スキルの方式（docx-js）。文章は doc_blocks.json（build_docx.py から抽出）を使用
// 実行：cd 06_制作途中/deck && node build_doc.js
const fs = require("fs"), path = require("path"), sharp = require("sharp");
const { Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, BorderStyle,
  Header, Footer, PageNumber, LevelFormat, HeadingLevel, TableLayoutType, VerticalAlign, LineRuleType } = require("docx");

const ROOT = path.resolve(__dirname, "..", "..");
const OUT = path.join(ROOT, "07_完成資料", "県大会研究資料_生成AI授業再構築.docx");
const BLOCKS = JSON.parse(fs.readFileSync(path.join(__dirname, "doc_blocks.json"), "utf8"));
const COL = { forest: "2C5F2D", tint: "EEF4EA", sakura: "D9577A", sakuraTint: "FBE9EE", gray: "6B7A70", line: "C9D6CB", ink: "1E2A22" };
const MIN = "游明朝", GOT = "游ゴシック";
const W = 9638; // 本文幅（A4 − 左右20mm）DXA
const mm = v => Math.round(v * 56.7);

const run = (text, o = {}) => new TextRun(Object.assign({ text, font: { name: o.got ? GOT : MIN, eastAsia: o.got ? GOT : MIN } }, o));
const border1 = c => ({ style: BorderStyle.SINGLE, size: 6, color: c, space: 4 });

async function build() {
  const children = [];
  let i = 0;
  // ---- 表題ブロック ----
  const [conf, title, sub, author] = BLOCKS.slice(0, 4).map(b => b.text); i = 4;
  children.push(new Paragraph({ spacing: { after: 60 }, children: [run(conf, { got: true, size: 18, color: COL.sakura, bold: true })] }));
  children.push(new Paragraph({ spacing: { after: 40 }, children: [run(title, { got: true, size: 30, bold: true, color: COL.forest })] }));
  children.push(new Paragraph({ spacing: { after: 80 }, children: [run(sub, { got: true, size: 24, color: COL.ink })] }));
  children.push(new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 240 }, border: { bottom: border1(COL.forest) }, children: [run(author, { got: true, size: 22 })] }));

  for (; i < BLOCKS.length; i++) {
    const b = BLOCKS[i];
    if (b.t === "h1") {
      children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [run(b.text, { got: true })] }));
    } else if (b.t === "h2") {
      children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [run(b.text, { got: true })] }));
    } else if (b.t === "li") {
      if (b.mark === "・") children.push(new Paragraph({ numbering: { reference: "bul", level: 0 }, spacing: { after: 80 }, children: [run(b.text)] }));
      else children.push(new Paragraph({ indent: { left: 360, hanging: 360 }, spacing: { after: 60 }, children: [run(b.text, { size: b.mark === "◆" ? 19 : 22 })] }));
    } else if (b.t === "table") {
      const tw = b.widths.reduce((a, c) => a + c, 0), cw = b.widths.map(w => Math.round(w / tw * W));
      cw[cw.length - 1] += W - cw.reduce((a, c) => a + c, 0);
      const rows = b.rows.map((r, ri) => new TableRow({ tableHeader: ri === 0, children: r.map((v, ci) => new TableCell({
        width: { size: cw[ci], type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        shading: { type: ShadingType.CLEAR, color: "auto", fill: ri === 0 ? COL.forest : (ci === 0 ? COL.tint : "FFFFFF") },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({ spacing: { after: 0, line: 280 }, children: [run(v, { got: ri === 0 || ci === 0, size: 19, bold: ri === 0, color: ri === 0 ? "FFFFFF" : (ci === 0 ? COL.forest : COL.ink) })] })] })) }));
      const bd = { style: BorderStyle.SINGLE, size: 4, color: COL.line };
      children.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cw, layout: TableLayoutType.FIXED, rows, borders: { top: bd, bottom: bd, left: bd, right: bd, insideHorizontal: bd, insideVertical: bd } }));
      children.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
    } else if (b.t === "fig") {
      const buf = fs.readFileSync(b.path), meta = await sharp(buf).metadata();
      const wpx = Math.round(b.w * 3.78), hpx = Math.round(wpx * meta.height / meta.width);
      children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 40, line: 240, lineRule: LineRuleType.AUTO }, keepNext: true, children: [new ImageRun({ type: "png", data: buf, transformation: { width: wpx, height: hpx }, altText: { title: b.cap, description: b.cap, name: "fig" + i } })] }));
      children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [run(b.cap, { got: true, size: 17, color: COL.gray })] }));
    } else if (b.t === "callout") {
      const fill = b.col === "forest" ? COL.tint : COL.sakuraTint, col = b.col === "forest" ? COL.forest : COL.sakura;
      children.push(new Paragraph({ shading: { type: ShadingType.CLEAR, color: "auto", fill }, border: { top: border1(fill), bottom: border1(fill), left: border1(fill), right: border1(fill) }, spacing: { before: 120, after: 200, line: 360, lineRule: LineRuleType.AUTO }, indent: { left: 160, right: 160 }, children: [run(b.text, { got: true, bold: true, size: 23, color: col })] }));
    } else if (b.t === "formula") {
      children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 160 }, children: [run(b.text, { got: true, bold: true, size: 34, color: COL.forest })] }));
    } else if (b.t === "p") {
      const t = b.text;
      if (t.startsWith("従来の数学科授業実践における")) {           // 研究仮説：囲み
        children.push(new Paragraph({ shading: { type: ShadingType.CLEAR, color: "auto", fill: COL.sakuraTint }, border: { top: border1(COL.sakuraTint), bottom: border1(COL.sakuraTint), left: border1(COL.sakuraTint), right: border1(COL.sakuraTint) }, spacing: { before: 60, after: 160, line: 340 }, indent: { left: 120, right: 120 }, children: [run(t, { bold: true, got: true, size: 22, color: COL.ink })] }));
      } else if (b.align && b.align.includes("CENTER")) {         // 数式など
        children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 120 }, children: [run(t, { got: true, bold: true, size: t.startsWith("B ＝") ? 30 : 22, color: t.startsWith("B ＝") ? COL.forest : COL.sakura })] }));
      } else {
        const label = t.match(/^(期待される効果（未検証）：|研究の限界：|今後の検証：)/);
        const kids = label ? [run(label[1], { got: true, bold: true, color: COL.forest }), run(t.slice(label[1].length))] : [run(t)];
        children.push(new Paragraph({ children: kids }));
      }
    }
  }

  const doc = new Document({
    creator: "新田正幸", title: title,
    styles: {
      default: { document: { run: { font: { name: MIN, eastAsia: MIN }, size: 22, color: COL.ink }, paragraph: { spacing: { after: 160, line: 380, lineRule: LineRuleType.AUTO }, alignment: AlignmentType.BOTH } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: { name: GOT, eastAsia: GOT }, size: 26, bold: true, color: COL.forest },
          paragraph: { spacing: { before: 320, after: 140 }, keepNext: true, keepLines: true, outlineLevel: 0, shading: { type: ShadingType.CLEAR, color: "auto", fill: COL.tint }, indent: { left: 60, right: 60 }, border: { top: border1(COL.tint), bottom: border1(COL.tint), left: border1(COL.tint), right: border1(COL.tint) } } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: { name: GOT, eastAsia: GOT }, size: 23, bold: true, color: COL.forest },
          paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, keepLines: true, outlineLevel: 1 } },
      ],
    },
    numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "・", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 300 } } } }] }] },
    sections: [{
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: mm(20), bottom: mm(20), left: mm(20), right: mm(20), header: mm(10), footer: mm(10) } } },
      headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run(conf + "　発表資料", { got: true, size: 16, color: COL.gray })] })] }) },
      footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: COL.gray })] })] }) },
      children,
    }],
  });
  fs.writeFileSync(OUT, await Packer.toBuffer(doc));
  console.log("saved", OUT, children.length, "elements");
}
build();
