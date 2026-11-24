// 板書型指導案を JSON から作る（HTML → PNG・PDF）
// 使い方: node render_bansho.js 板書.json 出力フォルダ
// 出力: 板書型指導案.html / 板書型指導案.png（A4横、印刷用）/ 板書型指導案.pdf / 板書のみ.png（指導案Wordに貼る用）
// JSON の形は ../examples/sample_bansho.json を参照。
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const [, , inFile, outDir = "."] = process.argv;
if (!inFile) { console.error("使い方: node render_bansho.js 板書.json 出力フォルダ"); process.exit(1); }
const J = JSON.parse(fs.readFileSync(inFile, "utf8"));
const baseDir = path.dirname(path.resolve(inFile));
fs.mkdirSync(outDir, { recursive: true });

const esc = s => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
// ^2 → ², 改行 → <br>, **強調** → 黄色チョーク
const fmt = s => esc(s).replace(/\^2/g, "²").replace(/\^3/g, "³").replace(/\*\*(.+?)\*\*/g, '<span class="c-yellow">$1</span>').replace(/\n/g, "<br>");
const COLORS = { white: "c-white", yellow: "c-yellow", pink: "c-pink", blue: "c-blue" };
const col = c => COLORS[c] || "c-white";

function graph(it) {
  // 黒板の簡易グラフ（点と曲線）。curve は x の式（例 "0.25*x*x"）
  const W = it.w || 260, H = it.h || 200, P = 26;
  const xmax = it.xmax || 2, ymax = it.ymax || 1;
  const X = x => P + (x / xmax) * (W - P - 8), Y = y => H - P - (y / ymax) * (H - P - 8);
  let s = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" class="graph">`;
  s += `<line x1="${P}" y1="${H - P}" x2="${W - 4}" y2="${H - P}" class="ax"/><line x1="${P}" y1="${H - P}" x2="${P}" y2="4" class="ax"/>`;
  s += `<text x="${W - 10}" y="${H - P + 18}" class="lab">${esc(it.xlabel || "x")}</text><text x="${P + 6}" y="14" class="lab">${esc(it.ylabel || "y")}</text><text x="${P - 16}" y="${H - P + 18}" class="lab">O</text>`;
  if (it.curve) {
    const f = new Function("x", `return ${it.curve};`);
    let d = ""; for (let i = 0; i <= 60; i++) { const x = xmax * i / 60, y = f(x); if (y > ymax * 1.02) break; d += `${i ? "L" : "M"}${X(x).toFixed(1)},${Y(y).toFixed(1)}`; }
    s += `<path d="${d}" class="curve ${it.curveColor === "yellow" ? "cy" : "cp"}"/>`;
  }
  for (const [x, y] of it.points || []) s += `<circle cx="${X(x)}" cy="${Y(y)}" r="4" class="pt"/>`;
  if (it.label) s += `<text x="${W * 0.45}" y="${H * 0.3}" class="lab big">${fmt(it.label)}</text>`;
  return s + "</svg>";
}

function item(it) {
  switch (it.type) {
    case "date": return `<div class="date">${fmt(it.text || "○月○日（　）")}</div>`;
    case "box": return `<div class="box b-${it.color || "white"}"><span class="blabel">${esc(it.label || "")}</span>${fmt(it.text)}</div>`;
    case "list": return `<ul class="list ${col(it.color)}">${(it.items || []).map(t => `<li>${fmt(t)}</li>`).join("")}</ul>`;
    case "formula": return `<div class="formula ${col(it.color || "yellow")}">${fmt(it.text)}</div>`;
    case "sticky": return `<div class="sticky">${fmt(it.text)}</div>`;
    case "card": return `<div class="card">${fmt(it.text)}</div>`; // 生徒の考えを書いたホワイトボード等
    case "arrow": return `<div class="arrow ${col(it.color)}">${esc(it.text || "⇩")}</div>`;
    case "image": {
      const src = "file://" + path.resolve(baseDir, it.src);
      return `<figure class="img"><span class="mag"></span><img src="${src}" style="width:${it.width || 100}%"><figcaption>${fmt(it.caption || "")}</figcaption></figure>`;
    }
    case "table": return `<table class="tbl ${col(it.color)}">${(it.rows || []).map((r, i) => `<tr>${r.map(c => i === 0 || it.headerCol ? `<th>${fmt(c)}</th>` : `<td>${fmt(c)}</td>`).join("")}</tr>`).join("")}</table>`;
    case "graph": return graph(it);
    case "note": return `<div class="note ${col(it.color)}">${fmt(it.text)}</div>`;
    default: return `<div class="text ${col(it.color)} ${it.big ? "big" : ""} ${it.bold ? "bold" : ""}">${fmt(it.text)}</div>`;
  }
}

