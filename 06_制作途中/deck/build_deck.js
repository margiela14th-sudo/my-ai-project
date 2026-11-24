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

// ===== 第3版：二つの問題意識／AI活用前の痕跡と変容／答えではなく問いで終える =====
const IMG = path.join(ROOT, "01_過去資料", "画像");
function fit(s, file, iw, ih, x, y, bw, bh, frame = true) {
  const r = Math.min(bw / iw, bh / ih), w = iw * r, h = ih * r, ox = x + (bw - w) / 2, oy = y + (bh - h) / 2;
  if (frame) s.addShape(pres.shapes.RECTANGLE, { x: ox - 0.04, y: oy - 0.04, w: w + 0.08, h: h + 0.08, fill: { color: WHITE }, line: { color: HEX.line, width: 1 }, shadow: { type: "outer", color: "000000", opacity: 0.15, blur: 5, offset: 2, angle: 90 } });
  s.addImage({ path: file, x: ox, y: oy, w, h });
}
function tag(s, text, x, y, w, col) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.38, fill: { color: col }, line: { color: col }, rectRadius: 0.19 });
  T(s, text, { x, y, w, h: 0.38, fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle" });
}
const bl = (arr, o = {}) => arr.map((t, j) => ({ text: t, options: Object.assign({ bullet: true, breakLine: j < arr.length - 1 }, o) }));

NOTES.length = 0;
NOTES.push(
  // 1
  "【0:20】今から、「生成AIを活用した数学科授業の改善と新たな授業モデルの提案 ～関数分野における従来の授業実践を通して～」という題で発表をします。下関市立名陵中学校の新田です。よろしくお願いします。",
  // 2
  "【0:40】はじめに、お伝えしておきたいことがあります。今回の発表資料は、構成もスライドも原稿も、そして後でお見せする教材も、すべて生成AIを活用して作りました。賛否両論あると思います。"
  + "ただ、中身には、私がこの14年間、授業で大切にしてきた思いと、その蓄積を載せたつもりです。AIを使う前の資料も、そのまま残してお見せします。どう受け取るかは、皆さんの受け取り方次第です。",
  // 3
  "【0:50】今日の発表には、二つの問題意識があります。一つは、教員不足という社会的な問題です。なぜ数学の研究協議会でこれを取り上げるのか。それは、授業の質を支える教師の時間が、この問題と切り離せないと考えるからです。"
  + "もう一つは、学校現場へのAIの活用、とくに授業構想・授業づくりにどう生かすかという問題です。二つは別々の問題ですが、「教師の時間」と「授業の質」というところで、重なり合っていると感じています。"
  + "今日は、どちらにも一つの答えを示すつもりはありません。私なりの試みをお見せして、最後に皆さんと指導助言の先生に問いかけ、ご意見をいただきたいと思っています。",
  // 4
  "【0:30】少しだけ、これまでの歩みを振り返ります。2015年ごろから振り子の授業を続け、2017年には桜の開花日やバトンパスの授業をつくりました。2021年はGeoGebra、2022年はジグソー法、2023年は教師の手立てを発表しました。"
  + "振り返ると、どれも「良い授業を、新しい手段で改善する」ことでした。今回、その手段が生成AIです。",
  // 5
  "【0:50】一つ目の問題意識、教員不足です。ここは、関数的な表現やデータの活用の視点で、数値を少し見てみたいと思いました。資料として載せておく意味合いですので、ご覧ください。"
  + "中学校の教員採用の倍率は、平成12年度の17.9倍から、令和7年度は3.6倍まで下がっています。ただし、これは受験者数の推移で、教員の総数が減っているという意味ではありません。採用者数が増えたことも影響しています。"
  + "勤務の実態を見ると、在校時間は少し減りましたが、授業準備の時間はほとんど変わっていません。",
  // 6
  "【0:50】この問題を数学で考えると、教員1人当たりの業務時間Bは、業務量Wを、教員数Nと業務効率Eの積でわったもの、と表せます。もちろん、仮定に基づく簡単なモデルです。"
  + "Nを増やすことは、社会や行政の課題です。Wを減らすことは、学校という組織の課題です。そしてEを高めることは、私たち一人一人が、授業づくりの中で考えられることです。"
  + "ここで、一つ目の問題意識と、二つ目のAI活用の問題意識がつながります。",
  // 7
  "【0:30】そこで、次の仮説を立てました。従来の数学科授業実践における数学的な価値や教師の指導意図を継承しながら、生成AIを活用して授業を再構築することで、教師の授業準備に関わる負担を軽減するとともに、生徒の数学的な見方・考え方を働かせる授業の実現につながるのではないか。",
  // 8
  "【0:50】ここで、AIを使う前の姿を、そのままお見せします。左は2021年の全国大会の発表スライドです。GeoGebraの画面を貼り付け、比例、一次関数、反比例と、関数を一つずつ取り出して比べていました。"
  + "真ん中は、その授業の板書計画です。右は2022年の発表の単元計画の表です。スライドも、板書計画も、ワークシートも、すべて自分の手で一枚ずつ作ってきました。これが、AIを使う前の私の実態です。",
  // 9
  "【0:50】これは2024年に使った振り子のワークシートです。表とグラフを書く欄だけの、シンプルなものでした。"
  + "2021年の発表では、GeoGebraで「みなす」活動がしやすくなったという成果の一方で、ICTの効果を計る項目がないこと、ICTを使うタイミング、という課題を残していました。教材も、毎年自分で作り直していました。",
  // 10
  "【0:40】関数分野では、ほかにも、1年で地震の初期微動継続時間と震源からの距離を比例とみる授業、2年で山口県の2月の平均気温とソメイヨシノの開花日を一次関数とみなして予想する授業をしてきました。"
  + "2015年の気温7.5℃から3月27日ごろと予想し、実際も3月27日でした。どれも、現実の事象を関数とみなし、予測し、確かめる授業です。ここが、私の授業の土台です。",
  // 11
  "【1:00】これらの授業を、AIを使ってどうアレンジしたか。手順を7つのステップにまとめました。過去の資料をAIに入れ、良かった点と課題を整理し、AIに改善案を出させます。"
  + "大事なのはステップ5と6で、数学的に正しいか、生徒にとって価値があるかを判断し、何を残して何を変えるかを決めるのは、教師です。"
  + "残すのは授業の本質、変えるのは本質にたどり着く手段、削るのは本質に役立たない作業です。",
  // 12
  "【1:00】では、実際に何がどう置き換わったのか。左がAIを使う前、右が今回です。発表スライドは、これまで手作業で作っていましたが、今回はAIが構成とデザインをし、私が中身を判断しました。"
  + "教員不足などの統計は、これまで扱っていませんでしたが、AIが文部科学省の原典を集めてグラフにし、私が確かめました。GeoGebraで自作していた教材は、AIがブラウザで動く教材に作り直し、私が数学的に確かめました。"
  + "一方で、変わらなかったものもあります。中心発問、実物の振り子を測る体験、「関数とみなす」という本質です。ここは残しました。",
  // 13
  "【0:50】授業の流れでいうと、導入と中心発問、実物の振り子を測る体験はそのまま残しました。変えたのは、見た目で比べていた場面を数値の「ずれ」で比べられるようにしたこと、ヒントを3段階にしたこと、そして生成AIの答えを生徒が確かめる活動を入れたことです。"
  + "実物の振り子を測るのは時間がかかります。AIを使えば全部シミュレーションで済ませることもできますが、それはしませんでした。自分の手で測って、ばらつきに悩む経験こそ、数学で現実を考える出発点だと思うからです。",
  // 14
  "【1:00】これが、生成AIと一緒に作った「振り子ラボ」です。実物で測ったデータを入れると、表とグラフに点が出ます。2021年の授業のデータでは、y＝0.25x²のときのずれは0.025m、比例だと0.138mでした。見た目だけでなく、数値を根拠に「y＝ax²とみなす」と説明できます。"
  + "そして、「ある生成AIは、振り子の長さは周期に比例すると答えた。本当か」と問います。AIの答えをうのみにせず、データで確かめる。これからの時代に必要な力だと思っています。この教材のプログラムもAIが作ったものですが、使う前に数学的に正しいかを確かめるのは、人間です。",
  // 15
  "【0:40】1年と2年も同じ手順でアレンジを考えました。2年の桜は、AIの補助でデータを最新の年まで整え、散布図に自分で直線を引いて予想し、「AIの答え」もデータで確かめます。1年の地震は、観測点のデータで比例を確かめる教材を構想しているところです。",
  // 16
  "【0:50】AIと一緒に資料を作ってみて感じたことです。AIは、案を出すこと、作業、プログラムを書くことはとても速いです。でも、何を残すかを決めること、生徒の表情を見て問い返すこと、授業に思いを込めること、結果に責任を持つことは、人間にしかできません。"
  + "そもそも、土台がなければAIでアレンジすることもできません。私自身、土台があると言い切れるものではありませんが、14年間の授業がなければ、今回の資料は作れませんでした。",
  // 17
  "【1:00】最後に、皆さんに問いかけたいことがあります。一つ目。教員不足という社会の問題に対して、学校や私たち教師にできること、すべきことは何でしょうか。教育の質を守るために、教師の時間をどう守ればよいでしょうか。"
  + "二つ目。学校現場、とくに授業づくりに、AIをどう取り入れればよいでしょうか。何をAIに任せ、何を人間が担うべきでしょうか。"
  + "今日お見せしたのは、一つの試みにすぎません。リメイクした授業はまだ実践しておらず、効果も測っていません。だからこそ、一つの答えではなく、これからへの示唆を、皆さんと指導助言の先生からいただけたらと思っています。",
  // 18
  "【0:50】AIは、これからの世の中で必ず必要になってきます。それを学校教育にどう取り入れ、人間らしさでどう扱い、人間にしかできない部分でどう共存していくか。それがとても大事なのではないかと考えています。"
  + "今回の発表には、いろいろな賛否があると思います。それでも、私の14年間分の蓄積を込めました。私にとっては、最後の発表という部分もあると思っています。その部分を、少しでも感じ取っていただけたらと思います。ご清聴ありがとうございました。",
  // 補足
  "【補足・質疑用】統計の出典と詳細です。", "【補足・質疑用】振り子の式の根拠と、2021年の実測データです。", "【補足・質疑用】期待される効果と研究の限界、今後の検証計画です。", "【補足・質疑用】2017年に実践したバトンパスの授業です。今回は本編では扱いません。"
);

(async () => {
  // ===== 1 表紙 =====
  pres.addSection({ title: "はじめに" }); _sec = "はじめに";
  let s = pres.addSlide({ masterName: "DARK", sectionTitle: _sec }); s.addNotes(NOTES[idx++]);
  T(s, CONF, { x: 0.7, y: 0.6, w: 9, h: 0.4, fontSize: 16, color: MOSS, bold: true });
  T(s, TITLE, { x: 0.7, y: 1.6, w: 8.6, h: 2.2, fontSize: 36, bold: true, color: WHITE, valign: "middle" });
  T(s, "～関数分野における従来の授業実践を通して～", { x: 0.7, y: 3.85, w: 8.6, h: 0.5, fontSize: 20, color: "E5EEDF" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.7, y: 4.75, w: 6.4, h: 0.6, fill: { color: SAKURA }, line: { color: SAKURA }, rectRadius: 0.3 });
  T(s, "14年間の授業実践 × 生成AI", { x: 0.7, y: 4.75, w: 6.4, h: 0.6, fontSize: 18, bold: true, color: WHITE, align: "center", valign: "middle" });
  T(s, "下関市立名陵中学校　新田正幸", { x: 0.7, y: 6.15, w: 7, h: 0.5, fontSize: 20, color: WHITE });
  s.addShape(pres.shapes.OVAL, { x: 9.55, y: 1.55, w: 3.4, h: 3.4, fill: { color: "3B7A3C" }, line: { color: "3B7A3C" } });
  s.addImage({ data: await icon(gi.GiPendulumSwing, "E5EEDF"), x: 10.35, y: 2.35, w: 1.8, h: 1.8 });

  // ===== 2 この発表資料について =====
  s = content("この発表資料について", "はじめに");
  card(s, 0.6, 1.45, 12.15, 1.45, HEX.sakuraTint);
  T(s, [{ text: "この発表資料は、" }, { text: "すべて生成AIを活用して", options: { color: SAKURA, bold: true } }, { text: "作成しました。" }], { x: 0.95, y: 1.6, w: 11.5, h: 0.75, fontSize: 28, bold: true, valign: "middle" });
  T(s, "構成・スライド・発表原稿・グラフ・数学教材（振り子ラボ）／AIを使う前の資料も、そのまま残してお見せします", { x: 0.95, y: 2.35, w: 11.5, h: 0.4, fontSize: 15, color: GRAY });
  const two = [[fa.FaRobot, HEX.ai, "AIが担ったこと", ["資料の整理と構成案", "統計資料の収集とグラフ化", "スライド・原稿・教材の下書き"]],
               [gi.GiPlantSeed, HEX.forest, "中身（土台）", ["14年間の授業実践と研究発表", "授業で大切にしてきた思い", "何を残し、何を変えるかの判断"]]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, h, li] = two[i]; const x = 0.6 + i * 6.25;
    card(s, x, 3.2, 5.9, 2.75, WHITE, true);
    await iconCircle(s, ic, x + 0.3, 3.45, 0.85, col);
    T(s, h, { x: x + 1.35, y: 3.5, w: 4.3, h: 0.7, fontSize: 21, bold: true, color: col, valign: "middle" });
    T(s, bl(li), { x: x + 0.45, y: 4.4, w: 5.2, h: 1.4, fontSize: 17, paraSpaceAfter: 4 });
  }
  T(s, "賛否両論あると思います。受け取り方は、皆さんにお任せします。", { x: 0.6, y: 6.2, w: 12.15, h: 0.5, fontSize: 18, italic: true, bold: true, color: FOREST, align: "center", valign: "middle" });

  // ===== 3 二つの問題意識 =====
  s = content("二つの問題意識", "はじめに");
  s.addShape(pres.shapes.OVAL, { x: 0.9, y: 1.3, w: 6.75, h: 4.3, fill: { color: HEX.forest, transparency: 82 }, line: { color: HEX.forest, width: 2 } });
  s.addShape(pres.shapes.OVAL, { x: 5.65, y: 1.3, w: 6.75, h: 4.3, fill: { color: HEX.ai, transparency: 82 }, line: { color: HEX.ai, width: 2 } });
  await iconCircle(s, fa.FaUsers, 2.9, 1.75, 0.85, HEX.forest);
  T(s, [{ text: "問題意識①", options: { fontSize: 15, color: FOREST, bold: true, breakLine: true } }, { text: "教員不足という\n社会的な問題", options: { fontSize: 22, bold: true } }], { x: 1.6, y: 2.75, w: 3.8, h: 1.4, valign: "middle" });
  T(s, "なぜ数学の研究協議会で取り上げるのか", { x: 1.6, y: 4.2, w: 3.8, h: 0.7, fontSize: 14, color: GRAY });
  await iconCircle(s, fa.FaLaptopCode, 9.55, 1.75, 0.85, HEX.ai);
  T(s, [{ text: "問題意識②", options: { fontSize: 15, color: AI, bold: true, breakLine: true } }, { text: "学校現場への\nAI活用・授業づくり", options: { fontSize: 22, bold: true } }], { x: 7.95, y: 2.75, w: 3.8, h: 1.4, valign: "middle", align: "right" });
  T(s, "授業構想・授業づくりにどう生かすか", { x: 7.95, y: 4.2, w: 3.8, h: 0.7, fontSize: 14, color: GRAY, align: "right" });
  T(s, [{ text: "重なり", options: { fontSize: 14, color: SAKURA, bold: true, breakLine: true } }, { text: "教師の時間\nと\n授業の質", options: { fontSize: 17, bold: true, color: INK } }], { x: 5.85, y: 2.3, w: 1.6, h: 2.2, align: "center", valign: "middle" });
  card(s, 0.6, 5.8, 12.15, 0.9, HEX.sakuraTint);
  T(s, [{ text: "今日は、一つの答えではなく、" }, { text: "問いを共有したい", options: { bold: true, color: SAKURA } }, { text: "（最後に、皆さまと指導助言の先生にご意見をいただきます）", options: { fontSize: 15, color: GRAY } }], { x: 0.6, y: 5.8, w: 12.15, h: 0.9, fontSize: 20, align: "center", valign: "middle" });

  // ===== 4 14年間の歩み =====
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

  // ===== 5 問題意識① 数値 =====
  s = content("問題意識①：数値で見る教員不足", "第1章", "第1章 問題意識");
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

  // ===== 6 BWNE：①と②をつなぐ =====
  s = content("①と②をつなぐ：B ＝ W ÷（N × E）", "第1章");
  card(s, 0.6, 1.45, 12.15, 1.25, TINT);
  T(s, "B ＝ W ÷（N × E）", { x: 0.6, y: 1.45, w: 5.2, h: 1.25, fontSize: 36, bold: true, color: FOREST, align: "center", valign: "middle" });
  T(s, "B：教員1人当たりの業務時間　W：学校全体の業務量\nN：教員数　E：業務効率（従来を1）　※仮定に基づく簡易モデル", { x: 5.8, y: 1.45, w: 6.8, h: 1.25, fontSize: 15, valign: "middle" });
  const lv = [[fa.FaUsers, HEX.gray, "N を増やす", "社会・行政の課題", "採用・人材確保・外部人材"], [fa.FaCut, HEX.moss, "W を減らす", "学校組織の課題", "業務の精選・会議の削減"], [fa.FaChalkboardTeacher, HEX.sakura, "E を高める", "一人一人の授業づくり", "生成AIの活用・教材の再利用"]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, who, ex] = lv[i], x = 0.6 + i * 4.15, last = i === 2;
    card(s, x, 3.0, 3.85, 2.55, last ? HEX.sakuraTint : WHITE, !last);
    await iconCircle(s, ic, x + 0.3, 3.25, 0.8, col);
    T(s, h, { x: x + 1.25, y: 3.25, w: 2.5, h: 0.8, fontSize: 21, bold: true, color: last ? SAKURA : INK, valign: "middle" });
    T(s, [{ text: who, options: { bold: true, breakLine: true } }, { text: ex, options: { color: GRAY, fontSize: 14 } }], { x: x + 0.35, y: 4.3, w: 3.2, h: 1.1, fontSize: 17 });
  }
  T(s, [{ text: "Nを25%増やしてもBは20%減（反比例）。" }, { text: "Eは、問題意識②につながる", options: { bold: true, color: SAKURA } }], { x: 0.6, y: 5.85, w: 12.15, h: 0.8, fontSize: 18, align: "center", valign: "middle" });

  // ===== 7 研究仮説 =====
  s = content("研究仮説", "第1章");
  card(s, 0.6, 1.45, 12.15, 3.4, TINT);
  s.addImage({ data: await icon(fa.FaQuoteLeft, HEX.moss), x: 0.95, y: 1.75, w: 0.7, h: 0.6 });
  T(s, "従来の数学科授業実践における数学的な価値や教師の指導意図を継承しながら、生成AIを活用して授業を再構築することで、教師の授業準備に関わる負担を軽減するとともに、生徒の数学的な見方・考え方を働かせる授業の実現につながるのではないか。", { x: 1.9, y: 1.75, w: 10.5, h: 2.8, fontSize: 22, valign: "middle" });
  T(s, "※ リメイク授業は未実践。成果ではなく、一つの試みとその変容を示し、問いとして共有する。", { x: 0.6, y: 5.2, w: 12.15, h: 0.5, fontSize: 15, color: GRAY });

  // ===== 8 AI活用前①：これまでの発表資料 =====
  s = content("AIを使う前①：これまでの発表資料（実物）", "第2章", "第2章 AIを使う前");
  tag(s, "AI活用前", 11.2, 0.5, 1.55, HEX.gray);
  const past = [["2021_発表スライド_関数を取り出す.png", 2000, 1125, "2021 全国大会の発表スライド", "GeoGebraの画面を貼り、関数を一つずつ比較"], ["2021_板書計画_振り子.png", 1754, 1241, "2021 振り子の板書計画", "Wordで手作業で作成"], ["2022_発表スライド_単元計画.png", 1700, 957, "2022 全国大会の発表スライド", "単元計画を表で作成"]];
  for (let i = 0; i < 3; i++) {
    const [f, iw, ih, cap, sub] = past[i], x = 0.6 + i * 4.15;
    fit(s, path.join(IMG, f), iw, ih, x, 1.5, 3.85, 3.0);
    T(s, [{ text: cap, options: { bold: true, breakLine: true } }, { text: sub, options: { color: GRAY, fontSize: 14 } }], { x, y: 4.7, w: 3.85, h: 0.9, fontSize: 16, align: "center" });
  }
  card(s, 0.6, 5.85, 12.15, 0.8, TINT);
  T(s, "スライドも、板書計画も、ワークシートも、すべて自分の手で一枚ずつ作ってきた", { x: 0.6, y: 5.85, w: 12.15, h: 0.8, fontSize: 19, bold: true, color: FOREST, align: "center", valign: "middle" });

  // ===== 9 AI活用前②：振り子の授業 =====
  s = content("AIを使う前②：振り子の授業と2021年の課題", "第2章");
  tag(s, "AI活用前", 11.2, 0.5, 1.55, HEX.gray);
  fit(s, path.join(IMG, "2024_振り子ワークシート.png"), 1518, 666, 0.6, 1.5, 6.6, 2.9);
  T(s, [{ text: "2024年の振り子のワークシート", options: { bold: true, breakLine: true } }, { text: "表とグラフを書く欄だけのシンプルなもの", options: { color: GRAY, fontSize: 14 } }], { x: 0.6, y: 4.55, w: 6.6, h: 0.8, fontSize: 16, align: "center" });
  card(s, 7.55, 1.45, 5.2, 2.0, TINT);
  T(s, [{ text: "2021年の成果", options: { bold: true, color: FOREST, breakLine: true } }].concat(bl(["「みなす」活動がしやすくなった（GeoGebra）", "実測値から予想し解決できた"], { fontSize: 15 })), { x: 7.8, y: 1.55, w: 4.8, h: 1.85, fontSize: 17, valign: "middle", paraSpaceAfter: 2 });
  card(s, 7.55, 3.6, 5.2, 2.0, HEX.sakuraTint);
  T(s, [{ text: "2021年の課題", options: { bold: true, color: SAKURA, breakLine: true } }].concat(bl(["ICTの効果を計る項目がない", "ICTを扱うタイミング（実物の良さもある）", "教材を毎年つくり直す時間"], { fontSize: 15 })), { x: 7.8, y: 3.7, w: 4.8, h: 1.85, fontSize: 17, valign: "middle", paraSpaceAfter: 2 });
  T(s, "出典：第103回全国算数・数学教育研究（埼玉）大会 発表資料・大会誌原稿（新田・山本 2021）", { x: 0.6, y: 6.3, w: 12, h: 0.4, fontSize: 11, color: GRAY });

  // ===== 10 三つの実践 =====
  s = content("土台：関数分野の三つの実践", "第2章");
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

  // ===== 11 AI LESSON REMAKE + 残す変える削る =====
  s = content("AI LESSON REMAKE：AIでアレンジする手順", "第3章", "第3章 AIでアレンジ");
  const steps = ["過去の授業資料をAIに入力", "良かった点を三つ整理", "課題を三つ整理", "AIに改善案を出させる", "数学的妥当性と価値を吟味", "残す・変える・削る", "実践・評価・再改善"];
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.28, y: 1.3, w: 3.55, h: 2.75, fill: { color: HEX.sakuraTint }, line: { color: HEX.sakuraTint }, rectRadius: 0.15 });
  for (let i = 0; i < 7; i++) {
    const cx = 1.1 + i * 1.78, human = i === 4 || i === 5;
    numCircle(s, i + 1, cx - 0.38, 1.5, 0.76, human ? HEX.sakura : HEX.forest);
    T(s, steps[i], { x: cx - 0.82, y: 2.4, w: 1.64, h: 1.0, fontSize: 14, align: "center" });
  }
  T(s, "人間の判断（AIに任せない）", { x: 7.28, y: 3.6, w: 3.55, h: 0.4, fontSize: 14, bold: true, color: SAKURA, align: "center" });
  const rk = [[fa.FaLock, HEX.forest, "残す", "授業の本質", "数学的な価値・中心発問・考える時間・実物の体験"], [fa.FaSyncAlt, HEX.ai, "変える", "本質にたどり着く手段", "教材の形・データの扱い・支援の出し方"], [fa.FaCut, HEX.sakura, "削る", "本質に寄与しない作業", "手作業の転記・データ打ち直し・作り直し"]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, sub, ex] = rk[i], x = 0.6 + i * 4.15;
    card(s, x, 4.35, 3.85, 2.3, TINT);
    await iconCircle(s, ic, x + 0.25, 4.55, 0.75, col);
    T(s, [{ text: h, options: { bold: true, fontSize: 24, color: col, breakLine: true } }, { text: sub, options: { fontSize: 13, color: GRAY } }], { x: x + 1.15, y: 4.5, w: 2.6, h: 0.9, valign: "middle" });
    T(s, ex, { x: x + 0.3, y: 5.5, w: 3.3, h: 1.0, fontSize: 14 });
  }

  // ===== 12 何がどう置き換わったか =====
  s = content("AIを使って、何がどう置き換わったか", "第3章");
  const hdr = (t, col) => ({ text: t, options: { bold: true, color: WHITE, fill: { color: col }, fontSize: 15, valign: "middle" } });
  const ch = [["発表スライド", "手作業で作成（2021・2022・2023）", "AIが構成・デザイン → 中身は自分で判断"], ["統計・背景資料", "扱っていなかった", "AIが文部科学省の原典を収集・グラフ化 → 自分で確認"],
              ["数学教材", "GeoGebraファイルを自作", "AIがブラウザで動く「振り子ラボ」を作成 → 数学的に確認"], ["ワークシート", "表とグラフの欄のみ（2024）", "段階的ヒント・AIの答えの検証を組み込む（案）"],
              ["授業案・板書計画", "Wordで手作業（2021板書計画）", "AIが下書き → 吟味して修正"], ["発表原稿", "自分で作成", "AIが下書き → 自分の言葉で修正"]];
  const tb2 = [[hdr("", FOREST), hdr("AI活用前（実際）", HEX.gray), hdr("AI活用後（今回）", SAKURA)]];
  for (const [a, b, c] of ch) tb2.push([{ text: a, options: { bold: true, fill: { color: TINT }, color: FOREST } }, { text: b, options: { color: GRAY } }, { text: c, options: { bold: true, color: INK, fill: { color: HEX.sakuraTint } } }]);
  tb2.push([{ text: "変わらないもの", options: { bold: true, fill: { color: FOREST }, color: WHITE } }, { text: "中心発問・実物の振り子を測る体験・「関数とみなす」という本質", options: { bold: true, color: FOREST, fill: { color: TINT }, colspan: 2 } }]);
  s.addTable(tb2, { x: 0.6, y: 1.45, w: 12.15, colW: [2.3, 4.2, 5.65], fontSize: 15, color: INK, valign: "middle", rowH: 0.62, border: { type: "solid", pt: 1, color: HEX.white }, fill: { color: "F7F9F6" }, margin: [0, 0.12, 0, 0.12] });

  // ===== 13 Before/After 授業 =====
  s = content("振り子の授業：Before／After", "第3章");
  const ba = [["導入・中心発問", "巨大ブランコ／長さと1往復の時間の関係は？", "同じ（残す）", 0], ["自力解決", "実物の振り子を測る → 点をとる", "実物で測る（残す）→ 振り子ラボに入力", 0],
              ["練り上げ", "GeoGebraで関数を重ね、見た目で比べる", "関数ごとの「ずれ」を数値で比べ、根拠をもってみなす", 1], ["個別の支援", "机間指導", "3段階のヒント（正解はすぐに見せない）", 1],
              ["数学的考察", "y＝0.25x²、周期2秒 → 1m", "＋「AIの答え」を検証する／成立条件にふれる", 1], ["振り返り", "わかったこと・理解度", "＋ ICTの効果を計る項目（2021年の課題）", 1]];
  const tbl = [[hdr("", FOREST), hdr("Before（2021年の実践）", HEX.gray), hdr("After（AIでアレンジ）", SAKURA)]];
  for (const [a, b, c, chg] of ba) tbl.push([{ text: a, options: { bold: true, fill: { color: TINT }, color: FOREST } }, { text: b, options: { color: GRAY } }, { text: c, options: chg ? { bold: true, color: SAKURA, fill: { color: HEX.sakuraTint } } : { color: GRAY } }]);
  s.addTable(tbl, { x: 0.6, y: 1.45, w: 12.15, colW: [2.2, 4.6, 5.35], fontSize: 15, color: INK, valign: "middle", rowH: 0.66, border: { type: "solid", pt: 1, color: HEX.white }, fill: { color: "F7F9F6" }, margin: [0, 0.12, 0, 0.12] });
  T(s, "実物を測る体験は、あえて残した（ばらつきに悩む経験こそ、数学で現実を考える出発点）", { x: 0.6, y: 6.25, w: 12.15, h: 0.45, fontSize: 15, bold: true, color: FOREST, align: "center" });

  // ===== 14 振り子ラボ =====
  s = content("AIと作った教材「振り子ラボ」", "第3章");
  tag(s, "AI活用後", 11.2, 0.5, 1.55, HEX.sakura);
  s.addImage({ path: path.join(ROOT, "05_数学教材", "振り子ラボ_画面.png"), x: 0.6, y: 1.45, w: 7.9, h: 4.44, shadow: { type: "outer", color: "000000", opacity: 0.2, blur: 8, offset: 3, angle: 90 } });
  const lab = [["実物のデータを入力", "表・グラフ・式が連動"], ["関数を選び a を動かす", "ずれ：y＝0.25x² 0.025m／比例 0.138m"], ["AIの答えを検証", "「長さは周期に比例する」は本当？"], ["周期2秒の振り子", "y＝0.25×2²＝1（m）→ 実物で確認"]];
  for (let i = 0; i < 4; i++) {
    const y = 1.45 + i * 1.15; numCircle(s, i + 1, 8.85, y + 0.1, 0.6, i === 1 ? HEX.sakura : HEX.forest);
    T(s, [{ text: lab[i][0], options: { bold: true, breakLine: true } }, { text: lab[i][1], options: { fontSize: 14, color: i === 1 ? SAKURA : GRAY } }], { x: 9.6, y, w: 3.2, h: 0.95, fontSize: 17, valign: "middle" });
  }
  card(s, 0.6, 6.1, 12.15, 0.65, TINT);
  T(s, "T＝2π√(L/g) より L＝(g/4π²)T²、g/4π²≒0.248（ふれはばが小さいときの近似）。AIが作ったプログラムを、使う前に人間が数学的に確認。", { x: 0.85, y: 6.1, w: 11.7, h: 0.65, fontSize: 14, valign: "middle" });

  // ===== 15 1年・2年 =====
  s = content("1年「地震」・2年「桜の開花日」のアレンジ", "第3章");
  fit(s, path.join(IMG, "桜の開花日ワークシート.png"), 1042, 964, 0.6, 1.45, 3.4, 3.15);
  T(s, [{ text: "AI活用前：桜の開花日ワークシート", options: { bold: true, breakLine: true } }, { text: "1980〜2017年の表データ", options: { color: GRAY, fontSize: 13 } }], { x: 0.6, y: 4.75, w: 3.4, h: 0.8, fontSize: 14, align: "center" });
  const yr = [[gi.GiCherry, HEX.sakura, "2年　桜の開花日（一次関数）", ["データを最新年まで更新（AIが補助・教師が原典照合）", "散布図に自分で直線を引く動的教材", "「AIの答え」をデータで確かめる"]],
              [gi.GiEarthCrack, HEX.forest, "1年　地震（比例）", ["観測点のデータで比例を確かめる教材（構想）", "比例定数＝1秒あたり何kmか／理科との関連"]]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, h, af] = yr[i], y = 1.45 + i * 2.55;
    card(s, 4.4, y, 8.35, 2.3, i ? TINT : HEX.sakuraTint);
    await iconCircle(s, ic, 4.65, y + 0.25, 0.8, col);
    T(s, h, { x: 5.65, y: y + 0.25, w: 6.8, h: 0.8, fontSize: 19, bold: true, valign: "middle" });
    T(s, bl(af), { x: 5.0, y: y + 1.1, w: 7.5, h: 1.1, fontSize: 15, paraSpaceAfter: 2 });
  }

  // ===== 16 AIと共存する =====
  s = content("AIと共存する：人間にしかできない部分", "第4章", "第4章 問いかけ");
  const co = [[fa.FaRobot, HEX.ai, "aiTint", "AIが得意なこと", ["案をたくさん出す", "資料の整理・作業", "教材のプログラムを書く", "データを集めて形にする"]],
              [fa.FaChalkboardTeacher, HEX.sakura, "sakuraTint", "人間にしかできないこと", ["何を残すかを決める", "生徒の表情を見て問い返す", "授業に思いを込める", "結果に責任をもつ"]]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, tint, h, li] = co[i], x = 0.6 + i * 6.25;
    card(s, x, 1.45, 5.9, 3.5, HEX[tint]);
    await iconCircle(s, ic, x + 0.3, 1.7, 0.95, col);
    T(s, h, { x: x + 1.45, y: 1.7, w: 4.2, h: 0.95, fontSize: 22, bold: true, color: col, valign: "middle" });
    T(s, bl(li), { x: x + 0.5, y: 2.9, w: 5.2, h: 1.9, fontSize: 18, paraSpaceAfter: 4 });
  }
  card(s, 0.6, 5.2, 12.15, 1.5, TINT);
  await iconCircle(s, gi.GiPlantSeed, 0.9, 5.42, 1.05, HEX.forest);
  T(s, [{ text: "土台（14年間の授業実践）があってこそ、AIでアレンジできる", options: { bold: true, color: FOREST, breakLine: true } }, { text: "土台があると言い切れるものではないが、14年間の授業がなければ今回の資料は作れなかった", options: { fontSize: 15 } }], { x: 2.2, y: 5.3, w: 10.4, h: 1.3, fontSize: 18, valign: "middle" });

  // ===== 17 皆さまへの問い =====
  s = content("皆さまにご意見をいただきたいこと", "第4章");
  const qs = [[fa.FaUsers, HEX.forest, "問い①　教員不足という社会の問題", "学校や教師にできること、すべきことは何か。\n教育の質を守るために、教師の時間をどう守るか。"],
              [fa.FaLaptopCode, HEX.ai, "問い②　学校現場へのAI活用・授業づくり", "授業づくりにAIをどう取り入れるか。\n何をAIに任せ、何を人間が担うべきか。"]];
  for (let i = 0; i < 2; i++) {
    const [ic, col, h, q] = qs[i], x = 0.6 + i * 6.25;
    card(s, x, 1.45, 5.9, 3.55, WHITE, true);
    await iconCircle(s, ic, x + 0.3, 1.7, 0.9, col);
    T(s, h, { x: x + 1.4, y: 1.7, w: 4.3, h: 0.9, fontSize: 19, bold: true, color: col, valign: "middle" });
    T(s, q, { x: x + 0.45, y: 2.85, w: 5.1, h: 1.9, fontSize: 19, valign: "middle" });
  }
  card(s, 0.6, 5.3, 12.15, 1.4, HEX.sakuraTint);
  await iconCircle(s, fa.FaHandshake, 0.9, 5.5, 1.0, HEX.sakura);
  T(s, [{ text: "一つの答えではなく、これからへの示唆を", options: { bold: true, color: SAKURA, breakLine: true } }, { text: "皆さまと指導助言の先生からいただきたい（本研究は実践前・未測定の一つの試み）", options: { fontSize: 15 } }], { x: 2.15, y: 5.35, w: 10.4, h: 1.3, fontSize: 21, valign: "middle" });

  // ===== 18 おわりに =====
  s = pres.addSlide({ masterName: "DARK", sectionTitle: _sec }); s.addNotes(NOTES[idx++]);
  T(s, "おわりに　14年間の蓄積を込めて", { x: 0.7, y: 0.55, w: 11, h: 0.6, fontSize: 22, bold: true, color: MOSS });
  T(s, "変えるべきは、授業の本質ではない。\nその本質にたどり着くための手段である。", { x: 0.7, y: 1.45, w: 11.9, h: 1.9, fontSize: 36, bold: true, color: WHITE, valign: "middle" });
  T(s, "教育の質を守るために、教師の時間を守る。", { x: 0.7, y: 3.45, w: 11.9, h: 0.9, fontSize: 30, bold: true, color: "F4B6C6", valign: "middle" });
  T(s, "AIを学校教育にどう取り入れ、人間らしさでどう扱い、人間にしかできない部分でどう共存するか。\n14年間の授業実践の蓄積を、生成AIを活用して形にしました。受け取り方は、皆さんにお任せします。", { x: 0.7, y: 4.55, w: 11.9, h: 1.2, fontSize: 18, color: "E5EEDF" });
  T(s, "ご清聴ありがとうございました。", { x: 0.7, y: 6.05, w: 11.9, h: 0.7, fontSize: 24, bold: true, color: WHITE });

  // ===== 補足 =====
  s = content("補足① 統計データの出典と詳細", "補足", "補足");
  T(s, [
    { text: "中学校 受験者数：H25 62,998人 → R7 36,621人　採用者数：H12 2,673人 → R7 10,168人", options: { bullet: true, breakLine: true } },
    { text: "教師不足（R3始業日）：中学校868人（0.40%）、全体2,558人（0.31%）※全国調査はこの1回", options: { bullet: true, breakLine: true } },
    { text: "中学校教諭 平日の在校等時間 11:32 → 11:01、授業準備 1:26 → 1:23（H28 → R4）", options: { bullet: true, breakLine: true } },
    { text: "文部科学省「令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況等」参考資料1 https://www.mext.go.jp/content/20261001-kyoikushokuin-000046447_2.pdf", options: { bullet: true, breakLine: true } },
    { text: "文部科学省「教員勤務実態調査（令和4年度）集計【確定値】」 https://www.mext.go.jp/content/20240404-mxt_zaimu01-100003067-1.pdf", options: { bullet: true, breakLine: true } },
    { text: "文部科学省「『教師不足』に関する実態調査」（令和4年1月） https://www.mext.go.jp/content/20220128-mxt_kyoikujinzai01-000020293-1.pdf", options: { bullet: true, breakLine: true } },
    { text: "注意：採用選考の受験者数の推移であり、教員総数の推移ではない。", options: { color: SAKURA, bold: true } }], { x: 0.6, y: 1.45, w: 12.15, h: 5.2, fontSize: 16, paraSpaceAfter: 8 });
  s = content("補足② 振り子モデルの成立条件と過去のデータ", "補足");
  card(s, 0.6, 1.45, 6.0, 5.2, TINT);
  T(s, [{ text: "単振り子の周期", options: { bold: true, color: FOREST, breakLine: true } }, { text: "T＝2π√(L/g) → L＝(g/4π²)T²", options: { breakLine: true } }, { text: "g＝9.80665 m/s² のとき g/4π²≒0.248", options: { breakLine: true } }, { text: "周期2秒 → L≒0.99 m（秒振り子）", options: { breakLine: true } },
    { text: "成り立つ条件", options: { bold: true, color: FOREST, breakLine: true } }, { text: "ふれはばが小さい（30°で周期は約1.7%長くなる）", options: { bullet: true, breakLine: true } }, { text: "長さはおもりの重心まで", options: { bullet: true, breakLine: true } }, { text: "糸の質量・空気抵抗が小さい", options: { bullet: true, breakLine: true } },
    { text: "巨大ブランコは人の重心・大きなふれはばで近似が粗くなる", options: { color: SAKURA, bold: true } }], { x: 0.9, y: 1.65, w: 5.5, h: 4.8, fontSize: 16, paraSpaceAfter: 6 });
  const d21 = [[0.65, 0.10], [0.90, 0.19], [1.01, 0.27], [1.08, 0.31], [1.14, 0.38], [1.39, 0.50], [1.59, 0.64], [1.70, 0.72], [1.72, 0.78], [1.81, 0.84]];
  const t2 = [[hdr("周期x（秒）", FOREST), hdr("長さy（m）", FOREST), hdr("y÷x²", SAKURA)]].concat(d21.map(([x, y]) => [x.toFixed(2), y.toFixed(2), (y / x / x).toFixed(3)].map(v => ({ text: v, options: { align: "center" } }))));
  s.addTable(t2, { x: 7.0, y: 1.45, w: 5.75, colW: [1.95, 1.9, 1.9], fontSize: 14, rowH: 0.45, color: INK, valign: "middle", border: { type: "solid", pt: 1, color: HEX.white }, fill: { color: "F7F9F6" } });
  s = content("補足③ 期待される効果と研究の限界、今後の検証", "補足");
  const ev = [[fa.FaLightbulb, HEX.forest, "期待される効果（未検証）", ["準備時間の短縮", "段階的ヒントで基礎を支える", "数値の根拠で「みなす」説明", "AIの答えを検証する力"]],
              [fa.FaBalanceScale, HEX.sakura, "研究の限界", ["B＝W÷(N×E) は仮定のモデル", "時間短縮・理解向上は未測定", "AI出力の確認にも時間がかかる", "個人情報を入力しない運用が前提"]],
              [fa.FaSearch, HEX.ai, "今後の検証", ["教師：準備・作成・確認の時間、負担感", "生徒：到達率・説明・振り返り", "時間削減率＝(前−後)÷前×100"]]];
  for (let i = 0; i < 3; i++) {
    const [ic, col, h, li] = ev[i], x = 0.6 + i * 4.15;
    card(s, x, 1.45, 3.85, 4.4, WHITE, true);
    await iconCircle(s, ic, x + 0.3, 1.7, 0.8, col);
    T(s, h, { x: x + 1.25, y: 1.7, w: 2.5, h: 0.8, fontSize: 17, bold: true, color: col, valign: "middle" });
    T(s, bl(li), { x: x + 0.35, y: 2.75, w: 3.35, h: 2.9, fontSize: 15, paraSpaceAfter: 6 });
  }
  s = content("補足④ 理想的なバトンパス（2017年・3年）", "補足");
  await iconCircle(s, fa.FaUsers, 0.6, 1.5, 1.0, HEX.forest);
  T(s, bl(["運動会のリレー練習の場面設定（バトンが渡せない会話文）から問題をつくる", "加速して走り出す次走者（y＝ax²）と、一定の速さで走る前走者（一次関数）のグラフで考える", "今後のアレンジ候補：スタート位置やタイミングを動かしてグラフの交点を確かめる動的教材"]), { x: 1.9, y: 1.5, w: 10.8, h: 3.0, fontSize: 19, paraSpaceAfter: 10 });

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("saved", OUT, "notes used", idx, "/", NOTES.length);
})();
