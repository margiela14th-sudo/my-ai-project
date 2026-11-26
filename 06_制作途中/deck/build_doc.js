// 研究資料（Word）— 過去の大会誌原稿の様式（A4・2段組・表題枠・「１．」見出し・「（１）」小見出し・明朝本文）
// 実行：cd 06_制作途中/deck && node build_doc.js
const fs = require("fs"), path = require("path"), sharp = require("sharp");
const { Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, BorderStyle,
  Footer, PageNumber, TableLayoutType, VerticalAlign, LineRuleType, SectionType } = require("docx");

const ROOT = path.resolve(__dirname, "..", "..");
const IMG = path.join(ROOT, "01_過去資料", "画像");
const OUT = path.join(ROOT, "07_完成資料", "県大会研究資料_生成AI授業再構築.docx");
const MIN = "ＭＳ 明朝", GOT = "ＭＳ ゴシック";
const C = { forest: "2C5F2D", tint: "EEF4EA", sakura: "B8405F", sakuraTint: "FBE9EE", gray: "666666", line: "9FB3A2", ink: "111111" };
const mm = v => Math.round(v * 56.7);
const PAGE_W = 11906, ML = mm(18), MR = mm(18), GAP = mm(7);
const FULL = PAGE_W - ML - MR, COLW = Math.floor((FULL - GAP) / 2);

const r = (text, o = {}) => new TextRun(Object.assign({ text, font: { name: o.got ? GOT : MIN, eastAsia: o.got ? GOT : MIN } }, o));
const bd = (c, sz = 6) => ({ style: BorderStyle.SINGLE, size: sz, color: c, space: 3 });
let figN = 0, tblN = 0;

const kids = [];
const P = (text, o = {}) => kids.push(new Paragraph({ indent: { firstLine: o.noIndent ? 0 : 200 }, spacing: { after: 60 }, alignment: AlignmentType.BOTH, children: Array.isArray(text) ? text : [r(text)] }));
const H1 = t => kids.push(new Paragraph({ keepNext: true, spacing: { before: 200, after: 80 }, border: { bottom: bd(C.forest, 8) }, children: [r(t, { got: true, bold: true, size: 23, color: C.forest })] }));
const H2 = t => kids.push(new Paragraph({ keepNext: true, spacing: { before: 120, after: 40 }, children: [r(t, { got: true, bold: true, size: 21 })] }));
const LI = (t, mark = "・") => kids.push(new Paragraph({ indent: { left: 220, hanging: 220 }, spacing: { after: 30 }, children: [r(mark + t)] }));
const BOX = (lines, col = "forest") => {
  const fill = col === "forest" ? C.tint : C.sakuraTint, c = col === "forest" ? C.forest : C.sakura;
  lines.forEach((t, i) => kids.push(new Paragraph({ shading: { type: ShadingType.CLEAR, color: "auto", fill }, border: { top: bd(c, 6), bottom: bd(c, 6), left: bd(c, 6), right: bd(c, 6) },
    indent: { left: 80, right: 80 }, spacing: { before: i === 0 ? 100 : 0, after: i === lines.length - 1 ? 140 : 0, line: 300, lineRule: LineRuleType.AUTO },
    children: [r(t, { got: i === 0 && lines.length > 1, bold: true, size: 20, color: i === 0 && lines.length > 1 ? c : C.ink })] })));
};
const FORMULA = t => kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 100 }, children: [r(t, { got: true, bold: true, size: 30, color: C.forest })] }));
async function FIG(file, cap, widthMm = 80) {
  const buf = fs.readFileSync(file), m = await sharp(buf).metadata(); figN++;
  const w = Math.round(widthMm * 3.78), h = Math.round(w * m.height / m.width);
  kids.push(new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 100, after: 30, line: 240, lineRule: LineRuleType.AUTO },
    children: [new ImageRun({ type: "png", data: buf, transformation: { width: w, height: h }, altText: { title: cap, description: cap, name: "fig" + figN } })] }));
  kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [r(`図${figN}　${cap}`, { got: true, size: 16, color: C.gray })] }));
}
function TABLE(cap, rows, ratios) {
  tblN++;
  kids.push(new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 100, after: 40 }, children: [r(`表${tblN}　${cap}`, { got: true, size: 16, color: C.gray })] }));
  const tot = ratios.reduce((a, b) => a + b, 0), cw = ratios.map(x => Math.floor(x / tot * COLW)); cw[cw.length - 1] += COLW - cw.reduce((a, b) => a + b, 0);
  const line = { style: BorderStyle.SINGLE, size: 4, color: C.line };
  kids.push(new Table({ width: { size: COLW, type: WidthType.DXA }, columnWidths: cw, layout: TableLayoutType.FIXED, borders: { top: line, bottom: line, left: line, right: line, insideHorizontal: line, insideVertical: line },
    rows: rows.map((row, ri) => new TableRow({ tableHeader: ri === 0, children: row.map((v, ci) => new TableCell({ width: { size: cw[ci], type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
      margins: { top: 40, bottom: 40, left: 70, right: 70 }, shading: { type: ShadingType.CLEAR, color: "auto", fill: ri === 0 ? C.forest : (ci === 0 ? C.tint : "FFFFFF") },
      children: [new Paragraph({ spacing: { after: 0, line: 250, lineRule: LineRuleType.AUTO }, children: [r(v, { got: ri === 0 || ci === 0, bold: ri === 0, size: 16, color: ri === 0 ? "FFFFFF" : C.ink })] })] })) })) }));
  kids.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
}