const cols = J.columns || [];
const grid = cols.map(c => `${c.width || 1}fr`).join(" ");
const board = `<div class="board"><div class="slate" style="grid-template-columns:${grid}">${cols.map(c => `<div class="col">${(c.items || []).map(item).join("")}</div>`).join("")}</div><div class="tray"></div></div>`;
const hasNotes = cols.some(c => c.hatsumon || c.hannou || c.ryuiten);
const notes = !hasNotes ? "" : `<div class="notes" style="grid-template-columns:${grid}">${cols.map(c => `
  <div class="ncol">
    ${c.stage ? `<div class="stage">${esc(c.stage)}</div>` : ""}
    ${c.hatsumon ? `<div class="nrow"><b>○発問</b>${fmt(c.hatsumon)}</div>` : ""}
    ${c.hannou ? `<div class="nrow"><b>・反応</b>${fmt(c.hannou)}</div>` : ""}
    ${c.ryuiten ? `<div class="nrow"><b>留意点・評価</b>${fmt(c.ryuiten)}</div>` : ""}
  </div>`).join("")}</div>`;

const css = `
:root{--board:#1f4a37;--frame:#7a5230;--white:#f4f4ec;--yellow:#f6e05e;--pink:#f5a3b8;--blue:#8fd3f7;--ink:#222;--line:#9aa79a;--tint:#eef4ea;--head:#2c5f2d}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;color:var(--ink);font-family:"BIZ UDPGothic","Hiragino Maru Gothic ProN","Yu Gothic","Meiryo","IPAPGothic",sans-serif;width:1600px;padding:28px 34px}
.head{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;border:2px solid var(--head);border-radius:8px;padding:10px 16px;margin-bottom:14px;font-size:17px;line-height:1.5}
.head h1{grid-column:1/3;font-size:24px;color:var(--head);font-family:"Yu Gothic","Meiryo","IPAGothic",sans-serif}
.head .k{font-weight:bold;color:var(--head);white-space:nowrap}
.board{background:var(--frame);padding:14px;border-radius:6px;box-shadow:0 3px 8px rgba(0,0,0,.25)}
.slate{background:radial-gradient(ellipse at 40% 30%,#265a43,var(--board));min-height:${J.boardHeight || 600}px;display:grid;gap:0;padding:18px 10px;border-radius:2px}
.col{padding:0 14px;border-right:1px dashed rgba(255,255,255,.14);display:flex;flex-direction:column;gap:12px;font-size:21px;line-height:1.45}
.col:last-child{border-right:none}
.tray{height:10px;background:#5c3d22;margin:8px -4px -6px;border-radius:2px}
.c-white{color:var(--white)}.c-yellow{color:var(--yellow)}.c-pink{color:var(--pink)}.c-blue{color:var(--blue)}
.text.big{font-size:27px}.bold{font-weight:bold}
.date{color:var(--white);font-size:18px}
.box{border:2.5px solid var(--white);padding:8px 12px;color:var(--white);border-radius:3px}
.box.b-yellow{border-color:var(--yellow)}.box.b-pink{border-color:var(--pink)}.box.b-blue{border-color:var(--blue)}
.blabel{display:inline-block;font-weight:bold;margin-right:10px;color:var(--yellow)}
.box.b-pink .blabel{color:var(--pink)}
.list{list-style:none}.list li::before{content:"・"}
.formula{font-size:32px;font-weight:bold;text-align:center;font-family:"Times New Roman","IPAPMincho",serif;letter-spacing:1px}
.sticky{background:#fff35a;color:#c0182c;padding:8px 12px;font-weight:bold;box-shadow:2px 3px 4px rgba(0,0,0,.35);transform:rotate(-1deg);font-size:19px;border-radius:2px}
.card{background:#fdfdf8;color:#123;padding:8px 12px;border-radius:4px;font-size:18px;box-shadow:2px 3px 4px rgba(0,0,0,.35)}
.arrow{font-size:30px;text-align:center;line-height:1}
.img{position:relative;background:#fff;padding:6px;box-shadow:2px 3px 5px rgba(0,0,0,.4)}
.img img{display:block;margin:auto}.img figcaption{font-size:14px;color:#333;text-align:center}
.mag{position:absolute;top:-7px;left:50%;width:16px;height:16px;border-radius:50%;background:#d33;box-shadow:1px 1px 2px rgba(0,0,0,.5)}
.tbl{border-collapse:collapse;font-size:17px;width:100%}.tbl td,.tbl th{border:1.5px solid currentColor;padding:3px 6px;text-align:center;font-weight:normal}
.tbl th{color:var(--yellow)}
.graph .ax{stroke:var(--white);stroke-width:2}.graph .lab{fill:var(--white);font-size:15px}.graph .lab.big{font-size:20px;fill:var(--yellow)}
.graph .curve{fill:none;stroke-width:3}.graph .cp{stroke:var(--pink)}.graph .cy{stroke:var(--yellow)}.graph .pt{fill:var(--white)}
.note{font-size:16px;opacity:.95}
.notes{display:grid;margin-top:10px;border:1.5px solid var(--line);border-radius:6px;overflow:hidden}
.ncol{padding:8px 12px;border-right:1.5px solid var(--line);font-size:15px;line-height:1.5}
.ncol:last-child{border-right:none}
.stage{background:var(--tint);color:var(--head);font-weight:bold;margin:-8px -12px 6px;padding:5px 12px;font-size:16px}
.nrow{margin-bottom:6px}.nrow b{display:block;color:var(--head);font-size:13.5px}
.foot{margin-top:8px;font-size:12.5px;color:#666}
`;

