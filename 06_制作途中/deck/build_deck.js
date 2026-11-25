// 県大会発表スライド（公式 pptx スキルの方針：構造化デッキ・テーマ・帯や線を使わない・アイコン円のモチーフ）
// 実行：cd 06_制作途中/deck && node build_deck.js
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const gi = require("react-icons/gi");
const { applyTheme } = require("/root/.claude/skills/synced/fcbb0551-8e0b-45b5-a64a-4a5f660efc7b_964ac49c-86a9-4711-8821-480c86028dac/pptx/scripts/apply_theme.js");

const ROOT = path.resolve(__dirname, "..", "..");
const OUT = path.join(ROOT, "07_完成資料", "県大会発表_生成AI授業再構築.pptx");
const NOTES = JSON.parse(fs.readFileSync(path.join(__dirname, "notes.json"), "utf8"));

// ---- テーマ：過去の発表の緑を受け継ぐ「森の緑」＋桜色のアクセント ----
const HEX = { ink: "1E2A22", forest: "2C5F2D", moss: "97BC62", tint: "EEF4EA", sakura: "D9577A", sakuraTint: "FBE9EE", amber: "E9A23B", ai: "3E7CB1", aiTint: "E8F0F8", gray: "6B7A70", white: "FFFFFF", line: "D5DED6" };
const THEME = {
  name: "Forest Sakura", headFontFace: "Meiryo", bodyFontFace: "Meiryo",
  colors: { dk1: HEX.ink, lt1: HEX.white, dk2: HEX.forest, lt2: HEX.tint, accent1: HEX.forest, accent2: HEX.moss, accent3: HEX.sakura, accent4: HEX.amber, accent5: HEX.ai, accent6: HEX.gray, hlink: HEX.ai, folHlink: HEX.gray },
};
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "生成AIを活用した数学科授業の改善と新たな授業モデルの提案";
pres.author = "新田正幸";
const C = pres.SchemeColor;
// 色の対応：text1=ink, text2=forest, background1=white, background2=tint, accent3=sakura, accent5=ai, accent6=gray
const FOREST = C.accent1, MOSS = C.accent2, SAKURA = C.accent3, AMBER = C.accent4, AI = C.accent5, GRAY = C.accent6, INK = C.text1, WHITE = C.background1, TINT = C.background2;
const CONF = "令和8年度山口県中学校数学教育第二地区研究協議会";
const TITLE = "生成AIを活用した数学科授業の改善と新たな授業モデルの提案";

// ---- レイアウト（枠） ----
pres.defineSlideMaster({
  title: "CONTENT", background: { color: WHITE },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 10.6, h: 0.85, fontSize: 30, bold: true, color: FOREST, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "sec", type: "body", x: 10.9, y: 0.45, w: 1.85, h: 0.45, fontSize: 13, bold: true, color: SAKURA, align: "right", valign: "middle", margin: 0 }, text: "" } },
    { text: { text: CONF + "　発表資料", options: { x: 0.6, y: 7.0, w: 9.5, h: 0.3, fontSize: 10, color: GRAY, margin: 0 } } },
  ],
  slideNumber: { x: 12.15, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: GRAY, align: "right" },
});
pres.defineSlideMaster({ title: "DARK", background: { color: FOREST }, objects: [] });

// ---- 部品 ----
const iconCache = {};
async function icon(Comp, color = "FFFFFF") {
  const key = Comp.name + color;
  if (!iconCache[key]) {
    const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: 256 }));
    const buf = await sharp(Buffer.from(svg)).png().toBuffer();
    iconCache[key] = "image/png;base64," + buf.toString("base64");
  }
  return iconCache[key];
}
async function iconCircle(s, Comp, x, y, d, fill, iconColor = HEX.white) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill } });
  const pad = d * 0.24;
  s.addImage({ data: await icon(Comp, iconColor), x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad });
}
function card(s, x, y, w, h, fill = TINT, shadow = false) {
  const o = { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.12 };
  if (shadow) o.shadow = { type: "outer", color: "000000", opacity: 0.12, blur: 6, offset: 2, angle: 90 };
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, o);
}
function T(s, text, o) { s.addText(text, Object.assign({ isTextBox: true, margin: 0, valign: "top", color: INK, fontSize: 16 }, o)); }
function numCircle(s, n, x, y, d, fill) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill } });
  T(s, String(n), { x, y, w: d, h: d, align: "center", valign: "middle", color: WHITE, bold: true, fontSize: Math.round(d * 30) });
}
let idx = 0;
function content(title, sec, section) {
  if (section) pres.addSection({ title: section });
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: curSection(section) });
  s.addText(title, { placeholder: "title" });
  if (sec) s.addText(sec, { placeholder: "sec" });
  s.addNotes(NOTES[idx++]);
  return s;
}
let _sec = null; function curSection(s) { if (s) _sec = s; return _sec; }
const chartText = { catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", titleFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", catAxisLabelColor: HEX.gray, valAxisLabelColor: HEX.gray, catAxisLabelFontSize: 11, valAxisLabelFontSize: 11, titleFontSize: 14, titleColor: HEX.ink, valGridLine: { color: HEX.line, size: 0.75 }, catGridLine: { style: "none" }, showLegend: false };

// ===== 第4版：1枚1メッセージ・文字を減らす・大きな数字・章扉でリズム（17〜18分想定） =====
const IMG = path.join(ROOT, "01_過去資料", "画像");
function fit(s, file, iw, ih, x, y, bw, bh) {
  const r = Math.min(bw / iw, bh / ih), w = iw * r, h = ih * r, ox = x + (bw - w) / 2, oy = y + (bh - h) / 2;
  s.addShape(pres.shapes.RECTANGLE, { x: ox - 0.05, y: oy - 0.05, w: w + 0.1, h: h + 0.1, fill: { color: WHITE }, line: { color: HEX.line, width: 1 }, shadow: { type: "outer", color: "000000", opacity: 0.15, blur: 6, offset: 2, angle: 90 } });
  s.addImage({ path: file, x: ox, y: oy, w, h });
}
function tag(s, text, col) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 11.05, y: 0.5, w: 1.7, h: 0.42, fill: { color: col }, line: { color: col }, rectRadius: 0.21 });
  T(s, text, { x: 11.05, y: 0.5, w: 1.7, h: 0.42, fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle" });
}
const bl = (arr, o = {}) => arr.map((t, j) => ({ text: t, options: Object.assign({ bullet: true, breakLine: j < arr.length - 1 }, o) }));
const N = [];               // ノート（スライド順）
const note = t => N.push(t);
// 章扉＝つなぎのスライド：「ここまで」と「この章で」を必ず示す（第9版）
function divider(num, title, sub, notesText, bridge) {
  pres.addSection({ title: num + " " + title }); _sec = num + " " + title;
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: _sec }); s.addNotes(notesText);
  T(s, num, { x: 0.9, y: 0.9, w: 6, h: 0.7, fontSize: 26, bold: true, color: MOSS });
  T(s, title, { x: 0.9, y: 1.6, w: 11.5, h: 1.2, fontSize: 44, bold: true, color: WHITE, valign: "middle" });
  if (sub) T(s, sub, { x: 0.9, y: 2.85, w: 11.5, h: 0.6, fontSize: 22, color: "E5EEDF" });
  if (bridge) {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.9, y: 3.9, w: 11.55, h: 2.6, fill: { color: "3B7A3C" }, line: { color: "3B7A3C" }, rectRadius: 0.15 });
    const rows = [["ここまで", bridge[0], "E5EEDF"], ["この章で", bridge[1], "F4B6C6"]];
    rows.forEach(([lab, txt, col], k) => {
      T(s, lab, { x: 1.2, y: 4.1 + k * 1.15, w: 1.7, h: 0.95, fontSize: 18, bold: true, color: "CFE3C0", valign: "middle" });
      T(s, txt, { x: 2.95, y: 4.1 + k * 1.15, w: 9.3, h: 0.95, fontSize: 22, bold: true, color: col, valign: "middle" });
    });
  }
  return s;
}
function slide(title, sec, notesText) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: _sec });
  s.addText(title, { placeholder: "title" });
  if (sec) s.addText(sec, { placeholder: "sec" });
  s.addNotes(notesText);
  return s;
}