(async () => {
  // ===== 本文（2段組） =====
  H1("１．研究のねらい");
  H2("（１）本資料の作成について");
  P("生成AIを使えば、今は、本資料のような発表資料が作れる時代である。本資料も、構成・文章・グラフ・教材まで生成AIを活用して作成した（中身は、筆者の14年間の授業実践である）。これは、AIで作ったことを示したいのではなく、今の時代を共有するためである。");
  BOX(["使っても、使わなくてもいい。ただ、学びは止めない。これが本研究の根底にある思いである。"], "sakura");
  H2("（２）二つの問い");
  P("教員不足は、待遇や制度、社会の状況まで含む大きな問題であり、一つの研究で議論を深めることは難しい。そこで本研究では、教員一人一人が考えられる「教員の魅力」に視点を絞る。また、教師が学び続けるためには、これからはAIとの共存が欠かせないと考える。本研究では、次の二つを問いとして共有したい。");
  BOX(["問い①", "教員の魅力とは、何か。"]);
  BOX(["問い②（筆者の主張）", "これから教師が学び続けるために、AIとの共存は不可欠である。"], "sakura");
  P("二つをつなぐのは「学び続ける教師」である。本稿は、教員不足を数値で見る（問い①の入口）→教員のAI活用を数値で見る（問い②の背景）→AIを使う前と後の比較→研究仮説に基づく考察と提案→結論と二つの問い、の順に述べる。結論は「授業の質＝土台×AI」であり、その土台を育てるのは学び続けることである。");

  H1("２．研究仮説");
  BOX(["従来の数学科授業実践における数学的な価値や教師の指導意図を継承しながら、生成AIを活用して授業を再構築することで、教師の授業準備に関わる負担を軽減するとともに、生徒の数学的な見方・考え方を働かせる授業の実現につながるのではないか。"]);

  H1("３．研究の方法と内容");
  P("本研究は、次の①～③の流れで行う。");
  LI("過去の自分の授業実践（関数分野）を振り返る。", "①");
  LI("生成AIでアレンジする手順をモデル化する。", "②");
  LI("リメイク授業と教材を提案し、検証計画を立てる（実践前）。", "③");
  H2("（１）教員不足を数値で見る（問い①の入口）");
  P("関数やデータの活用の視点から、教員不足を数値で見てみる。公立中学校の教員採用倍率は、平成12年度の17.9倍から令和7年度には3.6倍となり、過去最低となった（図1）〔文献1 第7表〕。山口県の中学校数学（令和7年度）は、受験37人、採用17人、2.2倍であった〔文献1 第9表-1〕。");
  await FIG(path.join(ROOT, "02_統計データ", "図1_中学校_受験者数と採用倍率.png"), "公立中学校の受験者数と採用倍率（出典：文部科学省（2025）文献1 参考資料1 第7表 p.9より筆者作成）");
  P("ただし、これは受験者数の推移であり、教員総数の推移ではない。倍率の低下には採用者数の増加も影響している。また、中学校教諭の平日1日当たりの在校等時間（10・11月）は、平成28年度11時間32分から令和4年度11時間1分へと31分減ったが、授業準備は1時間26分から1時間23分と、ほとんど変わっていない〔文献2 p.1・p.2〕。");
  P("さらに、令和元年度から7年度の受験者数はほぼ一直線に減少しており、一次関数とみなすことができる（図2）。変化の割合は、(36,621−49,190)÷6≒−2,095（人／年）である（受験者数は文献1 第7表、計算は筆者）。中学校2年で学ぶ「変化の割合」が、学校の課題を読み解く道具になる。ただし、今後も同じ割合で減り続けると決めつけることはできない。");
  await FIG(path.join(ROOT, "02_統計データ", "図4_受験者数_一次関数.png"), "中学校の受験者数（R1〜R7）と一次関数とみなした直線（データ：文献1 第7表 p.9、直線は筆者が作成）");
  H2("（２）二つの問いをつなぐ数学的な視点");
  P("教員1人当たりの業務時間Bを、次の簡易モデルで表す（仮定に基づくもので、実測値ではない）。", { noIndent: true });
  FORMULA("B ＝ W ÷（N × E）");
  P("Wは業務量、Nは教員数、Eは業務効率である。Nを増やすことは社会・行政の課題、Wを減らすことは学校組織の課題であり、Eを高めることは、教師一人一人が授業づくりの中で考えられることである。ここで、AIの活用（問い②）が結びつく。筆者が設定した仮の数値（N＝20人、W＝200時間）では、どの方法でもBは10時間から8時間になる。Nを25％増やしてもBは20％しか減らない（反比例）。ただし、効率化そのものが目的ではない（９．で述べる）。");
  H2("（３）教員のAI活用を数値で見る（問い②の背景）");
  P("TALIS 2024（2024年2〜3月調査、日本の中学校教員3,558名が回答）によると、過去12か月に授業等でAIを使用した中学校教員は、日本17.4％で、OECD平均36.3％の約半分である（図3）。一方、AIが「事務的業務の自動化に役立つ」と考える教員は73.1％（OECD平均44.9％）、「授業計画の作成・改善に役立つ」は59.1％（同53.0％）と、期待はOECD平均より高い〔文献3 p.7〕。期待はあるが、まだ使えていない。ここに活用の余地がある。");
  await FIG(path.join(ROOT, "02_統計データ", "図5_TALIS2024_AI.png"), "教員のAIの使用と考え方（出典：文献3 p.7より筆者作成。日本・OECD平均とも中学校）");
  P("また、校務で生成AIを全く活用していない学校は、令和5年度76.7％、6年度58.9％、7年度16.3％と急速に減少し、教職員の半数以上が活用している学校は1.2％から17.1％に増えた（図4）〔文献4 p.12〕。「半数以上」は「一部の教職員が活用（半分以上）」と「ほぼ全員が活用」の合計で、筆者が算出した。また、教職員の半数以上が活用した学校のうち98％が、働き方の改善に効果があったと回答している〔文献4 p.12〕。");
  await FIG(path.join(ROOT, "02_統計データ", "図6_校務生成AI活用.png"), "校務での生成AIの活用状況（出典：文献4 p.12「校務DXチェックリスト 自己点検結果［確定値］」より筆者作成）");
  H2("（４）活用の余地を関数で見る");
  P("中学校教諭の授業準備は平日1日当たり83分（1時間23分）である〔文献2 p.2〕。このうちAIで短縮できる割合をr％とすると、1日に短縮できる時間y（分）は、y＝0.83rという比例の式で表せる（図5）。r＝10なら1日8.3分、年間200日と仮定すると約28時間となる（r と200日は筆者の仮定）。ただし、これは仮定に基づくモデルであり、実際の短縮時間は今後の検証で確かめる必要がある。");
  await FIG(path.join(ROOT, "02_統計データ", "図7_短縮の余地_比例.png"), "AIで短縮できる割合rと1日の短縮時間y（83分は文献2、rは仮定。実測値ではない）");

  H1("４．AIを使う前の実態");
  H2("（１）これまでの歩み：原問題をアレンジしてきた");
  P("筆者は、2015年の北海道大会（平行四辺形）、2016年の岐阜大会（仮定と証明）、2017年の和歌山大会（複合図）、2018年の東京大会（お掃除ロボット）、2021年の埼玉大会（振り子×ICT）、2022年の島根大会（ジグソー法）、2023年の第二地区（ねじれの位置）と研究を発表してきた。");
  P("どの研究でも、教科書の「原問題」を、生徒が考えたくなる教材に「アレンジ」してきた（図6）。今回は、そのアレンジをAIと一緒に行った。");
  await FIG(path.join(IMG, "2015_発表スライド_アレンジした教材.png"), "2015年 全国大会（北海道）の発表スライド「アレンジした教材」", 72);
  H2("（２）手作業でつくってきた資料");
  P("発表スライドも、板書計画も、ワークシートも、すべて手作業で一枚ずつ作成していた。図7は2021年の発表スライドで、GeoGebraの画面を貼り、関数を一つずつ取り出して比較していた。図8は2024年の振り子のワークシートで、表とグラフの欄のみであった。");
  await FIG(path.join(IMG, "2021_発表スライド_関数を取り出す.png"), "AI活用前：2021年 全国大会（埼玉）の発表スライド", 72);
  await FIG(path.join(IMG, "2024_振り子ワークシート.png"), "AI活用前：2024年の振り子のワークシート");
  P("2021年の発表では、課題として、ICTの効果を計る項目がないこと、ICTを使うタイミング（実物の良さもある）を挙げていた。教材を毎年作り直す時間もかかっていた。");
  H2("（３）土台となる関数分野の三つの授業");
  TABLE("関数分野の三つの授業", [["学年", "題材", "数学的な価値"], ["1年 比例", "地震（初期微動継続時間と震源距離）", "比例とみなす"], ["2年 一次関数", "ソメイヨシノの開花日（山口県）", "一次関数とみなし予想する"], ["3年 y＝ax²", "振り子・巨大ブランコ", "y＝ax²とみなし、周期2秒の振り子をつくる"]], [22, 42, 40]);
  P("いずれも「現実の事象を関数とみなし、予測し、確かめる」授業である。2年の授業では、気象庁の下関の観測データ（2月の平均気温とさくらの開花日）を用いた〔文献5〕。2015年2月の平均気温7.5℃から、グラフで3月27日頃と予想した。気象庁の記録では、実際の開花日は3月25日であり、2日の差で予想できた。");

  H1("５．AIでアレンジする");
  H2("（１）AI LESSON REMAKE（7つのステップ）");
  P("①資料をAIに入力、②良い点を整理、③課題を整理、④AIが改善案を出す、⑤教師が数学的妥当性と教育的価値を吟味、⑥残す・変える・削るで再構築、⑦実践・検証・再改善、の7段階とした。⑤⑥は人間が判断し、AIに任せない。");
  BOX(["残す＝授業の本質／変える＝本質にたどり着く手段／削る＝本質に役立たない作業"]);
  H2("（２）何が、どう置き換わったか");
  TABLE("AI活用前と活用後", [["項目", "AI活用前", "AI活用後"], ["発表スライド", "手作業", "AIが構成・デザイン"], ["統計資料", "扱っていない", "AIが原典から収集・グラフ化"], ["数学教材", "GeoGebraで自作", "AIがWeb教材を作成"], ["発表原稿", "自分で作成", "AIが下書き、自分の言葉で修正"]], [26, 30, 44]);
  P("どれも、最後に確かめ、判断したのは筆者である。変わらなかったのは、中心発問、実物の振り子を測る体験、「関数とみなす」という本質である。実物を測る体験は、ばらつきに悩む経験こそ数学で現実を考える出発点であると考え、あえて残した。");
  H2("（３）AIと作った教材「振り子ラボ」");
  P("実物で測ったデータを入力すると、表・グラフ・式が連動する。2021年の授業で実測した10組のデータ〔文献6〕では、点とグラフのずれ（二乗平均平方根）はy＝0.25x²で0.025m、比例（最もずれが小さくなるa≒0.39）で0.108mとなり、数値を根拠に「y＝ax²とみなす」ことを説明できる（図9）。");
  await FIG(path.join(ROOT, "05_数学教材", "振り子ラボ_画面.png"), "振り子ラボ（2021年の授業データにy＝0.25x²を当てはめた画面）");
  P("また、「ある生成AIは『振り子の長さは周期に比例する』と答えた。本当か」と問い、AIの回答をデータで確かめさせる。周期2秒の振り子は、y＝0.25×2²＝1mと求め、実物で確かめる（理論値は単振り子の周期の式T＝2π√(L/g)、g＝9.8m/s²から約0.99m。振れ幅が小さいときの近似）。");
  H2("（４）1年・2年のアレンジ");
  LI("2年（桜の開花日）：データを最新年まで更新し（AIが補助、教師が原典照合）、散布図に自分で直線を引いて予想する。");
  LI("1年（地震）：観測データで比例を確かめる教材を構想している。");

  H1("６．考察：研究仮説から何が言えるか");
  P("研究仮説を、①数学的な価値・指導意図の継承、②授業準備の負担軽減、③数学的な見方・考え方を働かせる授業、の三つの要素に分け、根拠をもとに検討する。");
  TABLE("研究仮説の要素と根拠", [["要素", "根拠（事実）", "現時点で言えること"], ["①継承", "中心発問・実物の体験・「みなす」を残せた。a：理論0.248／実測約0.258（差約4％）。ずれ：y＝0.25x² 0.025m、比例0.108m", "事例として言える"], ["②負担軽減", "統計収集とグラフ・Web教材・スライドと原稿の下書きをAIが担った。確認・修正の時間も必要だった", "見通しはある（時間は未測定）"], ["③見方・考え方", "数値で比べる場面、AIの答えを検証する場面、段階的ヒントを教材として設計できた", "設計はできた（生徒では未検証）"]], [18, 54, 28]);
  H2("（１）継承について");
  P("AI LESSON REMAKEのSTEP5・6で、中心発問、実物の振り子を測る体験、「関数とみなす」という本質を、教師の判断で残すことができた。振り子ラボの係数は理論値g/4π²≒0.248（g＝9.8m/s²）と一致し、2021年の実測データ〔文献6〕から最小二乗法で求めた値（約0.258）との差は約4％であった（計算は筆者）。数学的な妥当性を保ったまま教材を作り直せたことは、今回の事例について言える。");
  H2("（２）負担軽減について");
  P("統計資料の収集とグラフ化、ブラウザで動く教材、スライドと原稿の下書きはAIが担った。一方、AIの出力には人の確認が必要であった。実際に、グラフで7.5時間が「8」と表示された、資料のURLが移動していた、AIがまとめた数値を元のPDFで照合する必要があった、国際調査のグラフの凡例を画像で確かめた、といった場面があり、いずれも人が確認して修正した。また、2017年に筆者が手作業で作成した桜のワークシートにも、2015年の開花日の誤記（3/27。気象庁の下関の記録は3/25で、ほかの年は一致）があった。確かめる必要があるのは、AIの出力に限らない。作業の多くはAIに置き換えられたが、時間を測っていないため、負担が軽減できたとはまだ言えない。");
  H2("（３）見方・考え方について");
  P("振り子ラボでは、関数ごとのずれを数値で比べ、根拠をもって「y＝ax²とみなす」場面や、AIの答えを数学的に検証する場面を設計できた。ただし、生徒の学びへの効果は実践前であり、未検証である。");
  H2("（４）AIを使う前と後：利点・欠点・可能性");
  P("実証前であるため、ここでは見えてきた見通しとして、数学の授業づくりに限定して整理する（表4）。");
  TABLE("AIを使う前と後の利点・欠点・可能性（実証前の見通し）", [["観点", "内容"], ["利点", "原典データをすぐにグラフ化できる。動く教材を短時間でつくれる。過去の授業を整理し、課題を言葉にできる。"], ["欠点", "もっともらしい誤りが混ざる。確かめる時間が要る。生徒の実態は知らない。頼りすぎると、自分で考える機会が減るおそれがある。"], ["可能性", "過去の授業を生かし直せる。AIの答えを数学で確かめる授業ができる。若手が先輩の実践を土台に学べる。"]], [18, 82]);
  BOX(["結論", "①は事例として支持される。②③は見通しがあり、今後の検証が必要である。"]);

  H1("７．提案と今後の検証");
  LI("提案1：AI LESSON REMAKE。特に、人間が判断するステップ（STEP5・6）を手順に組み込む。");
  LI("提案2：AIの答えを数学で確かめる活動を、授業に取り入れる。");
  LI("提案3：効果を測る。授業準備・教材作成・AI出力の確認修正の時間を改善の前後で記録し、時間削減率＝（改善前−改善後）÷改善前×100で求める。教師の意識はTALISと同じ項目で、生徒は到達率・説明・振り返りで比較する。");

  LI("提案4：授業づくりの「超自動化」。教師が授業記録とねらいを入れ、Claude Code（生成AI）が日々の授業案・学習指導案・板書型指導案・教材を作り、別の生成AI（Codex）が数値・数学・誤りを二重に確かめ、最後に教師が決める。以前は、板書型指導案も1枚ずつ手作業で作成していた（例：2019年 数学教育サマーフェスタ持参資料）。作る手順の型と二つのAIの連携の設定は作成済みで、指導案の見本を試作した。日々の運用と時間の測定はこれからである。");
  LI("提案5：振り返りの自動化。生徒が毎時間の振り返りをフォームで入力し、スプレッドシートに集める。氏名・成績を外して匿名化したうえでAIが分析し（つまずき・見方考え方・よく出た言葉）、教師が読んで加筆し、生徒に返す。結果は次の授業案に生かす。構想段階であり、外部のAIには匿名化したデータのみを渡し、返却前に必ず教師が読む。");

  H1("８．結論：授業の質＝土台×AI");
  P("AIは、案を出すこと、資料の整理、教材のプログラム作成に優れている。一方で、何を残すかを決めること、生徒の表情を見て問い返すこと、授業に思いを込めることは、人間にしかできない。土台がなければ、AIでアレンジすることもできない。筆者自身、土台があると言い切れるものではないが、14年間の授業実践がなければ本資料は作成できなかった。");
  FORMULA("授業の質 ＝ 土台 × AI");
  P("ここでいう土台とは、自分の授業記録、成功も失敗も含めた経験、生徒の反応といった一次情報である。土台が0なら、AIをかけても0である。土台がないままAIを使えば、AIを使いこなすのではなく、AIに使われるだけになり、授業も資料も薄っぺらなものになる。結局は、生成AIを使う人間の質の問題である。筆者は以前、振り返りのプリントに「このたかが１枚の積み重ねが，大きな差をうむのです。」と書いていた。土台とは、この積み重ねである。");
  BOX(["だからこそ、土台とともに、生成AIの活用を進めたい。"], "sakura");
  P("そして、その土台を育てるのは、学び続けることである。AIには作業・下書き・過去の授業や振り返りの整理を任せ、確かめること、決めること、生徒を見て問い返すことは人間が担う。任せて生まれた時間と気づきを、学び続けることに使いたい。");

  H1("９．時短は、目的ではない");
  P("昨今、時短や効率化が盛んに言われている。しかし、本当にこのままでよいのだろうか。お金を得る仕事の効率（速く・安く・多く）と、教育の営みは、同じ物差しでは測れないと筆者は考える。決して楽な方を選べということではない。");
  BOX(["楽をするための効率化ではない。学びを止めないためのAIである。"]);
  P("AIで生まれた時間は、学ぶことと、子どもに向き合うことに使いたい。一方で、学べば学ぶほど子どもに還元できるとは限らず、学ぶには時間もかかる。教員の在り方は難しいと、筆者自身つくづく感じている。");

  H1("10．皆さまと考えたいこと");
  H2("（１）ある数学の先生との対話から");
  P("先輩の数学教員との対話（2026年11月）では、なり手不足そのものの解決は難しいという前提に立ったうえで、一つの方向が示された。生徒数に対する教員の配置の「標準」をそろえることである。教員に余裕のある学校もあれば、ぎりぎりの学校もある。統廃合も含めて、標準に合う学校規模にしていかなければ、同じ土俵で議論できない。その差が、多忙感や疲弊、さらには学ぶ姿勢の衰えにつながっているのではないか、という見方である（一つの見方であり、数値での裏付けは示していない）。");
  P("もちろん、学び続ける教員もいる。ただ、社会が変化する中で、学び続ける教員の姿は形を変えてきていると筆者は感じている。これも一つの着地点である。では、ほかにはどうか。");
  H2("（２）二つの問い");
  BOX(["問い①　教員の魅力とは、何か", "教員不足を、なり手の「数」ではなく「魅力」から考えたい。学び続ける姿そのものが、その答えの一つにならないか（筆者の考え）。"]);
  BOX(["問い②　学び続けるために、AIとの共存は不可欠", "では、何をAIに任せ、何を人間が担うか。"], "sakura");
  P("本研究は実践前・未測定の一つの試みである。一つの答えではなく、今後への示唆をいただきたい。");

  H1("11．おわりに");
  P("私たちの仕事は、最終的には目の前の子どもたちのためにある。いくらAIが入ってこようとも、どれだけ時間を短縮できようとも、最も大事なのは、それを使う人の誠実さと謙虚さである。");
  BOX(["人間性を磨き続ける。学び続ける。"], "sakura");
  P("変えるべきは、授業の本質ではない。その本質にたどり着くための手段である。");

  kids.push(new Paragraph({ keepNext: true, spacing: { before: 160, after: 40 }, children: [r("＜参考・引用文献＞", { got: true, bold: true, size: 19 })] }));
  for (const t of [
    "〔文献1〕文部科学省（2025）「令和7年度（令和6年度実施）公立学校教員採用選考試験の実施状況について」参考資料1（第2表-1、第7表 p.9、第9表-1），令和7年12月25日公表，https://www.mext.go.jp/content/20261001-kyoikushokuin-000046447_2.pdf（ポイント資料：https://www.mext.go.jp/content/20261001-kyoikushokuin-000046447_1.pdf）",
    "〔文献2〕文部科学省（2024）「教員勤務実態調査（令和4年度）集計【確定値】」p.1・p.2（10・11月の1日当たり、教諭），https://www.mext.go.jp/content/20240404-mxt_zaimu01-100003067-1.pdf",
    "〔文献3〕文部科学省・国立教育政策研究所（2025）「OECD国際教員指導環境調査（TALIS）2024報告書のポイント」p.7（2025年10月7日 OECD結果公表），https://www.mext.go.jp/b_menu/toukei/data/Others/20251006-ope_dev02-2.pdf",
    "〔文献4〕中央教育審議会 初等中等教育分科会 デジタル学習基盤特別委員会（第10回，2026年6月30日）資料1「学校教育におけるAI活用に関するこれまでの取組と今後の方向性」p.12，https://www.mext.go.jp/content/20260630-mxt_shuukyo01-000050664_2.pdf",
    "〔文献5〕気象庁「過去の気象データ検索」下関（山口県）月ごとの値（2月の平均気温），https://www.data.jma.go.jp/stats/etrn/ ／気象庁「さくらの開花日」（生物季節観測，下関），https://www.data.jma.go.jp/sakura/data/sakura003_06.html",
    "〔文献6〕新田正幸・山本剛（2021）「主体的・対話的で深い学び」の視点からの授業改善 ～関数y＝ax²におけるICT活用をとおして～，第103回全国算数・数学教育研究（埼玉）大会（振り子の実測データ）",
    "新田正幸・松村崇史（2015）説明することにおもしろさを見いだす授業，第97回全国算数・数学教育研究（北海道）大会",
    "文部科学省（2017）中学校学習指導要領（平成29年告示）解説 数学編／啓林館「未来へひろがる数学3」",
    "※URLと数値は、2026年11月24日に原典で確認した。統計の数値は原典のとおりとし、筆者が計算・作成した値やグラフはその旨を明記した。"])
    kids.push(new Paragraph({ indent: { left: 200, hanging: 200 }, spacing: { after: 20 }, children: [r((/^[〔※]/.test(t) ? "" : "・") + t, { size: 15 })] }));

  // ===== 表題（1段）=====
  const head = [];
  head.push(new Paragraph({ spacing: { after: 80 }, children: [r("令和8年度山口県中学校数学教育第二地区研究協議会　　関数", { got: true, size: 18 })] }));
  const noB = { style: BorderStyle.SINGLE, size: 8, color: C.forest };
  head.push(new Table({ width: { size: FULL, type: WidthType.DXA }, columnWidths: [FULL], layout: TableLayoutType.FIXED, borders: { top: noB, bottom: noB, left: noB, right: noB, insideHorizontal: noB, insideVertical: noB },
    rows: [new TableRow({ children: [new TableCell({ width: { size: FULL, type: WidthType.DXA }, margins: { top: 140, bottom: 120, left: 200, right: 200 }, children: [
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 }, children: [r("生成AIを活用した数学科授業の改善と新たな授業モデルの提案", { got: true, bold: true, size: 32 })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [r("～関数分野における従来の授業実践を通して～", { got: true, size: 23 })] }),
      new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 0 }, children: [r("山口県・下関市立名陵中学校　新田 正幸", { size: 21 })] }),
    ] })] })] }));
  head.push(new Paragraph({ spacing: { after: 60 }, children: [] }));

  const footer = new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ["－ ", PageNumber.CURRENT, " －"], size: 18, font: MIN })] })] });
  const page = { size: { width: PAGE_W, height: 16838 }, margin: { top: mm(18), bottom: mm(18), left: ML, right: MR, header: mm(8), footer: mm(8) } };
  const doc = new Document({
    creator: "新田正幸", title: "生成AIを活用した数学科授業の改善と新たな授業モデルの提案",
    styles: { default: { document: { run: { font: { name: MIN, eastAsia: MIN }, size: 20, color: C.ink }, paragraph: { spacing: { line: 320, lineRule: LineRuleType.AUTO } } } } },
    sections: [
      { properties: { page }, footers: { default: footer }, children: head },
      { properties: { page, type: SectionType.CONTINUOUS, column: { count: 2, space: GAP, equalWidth: true } }, footers: { default: footer }, children: kids },
    ],
  });
  fs.writeFileSync(OUT, await Packer.toBuffer(doc));
  console.log("saved", OUT, "figs", figN, "tables", tblN);
})();