const head = `<div class="head"><h1>${esc(J.title || "板書型指導案")}</h1>
  ${J.unit ? `<span class="k">単元</span><span>${fmt(J.unit)}</span>` : ""}
  ${J.goal ? `<span class="k">本時の目標</span><span>${fmt(J.goal)}</span>` : ""}
  ${J.eval ? `<span class="k">評価</span><span>${fmt(J.eval)}</span>` : ""}</div>`;
const foot = J.footnote ? `<div class="foot">${fmt(J.footnote)}</div>` : "";
const html = `<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>${esc(J.title || "板書型指導案")}</title><style>${css}</style></head><body>${head}${board}${notes}${foot}</body></html>`;

(async () => {
  const htmlPath = path.resolve(outDir, "板書型指導案.html");
  fs.writeFileSync(htmlPath, html);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1100 }, deviceScaleFactor: 2 });
  await page.goto("file://" + htmlPath);
  await page.waitForLoadState("networkidle");
  await page.screenshot({ path: path.resolve(outDir, "板書型指導案.png"), fullPage: true });
  await (await page.$(".board")).screenshot({ path: path.resolve(outDir, "板書のみ.png") });
  const h = await page.evaluate(() => document.body.scrollHeight);
  // A4横に収まるよう縮小して PDF 化
  const scale = Math.min(1, (297 - 16) / 25.4 * 96 / 1600, (210 - 16) / 25.4 * 96 / h);
  await page.pdf({ path: path.resolve(outDir, "板書型指導案.pdf"), format: "A4", landscape: true, printBackground: true, scale: Math.max(0.1, scale), margin: { top: "8mm", bottom: "8mm", left: "8mm", right: "8mm" } });
  await browser.close();
  console.log("saved", outDir, "(板書型指導案.html / .png / .pdf, 板書のみ.png)");
})();