(async () => {
  // 1 表紙
  pres.addSection({ title: "はじめに" }); _sec = "はじめに";
  let s = pres.addSlide({ masterName: "DARK", sectionTitle: _sec });
  s.addNotes("【0:20】今から、「生成AIを活用した数学科授業の改善と新たな授業モデルの提案 ～関数分野における従来の授業実践を通して～」という題で発表をします。下関市立名陵中学校の新田です。よろしくお願いします。");
  T(s, CONF, { x: 0.8, y: 0.6, w: 9, h: 0.4, fontSize: 16, color: MOSS, bold: true });
  T(s, "生成AIを活用した\n数学科授業の改善と\n新たな授業モデルの提案", { x: 0.8, y: 1.55, w: 8.6, h: 2.4, fontSize: 38, bold: true, color: WHITE, valign: "middle" });
  T(s, "～関数分野における従来の授業実践を通して～", { x: 0.8, y: 3.95, w: 8.4, h: 0.5, fontSize: 20, color: "E5EEDF" });
  T(s, "下関市立名陵中学校　新田正幸", { x: 0.8, y: 6.0, w: 7, h: 0.5, fontSize: 22, color: WHITE });
  s.addShape(pres.shapes.OVAL, { x: 9.6, y: 1.6, w: 3.3, h: 3.3, fill: { color: "3B7A3C" }, line: { color: "3B7A3C" } });
  s.addImage({ data: await icon(gi.GiPendulumSwing, "E5EEDF"), x: 10.35, y: 2.35, w: 1.8, h: 1.8 });

  // 2 AIで作った
  s = slide("この発表資料について", "はじめに", "【0:40】はじめに、お伝えしておきたいことがあります。今回の発表資料は、構成もスライドも原稿も、そして後でお見せする教材も、すべて生成AIを活用して作りました。賛否両論あると思います。ただ、中身には、私がこの14年間、授業で大切にしてきた思いと、その蓄積を載せたつもりです。AIを使う前の資料も、そのまま残してお見せします。どう受け取るかは、皆さんの受け取り方次第です。");
  T(s, [{ text: "生成AIを使えば、\n" }, { text: "このような資料が作れる時代", options: { color: SAKURA } }, { text: "です。" }], { x: 0.8, y: 1.5, w: 11.7, h: 2.4, fontSize: 42, bold: true, valign: "middle" });
  await iconCircle(s, fa.FaRobot, 0.8, 4.35, 0.9, HEX.ai);
  T(s, "使っても、使わなくてもいい", { x: 1.9, y: 4.35, w: 4.6, h: 0.9, fontSize: 22, bold: true, color: AI, valign: "middle" });
  await iconCircle(s, gi.GiPlantSeed, 6.6, 4.35, 0.9, HEX.forest);
  T(s, "ただ、学びは止めない", { x: 7.7, y: 4.35, w: 5.0, h: 0.9, fontSize: 24, bold: true, color: FOREST, valign: "middle" });
  T(s, "この資料も生成AIで作りました（中身は14年間の授業）。自慢ではなく、今の時代を共有するためです。", { x: 0.8, y: 5.75, w: 11.7, h: 0.6, fontSize: 20, italic: true, color: GRAY });

  // 3 二つの問題意識
  s = slide("今日、皆さんと考えたい二つの問い", "はじめに", "【0:50】今日の発表には、二つの問題意識があります。一つは、教員不足という社会的な問題です。なぜ数学の研究協議会でこれを取り上げるのか。それは、授業の質を支える教師の時間が、この問題と切り離せないと考えるからです。もう一つは、学校現場へのAIの活用、とくに授業づくりにどう生かすかという問題です。二つは別々の問題ですが、「教師の時間」と「授業の質」というところで重なり合っていると感じています。");
  s.addShape(pres.shapes.OVAL, { x: 0.9, y: 1.35, w: 6.75, h: 4.6, fill: { color: HEX.forest, transparency: 82 }, line: { color: HEX.forest, width: 2 } });
  s.addShape(pres.shapes.OVAL, { x: 5.65, y: 1.35, w: 6.75, h: 4.6, fill: { color: HEX.ai, transparency: 82 }, line: { color: HEX.ai, width: 2 } });
  T(s, [{ text: "問い①\n", options: { fontSize: 24, color: FOREST } }, { text: "教員の\n魅力とは、\n何か" }], { x: 1.5, y: 2.1, w: 4.0, h: 2.8, fontSize: 32, bold: true, valign: "middle" });
  T(s, [{ text: "問い②\n", options: { fontSize: 24, color: AI } }, { text: "学び続ける\nために、AIと\n共存する" }], { x: 7.8, y: 2.1, w: 4.0, h: 2.8, fontSize: 32, bold: true, valign: "middle", align: "right" });
  T(s, "学び\n続ける\n教師", { x: 5.7, y: 2.45, w: 1.9, h: 2.3, fontSize: 22, bold: true, color: SAKURA, align: "center", valign: "middle" });
  T(s, "教員不足という大きな問題を、「教員の魅力」に絞って考えたい", { x: 0.8, y: 6.1, w: 11.7, h: 0.6, fontSize: 22, bold: true, color: FOREST, align: "center" });

  // 4 答えではなく問い
  s = slide("今日の発表の流れ", "はじめに", "【0:40】今日の発表の流れです。まず、二つの問題を提起します。一つ目は教員不足、二つ目は学校でのAIの活用です。どちらも、関数やデータで数値を見ていきます。次に、私の過去の数学の授業を、AIを使う前と使った後で比べます。実証まではできていませんが、どんな可能性があり、どんな利点と欠点があるのかを考えます。そして最後に、研究仮説から考察し、結論として、AIの価値を決めるのは使う人の質だ、というところまでお話しします。どちらの問題にも一つの答えを示すつもりはありません。最後に、皆さんと指導助言の先生にご意見をいただけたらと思っています。");
  const flow = [[fa.FaUsers, HEX.forest, "第1章", "教員不足を\n数値で見る\n（問い①の入口）"], [fa.FaLaptopCode, HEX.ai, "第2章", "教員のAI活用を\n数値で見る\n（問い②の背景）"], [fa.FaSyncAlt, HEX.moss, "第3・4章", "自分の授業で\n試してみた\n（AIの前と後）"], [fa.FaSearch, HEX.gray, "第5章", "考察と提案\n言えること・\nまだ言えないこと"], [gi.GiPlantSeed, HEX.sakura, "第6章", "結論と\n二つの問い"]];
  for (let i = 0; i < 5; i++) {
    const [ic, col, h, t] = flow[i], x = 0.8 + i * 2.42, last = i === 4;
    card(s, x, 1.6, 2.15, 3.6, last ? HEX.sakuraTint : TINT);
    await iconCircle(s, ic, x + 0.6, 1.85, 0.95, col);
    T(s, h, { x, y: 2.95, w: 2.15, h: 0.5, fontSize: 18, bold: true, color: last ? SAKURA : INK, align: "center" });
    T(s, t, { x, y: 3.45, w: 2.15, h: 1.6, fontSize: 16, align: "center", valign: "middle" });
    if (i < 4) s.addImage({ data: await icon(fa.FaArrowRight, HEX.gray), x: x + 2.17, y: 3.2, w: 0.23, h: 0.25 });
  }
  T(s, [{ text: "結論：" }, { text: "授業の質 ＝ 土台 × AI", options: { color: SAKURA } }, { text: "　土台を育てるのは、学び続けること" }], { x: 0.8, y: 5.55, w: 11.9, h: 0.8, fontSize: 24, bold: true, align: "center", valign: "middle" });

  // 5 14年間の歩み
  s = slide("14年間の歩み", "はじめに", "【0:40】少しだけ、これまでの歩みを振り返ります。2015年の北海道大会では平行四辺形の証明、2017年の和歌山大会では複合図、2018年の東京大会ではお掃除ロボットの授業を発表しました。2021年は振り子とGeoGebra、2022年はジグソー法、2023年は教師の手立てです。振り返ると、どれも「良い授業を、新しい手段で改善する」ことでした。今回、その手段が生成AIです。");
  const tl = [["2015", "平行四辺形"], ["2016", "仮定と証明"], ["2017", "複合図"], ["2018", "お掃除ロボ"], ["2021", "振り子×ICT"], ["2022", "ジグソー法"], ["2023", "ねじれの位置"], ["2026", "生成AI"]];
  s.addShape(pres.shapes.LINE, { x: 1.0, y: 3.2, w: 11.3, h: 0, line: { color: HEX.line, width: 4 } });
  for (let i = 0; i < tl.length; i++) {
    const cx = 1.0 + i * 1.614, last = i === tl.length - 1, col = last ? SAKURA : FOREST;
    T(s, tl[i][0], { x: cx - 0.8, y: 1.9, w: 1.6, h: 0.6, fontSize: 22, bold: true, color: col, align: "center" });
    s.addShape(pres.shapes.OVAL, { x: cx - 0.3, y: 2.9, w: 0.6, h: 0.6, fill: { color: col }, line: { color: WHITE, width: 3 } });
    T(s, tl[i][1], { x: cx - 0.8, y: 3.8, w: 1.6, h: 0.9, fontSize: 17, bold: true, align: "center" });
  }
  T(s, [{ text: "新しい手段を" }, { text: "学び", options: { color: SAKURA } }, { text: "、授業を改善し続けてきた" }], { x: 0.8, y: 5.3, w: 11.7, h: 0.9, fontSize: 30, bold: true, align: "center", valign: "middle" });

  // 5b ずっと続けてきたこと：原問題をアレンジ
  s = slide("ずっと続けてきたこと：原問題をアレンジする", "はじめに", "【0:50】そして、14年間ずっと続けてきたことがあります。それは、教科書の原問題をアレンジすることです。これは2015年の北海道大会の発表スライドです。左が教科書にある命題、右が、生徒が仮定を意識できるようにアレンジした教材です。2017年の複合図も、2021年の振り子も、いつも原問題をアレンジして授業をつくってきました。今回は、そのアレンジを、AIと一緒にやってみました。");
  tag(s, "AI活用前", HEX.gray);
  fit(s, path.join(IMG, "2015_発表スライド_教科書の命題.png"), 1467, 825, 0.8, 1.55, 5.3, 3.0);
  s.addImage({ data: await icon(fa.FaArrowRight, HEX.sakura), x: 6.35, y: 2.75, w: 0.6, h: 0.55 });
  fit(s, path.join(IMG, "2015_発表スライド_アレンジした教材.png"), 1467, 825, 7.2, 1.55, 5.3, 3.0);
  T(s, "原問題（教科書）", { x: 0.8, y: 4.7, w: 5.3, h: 0.5, fontSize: 20, bold: true, color: GRAY, align: "center" });
  T(s, "アレンジした教材", { x: 7.2, y: 4.7, w: 5.3, h: 0.5, fontSize: 20, bold: true, color: FOREST, align: "center" });
  T(s, "2015年 全国大会（北海道）の発表スライド", { x: 0.8, y: 5.15, w: 11.7, h: 0.4, fontSize: 14, color: GRAY, align: "center" });
  T(s, [{ text: "2015 平行四辺形 ／ 2017 複合図 ／ 2021 振り子　→　" }, { text: "2026 AIでアレンジ", options: { color: SAKURA } }], { x: 0.8, y: 5.75, w: 11.7, h: 0.8, fontSize: 21, bold: true, align: "center", valign: "middle" });

  // ===== 第1章 =====
  divider("第1章", "教員不足を、数値で見る", "問い①の背景　関数・データの目で", "【0:10】一つ目の問題意識、教員不足です。ここは、関数的な表現やデータの活用の視点で、数値を少し見てみたいと思いました。資料として載せておく意味合いですので、ご覧ください。", ["新しい手段を学びながら、授業を改善してきた", "教員のなり手と時間は、いまどうなっているか（教員の魅力を考える入口）"]);

  // 7 採用倍率
  s = slide("中学校の教員採用倍率", "問い①の背景", "【0:40】中学校の教員採用の倍率は、平成12年度の17.9倍から、令和7年度は3.6倍まで下がり、過去最低です。ただし、これは受験者数の推移で、教員の総数が減っているという意味ではありません。採用者数が増えたことも影響しています。ちなみに、山口県の中学校数学は、令和7年度、2.2倍でした。");
  T(s, "17.9倍", { x: 0.8, y: 1.6, w: 4.6, h: 1.4, fontSize: 72, bold: true, color: GRAY, valign: "middle" });
  T(s, "平成12年度", { x: 0.8, y: 3.0, w: 4.6, h: 0.5, fontSize: 20, color: GRAY });
  s.addImage({ data: await icon(fa.FaArrowDown, HEX.sakura), x: 1.9, y: 3.6, w: 0.7, h: 0.7 });
  T(s, "3.6倍", { x: 0.8, y: 4.3, w: 4.6, h: 1.4, fontSize: 88, bold: true, color: SAKURA, valign: "middle" });
  T(s, "令和7年度（過去最低）", { x: 0.8, y: 5.7, w: 4.6, h: 0.5, fontSize: 20, bold: true, color: SAKURA });
  const csv = fs.readFileSync(path.join(ROOT, "02_統計データ", "全国_教員採用選考_長期推移.csv"), "utf8").replace(/^﻿/, "").trim().split("\n").map(l => l.split(","));
  const rows = csv.slice(1).filter(r => +r[1] >= 2000);
  const labs = rows.map(r => r[0].replace("年度", "").replace("平成", "H").replace("令和", "R").replace("元", "1"));
  s.addChart(pres.charts.LINE, [{ name: "採用倍率", labels: labs, values: rows.map(r => +r[4]) }], Object.assign({}, chartText, {
    x: 5.8, y: 1.45, w: 7.0, h: 4.9, showTitle: false, chartColors: [HEX.sakura], lineSize: 4, lineDataSymbolSize: 7, valAxisMinVal: 0, valAxisMaxVal: 20, catAxisLabelFrequency: 3, catAxisLabelFontSize: 13, valAxisLabelFontSize: 13 }));
  T(s, "出典：文部科学省「令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況について」参考資料1 第7表 p.9（2025年12月25日公表）　※採用倍率＝受験者数÷採用者数。受験者数の推移であり、教員総数の推移ではない", { x: 0.8, y: 6.45, w: 12, h: 0.4, fontSize: 11, color: GRAY });

  // 7b 一次関数とみなす
  s = slide("受験者数を、一次関数とみなすと", "問い①の背景", "【0:50】ここを数学の目で見てみます。令和元年から7年の中学校の受験者数は、ほぼ一直線に減っています。一次関数とみなすと、変化の割合は、1年あたり約マイナス2,095人、およそ2,100人です。2年生で学ぶ「変化の割合」が、そのまま今の学校の課題を読み解く道具になります。ただし、このまま減り続けると決めつけることはできません。データから何が言えて、何が言えないかを考えることも、数学の大切な見方だと思います。");
  { const yrs = [2019, 2020, 2021, 2022, 2023, 2024, 2025], obs = [49190, 45763, 44105, 42587, 40960, 39273, 36621];
    const fitv = yrs.map(x => Math.round(49190 - 2094.8 * (x - 2019)));
    s.addChart(pres.charts.LINE, [{ name: "受験者数（実際）", labels: ["R1", "R2", "R3", "R4", "R5", "R6", "R7"], values: obs }, { name: "一次関数とみなした直線", labels: ["R1", "R2", "R3", "R4", "R5", "R6", "R7"], values: fitv }],
      Object.assign({}, chartText, { x: 0.8, y: 1.45, w: 7.3, h: 4.9, chartColors: [HEX.sakura, HEX.gray], lineSize: 3, lineDataSymbolSize: 8, showLegend: true, legendPos: "b", legendFontSize: 13, legendFontFace: "+mn-lt", valAxisMinVal: 30000, valAxisMaxVal: 52000, valAxisLabelFormatCode: "#,##0", catAxisLabelFontSize: 14 })); }
  card(s, 8.5, 1.55, 4.25, 2.3, HEX.sakuraTint);
  T(s, [{ text: "変化の割合\n", options: { fontSize: 20, bold: true } }, { text: "≒ −2,095人／年", options: { fontSize: 32, bold: true, color: SAKURA } }], { x: 8.5, y: 1.55, w: 4.25, h: 2.3, align: "center", valign: "middle" });
  card(s, 8.5, 4.05, 4.25, 2.3, TINT);
  T(s, [{ text: "(36,621 − 49,190) ÷ 6\n", options: { fontSize: 18 } }, { text: "ほぼ一直線に減少", options: { fontSize: 22, bold: true, color: FOREST } }], { x: 8.5, y: 4.05, w: 4.25, h: 2.3, align: "center", valign: "middle" });
  T(s, "データ：文部科学省「令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況について」参考資料1 第7表 p.9（2025年12月25日公表）の中学校受験者数。変化の割合・直線は発表者が計算。※今後も同じ割合で減るとは限らない", { x: 0.8, y: 6.45, w: 12, h: 0.4, fontSize: 11, color: GRAY });

  // 8 授業準備の時間
  s = slide("授業準備の時間は、変わっていない", "問い①の背景", "【0:40】勤務の実態です。文部科学省の調査では、中学校の先生の平日の在校時間は、11時間32分から11時間1分へと、31分減りました。でも、授業準備の時間は、1時間26分から1時間23分。ほとんど変わっていません。");
  card(s, 0.8, 1.55, 5.6, 4.2, TINT);
  T(s, "平日の在校等時間", { x: 0.8, y: 1.85, w: 5.6, h: 0.6, fontSize: 22, bold: true, align: "center" });
  T(s, "11:32 → 11:01", { x: 0.8, y: 2.6, w: 5.6, h: 1.2, fontSize: 48, bold: true, color: FOREST, align: "center", valign: "middle" });
  T(s, "−31分", { x: 0.8, y: 3.9, w: 5.6, h: 1.1, fontSize: 54, bold: true, color: FOREST, align: "center", valign: "middle" });
  card(s, 6.9, 1.55, 5.6, 4.2, HEX.sakuraTint);
  T(s, "授業準備", { x: 6.9, y: 1.85, w: 5.6, h: 0.6, fontSize: 22, bold: true, align: "center" });
  T(s, "1:26 → 1:23", { x: 6.9, y: 2.6, w: 5.6, h: 1.2, fontSize: 48, bold: true, color: SAKURA, align: "center", valign: "middle" });
  T(s, "−3分", { x: 6.9, y: 3.9, w: 5.6, h: 1.1, fontSize: 54, bold: true, color: SAKURA, align: "center", valign: "middle" });
  T(s, "中学校教諭・平日1日当たり（10・11月、平成28年度 → 令和4年度）\n出典：文部科学省「教員勤務実態調査（令和4年度）集計【確定値】」p.1・p.2（2024年4月公表）", { x: 0.8, y: 6.1, w: 12, h: 0.4, fontSize: 11, color: GRAY });

  // 9 B=W/(NE)
  s = slide("数学で考えてみる", "問い①の背景", "【0:50】この問題を数学で考えると、教員1人当たりの業務時間Bは、業務量Wを、教員数Nと業務効率Eの積でわったもの、と表せます。もちろん、仮定に基づく簡単なモデルです。Nを増やすことは、社会や行政の課題。Wを減らすことは、学校という組織の課題。そしてEを高めることは、私たち一人一人が、授業づくりの中で考えられることです。");
  T(s, "B ＝ W ÷（N × E）", { x: 0.8, y: 1.4, w: 11.7, h: 1.4, fontSize: 60, bold: true, color: FOREST, align: "center", valign: "middle" });
  const lv = [[fa.FaUsers, HEX.gray, "N を増やす", "社会・行政"], [fa.FaCut, HEX.moss, "W を減らす", "学校の組織"], [fa.FaChalkboardTeacher, HEX.sakura, "E を高める", "一人一人の授業づくり"]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, who] = lv[i], x = 0.8 + i * 4.0, last = i === 2;
    card(s, x, 3.2, 3.7, 2.7, last ? HEX.sakuraTint : TINT);
    await iconCircle(s, ic, x + 1.4, 3.45, 0.9, col);
    T(s, h, { x, y: 4.45, w: 3.7, h: 0.6, fontSize: 26, bold: true, color: last ? SAKURA : INK, align: "center" });
    T(s, who, { x, y: 5.1, w: 3.7, h: 0.55, fontSize: 18, color: GRAY, align: "center" });
  }
  T(s, "B：1人当たりの業務時間　W：業務量　N：教員数　E：業務効率（従来を1）　※仮定に基づく簡易モデル", { x: 0.8, y: 6.15, w: 12, h: 0.4, fontSize: 13, color: GRAY, align: "center" });

  // 10 シミュレーション
  s = slide("どれも、同じ「8時間」にできる", "問い①の背景", "【0:40】仮の数値で計算してみます。教員20人、業務量200時間なら、1人10時間。教員を25人にしても、業務量を160時間にしても、効率を125％にしても、どれも8時間です。面白いのは、教員を25％増やしても、Bは20％しか減らないこと。反比例だからです。そしてEは、ここで二つ目の問題意識、AIの活用とつながります。");
  s.addChart(pres.charts.BAR, [{ name: "B", labels: ["現状", "N を増やす", "W を減らす", "E を高める"], values: [10, 8, 8, 8] }], Object.assign({}, chartText, {
    x: 0.8, y: 1.4, w: 7.2, h: 4.9, barDir: "col", showTitle: false, chartColors: [HEX.gray, HEX.moss, HEX.moss, HEX.sakura], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0", dataLabelFontSize: 22, dataLabelColor: HEX.ink, valAxisMinVal: 0, valAxisMaxVal: 12, barGapWidthPct: 55, catAxisLabelFontSize: 16, valAxisHidden: true, valGridLine: { style: "none" } }));
  T(s, "1人当たりの業務時間（時間）", { x: 0.8, y: 6.3, w: 7.2, h: 0.4, fontSize: 13, color: GRAY, align: "center" });
  T(s, "※ N＝20人・W＝200時間などは発表者が設定した仮の数値（実測値ではない）", { x: 8.4, y: 6.35, w: 4.4, h: 0.5, fontSize: 11, color: GRAY });
  card(s, 8.4, 1.6, 4.35, 2.2, TINT);
  T(s, [{ text: "N を25％増やしても\n", options: { fontSize: 20 } }, { text: "B は20％減", options: { fontSize: 32, bold: true, color: FOREST } }], { x: 8.4, y: 1.6, w: 4.35, h: 2.2, align: "center", valign: "middle" });
  card(s, 8.4, 4.05, 4.35, 2.2, HEX.sakuraTint);
  T(s, [{ text: "E を高めるのは\n", options: { fontSize: 20 } }, { text: "AI活用とつながる", options: { fontSize: 28, bold: true, color: SAKURA } }], { x: 8.4, y: 4.05, w: 4.35, h: 2.2, align: "center", valign: "middle" });

  // ===== 問題意識② =====
  divider("第2章", "教員のAI活用を、数値で見る", "問い②の背景　期待と、活用の余地", "第2章", ["教員は増えにくく、授業準備の時間も変わらない。カギは一人一人の効率 E", "E を高める手段として、AIはどこまで使われているか"]);

  s = slide("授業でのAI使用：日本はOECD平均の約半分", "問い②の背景", "【0:50】OECDの国際教員指導環境調査、TALIS 2024の結果です。過去1年間に授業などでAIを使った中学校の先生は、日本は17.4％。OECD平均の36.3％の約半分です。一方で、AIは事務的な業務の自動化に役立つと考える先生は73.1％、授業計画の作成や改善に役立つと考える先生は59.1％と、どちらもOECD平均より高くなっています。期待はあるのに、まだ使えていない。ここに、活用の余地があると考えました。");
  T(s, "17.4%", { x: 0.8, y: 1.55, w: 4.2, h: 1.3, fontSize: 72, bold: true, color: SAKURA, valign: "middle" });
  T(s, "日本（中学校）", { x: 0.8, y: 2.85, w: 4.2, h: 0.5, fontSize: 20, bold: true, color: SAKURA });
  T(s, "36.3%", { x: 0.8, y: 3.55, w: 4.2, h: 1.0, fontSize: 48, bold: true, color: GRAY, valign: "middle" });
  T(s, "OECD平均（中学校）", { x: 0.8, y: 4.55, w: 4.2, h: 0.5, fontSize: 18, color: GRAY });
  T(s, "過去12か月にAIを授業等で使用した教員の割合", { x: 0.8, y: 5.2, w: 4.4, h: 0.8, fontSize: 15, color: INK });
  s.addChart(pres.charts.BAR, [{ name: "日本（中学校）", labels: ["事務的業務の自動化に役立つ", "授業計画の作成・改善に役立つ", "不適切な提案をすることがある"], values: [73.1, 59.1, 66.5] }, { name: "OECD平均（中学校）", labels: ["事務的業務の自動化に役立つ", "授業計画の作成・改善に役立つ", "不適切な提案をすることがある"], values: [44.9, 53.0, 66.4] }],
    Object.assign({}, chartText, { x: 5.4, y: 1.45, w: 7.4, h: 4.9, barDir: "bar", showTitle: true, title: "AIについての考え方（「当てはまる」の割合、%）", chartColors: [HEX.sakura, HEX.gray], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", dataLabelFontSize: 13, dataLabelColor: HEX.ink, valAxisMinVal: 0, valAxisMaxVal: 100, valAxisHidden: true, valGridLine: { style: "none" }, catAxisLabelFontSize: 14, showLegend: true, legendPos: "b", legendFontSize: 13, legendFontFace: "+mn-lt", barGapWidthPct: 60 }));
  T(s, "出典：文部科学省・国立教育政策研究所「OECD国際教員指導環境調査（TALIS）2024報告書のポイント」p.7（2025年10月公表）。調査は2024年2〜3月、日本の中学校教員3,558名", { x: 0.8, y: 6.45, w: 12, h: 0.4, fontSize: 11, color: GRAY });

  s = slide("校務での生成AI活用は、この3年で急速に広がった", "問い②の背景", "【0:40】文部科学省の調査では、校務で生成AIを全く活用していない学校は、令和5年度の76.7％から、令和7年度には16.3％まで減りました。教職員の半数以上が活用している学校も、1.2％から17.1％に増えています。そして、活用した学校の98％が、働き方の改善に効果があったと感じています。AIは、もう特別なものではなくなりつつあります。");
  s.addChart(pres.charts.BAR, [{ name: "全く活用していない学校", labels: ["令和5年度", "令和6年度", "令和7年度"], values: [76.7, 58.9, 16.3] }, { name: "教職員の半数以上が活用している学校", labels: ["令和5年度", "令和6年度", "令和7年度"], values: [1.2, 2.7, 17.1] }],
    Object.assign({}, chartText, { x: 0.8, y: 1.45, w: 7.6, h: 4.9, barDir: "col", barGapWidthPct: 50, chartColors: [HEX.gray, HEX.sakura], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", dataLabelFontSize: 15, dataLabelColor: HEX.ink, valAxisMinVal: 0, valAxisMaxVal: 90, showLegend: true, legendPos: "b", legendFontSize: 14, legendFontFace: "+mn-lt", catAxisLabelFontSize: 15 }));
  card(s, 8.8, 1.55, 3.95, 4.7, HEX.sakuraTint);
  T(s, [{ text: "教職員の半数以上が\n活用した学校の\n", options: { fontSize: 18, bold: true } }, { text: "98%", options: { fontSize: 66, bold: true, color: SAKURA } }, { text: "\nが働き方の改善に\n効果があったと回答", options: { fontSize: 18, bold: true } }], { x: 8.8, y: 1.55, w: 3.95, h: 4.7, align: "center", valign: "middle" });
  T(s, "出典：中央教育審議会 デジタル学習基盤特別委員会（第10回、2026年6月30日）資料1 p.12「校務DXチェックリスト 自己点検結果［確定値］」。「半数以上」＝「半分以上」＋「ほぼ全員」（発表者が合算）", { x: 0.8, y: 6.45, w: 12, h: 0.4, fontSize: 11, color: GRAY });

  s = slide("活用の余地を、関数で見る", "問い②の背景", "【0:50】では、授業づくりでAIを使うと、どれくらいの余地があるのか。関数で考えてみます。中学校の先生の授業準備は、1日83分です。このうちAIで短縮できる割合をr％とすると、1日に短縮できる時間yは、y＝0.83rという比例の式で表せます。10％なら1日8.3分、仮に年間200日とすると約28時間です。ただし、これは仮定のモデルで、実際にどれだけ短縮できるかは、これから確かめる必要があります。");
  T(s, "y ＝ 0.83 r", { x: 0.8, y: 1.45, w: 6.0, h: 1.2, fontSize: 54, bold: true, color: FOREST, valign: "middle" });
  T(s, "y：1日に短縮できる時間（分）\nr：AIで短縮できる割合（％）\n授業準備 83分／日（中学校教諭・平日、令和4年度）\n出典：文部科学省「教員勤務実態調査（令和4年度）」p.2", { x: 0.8, y: 2.7, w: 6.0, h: 1.7, fontSize: 14 });
  s.addChart(pres.charts.LINE, [{ name: "短縮時間（分/日）", labels: ["0%", "5%", "10%", "15%", "20%", "25%", "30%"], values: [0, 4.15, 8.3, 12.45, 16.6, 20.75, 24.9] }],
    Object.assign({}, chartText, { x: 7.0, y: 1.45, w: 5.8, h: 4.1, showTitle: true, title: "短縮できる割合 r と、1日の短縮時間 y（分）", chartColors: [HEX.sakura], lineSize: 3, lineDataSymbolSize: 8, showValue: true, dataLabelPosition: "t", dataLabelFormatCode: "0.0", dataLabelFontSize: 12, dataLabelColor: HEX.ink, valAxisMinVal: 0, valAxisMaxVal: 30, catAxisLabelFontSize: 13 }));
  card(s, 0.8, 4.5, 6.0, 1.8, HEX.sakuraTint);
  T(s, [{ text: "r＝10% なら 1日 8.3分\n", options: { fontSize: 24, bold: true, color: SAKURA } }, { text: "年間200日と仮定すると 約28時間", options: { fontSize: 20, bold: true } }], { x: 0.8, y: 4.5, w: 6.0, h: 1.8, align: "center", valign: "middle" });
  T(s, "※ r と年間200日は発表者の仮定。実際の短縮時間は未測定であり、今後の検証で確かめる。", { x: 7.0, y: 5.7, w: 5.8, h: 0.6, fontSize: 13, color: GRAY });

  // ===== 第2章 AIを使う前 =====
  divider("第3章", "AIを使う前の、私の授業", "実物をそのままお見せします", "第3章", ["AIへの期待は大きいが、授業ではまだ使えていない", "では、自分の授業で試す。まず、AIを使う前の姿から"]);

  // 12 これまでの発表資料
  s = slide("これまでの発表資料（実物）", null, "【0:50】左は2015年の発表スライドで、板書の写真を貼り、授業の流れを説明していました。真ん中は2021年の全国大会の発表スライドです。GeoGebraの画面を貼り付け、関数を一つずつ取り出して比べていました。右はその授業の板書計画です。スライドも、板書計画も、ワークシートも、すべて自分の手で一枚ずつ作ってきました。これが、AIを使う前の私の実態です。");
  tag(s, "AI活用前", HEX.gray);
  const past = [["2015_発表スライド_授業の流れ_板書.png", 1467, 825, "2015 発表スライド"], ["2021_発表スライド_関数を取り出す.png", 2000, 1125, "2021 発表スライド"], ["2021_板書計画_振り子.png", 1754, 1241, "2021 板書計画"]];
  for (let i = 0; i < 3; i++) {
    const [f, iw, ih, cap] = past[i], x = 0.8 + i * 4.0;
    fit(s, path.join(IMG, f), iw, ih, x, 1.6, 3.7, 3.2);
    T(s, cap, { x, y: 4.95, w: 3.7, h: 0.5, fontSize: 20, bold: true, align: "center" });
  }
  T(s, "すべて、自分の手で一枚ずつ", { x: 0.8, y: 5.75, w: 11.7, h: 0.7, fontSize: 28, bold: true, color: FOREST, align: "center" });

  // 13 振り子ワークシート
  s = slide("振り子の授業のワークシート（2024）", null, "【0:30】これは2024年に使った振り子のワークシートです。表とグラフを書く欄だけの、シンプルなものでした。");
  tag(s, "AI活用前", HEX.gray);
  fit(s, path.join(IMG, "2024_振り子ワークシート.png"), 1518, 666, 0.8, 1.55, 11.7, 4.3);
  T(s, "表とグラフを書く欄だけ", { x: 0.8, y: 6.05, w: 11.7, h: 0.6, fontSize: 24, bold: true, color: FOREST, align: "center" });

  // 14 2021年の課題
  s = slide("2021年に残した課題", null, "【0:40】2021年の全国大会では、GeoGebraで「2乗に比例する関数とみなす」活動がしやすくなったという成果の一方で、課題を残していました。ICTの効果を計る項目がないこと。ICTを使うタイミング。そして、教材を毎年自分で作り直す時間です。この課題が、今回の出発点です。");
  tag(s, "AI活用前", HEX.gray);
  const kd = [[fa.FaSearch, "ICTの効果を\n計る項目がない"], [fa.FaClock, "ICTを使う\nタイミング"], [fa.FaHourglassHalf, "教材を毎年\n作り直す時間"]];
  for (let i = 0; i < 3; i++) {
    const x = 0.8 + i * 4.0;
    card(s, x, 1.6, 3.7, 3.9, HEX.sakuraTint);
    await iconCircle(s, kd[i][0], x + 1.3, 1.95, 1.1, HEX.sakura);
    T(s, kd[i][1], { x, y: 3.3, w: 3.7, h: 1.8, fontSize: 26, bold: true, align: "center", valign: "middle" });
  }
  T(s, "→ 今回の出発点", { x: 0.8, y: 5.8, w: 11.7, h: 0.7, fontSize: 28, bold: true, color: SAKURA, align: "center" });

  // 15 三つの実践
  s = slide("土台：関数分野の三つの授業", null, "【0:40】関数分野では、1年で地震の初期微動継続時間と震源からの距離を比例とみる授業、2年で山口県の2月の気温とソメイヨシノの開花日を一次関数とみなして予想する授業、3年で振り子の授業をしてきました。2015年2月の気温7.5℃から3月27日ごろと予想し、気象庁の記録では実際の開花は3月25日でした。どれも、現実の事象を関数とみなし、予測し、確かめる授業です。ここが、私の授業の土台です。");
  const pr = [[gi.GiEarthCrack, HEX.forest, "1年　比例", "地震"], [gi.GiCherry, HEX.sakura, "2年　一次関数", "桜の開花日"], [gi.GiPendulumSwing, HEX.forest, "3年　y＝ax²", "振り子"]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, g, t] = pr[i], x = 0.8 + i * 4.0;
    card(s, x, 1.6, 3.7, 3.6, WHITE, true);
    await iconCircle(s, ic, x + 1.2, 1.9, 1.3, col);
    T(s, g, { x, y: 3.4, w: 3.7, h: 0.5, fontSize: 18, color: GRAY, align: "center" });
    T(s, t, { x, y: 3.95, w: 3.7, h: 0.8, fontSize: 32, bold: true, align: "center" });
  }
  T(s, [{ text: "現実を" }, { text: "関数とみなし", options: { color: SAKURA } }, { text: "、予測し、確かめる" }], { x: 0.8, y: 5.6, w: 11.7, h: 0.9, fontSize: 30, bold: true, align: "center", valign: "middle" });

  T(s, "桜のデータ：気象庁「過去の気象データ検索」下関 2月の平均気温／「さくらの開花日」下関（2015年：7.5℃、開花3月25日）", { x: 0.8, y: 6.5, w: 11.7, h: 0.35, fontSize: 11, color: GRAY });
  // ===== 第3章 AIでアレンジ =====
  divider("第4章", "AIで、アレンジしてみた", "AI LESSON REMAKE", "第4章", ["土台となる授業はあるが、教材は毎年、自分の手で作り直していた", "その授業を、AIでどうアレンジしたか"]);

  // 17 7ステップ
  s = slide("AI LESSON REMAKE（7つのステップ）", null, "【0:50】手順を7つのステップにまとめました。過去の資料をAIに入れ、良かった点と課題を整理し、AIに改善案を出させます。大事なのはステップ5と6です。数学的に正しいか、生徒にとって価値があるかを判断し、何を残して何を変えるかを決めるのは、教師です。ここはAIに任せません。");
  const steps = ["資料を\nAIに入力", "良い点を\n整理", "課題を\n整理", "AIが\n改善案", "教師が\n吟味", "残す・変える\n・削る", "実践・\n検証"];
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.35, y: 1.5, w: 3.65, h: 3.9, fill: { color: HEX.sakuraTint }, line: { color: HEX.sakuraTint }, rectRadius: 0.2 });
  for (let i = 0; i < 7; i++) {
    const cx = 1.25 + i * 1.8, human = i === 4 || i === 5;
    numCircle(s, i + 1, cx - 0.5, 1.9, 1.0, human ? HEX.sakura : HEX.forest);
    T(s, steps[i], { x: cx - 0.85, y: 3.1, w: 1.7, h: 1.2, fontSize: 18, bold: true, align: "center" });
  }
  T(s, "人間が判断", { x: 7.35, y: 4.55, w: 3.65, h: 0.6, fontSize: 22, bold: true, color: SAKURA, align: "center" });
  T(s, "AIに、判断は任せない", { x: 0.8, y: 5.75, w: 11.7, h: 0.8, fontSize: 30, bold: true, color: FOREST, align: "center" });

  // 18 残す・変える・削る
  s = slide("残す・変える・削る", null, "【0:40】判断の基準は三つです。残すのは、授業の本質。変えるのは、本質にたどり着くための手段。削るのは、本質に役立たない作業です。変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。これが今回の考え方です。");
  const rk = [[fa.FaLock, HEX.forest, "残す", "授業の本質"], [fa.FaSyncAlt, HEX.ai, "変える", "たどり着く手段"], [fa.FaCut, HEX.sakura, "削る", "役立たない作業"]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, sub] = rk[i], x = 0.8 + i * 4.0;
    card(s, x, 1.55, 3.7, 3.6, TINT);
    await iconCircle(s, ic, x + 1.25, 1.85, 1.2, col);
    T(s, h, { x, y: 3.2, w: 3.7, h: 0.9, fontSize: 40, bold: true, color: col, align: "center", valign: "middle" });
    T(s, sub, { x, y: 4.15, w: 3.7, h: 0.6, fontSize: 22, align: "center" });
  }
  T(s, "変えるべきは、授業の本質ではない。\nその本質にたどり着くための手段である。", { x: 0.8, y: 5.35, w: 11.7, h: 1.3, fontSize: 24, bold: true, italic: true, color: FOREST, align: "center", valign: "middle" });

  // 19 何が置き換わったか
  s = slide("何が、どう置き換わったか", null, "【0:50】実際に何がどう置き換わったか。発表スライドは、手作業から、AIが構成・デザインをするように。統計の資料は、これまで扱っていませんでしたが、AIが文部科学省の原典を集めてグラフにしました。GeoGebraで自作していた教材は、AIがブラウザで動く教材に。原稿も、AIが下書きし、自分の言葉で直しました。どれも、最後に確かめ、判断したのは自分です。");
  const rep = [[fa.FaChalkboardTeacher, "発表スライド", "手作業", "AIが構成"], [fa.FaChartLine, "統計資料", "扱っていない", "AIが原典から"], [fa.FaLaptopCode, "数学教材", "GeoGebra 自作", "AIがWeb教材"], [fa.FaQuoteLeft, "発表原稿", "自分で作成", "AIが下書き"]];
  T(s, "AI活用前", { x: 4.6, y: 1.35, w: 3.3, h: 0.5, fontSize: 18, bold: true, color: GRAY, align: "center" });
  T(s, "AI活用後", { x: 9.2, y: 1.35, w: 3.5, h: 0.5, fontSize: 18, bold: true, color: SAKURA, align: "center" });
  for (let i = 0; i < 4; i++) {
    const y = 1.95 + i * 1.0, [ic, item, bf, af] = rep[i];
    await iconCircle(s, ic, 0.8, y + 0.05, 0.75, HEX.forest);
    T(s, item, { x: 1.75, y, w: 2.8, h: 0.85, fontSize: 22, bold: true, valign: "middle" });
    card(s, 4.6, y, 3.3, 0.85, "F2F2F2");
    T(s, bf, { x: 4.6, y, w: 3.3, h: 0.85, fontSize: 20, color: GRAY, align: "center", valign: "middle" });
    s.addImage({ data: await icon(fa.FaArrowRight, HEX.sakura), x: 8.2, y: y + 0.2, w: 0.5, h: 0.45 });
    card(s, 9.2, y, 3.5, 0.85, HEX.sakuraTint);
    T(s, af, { x: 9.2, y, w: 3.5, h: 0.85, fontSize: 20, bold: true, color: SAKURA, align: "center", valign: "middle" });
  }
  T(s, "確かめ、判断したのは自分", { x: 0.8, y: 6.05, w: 11.7, h: 0.6, fontSize: 24, bold: true, color: FOREST, align: "center" });

  // 20 変わらないもの
  s = slide("変わらなかったもの", null, "【0:40】一方で、変わらなかったものもあります。中心発問。実物の振り子を測る体験。そして「関数とみなす」という本質です。実物を測るのは時間がかかります。AIを使えば全部シミュレーションで済ませることもできますが、それはしませんでした。自分の手で測って、ばらつきに悩む経験こそ、数学で現実を考える出発点だと思うからです。");
  const keep = [[fa.FaQuoteLeft, "中心発問"], [gi.GiPendulumSwing, "実物の振り子\nを測る体験"], [fa.FaLightbulb, "関数と\nみなす"]];
  for (let i = 0; i < 3; i++) {
    const x = 0.8 + i * 4.0;
    card(s, x, 1.55, 3.7, 3.7, TINT);
    await iconCircle(s, keep[i][0], x + 1.25, 1.9, 1.2, HEX.forest);
    T(s, keep[i][1], { x, y: 3.3, w: 3.7, h: 1.6, fontSize: 28, bold: true, align: "center", valign: "middle" });
  }
  T(s, "実物を測る体験は、あえて残した", { x: 0.8, y: 5.6, w: 11.7, h: 0.8, fontSize: 30, bold: true, color: SAKURA, align: "center" });

  // 21 振り子ラボ
  s = slide("AIと作った教材「振り子ラボ」", null, "【0:50】これが、生成AIと一緒に作った「振り子ラボ」です。ブラウザで動き、インストールはいりません。実物で測ったデータを入れると、表とグラフに点が出ます。生徒は関数を選び、aを動かして、点にいちばん近いグラフを探します。2021年のデータでは、y＝0.25x²のずれが0.025m、比例は、いちばん合うaにしても0.108mでした。見た目だけでなく、数値を根拠に「y＝ax²とみなす」と説明できます。");
  tag(s, "AI活用後", HEX.sakura);
  s.addImage({ path: path.join(ROOT, "05_数学教材", "振り子ラボ_画面.png"), x: 0.8, y: 1.5, w: 8.2, h: 4.61, shadow: { type: "outer", color: "000000", opacity: 0.2, blur: 8, offset: 3, angle: 90 } });
  T(s, "点とグラフのずれ", { x: 9.35, y: 1.6, w: 3.4, h: 0.5, fontSize: 20, bold: true, align: "center" });
  T(s, "y＝0.25x²", { x: 9.35, y: 2.2, w: 3.4, h: 0.5, fontSize: 20, color: SAKURA, align: "center" });
  T(s, "0.025m", { x: 9.35, y: 2.7, w: 3.4, h: 0.9, fontSize: 44, bold: true, color: SAKURA, align: "center", valign: "middle" });
  T(s, "比例 y＝ax", { x: 9.35, y: 3.85, w: 3.4, h: 0.5, fontSize: 20, color: GRAY, align: "center" });
  T(s, "0.108m", { x: 9.35, y: 4.35, w: 3.4, h: 0.9, fontSize: 44, bold: true, color: GRAY, align: "center", valign: "middle" });
  T(s, "データ：2021年の授業での実測10組（新田・山本 2021）。ずれ＝二乗平均平方根。比例はずれが最小のa≒0.39で比較（発表者が計算）", { x: 0.8, y: 6.75, w: 11.9, h: 0.3, fontSize: 10, color: GRAY });
  T(s, "数値を根拠に「みなす」", { x: 0.8, y: 6.2, w: 11.7, h: 0.5, fontSize: 22, bold: true, color: FOREST, align: "center" });

  // 22 AIの答えを検証
  s = slide("AIの答えを、データで確かめる", null, "【0:40】そして、生徒にこう問います。「ある生成AIは、振り子の長さは周期に比例すると答えた。本当か。」AIの答えをうのみにせず、データで確かめる。これからの時代に必要な力だと思っています。この教材のプログラムもAIが作ったものですが、使う前に数学的に正しいかを確かめるのは、人間です。");
  await iconCircle(s, fa.FaRobot, 0.8, 1.65, 1.2, HEX.ai);
  card(s, 2.3, 1.55, 10.4, 1.5, HEX.aiTint);
  T(s, "「振り子の長さは、周期に比例します」", { x: 2.3, y: 1.55, w: 10.4, h: 1.5, fontSize: 32, bold: true, color: AI, align: "center", valign: "middle" });
  T(s, "本当？", { x: 0.8, y: 3.3, w: 11.7, h: 1.2, fontSize: 64, bold: true, color: SAKURA, align: "center", valign: "middle" });
  T(s, "AIの答えを、うのみにしない", { x: 0.8, y: 4.75, w: 11.7, h: 0.8, fontSize: 30, bold: true, align: "center" });
  T(s, "（周期2秒の振り子 → y＝0.25×2²＝1m を、実物で確かめる）", { x: 0.8, y: 5.65, w: 11.7, h: 0.6, fontSize: 20, color: GRAY, align: "center" });

  // 23 1年・2年
  s = slide("1年・2年もアレンジ", null, "【0:40】1年と2年も、同じ手順でアレンジを考えました。2年の桜は、2017年までのデータをAIの補助で最新の年まで整え、散布図に自分で直線を引いて開花日を予想します。1年の地震は、観測点のデータで比例を確かめる教材を構想しているところです。");
  fit(s, path.join(IMG, "桜の開花日ワークシート.png"), 1042, 964, 0.8, 1.55, 3.6, 3.6);
  T(s, "AI活用前のワークシート", { x: 0.8, y: 5.3, w: 3.6, h: 0.5, fontSize: 16, color: GRAY, align: "center" });
  const yr = [[gi.GiCherry, HEX.sakura, "2年　桜の開花日", "データを最新年に\n自分で直線を引いて予想"], [gi.GiEarthCrack, HEX.forest, "1年　地震", "観測データで\n比例を確かめる（構想）"]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, h, d] = yr[i], y = 1.55 + i * 2.15;
    card(s, 4.9, y, 7.8, 1.95, i ? TINT : HEX.sakuraTint);
    await iconCircle(s, ic, 5.15, y + 0.45, 1.05, col);
    T(s, h, { x: 6.45, y: y + 0.2, w: 6.1, h: 0.6, fontSize: 24, bold: true, valign: "middle" });
    T(s, d, { x: 6.45, y: y + 0.8, w: 6.1, h: 1.0, fontSize: 19, color: INK });
  }

  // ===== 考察 =====
  divider("第5章", "考察と提案", "研究仮説から、言えること・まだ言えないこと", "第5章", ["AIで変えたのは手段。授業の本質は変えなかった", "研究仮説から何が言えるか。そして、何を提案するか"]);

  s = slide("研究仮説を、三つの要素に分けて検討する", "考察", "【0:40】研究仮説を三つの要素に分けました。一つ目は、数学的な価値や指導意図を継承できるか。二つ目は、授業準備の負担を軽減できるか。三つ目は、生徒の数学的な見方・考え方を働かせる授業につながるか。それぞれについて、根拠をもとに考えます。");
  const hy = [[fa.FaLock, HEX.forest, "①", "数学的な価値・\n指導意図の継承"], [fa.FaHourglassHalf, HEX.ai, "②", "授業準備の\n負担軽減"], [fa.FaLightbulb, HEX.sakura, "③", "数学的な見方・\n考え方を働かせる"]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, n, t] = hy[i], x = 0.8 + i * 4.0;
    card(s, x, 1.6, 3.7, 4.0, TINT);
    await iconCircle(s, ic, x + 1.25, 1.9, 1.2, col);
    T(s, n, { x, y: 3.25, w: 3.7, h: 0.6, fontSize: 30, bold: true, color: col, align: "center" });
    T(s, t, { x, y: 3.9, w: 3.7, h: 1.4, fontSize: 24, bold: true, align: "center", valign: "middle" });
  }
  T(s, "それぞれについて、根拠 → 言えること → まだ言えないこと", { x: 0.8, y: 5.85, w: 11.7, h: 0.7, fontSize: 24, bold: true, color: FOREST, align: "center" });

  s = slide("根拠から、言えること・まだ言えないこと", "考察", "【1:30】一つ目、継承です。中心発問、実物の振り子を測る体験、関数とみなすという本質は、教師の判断で残すことができました。数学的にも、振り子ラボの係数は理論値0.248、2021年の実測では約0.258と、差は約4％です。y＝0.25x²のずれは0.025m、比例は0.108mで、y＝ax²とみなす根拠を数値で示せました。ここは、今回の事例について言えることです。"
    + "二つ目、負担軽減です。統計の収集とグラフ、ブラウザで動く教材、スライドと原稿の下書きを、AIが担いました。ただし、時間はまだ測っていません。ですから「軽減できた」とは、まだ言えません。"
    + "三つ目、見方・考え方です。数値で比べる場面、AIの答えを確かめる場面を、教材として設計することはできました。ただし、生徒での効果はまだ確かめていません。");
  const hdr2 = (t, col) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: col }, fontSize: 16, valign: "middle", align: "center" } });
  const ev = [["① 継承", "中心発問・実物の体験・「みなす」を残せた\na：理論0.248／実測約0.258（差約4%）\nずれ：y=0.25x² 0.025m／比例 0.108m", "事例として言える", FOREST],
              ["② 負担軽減", "統計収集とグラフ・Web教材・スライドと原稿の下書きをAIが担った\n一方で、確認・修正の時間も必要だった", "見通しはある\n（時間は未測定）", AI],
              ["③ 見方・考え方", "数値で比べる場面・AIの答えを検証する場面・段階的ヒントを、教材として設計できた", "設計はできた\n（生徒では未検証）", SAKURA]];
  const tb = [[hdr2("要素", FOREST), hdr2("根拠（事実）", FOREST), hdr2("現時点で言えること", SAKURA)]];
  for (const [a, b, c, col] of ev) tb.push([{ text: a, options: { bold: true, color: col, fill: { color: TINT }, fontSize: 18, valign: "middle" } }, { text: b, options: { fontSize: 15, valign: "middle" } }, { text: c, options: { bold: true, fontSize: 17, color: col, valign: "middle", align: "center" } }]);
  s.addTable(tb, { x: 0.8, y: 1.45, w: 11.9, colW: [2.4, 6.6, 2.9], color: INK, rowH: [0.55, 1.5, 1.3, 1.3], border: { type: "solid", pt: 1, color: HEX.white }, fill: { color: "F7F9F6" }, margin: [0.05, 0.15, 0.05, 0.15] });
  T(s, [{ text: "結論：", options: { bold: true } }, { text: "①は事例として支持。②③は見通しがあり、これからの検証が必要", options: { bold: true, color: SAKURA } }], { x: 0.8, y: 6.2, w: 11.9, h: 0.6, fontSize: 21, align: "center" });

  s = slide("AIの出力は、人が確かめる必要があった", "考察", "【0:50】今回、資料を作る中で、実際にあったことです。グラフでは、7.5時間が「8」と表示されていました。文部科学省の資料は、URLが変わっていて開けませんでした。AIがまとめた数値は、元のPDFで確かめ直しました。国際調査のグラフは、凡例を画像で確認して、どの数値が中学校かを確定しました。どれも、人が確かめて直しました。AIは速い。でも、確かめる人がいて、はじめて使えるものになります。");
  const ex = [[fa.FaChartLine, "グラフの値", "7.5時間が「8」と表示 → 書式を修正"], [fa.FaSearch, "資料のURL", "移動して開けない → 原典を探し直す"], [fa.FaQuoteLeft, "AIの要約", "数値を元のPDFで照合して確定"], [fa.FaBalanceScale, "国際調査のグラフ", "凡例を画像で確認し、中学校の値を確定"]];
  for (let i = 0; i < 4; i++) {
    const [ic, h, d] = ex[i], x = 0.8 + (i % 2) * 6.05, y = 1.55 + Math.floor(i / 2) * 2.05;
    card(s, x, y, 5.75, 1.8, i % 2 ? TINT : HEX.sakuraTint);
    await iconCircle(s, ic, x + 0.3, y + 0.42, 0.95, i % 2 ? HEX.forest : HEX.sakura);
    T(s, [{ text: h + "\n", options: { bold: true, fontSize: 22 } }, { text: d, options: { fontSize: 17 } }], { x: x + 1.45, y, w: 4.2, h: 1.8, valign: "middle" });
  }
  T(s, "AIは速い。確かめる人がいて、はじめて使えるものになる", { x: 0.8, y: 5.85, w: 11.9, h: 0.7, fontSize: 26, bold: true, color: FOREST, align: "center" });

  s = slide("AIを使う前と後：利点・欠点・可能性", "考察", "【1:00】AIを使う前と後を比べて、数学の授業づくりについて、利点と欠点、そして可能性を整理しました。実証はまだですので、見えてきたこととしてお聞きください。利点は、原典のデータをすぐにグラフにできること、動く教材を短い時間で作れること、過去の授業を整理して課題を言葉にできることです。欠点は、もっともらしい誤りが混ざること、確かめる時間が要ること、そしてAIは目の前の生徒の実態を知らないことです。頼りすぎると、教師が自分で考える機会が減るおそれもあります。可能性としては、過去の授業をアレンジして生かし直せること、生徒がAIの答えを数学で確かめる授業、そして若い先生が先輩の実践を土台に学べることです。");
  const pc = [[fa.FaCheckCircle, HEX.forest, "TINT", "利点", ["原典データをすぐグラフ化", "動く教材を短時間で", "過去の授業を整理し\n課題を言葉にできる"]],
              [fa.FaExclamationCircle, HEX.sakura, "sakuraTint", "欠点", ["もっともらしい誤りが混ざる", "確かめる時間が要る", "生徒の実態は知らない\n（頼りすぎに注意）"]],
              [fa.FaLightbulb, HEX.ai, "aiTint", "可能性", ["過去の授業の生かし直し", "AIの答えを数学で\n確かめる授業", "若手が先輩の実践を\n土台に学べる"]]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, tint, h, li] = pc[i], x = 0.8 + i * 4.0;
    card(s, x, 1.55, 3.7, 4.55, tint === "TINT" ? TINT : HEX[tint]);
    await iconCircle(s, ic, x + 0.3, 1.8, 0.9, col);
    T(s, h, { x: x + 1.35, y: 1.8, w: 2.2, h: 0.9, fontSize: 30, bold: true, color: col, valign: "middle" });
    T(s, bl(li), { x: x + 0.35, y: 2.95, w: 3.2, h: 3.0, fontSize: 18, paraSpaceAfter: 10 });
  }
  T(s, "※ 数学の授業づくりに限定。実証前のため、見えてきた見通しとして示す", { x: 0.8, y: 6.3, w: 11.9, h: 0.4, fontSize: 13, color: GRAY, align: "center" });

  s = slide("提案と、これからの検証", "考察", "【0:50】以上から、三つを提案します。一つ目、AI LESSON REMAKE。特に、人間が判断するステップを手順に組み込むこと。二つ目、AIの答えを数学で確かめる活動を、授業に取り入れること。三つ目、効果を測ること。授業準備の時間を改善の前後で記録して時間削減率を求め、国際調査と同じ項目で、先生の意識も調べます。生徒の到達度や振り返りも比べていきます。");
  const pp = [[fa.FaSyncAlt, HEX.forest, "提案1", "AI LESSON REMAKE\n人間の判断を手順に"], [fa.FaSearch, HEX.sakura, "提案2", "AIの答えを\n数学で確かめる授業"], [fa.FaChartLine, HEX.ai, "提案3", "効果を測る\n（時間・意識・到達度）"]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, t] = pp[i], x = 0.8 + i * 4.0;
    card(s, x, 1.55, 3.7, 3.2, WHITE, true);
    await iconCircle(s, ic, x + 1.35, 1.8, 1.0, col);
    T(s, h, { x, y: 2.9, w: 3.7, h: 0.5, fontSize: 18, bold: true, color: col, align: "center" });
    T(s, t, { x, y: 3.4, w: 3.7, h: 1.2, fontSize: 20, bold: true, align: "center", valign: "middle" });
  }
  card(s, 0.8, 5.0, 11.9, 1.5, HEX.sakuraTint);
  T(s, [{ text: "時間削減率（%）＝（改善前 − 改善後）÷ 改善前 × 100\n", options: { fontSize: 22, bold: true, color: SAKURA } }, { text: "教師：準備時間・負担感（TALISと同じ項目）／生徒：到達率・説明・振り返り", options: { fontSize: 17 } }], { x: 0.8, y: 5.0, w: 11.9, h: 1.5, align: "center", valign: "middle" });

  // ===== 第8版 追加：提案4 授業づくりの超自動化／提案5 振り返りの自動化（構想。ノートは set_notes.py で上書き） =====
  s = slide("提案4　授業づくりの「超自動化」", "考察", "提案4（ノートは script.json）");
  const fl = [[fa.FaChalkboardTeacher, HEX.sakura, "sakuraTint", "教師", "入れる", "土台と意図\n（授業記録・ねらい）"],
              [fa.FaRobot, HEX.ai, "aiTint", "Claude Code", "作る", "日々の授業案\n学習指導案（文字）\n板書型指導案・教材"],
              [fa.FaCheckDouble, HEX.ai, "aiTint", "Codex", "確かめる", "数値・数学・誤りを\n別のAIで二重チェック"],
              [fa.FaChalkboardTeacher, HEX.sakura, "sakuraTint", "教師", "決める", "吟味して\n残す・変える・削る"]];
  for (let i = 0; i < 4; i++) {
    const [ic, col, tint, who, verb, det] = fl[i], x = 0.8 + i * 3.08;
    card(s, x, 1.45, 2.65, 3.55, HEX[tint]);
    await iconCircle(s, ic, x + 0.88, 1.6, 0.9, col);
    T(s, who, { x, y: 2.55, w: 2.65, h: 0.4, fontSize: 16, bold: true, color: col, align: "center" });
    T(s, verb, { x, y: 2.95, w: 2.65, h: 0.6, fontSize: 28, bold: true, align: "center", valign: "middle" });
    T(s, det, { x: x + 0.1, y: 3.6, w: 2.45, h: 1.3, fontSize: 15, align: "center", valign: "middle" });
    if (i < 3) T(s, "▶", { x: x + 2.65, y: 2.95, w: 0.43, h: 0.6, fontSize: 20, color: GRAY, align: "center", valign: "middle" });
  }
  T(s, "作る・確かめるはAI、決めるのは教師", { x: 0.8, y: 5.2, w: 11.9, h: 0.8, fontSize: 30, bold: true, color: FOREST, align: "center", valign: "middle" });
  T(s, "現状：作る手順（型）と2つのAIの連携の設定は作成済み、指導案の見本を試作。日々の運用と時間の測定はこれから（構想）", { x: 0.8, y: 6.15, w: 11.9, h: 0.4, fontSize: 13, color: GRAY, align: "center" });

  s = slide("提案5　振り返りの自動化サイクル", "考察", "提案5（ノートは script.json）");
  const rf = [[fa.FaPenFancy, HEX.forest, "生徒が書く", "毎時間の振り返りを\nフォームで入力\n→ スプレッドシートへ"],
              [fa.FaUserSecret, HEX.ai, "匿名化", "氏名・成績を外して\nからAIへ渡す"],
              [fa.FaChartBar, HEX.ai, "AIが分析", "つまずき・見方考え方\nよく出た言葉を整理"],
              [fa.FaChalkboardTeacher, HEX.sakura, "教師が確かめ\n加筆する", "一人一人への\nコメントを読み、直す"],
              [fa.FaReply, HEX.forest, "返却・次時へ", "生徒に返す\n次の授業案に生かす"]];
  for (let i = 0; i < 5; i++) {
    const [ic, col, h, det] = rf[i], cx = 1.75 + i * 2.45;
    await iconCircle(s, ic, cx - 0.55, 1.55, 1.1, col);
    if (i < 4) s.addShape(pres.shapes.LINE, { x: cx + 0.65, y: 2.1, w: 1.15, h: 0, line: { color: HEX.gray, width: 2, endArrowType: "triangle" } });
    T(s, h, { x: cx - 1.15, y: 2.8, w: 2.3, h: 0.85, fontSize: 20, bold: true, color: col, align: "center", valign: "middle" });
    T(s, det, { x: cx - 1.15, y: 3.7, w: 2.3, h: 1.1, fontSize: 14, align: "center" });
  }
  card(s, 0.8, 4.95, 11.9, 0.55, TINT);
  T(s, "分析結果は、提案4の「次の授業案づくり」に入れる（毎時間まわるサイクル）", { x: 0.8, y: 4.95, w: 11.9, h: 0.55, fontSize: 17, bold: true, color: FOREST, align: "center", valign: "middle" });
  T(s, "毎時間の振り返りを、次の1時間に生かす", { x: 0.8, y: 5.6, w: 11.9, h: 0.7, fontSize: 28, bold: true, color: SAKURA, align: "center", valign: "middle" });
  T(s, "構想段階（実践・効果の測定はこれから）。外部のAIには匿名化したデータだけを渡し、返却前に必ず教師が読む", { x: 0.8, y: 6.35, w: 11.9, h: 0.4, fontSize: 13, color: GRAY, align: "center" });

  s = slide("結論：AIの価値は、使う人の土台で決まる", "考察", "【1:00】ここまでをまとめると、結論はこうです。授業の質は、土台とAIのかけ算だと考えています。土台とは、自分の授業の記録、うまくいったことも失敗したことも含めた、一次情報です。土台がゼロなら、AIをどれだけかけても、ゼロです。AIをただ使うだけでは、薄っぺらいものしかできず、AIに使われるだけになってしまいます。私自身、薄っぺらいかもしれません。それでも、14年間の授業があったから、AIにアレンジを頼むことができました。だからこそ、現場の先生方には、自分の土台とともに、生成AIの活用を進めてほしいと思っています。");
  T(s, "授業の質 ＝ 土台 × AI", { x: 0.8, y: 1.4, w: 11.9, h: 1.3, fontSize: 56, bold: true, color: FOREST, align: "center", valign: "middle" });
  card(s, 0.8, 2.9, 5.75, 2.35, TINT);
  await iconCircle(s, gi.GiPlantSeed, 1.1, 3.15, 0.95, HEX.forest);
  T(s, [{ text: "土台（一次情報）\n", options: { fontSize: 22, bold: true, color: FOREST } }, { text: "自分の授業記録\n成功も失敗も、生徒の反応も", options: { fontSize: 18 } }], { x: 2.25, y: 2.95, w: 4.2, h: 2.25, valign: "middle" });
  card(s, 6.95, 2.9, 5.75, 2.35, HEX.sakuraTint);
  T(s, [{ text: "土台が 0 なら\n", options: { fontSize: 22, bold: true } }, { text: "AIをかけても 0", options: { fontSize: 36, bold: true, color: SAKURA } }, { text: "\n使われるだけ・薄っぺらくなる", options: { fontSize: 17 } }], { x: 6.95, y: 2.9, w: 5.75, h: 2.35, align: "center", valign: "middle" });
  T(s, "だからこそ、土台とともに、生成AIの活用を進めたい", { x: 0.8, y: 5.5, w: 11.9, h: 0.9, fontSize: 30, bold: true, color: SAKURA, align: "center", valign: "middle" });

  // ===== 第4章 問いかけ =====
  divider("第6章", "二つの問い", "教員の魅力と、学び続けるためのAIとの共存", "第6章", ["授業の質＝土台×AI。土台を育てるのは、学び続けること", "教員の魅力とは何か。学び続けるために、AIとどう共存するか"]);

  // 第9版 追加：今日の話を一本の線で
  s = slide("今日の話を、一本の線で", null, "一本の線");
  const ln = [[fa.FaUsers, HEX.forest, "教員不足", "人（N）は\nすぐには増えない"], [fa.FaChartLine, HEX.forest, "効率 E", "一人一人の\n授業づくりを\n変える"], [fa.FaRobot, HEX.ai, "AI", "手段として\n作業・整理を担う"], [gi.GiPlantSeed, HEX.sakura, "土台 × AI", "質を決めるのは\n自分の授業の蓄積"], [fa.FaBookOpen, HEX.sakura, "学び続ける", "土台を育て、\nAIを確かめる力"]];
  for (let i = 0; i < 5; i++) {
    const [ic, col, h, t] = ln[i], x = 0.8 + i * 2.42;
    card(s, x, 1.5, 2.15, 3.55, i >= 3 ? HEX.sakuraTint : (i === 2 ? HEX.aiTint : TINT));
    await iconCircle(s, ic, x + 0.6, 1.7, 0.95, col);
    T(s, h, { x, y: 2.8, w: 2.15, h: 0.55, fontSize: 21, bold: true, color: col, align: "center", valign: "middle" });
    T(s, t, { x, y: 3.4, w: 2.15, h: 1.5, fontSize: 16, align: "center", valign: "middle" });
    if (i < 4) s.addImage({ data: await icon(fa.FaArrowRight, HEX.gray), x: x + 2.17, y: 3.15, w: 0.23, h: 0.25 });
  }
  T(s, [{ text: "だから、" }, { text: "学び続けるために、AIと共存する", options: { color: SAKURA } }], { x: 0.8, y: 5.3, w: 11.9, h: 0.8, fontSize: 32, bold: true, align: "center", valign: "middle" });
  T(s, "AIが時間と気づきを生む → 教師が学ぶ → 土台が育つ → AIをよりよく使える（めざす循環。効果の検証はこれから）", { x: 0.8, y: 6.15, w: 11.9, h: 0.4, fontSize: 14, color: GRAY, align: "center" });

  // 第10版 追加：時短は目的ではない
  s = slide("時短は、目的ではない", null, "時短");
  card(s, 0.8, 1.5, 5.75, 3.3, TINT);
  await iconCircle(s, fa.FaCoins, 1.1, 1.75, 0.95, HEX.gray);
  T(s, [{ text: "お金を得る仕事の効率\n", options: { fontSize: 22, bold: true, color: GRAY } }, { text: "速く・安く・多く", options: { fontSize: 20 } }], { x: 2.25, y: 1.75, w: 4.2, h: 0.95, valign: "middle" });
  T(s, "教育は、同じ物差しでは\n測れない", { x: 1.1, y: 3.0, w: 5.2, h: 1.6, fontSize: 26, bold: true, valign: "middle" });
  card(s, 6.95, 1.5, 5.75, 3.3, HEX.sakuraTint);
  await iconCircle(s, fa.FaBookOpen, 7.25, 1.75, 0.95, HEX.sakura);
  T(s, [{ text: "生まれた時間は\n", options: { fontSize: 22, bold: true, color: SAKURA } }, { text: "どこに使うか", options: { fontSize: 20 } }], { x: 8.4, y: 1.75, w: 4.2, h: 0.95, valign: "middle" });
  T(s, "学ぶこと、\n子どもに向き合うことへ", { x: 7.25, y: 3.0, w: 5.2, h: 1.6, fontSize: 26, bold: true, valign: "middle" });
  T(s, "楽をするための効率化ではない。学びを止めないためのAI", { x: 0.8, y: 5.1, w: 11.9, h: 0.8, fontSize: 28, bold: true, color: FOREST, align: "center", valign: "middle" });
  T(s, "時短が叫ばれる今、本当にこのままでいいのか（発表者の問題意識）", { x: 0.8, y: 5.95, w: 11.9, h: 0.5, fontSize: 18, color: GRAY, align: "center" });

  // 26 問い①
  s = slide("問い①", null, "【0:40】ここで、皆さんに問いかけたいことがあります。一つ目。教員不足という社会の問題に対して、学校や私たち教師にできること、すべきことは何でしょうか。教育の質を守るために、教師の時間を、どう守ればよいでしょうか。");
  await iconCircle(s, fa.FaUsers, 0.8, 1.6, 1.2, HEX.forest);
  T(s, "教員不足を、なり手の「数」ではなく「魅力」から考える", { x: 2.25, y: 1.6, w: 10.4, h: 1.2, fontSize: 26, bold: true, color: FOREST, valign: "middle" });
  T(s, "教員の魅力とは、\n何か。", { x: 0.8, y: 3.0, w: 11.7, h: 2.6, fontSize: 46, bold: true, valign: "middle" });
  T(s, "学び続ける姿は、その答えの一つにならないか（発表者の考え）", { x: 0.8, y: 5.75, w: 11.7, h: 0.7, fontSize: 24, color: GRAY });

  // 25 AIと人間
  s = slide("学び続けるための、AIとの共存", null, "【0:50】AIは、案を出すこと、作業、プログラムを書くことはとても速いです。でも、何を残すかを決めること、生徒の表情を見て問い返すこと、授業に思いを込めることは、人間にしかできません。AIと人間、それぞれの得意なことを生かして、共存していくことが大切だと考えています。");
  const co = [[fa.FaRobot, HEX.ai, "aiTint", "AIに任せる", ["作業・下書き・整理", "過去の授業の良い点・課題", "振り返りの分析"]], [fa.FaChalkboardTeacher, HEX.sakura, "sakuraTint", "人間が担う", ["確かめる・決める", "生徒を見て問い返す", "思いを込める"]]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, tint, h, li] = co[i], x = 0.8 + i * 6.05;
    card(s, x, 1.55, 5.7, 3.8, HEX[tint]);
    await iconCircle(s, ic, x + 0.35, 1.8, 1.0, col);
    T(s, h, { x: x + 1.55, y: 1.8, w: 4.0, h: 1.0, fontSize: 28, bold: true, color: col, valign: "middle" });
    T(s, bl(li), { x: x + 0.6, y: 3.05, w: 5.0, h: 2.1, fontSize: 24, paraSpaceAfter: 6 });
  }
  T(s, "任せて生まれた時間と気づきを、学び続けることに", { x: 0.8, y: 5.7, w: 11.7, h: 0.8, fontSize: 28, bold: true, color: FOREST, align: "center" });

  // 27 問い②
  s = slide("問い②（主張）", null, "【0:40】二つ目。学校現場、とくに授業づくりに、AIをどう取り入れればよいでしょうか。何をAIに任せ、何を人間が担うべきでしょうか。今日お見せしたのは、一つの試みにすぎません。リメイクした授業はまだ実践しておらず、効果も測っていません。だからこそ、一つの答えではなく、これからへの示唆を、皆さんと指導助言の先生からいただけたらと思っています。");
  await iconCircle(s, fa.FaLaptopCode, 0.8, 1.6, 1.2, HEX.ai);
  T(s, "これから教師が学び続けるために", { x: 2.25, y: 1.6, w: 10.4, h: 1.2, fontSize: 28, bold: true, color: AI, valign: "middle" });
  T(s, "AIとの共存は、\n不可欠である。", { x: 0.8, y: 3.0, w: 11.7, h: 2.6, fontSize: 46, bold: true, valign: "middle" });
  T(s, "では、何をAIに任せ、何を人間が担うか。ご示唆をいただきたい", { x: 0.8, y: 5.75, w: 11.7, h: 0.7, fontSize: 24, color: SAKURA, bold: true });

  // 28 おわりに
  s = pres.addSlide({ masterName: "DARK", sectionTitle: _sec });
  s.addNotes("【1:00】今回の発表には、いろいろな賛否があると思います。それでも、私の14年間分の蓄積を込めました。最後に、一番伝えたいことです。私たちの仕事は、最終的には、目の前の子どもたちのためにあります。いくらAIが入ってこようとも、どれだけ時間を短縮できようとも、一番大事なのは、それを使う人の誠実さと謙虚さです。だからこそ、使う人である私たち自身が、人間性を磨き続け、学び続けることが大切だと思います。私自身もそうありたいと思いますし、皆さんにも、ともに頑張っていただけたらと思います。ご清聴ありがとうございました。");
  T(s, "目の前の子どもたちのことを、一番に。", { x: 0.8, y: 1.0, w: 11.7, h: 1.2, fontSize: 40, bold: true, color: WHITE, valign: "middle" });
  T(s, "AIが入っても、時間を短縮できても、\n大事なのは、使う人の誠実さと謙虚さ。", { x: 0.8, y: 2.45, w: 11.7, h: 1.5, fontSize: 26, color: "E5EEDF", valign: "middle" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 4.3, w: 11.7, h: 1.3, fill: { color: "3B7A3C" }, line: { color: "3B7A3C" }, rectRadius: 0.15 });
  s.addImage({ data: await icon(gi.GiPlantSeed, "F4B6C6"), x: 1.15, y: 4.5, w: 0.9, h: 0.9 });
  T(s, "人間性を磨き続ける。学び続ける。", { x: 2.3, y: 4.3, w: 10.0, h: 1.3, fontSize: 34, bold: true, color: "F4B6C6", valign: "middle" });
  T(s, "ご清聴ありがとうございました。", { x: 0.8, y: 6.05, w: 11.7, h: 0.7, fontSize: 24, bold: true, color: WHITE });

  // ===== 補足 =====
  pres.addSection({ title: "補足" }); _sec = "補足";
  s = slide("補足① データの出典一覧", "補足", "【補足・質疑用】本発表で使ったデータの出典です。数値はすべて原典で確認しました（2026年11月24日）。発表者が計算・作成した値は、その旨を明記しています。");
  { const H = t => ({ text: t, options: { bold: true, color: WHITE, fill: { color: FOREST }, fontSize: 11, align: "center", valign: "middle" } });
    const R = [
      ["採用倍率・受験者数（全国）\n山口県 中学校数学 37人・17人・2.2倍", "文部科学省「令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況について」参考資料1 第7表 p.9／第2表-1・第9表-1（2025年12月25日公表）", "mext.go.jp/content/20261001-kyoikushokuin-000046447_2.pdf"],
      ["在校等時間 11:32→11:01\n授業準備 1:26→1:23（83分）", "文部科学省「教員勤務実態調査（令和4年度）集計【確定値】」p.1・p.2（中学校教諭・平日・10・11月）", "mext.go.jp/content/20240404-mxt_zaimu01-100003067-1.pdf"],
      ["AI使用 17.4%（OECD 36.3%）\n役立つ 73.1%・59.1% ほか", "文部科学省・国立教育政策研究所「OECD国際教員指導環境調査（TALIS）2024報告書のポイント」p.7（2025年10月公表）", "mext.go.jp/b_menu/toukei/data/Others/20251006-ope_dev02-2.pdf"],
      ["校務での生成AI活用\n76.7→58.9→16.3%、98%", "中教審 初等中等教育分科会 デジタル学習基盤特別委員会（第10回、2026年6月30日）資料1 p.12", "mext.go.jp/content/20260630-mxt_shuukyo01-000050664_2.pdf"],
      ["教師不足 中学校868人（0.40%）\n※全国調査はこの1回のみ", "文部科学省「『教師不足』に関する実態調査」p.4（令和3年度始業日時点、2022年1月公表）", "mext.go.jp/content/20220128-mxt_kyoikujinzai01-000020293-1.pdf"],
      ["桜：下関 2月の平均気温\nさくらの開花日", "気象庁「過去の気象データ検索」下関（月ごとの値）／「さくらの開花日」（生物季節観測）", "data.jma.go.jp/stats/etrn/\ndata.jma.go.jp/sakura/data/sakura003_06.html"],
      ["振り子の実測データ10組", "新田正幸・山本剛（2021）第103回全国算数・数学教育研究（埼玉）大会 発表資料・授業記録", "（筆者の授業記録）"],
    ];
    s.addTable([[H("使ったデータ"), H("出典（発行・資料名・該当箇所・公表）"), H("URL（https://）")]].concat(R.map(r => r.map((v, ci) => ({ text: v, options: { fontSize: ci === 2 ? 9 : 10.5, bold: ci === 0, color: INK, valign: "middle" } })))),
      { x: 0.6, y: 1.25, w: 12.1, colW: [3.2, 5.6, 3.3], rowH: 0.6, border: { type: "solid", pt: 0.75, color: "C9D3C5" }, fill: { color: "FFFFFF" }, margin: 0.05 }); }
  T(s, "受験者数の推移は、教員総数の推移ではない。計算値（変化の割合・y＝0.83r・ずれ等）と仮の数値（B＝W÷(N×E)）は発表者によるもの。", { x: 0.6, y: 6.6, w: 12.1, h: 0.35, fontSize: 11, bold: true, color: SAKURA });
  s = slide("補足② 振り子の式の根拠", "補足", "【補足・質疑用】振り子の式の根拠と、2021年の実測データです。");
  T(s, [{ text: "T＝2π√(L/g)  →  L＝(g/4π²)T²", options: { bold: true, fontSize: 28, color: FOREST, breakLine: true } }, { text: "g/4π² ≒ 0.248　周期2秒 → 約0.99m", options: { fontSize: 22, breakLine: true } }, { text: "ふれはばが小さいときの近似（30°で周期は約1.7%長い）", options: { fontSize: 18, color: GRAY, breakLine: true } }, { text: "式：単振り子の周期の公式（g＝9.8 m/s²）\nデータ：2021年の授業での実測（新田・山本 2021）\n実測の a≒0.258 は最小二乗法で発表者が計算", options: { fontSize: 14, color: GRAY } }], { x: 0.8, y: 1.5, w: 6.0, h: 4.6, paraSpaceAfter: 10 });
  const hdr = (t, col) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: col }, fontSize: 15, valign: "middle", align: "center" } });
  const d21 = [[0.65, 0.10], [0.90, 0.19], [1.01, 0.27], [1.08, 0.31], [1.14, 0.38], [1.39, 0.50], [1.59, 0.64], [1.70, 0.72], [1.72, 0.78], [1.81, 0.84]];
  s.addTable([[hdr("周期x（秒）", FOREST), hdr("長さy（m）", FOREST), hdr("y÷x²", SAKURA)]].concat(d21.map(([x, y]) => [x.toFixed(2), y.toFixed(2), (y / x / x).toFixed(3)].map(v => ({ text: v, options: { align: "center" } })))), { x: 7.2, y: 1.45, w: 5.5, colW: [1.85, 1.85, 1.8], fontSize: 15, rowH: 0.44, color: INK, valign: "middle", border: { type: "solid", pt: 1, color: HEX.white }, fill: { color: "F7F9F6" } });
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("saved", OUT);
})();
