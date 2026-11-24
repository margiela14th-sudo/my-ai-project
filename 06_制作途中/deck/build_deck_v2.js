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

(async () => {
  // ===== 1 表紙 =====
  pres.addSection({ title: "はじめに" }); _sec = "はじめに";
  let s = pres.addSlide({ masterName: "DARK", sectionTitle: _sec });
  s.addNotes(NOTES[idx++]);
  T(s, CONF, { x: 0.7, y: 0.6, w: 9, h: 0.4, fontSize: 16, color: MOSS, bold: true });
  T(s, TITLE, { x: 0.7, y: 1.6, w: 8.6, h: 2.2, fontSize: 36, bold: true, color: WHITE, valign: "middle" });
  T(s, "～関数分野における従来の授業実践を通して～", { x: 0.7, y: 3.85, w: 8.6, h: 0.5, fontSize: 20, color: "E5EEDF" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.7, y: 4.75, w: 6.4, h: 0.6, fill: { color: SAKURA }, line: { color: SAKURA }, rectRadius: 0.3 });
  T(s, "14年間の授業実践 × 生成AI", { x: 0.7, y: 4.75, w: 6.4, h: 0.6, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle" });
  T(s, "下関市立名陵中学校　新田正幸", { x: 0.7, y: 6.15, w: 7, h: 0.5, fontSize: 20, color: WHITE });
  s.addShape(pres.shapes.OVAL, { x: 9.55, y: 1.55, w: 3.4, h: 3.4, fill: { color: "3B7A3C" }, line: { color: "3B7A3C" } });
  s.addImage({ data: await icon(gi.GiPendulumSwing, "E5EEDF"), x: 10.35, y: 2.35, w: 1.8, h: 1.8 });
  T(s, "変えるべきは、授業の本質ではない。\nその本質にたどり着くための手段である。", { x: 8.9, y: 5.25, w: 4.0, h: 0.9, fontSize: 13, italic: true, color: "E5EEDF", align: "right" });

  // ===== 2 この発表資料について =====
  s = content("この発表資料について", "はじめに");
  card(s, 0.6, 1.45, 12.15, 1.45, C.accent3 === SAKURA ? HEX.sakuraTint : TINT);
  T(s, [{ text: "この発表資料は、", options: {} }, { text: "すべて生成AIを活用して", options: { color: SAKURA, bold: true } }, { text: "作成しました。", options: {} }], { x: 0.95, y: 1.6, w: 11.5, h: 0.75, fontSize: 28, bold: true, valign: "middle" });
  T(s, "構成・スライド・発表原稿・グラフ・数学教材（振り子ラボ）", { x: 0.95, y: 2.35, w: 11.5, h: 0.4, fontSize: 15, color: GRAY });
  const two = [[fa.FaRobot, HEX.ai, "AIが担ったこと", ["資料の整理と構成案", "統計資料の収集とグラフ化", "スライド・原稿・教材の下書き"]],
               [gi.GiPlantSeed, HEX.forest, "中身（土台）", ["14年間の授業実践と研究発表", "授業で大切にしてきた思い", "何を残し、何を変えるかの判断"]]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, h, li] = two[i]; const x = 0.6 + i * 6.25;
    card(s, x, 3.2, 5.9, 2.75, WHITE, true);
    await iconCircle(s, ic, x + 0.3, 3.45, 0.85, col);
    T(s, h, { x: x + 1.35, y: 3.5, w: 4.3, h: 0.7, fontSize: 21, bold: true, color: col, valign: "middle" });
    T(s, li.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < li.length - 1 } })), { x: x + 0.45, y: 4.4, w: 5.2, h: 1.4, fontSize: 17, paraSpaceAfter: 4 });
  }
  T(s, "賛否両論あると思います。受け取り方は、皆さんにお任せします。", { x: 0.6, y: 6.2, w: 12.15, h: 0.5, fontSize: 18, italic: true, bold: true, color: FOREST, align: "center", valign: "middle" });

  // ===== 3 14年間の歩み =====
  s = content("14年間の歩み", "はじめに");
  const tl = [["2015〜", "振り子の授業", "3年 y＝ax²"], ["2017", "桜の開花日", "バトンパス"], ["2021", "ICT活用", "GeoGebra×振り子"], ["2022", "ジグソー法", "協働的な学び"], ["2023", "教師の手立て", "ねじれの位置"], ["2026", "生成AI", "授業を再構築"]];
  s.addShape(pres.shapes.LINE, { x: 1.1, y: 2.75, w: 11.1, h: 0, line: { color: HEX.line, width: 3 } });
  for (let i = 0; i < tl.length; i++) {
    const cx = 1.1 + i * 2.22, last = i === tl.length - 1, col = last ? SAKURA : FOREST;
    T(s, tl[i][0], { x: cx - 1.0, y: 1.55, w: 2.0, h: 0.5, fontSize: 20, bold: true, color: col, align: "center" });
    s.addShape(pres.shapes.OVAL, { x: cx - 0.28, y: 2.47, w: 0.56, h: 0.56, fill: { color: col }, line: { color: WHITE, width: 3 } });
    T(s, tl[i][1], { x: cx - 1.05, y: 3.25, w: 2.1, h: 0.5, fontSize: 17, bold: true, align: "center" });
    T(s, tl[i][2], { x: cx - 1.05, y: 3.75, w: 2.1, h: 0.45, fontSize: 14, color: GRAY, align: "center" });
  }
  card(s, 0.6, 4.75, 12.15, 1.85, TINT);
  await iconCircle(s, fa.FaLightbulb, 0.95, 5.12, 1.1, HEX.forest);
  T(s, [{ text: "共通する考え：", options: { bold: true } }, { text: "従来の良い授業を否定せず、" }, { text: "新しい手段", options: { bold: true, color: SAKURA } }, { text: "で改善する" }], { x: 2.35, y: 5.0, w: 10.1, h: 0.6, fontSize: 21, valign: "middle" });
  T(s, "2021年に残した課題「ICTの効果を計る項目」「ICTを扱うタイミング」が、今回の出発点", { x: 2.35, y: 5.65, w: 10.1, h: 0.6, fontSize: 16, color: AI, valign: "middle" });

  // ===== 4 数値で見る =====
  s = content("数値で見てみる：ここ数年の教員不足", "第1章", "第1章 現状");
  const csv = fs.readFileSync(path.join(ROOT, "02_統計データ", "全国_教員採用選考_長期推移.csv"), "utf8").replace(/^﻿/, "").trim().split("\n").map(l => l.split(","));
  const rows = csv.slice(1).filter(r => +r[1] >= 2000);
  const labs = rows.map(r => r[0].replace("年度", "").replace("平成", "H").replace("令和", "R").replace("元", "1"));
  s.addChart(pres.charts.LINE, [{ name: "採用倍率", labels: labs, values: rows.map(r => +r[4]) }], Object.assign({}, chartText, {
    x: 0.5, y: 1.4, w: 7.3, h: 4.9, showTitle: true, title: "公立中学校 教員採用選考の採用倍率（倍）", chartColors: [HEX.sakura], lineSize: 3, lineDataSymbolSize: 6, valAxisMinVal: 0, valAxisMaxVal: 20, catAxisLabelFrequency: 2 }));
  const stats = [["3.6倍", "中学校の採用倍率（R7）", "H12は17.9倍。過去最低", SAKURA], ["2.2倍", "山口県 中学校数学（R7）", "受験37人・採用17人", FOREST], ["−3分", "授業準備（中学校教諭・平日）", "1:26 → 1:23。ほぼ変わらず", AMBER]];
  for (let i = 0; i < 3; i++) {
    const y = 1.45 + i * 1.65; card(s, 8.15, y, 4.6, 1.45, TINT);
    T(s, stats[i][0], { x: 8.35, y: y + 0.12, w: 1.75, h: 1.2, fontSize: 34, bold: true, color: stats[i][3], valign: "middle" });
    T(s, [{ text: stats[i][1], options: { bold: true, breakLine: true } }, { text: stats[i][2], options: { color: GRAY, fontSize: 13 } }], { x: 10.15, y: y + 0.12, w: 2.5, h: 1.2, fontSize: 15, valign: "middle" });
  }
  T(s, "※ 受験者数・倍率の推移であり、教員総数の推移ではない（採用者数の増加も影響）。出典：文部科学省「令和7年度公立学校教員採用選考試験の実施状況等」参考資料1 第7表・第9表、「教員勤務実態調査（令和4年度）集計【確定値】」", { x: 0.6, y: 6.4, w: 12.15, h: 0.5, fontSize: 10, color: GRAY });

  // ===== 5 B=W/(NE) =====
  s = content("数学で考える：B ＝ W ÷（N × E）", "第2章", "第2章 数学的な問題解決");
  card(s, 0.6, 1.45, 6.1, 1.3, TINT);
  T(s, "B ＝ W ÷（N × E）", { x: 0.6, y: 1.45, w: 6.1, h: 1.3, fontSize: 38, bold: true, color: FOREST, align: "center", valign: "middle" });
  const vars = [["B", "教員1人当たりの平均業務時間"], ["W", "学校全体の業務量"], ["N", "教員数"], ["E", "業務効率（従来を1）"]];
  for (let i = 0; i < 4; i++) {
    const y = 3.0 + i * 0.62; numCircle(s, vars[i][0], 0.75, y, 0.48, i === 3 ? HEX.sakura : HEX.forest);
    T(s, vars[i][1], { x: 1.4, y, w: 5.2, h: 0.48, fontSize: 17, valign: "middle" });
  }
  const B = [10, 8, 8, 8, 7.5];
  s.addChart(pres.charts.BAR, [{ name: "B", labels: ["現状", "①N増", "②W減", "③E向上", "複合型"], values: B }], Object.assign({}, chartText, {
    x: 7.0, y: 1.4, w: 5.8, h: 3.9, barDir: "col", showTitle: true, title: "1人当たりの業務時間 B（時間）※仮定", chartColors: [HEX.gray, HEX.moss, HEX.moss, HEX.sakura, HEX.amber], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", dataLabelFontSize: 14, dataLabelColor: HEX.ink, valAxisMinVal: 0, valAxisMaxVal: 12, barGapWidthPct: 60 }));
  card(s, 7.0, 5.45, 5.8, 1.2, HEX.sakuraTint);
  T(s, [{ text: "Nを25%増やしても、Bは20%減（反比例）", options: { bold: true, breakLine: true } }, { text: "③ E を高める → 人も業務も減らさない", options: { bold: true, color: SAKURA } }], { x: 7.25, y: 5.5, w: 5.4, h: 1.1, fontSize: 16, valign: "middle" });
  T(s, "※ 実測値ではない仮定のモデル。条件 N=20人・W=200時間 → ①N=25 ②W=160 ③E=125% 複合 W=180・E=120%。業務の均等配分・一様な効率改善を仮定し、個人差や精神的負担は表せない。", { x: 0.6, y: 5.6, w: 6.1, h: 1.1, fontSize: 12, color: GRAY });

  // ===== 6 研究仮説 =====
  s = content("研究仮説", "第2章");
  card(s, 0.6, 1.45, 12.15, 3.2, TINT);
  s.addImage({ data: await icon(fa.FaQuoteLeft, HEX.moss), x: 0.95, y: 1.75, w: 0.7, h: 0.6 });
  T(s, "従来の数学科授業実践における数学的な価値や教師の指導意図を継承しながら、生成AIを活用して授業を再構築することで、教師の授業準備に関わる負担を軽減するとともに、生徒の数学的な見方・考え方を働かせる授業の実現につながるのではないか。", { x: 1.9, y: 1.75, w: 10.5, h: 2.6, fontSize: 22, valign: "middle" });
  const st3 = ["過去の自分の実践を振り返る", "AIでアレンジするモデルをつくる", "リメイク授業と検証計画を示す"];
  for (let i = 0; i < 3; i++) {
    const x = 0.6 + i * 4.1; numCircle(s, i + 1, x, 5.05, 0.7, HEX.forest);
    T(s, st3[i], { x: x + 0.85, y: 5.05, w: 3.1, h: 0.7, fontSize: 17, bold: true, valign: "middle" });
  }
  T(s, "※ リメイク授業は未実践。成果ではなく、提案と検証計画として示す。", { x: 0.6, y: 6.1, w: 12, h: 0.4, fontSize: 13, color: GRAY });

  // ===== 7 三つの実践 =====
  s = content("過去の自分の授業実践：関数分野の三つ", "第3章", "第3章 従来の授業実践");
  const pr = [[gi.GiEarthCrack, "1年　比例", "地震", "初期微動継続時間と震源からの距離", "比例とみなし、距離を求める"],
              [gi.GiCherry, "2年　一次関数", "ソメイヨシノの開花日", "2月の平均気温と開花日（山口県・気象庁）", "一次関数とみなし、開花日を予想"],
              [gi.GiPendulumSwing, "3年　関数y＝ax²", "振り子・巨大ブランコ", "周期 x 秒と長さ y m（実測データ）", "y＝ax²とみなし、周期2秒の振り子をつくる"]];
  for (let i = 0; i < 3; i++) {
    const x = 0.6 + i * 4.15, [ic, g, t, d, v] = pr[i];
    card(s, x, 1.45, 3.85, 3.85, WHITE, true);
    await iconCircle(s, ic, x + 1.42, 1.7, 1.0, i === 1 ? HEX.sakura : HEX.forest);
    T(s, g, { x: x + 0.2, y: 2.85, w: 3.45, h: 0.4, fontSize: 14, color: GRAY, align: "center" });
    T(s, t, { x: x + 0.2, y: 3.25, w: 3.45, h: 0.5, fontSize: 21, bold: true, align: "center" });
    T(s, d, { x: x + 0.3, y: 3.8, w: 3.25, h: 0.7, fontSize: 14, align: "center" });
    T(s, v, { x: x + 0.3, y: 4.5, w: 3.25, h: 0.7, fontSize: 14, bold: true, color: SAKURA, align: "center" });
  }
  card(s, 0.6, 5.6, 12.15, 0.95, TINT);
  T(s, [{ text: "土台：", options: { bold: true } }, { text: "現実の事象を" }, { text: "関数とみなし", options: { bold: true, color: SAKURA } }, { text: "、予測し、確かめる" }], { x: 0.6, y: 5.6, w: 12.15, h: 0.95, fontSize: 22, align: "center", valign: "middle" });

  // ===== 8 2021 成果と課題 =====
  s = content("2021年の振り子の授業：成果と課題", "第3章");
  const gc = [[fa.FaCheckCircle, HEX.forest, "成果", ["GeoGebraで「2乗に比例する関数とみなす」活動がしやすくなった", "実測値をもとに予想し解決でき、数学的活動が深まった", "実物の振り子とICTを関連づけ、主体的に取り組んだ"]],
              [fa.FaExclamationCircle, HEX.sakura, "課題", ["ICTの効果を計る項目を振り返りに設ける必要がある", "ICTを扱うタイミングは検討の余地がある（実物を使う良さもある）", "教材を毎年つくり直す準備の時間"]]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, h, li] = gc[i], x = 0.6 + i * 6.25;
    card(s, x, 1.45, 5.9, 4.6, i ? HEX.sakuraTint : TINT);
    await iconCircle(s, ic, x + 0.3, 1.7, 0.8, col);
    T(s, h, { x: x + 1.3, y: 1.7, w: 4, h: 0.8, fontSize: 24, bold: true, color: col, valign: "middle" });
    T(s, li.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < li.length - 1 } })), { x: x + 0.45, y: 2.8, w: 5.2, h: 3.0, fontSize: 18, paraSpaceAfter: 10 });
  }
  T(s, "出典：第103回全国算数・数学教育研究（埼玉）大会 発表資料・大会誌原稿（新田・山本 2021）", { x: 0.6, y: 6.3, w: 12, h: 0.4, fontSize: 11, color: GRAY });

  // ===== 9 AI LESSON REMAKE =====
  s = content("AI LESSON REMAKE（授業再構築モデル）", "第4章", "第4章 授業再構築モデル");
  const steps = ["過去の授業資料を生成AIに入力", "良かった点を三つ整理", "課題を三つ整理", "AIに複数の改善案を提案させる", "数学的妥当性と教育的価値を吟味", "残す・変える・削るで再構築", "実践・評価・検証・再改善"];
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.28, y: 1.3, w: 3.55, h: 3.45, fill: { color: HEX.sakuraTint }, line: { color: HEX.sakuraTint }, rectRadius: 0.15 });
  T(s, "人間の判断（AIに任せない）", { x: 7.28, y: 4.3, w: 3.55, h: 0.4, fontSize: 14, bold: true, color: SAKURA, align: "center" });
  for (let i = 0; i < 7; i++) {
    const cx = 1.1 + i * 1.78, human = i === 4 || i === 5;
    numCircle(s, i + 1, cx - 0.42, 1.55, 0.84, human ? HEX.sakura : HEX.forest);
    T(s, "STEP" + (i + 1), { x: cx - 0.8, y: 2.5, w: 1.6, h: 0.35, fontSize: 13, bold: true, color: human ? SAKURA : FOREST, align: "center" });
    T(s, steps[i], { x: cx - 0.8, y: 2.9, w: 1.6, h: 1.3, fontSize: 14, align: "center" });
  }
  card(s, 0.6, 5.0, 12.15, 1.6, TINT);
  await iconCircle(s, fa.FaLaptopCode, 0.9, 5.3, 0.95, HEX.ai);
  T(s, [{ text: "既存のAIツールの位置づけ", options: { bold: true, color: AI, breakLine: true } }, { text: "STEP4 導入発問メーカー・数学教材生成ツール／STEP6 板書型指導案メーカー・学習指導案メーカー／STEP7 振り返り自動化", options: { fontSize: 14, breakLine: true } }, { text: "他の先生も、自分の得意な授業で同じ手順をたどれる", options: { bold: true, color: FOREST } }], { x: 2.1, y: 5.12, w: 10.5, h: 1.4, fontSize: 16, valign: "middle" });

  // ===== 10 残す・変える・削る =====
  s = content("残す・変える・削る", "第4章");
  const rk = [[fa.FaLock, HEX.forest, "残す", "授業の本質", ["数学的な価値", "中心発問", "生徒が考える時間", "実物に触れる体験"]],
              [fa.FaSyncAlt, HEX.ai, "変える", "本質にたどり着く手段", ["教材の形（動的教材）", "データの扱い方", "支援の出し方（段階的ヒント）"]],
              [fa.FaCut, HEX.sakura, "削る", "本質に寄与しない作業", ["手作業の転記・計算", "毎年のデータ打ち直し", "教材の作り直し"]]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, sub, li] = rk[i], x = 0.6 + i * 4.15;
    card(s, x, 1.45, 3.85, 3.95, WHITE, true);
    await iconCircle(s, ic, x + 0.3, 1.7, 0.95, col);
    T(s, [{ text: h, options: { bold: true, fontSize: 28, color: col, breakLine: true } }, { text: sub, options: { fontSize: 14, color: GRAY } }], { x: x + 1.4, y: 1.65, w: 2.3, h: 1.1, valign: "middle" });
    T(s, li.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < li.length - 1 } })), { x: x + 0.4, y: 3.0, w: 3.25, h: 2.2, fontSize: 17, paraSpaceAfter: 6 });
  }
  T(s, "変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。", { x: 0.6, y: 5.75, w: 12.15, h: 0.8, fontSize: 22, bold: true, italic: true, color: FOREST, align: "center", valign: "middle" });

  // ===== 11 Before/After =====
  s = content("振り子の授業を、AIでアレンジ", "第5章", "第5章 リメイク授業");
  const ba = [["導入・中心発問", "巨大ブランコ／長さと1往復の時間の関係は？", "同じ（残す）", 0], ["自力解決", "実物の振り子を測る → 点をとる", "実物で測る（残す）→ 振り子ラボに入力", 0],
              ["練り上げ", "GeoGebraで関数を重ね、見た目で比べる", "関数ごとの「ずれ」を数値で比べ、根拠をもってみなす", 1], ["個別の支援", "机間指導", "3段階のヒント（正解はすぐに見せない）", 1],
              ["数学的考察", "y＝0.25x²、周期2秒 → 1m", "＋「AIの答え」を検証する／成立条件にふれる", 1], ["振り返り", "わかったこと・理解度", "＋ ICTの効果を計る項目（2021年の課題）", 1], ["教材研究・準備", "教材を個人で作成・修正", "AIで案を作り、教師が検証（時間を記録）", 1]];
  const hdr = (t, col) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: col }, fontSize: 15, valign: "middle" } });
  const tbl = [[hdr("", FOREST), hdr("Before（2021年の実践）", FOREST), hdr("After（AIでアレンジ）", SAKURA)]];
  for (const [a, b, c, ch] of ba) tbl.push([{ text: a, options: { bold: true, fill: { color: TINT }, color: FOREST } }, { text: b }, { text: c, options: ch ? { bold: true, color: SAKURA, fill: { color: HEX.sakuraTint } } : { color: GRAY } }]);
  s.addTable(tbl, { x: 0.6, y: 1.45, w: 12.15, colW: [2.2, 4.6, 5.35], fontSize: 15, color: INK, valign: "middle", rowH: 0.62, border: { type: "solid", pt: 1, color: HEX.white }, fill: { color: "F7F9F6" }, margin: [0, 0.12, 0, 0.12] });

  // ===== 12 振り子ラボ =====
  s = content("AIと作った教材「振り子ラボ」", "第5章");
  s.addImage({ path: path.join(ROOT, "05_数学教材", "振り子ラボ_画面.png"), x: 0.6, y: 1.45, w: 7.9, h: 4.44, rounding: false, shadow: { type: "outer", color: "000000", opacity: 0.2, blur: 8, offset: 3, angle: 90 } });
  const lab = [["実物のデータを入力", "表・グラフ・式が連動"], ["関数を選び a を動かす", "ずれ：y＝0.25x² 0.025m／比例 0.138m"], ["AIの答えを検証", "「長さは周期に比例する」は本当？"], ["周期2秒の振り子", "y＝0.25×2²＝1（m）→ 実物で確認"]];
  for (let i = 0; i < 4; i++) {
    const y = 1.45 + i * 1.15; numCircle(s, i + 1, 8.85, y + 0.1, 0.6, i === 1 ? HEX.sakura : HEX.forest);
    T(s, [{ text: lab[i][0], options: { bold: true, breakLine: true } }, { text: lab[i][1], options: { fontSize: 14, color: i === 1 ? SAKURA : GRAY } }], { x: 9.6, y, w: 3.2, h: 0.95, fontSize: 17, valign: "middle" });
  }
  card(s, 0.6, 6.1, 12.15, 0.65, TINT);
  T(s, "成立条件：T＝2π√(L/g) より L＝(g/4π²)T²、g/4π²≒0.248。ふれはばが小さいときの近似。単一HTML・インストール不要。", { x: 0.85, y: 6.1, w: 11.7, h: 0.65, fontSize: 14, valign: "middle" });

  // ===== 13 1年・2年 =====
  s = content("1年「地震」・2年「桜の開花日」のアレンジ", "第5章");
  const yr = [[gi.GiCherry, HEX.sakura, "2年　桜の開花日（一次関数）", ["2017年までの表データ", "グラフは手描き"], ["データを最新年まで更新（AIが補助・教師が原典照合）", "散布図に自分で直線を引く動的教材", "「AIの答え」をデータで確かめる"]],
            [gi.GiEarthCrack, HEX.forest, "1年　地震（比例）", ["初期微動継続時間と震源からの距離を比例とみる"], ["観測点のデータで比例を確かめる教材（構想）", "比例定数＝1秒あたり何kmか", "理科との関連"]]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, h, bf, af] = yr[i], y = 1.45 + i * 2.65;
    await iconCircle(s, ic, 0.6, y + 0.2, 0.95, col);
    T(s, h, { x: 1.75, y: y + 0.2, w: 4.5, h: 0.95, fontSize: 19, bold: true, valign: "middle" });
    card(s, 0.6, y + 1.25, 4.9, 1.15, TINT);
    T(s, bf.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < bf.length - 1 } })), { x: 0.8, y: y + 1.3, w: 4.6, h: 1.05, fontSize: 14, valign: "middle", color: GRAY });
    s.addImage({ data: await icon(fa.FaArrowRight, HEX.gray), x: 5.75, y: y + 1.0, w: 0.5, h: 0.5 });
    card(s, 6.5, y, 6.25, 2.4, HEX.sakuraTint);
    T(s, [{ text: "After（AIでアレンジ）", options: { bold: true, color: SAKURA, breakLine: true } }].concat(af.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < af.length - 1 } }))), { x: 6.8, y: y + 0.15, w: 5.8, h: 2.1, fontSize: 16, paraSpaceAfter: 4, valign: "middle" });
  }

  // ===== 14 AIと共存する =====
  s = content("AIと共存する：人間にしかできない部分", "第6章", "第6章 まとめ");
  const co = [[fa.FaRobot, HEX.ai, "aiTint", "AIが得意なこと", ["案をたくさん出す", "資料の整理・作業", "教材のプログラムを書く", "データを集めて形にする"]],
              [fa.FaChalkboardTeacher, HEX.sakura, "sakuraTint", "人間にしかできないこと", ["何を残すかを決める", "生徒の表情を見て問い返す", "授業に思いを込める", "結果に責任をもつ"]]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, tint, h, li] = co[i], x = 0.6 + i * 6.25;
    card(s, x, 1.45, 5.9, 3.5, HEX[tint]);
    await iconCircle(s, ic, x + 0.3, 1.7, 0.95, col);
    T(s, h, { x: x + 1.45, y: 1.7, w: 4.2, h: 0.95, fontSize: 22, bold: true, color: col, valign: "middle" });
    T(s, li.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < li.length - 1 } })), { x: x + 0.5, y: 2.9, w: 5.2, h: 1.9, fontSize: 18, paraSpaceAfter: 4 });
  }
  card(s, 0.6, 5.2, 12.15, 1.5, TINT);
  await iconCircle(s, gi.GiPlantSeed, 0.9, 5.42, 1.05, HEX.forest);
  T(s, [{ text: "土台（14年間の授業実践）があってこそ、AIでアレンジできる", options: { bold: true, color: FOREST, breakLine: true } }, { text: "AIを学校教育にどう取り入れ、人間らしさでどう扱い、" }, { text: "人間にしかできない部分でどう共存するか", options: { bold: true, color: SAKURA } }], { x: 2.2, y: 5.3, w: 10.4, h: 1.3, fontSize: 18, valign: "middle" });

  // ===== 15 期待される効果・限界・検証 =====
  s = content("期待される効果と研究の限界、今後の検証", "第6章");
  const ev = [[fa.FaLightbulb, HEX.forest, "期待される効果（未検証）", ["準備時間の短縮", "段階的ヒントで基礎を支える", "数値の根拠で「みなす」説明", "AIの答えを検証する力"]],
              [fa.FaBalanceScale, HEX.sakura, "研究の限界", ["B＝W÷(N×E) は仮定のモデル", "時間短縮・理解向上は未測定", "AI出力の確認にも時間がかかる", "個人情報を入力しない運用が前提"]],
              [fa.FaSearch, HEX.ai, "今後の検証", ["教師：準備・作成・確認の時間、負担感", "生徒：到達率・説明・振り返り", "改善前後で比較する"]]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, li] = ev[i], x = 0.6 + i * 4.15;
    card(s, x, 1.45, 3.85, 3.75, WHITE, true);
    await iconCircle(s, ic, x + 0.3, 1.7, 0.8, col);
    T(s, h, { x: x + 1.25, y: 1.7, w: 2.5, h: 0.8, fontSize: 17, bold: true, color: col, valign: "middle" });
    T(s, li.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < li.length - 1 } })), { x: x + 0.35, y: 2.75, w: 3.35, h: 2.3, fontSize: 15, paraSpaceAfter: 6 });
  }
  card(s, 0.6, 5.5, 12.15, 1.1, HEX.sakuraTint);
  T(s, [{ text: "時間削減率（％）", options: { bold: true, color: SAKURA } }, { text: "　＝（改善前の時間 − 改善後の時間）÷ 改善前の時間 × 100" }], { x: 0.6, y: 5.5, w: 12.15, h: 1.1, fontSize: 20, align: "center", valign: "middle" });

  // ===== 16 おわりに =====
  s = pres.addSlide({ masterName: "DARK", sectionTitle: _sec });
  s.addNotes(NOTES[idx++]);
  T(s, "おわりに　14年間の蓄積を込めて", { x: 0.7, y: 0.55, w: 11, h: 0.6, fontSize: 22, bold: true, color: MOSS });
  T(s, "変えるべきは、授業の本質ではない。\nその本質にたどり着くための手段である。", { x: 0.7, y: 1.45, w: 11.9, h: 1.9, fontSize: 36, bold: true, color: WHITE, valign: "middle" });
  T(s, "教育の質を守るために、教師の時間を守る。", { x: 0.7, y: 3.45, w: 11.9, h: 0.9, fontSize: 30, bold: true, color: "F4B6C6", valign: "middle" });
  T(s, "14年間の授業実践の蓄積を、生成AIを活用して形にしました。\n賛否はあると思います。受け取り方は、皆さんにお任せします。", { x: 0.7, y: 4.6, w: 11.9, h: 1.1, fontSize: 18, color: "E5EEDF" });
  T(s, "ご清聴ありがとうございました。", { x: 0.7, y: 6.05, w: 11.9, h: 0.7, fontSize: 24, bold: true, color: WHITE });

  // ===== 補足 =====
  s = content("補足① 統計データの出典と詳細", "補足", "補足");
  T(s, [
    { text: "中学校 受験者数：H25 62,998人 → R7 36,621人　採用者数：H12 2,673人 → R7 10,168人", options: { bullet: true, breakLine: true } },
    { text: "教師不足（R3始業日）：中学校868人（0.40%）、全体2,558人（0.31%）※全国調査はこの1回", options: { bullet: true, breakLine: true } },
    { text: "文部科学省「令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況等」参考資料1 第7表・第2表-1・第9表-1", options: { bullet: true, breakLine: true } },
    { text: "https://www.mext.go.jp/content/20261001-kyoikushokuin-000046447_2.pdf", options: { color: AI, fontSize: 13, breakLine: true } },
    { text: "文部科学省「教員勤務実態調査（令和4年度）集計【確定値】」", options: { bullet: true, breakLine: true } },
    { text: "https://www.mext.go.jp/content/20240404-mxt_zaimu01-100003067-1.pdf", options: { color: AI, fontSize: 13, breakLine: true } },
    { text: "文部科学省「『教師不足』に関する実態調査」（令和4年1月）", options: { bullet: true, breakLine: true } },
    { text: "https://www.mext.go.jp/content/20220128-mxt_kyoikujinzai01-000020293-1.pdf", options: { color: AI, fontSize: 13, breakLine: true } },
    { text: "注意：採用選考の受験者数の推移であり、教員総数の推移ではない。", options: { color: SAKURA, bold: true } }], { x: 0.6, y: 1.45, w: 12.15, h: 5.2, fontSize: 16, paraSpaceAfter: 6 });
  s = content("補足② 振り子モデルの成立条件と過去のデータ", "補足");
  card(s, 0.6, 1.45, 6.0, 5.2, TINT);
  T(s, [{ text: "単振り子の周期", options: { bold: true, color: FOREST, breakLine: true } }, { text: "T＝2π√(L/g) → L＝(g/4π²)T²", options: { breakLine: true } }, { text: "g＝9.80665 m/s² のとき g/4π²≒0.248", options: { breakLine: true } }, { text: "周期2秒 → L≒0.99 m（秒振り子）", options: { breakLine: true } },
    { text: "成り立つ条件", options: { bold: true, color: FOREST, breakLine: true } }, { text: "ふれはばが小さい（30°で周期は約1.7%長くなる）", options: { bullet: true, breakLine: true } }, { text: "長さはおもりの重心まで", options: { bullet: true, breakLine: true } }, { text: "糸の質量・空気抵抗が小さい", options: { bullet: true, breakLine: true } },
    { text: "巨大ブランコは人の重心・大きなふれはばで近似が粗くなる", options: { color: SAKURA, bold: true } }], { x: 0.9, y: 1.65, w: 5.5, h: 4.8, fontSize: 16, paraSpaceAfter: 6 });
  const d21 = [[0.65, 0.10], [0.90, 0.19], [1.01, 0.27], [1.08, 0.31], [1.14, 0.38], [1.39, 0.50], [1.59, 0.64], [1.70, 0.72], [1.72, 0.78], [1.81, 0.84]];
  const t2 = [[hdr("周期x（秒）", FOREST), hdr("長さy（m）", FOREST), hdr("y÷x²", SAKURA)]].concat(d21.map(([x, y]) => [x.toFixed(2), y.toFixed(2), (y / x / x).toFixed(3)].map(v => ({ text: v, options: { align: "center" } }))));
  s.addTable(t2, { x: 7.0, y: 1.45, w: 5.75, colW: [1.95, 1.9, 1.9], fontSize: 14, rowH: 0.45, color: INK, valign: "middle", border: { type: "solid", pt: 1, color: HEX.white }, fill: { color: "F7F9F6" } });
  s = content("補足③ 理想的なバトンパス（2017年・3年）", "補足");
  await iconCircle(s, fa.FaUsers, 0.6, 1.5, 1.0, HEX.forest);
  T(s, [{ text: "運動会のリレー練習の場面設定（バトンが渡せない会話文）から問題をつくる", options: { bullet: true, breakLine: true } }, { text: "加速して走り出す次走者（y＝ax²）と、一定の速さで走る前走者（一次関数）のグラフで考える", options: { bullet: true, breakLine: true } }, { text: "今後のアレンジ候補：スタート位置やタイミングを動かしてグラフの交点を確かめる動的教材", options: { bullet: true, bold: true, color: SAKURA } }], { x: 1.9, y: 1.5, w: 10.8, h: 3.0, fontSize: 19, paraSpaceAfter: 10 });

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("saved", OUT, "notes used", idx, "/", NOTES.length);
})();
