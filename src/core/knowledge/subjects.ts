/**
 * 教科ナレッジ（平成29・30年告示 学習指導要領の要点を要約したもの）。
 * 条文の逐語引用ではなく、指導案作成に必要な観点を整理した要約です。
 * 正確な文言は必ず学習指導要領・解説の原典で確認してください。
 */
import type { SchoolLevel } from "../types.js";

export interface SubjectKnowledge {
  id: string;
  name: string;
  /** 対象学年（この教科が置かれている学年） */
  grades: Record<SchoolLevel, number[]>;
  /** 教科の見方・考え方（要約） */
  perspective: string;
  /** 内容の構成（領域など） */
  structure: Partial<Record<SchoolLevel, string>>;
  /** 授業づくりの要点 */
  lessonTips: string[];
}

const ALL_ELEM = [1, 2, 3, 4, 5, 6];
const ALL_JH = [1, 2, 3];

export const SUBJECTS: Record<string, SubjectKnowledge> = {
  japanese: {
    id: "japanese",
    name: "国語",
    grades: { elementary: ALL_ELEM, juniorHigh: ALL_JH },
    perspective:
      "言葉による見方・考え方：対象と言葉、言葉と言葉との関係を、言葉の意味、働き、使い方等に着目して捉えたり問い直したりして、言葉への自覚を高めること。",
    structure: {
      elementary:
        "〔知識及び技能〕(1)言葉の特徴や使い方 (2)情報の扱い方 (3)我が国の言語文化／〔思考力、判断力、表現力等〕A話すこと・聞くこと B書くこと C読むこと",
      juniorHigh:
        "〔知識及び技能〕(1)言葉の特徴や使い方 (2)情報の扱い方 (3)我が国の言語文化／〔思考力、判断力、表現力等〕A話すこと・聞くこと B書くこと C読むこと",
    },
    lessonTips: [
      "単元で付けたい資質・能力（指導事項）を一つに絞り、言語活動をそれに合わせて設定する",
      "教材を「読む」こと自体を目的にせず、言語活動を通して指導事項を身に付けさせる",
      "根拠となる叙述に線を引く・付箋に書くなど、考えの根拠を本文に求めさせる",
    ],
  },
  social: {
    id: "social",
    name: "社会",
    grades: { elementary: [3, 4, 5, 6], juniorHigh: ALL_JH },
    perspective:
      "社会的事象の見方・考え方：位置や空間的な広がり、時期や時間の経過、事象や人々の相互関係などに着目して社会的事象を捉え、比較・分類したり総合したり、地域の人々や国民の生活と関連付けたりすること（中学校は地理的・歴史的・現代社会の見方・考え方）。",
    structure: {
      elementary: "3年：市区町村、4年：都道府県、5年：国土と産業、6年：政治・歴史・国際",
      juniorHigh: "地理的分野・歴史的分野・公民的分野",
    },
    lessonTips: [
      "資料（写真・グラフ・地図・年表）から問いを生む「学習問題」をつくる",
      "調べる→まとめる→いかす（社会への関わり方を選択・判断）の単元構成",
      "事実（何が）→意味（なぜ・どのような）へと問いを深める",
    ],
  },
  math: {
    id: "math",
    name: "算数・数学",
    grades: { elementary: ALL_ELEM, juniorHigh: ALL_JH },
    perspective:
      "数学的な見方・考え方：事象を数量や図形及びそれらの関係などに着目して捉え、根拠を基に筋道を立てて考え、統合的・発展的に考えること（中学校は「論理的、統合的・発展的に考えること」）。",
    structure: {
      elementary:
        "1〜3年：A数と計算 B図形 C測定 Dデータの活用／4〜6年：A数と計算 B図形 C変化と関係 Dデータの活用",
      juniorHigh: "A数と式 B図形 C関数 Dデータの活用",
    },
    lessonTips: ["算数・数学は専門ナレッジ（math.ts）を参照"],
  },
  science: {
    id: "science",
    name: "理科",
    grades: { elementary: [3, 4, 5, 6], juniorHigh: ALL_JH },
    perspective:
      "理科の見方・考え方：自然の事物・現象を、量的・関係的（エネルギー）、質的・実体的（粒子）、共通性・多様性（生命）、時間的・空間的（地球）な視点で捉え、比較・関係付け・条件制御・多面的に考えるなどの方法で探究すること。",
    structure: {
      elementary: "A物質・エネルギー B生命・地球",
      juniorHigh: "第1分野（物理・化学） 第2分野（生物・地学）",
    },
    lessonTips: [
      "自然事象への気付き→問題→予想・仮説→観察・実験の計画→結果→考察→結論の問題解決の過程",
      "学年ごとに重点の問題解決の力（3年:比較、4年:関係付け、5年:条件制御、6年:多面的に考える）",
      "安全指導（保護眼鏡・加熱器具・薬品）を指導案に明記する",
    ],
  },
  life: {
    id: "life",
    name: "生活",
    grades: { elementary: [1, 2], juniorHigh: [] },
    perspective:
      "身近な生活に関わる見方・考え方：身近な人々、社会及び自然を自分との関わりで捉え、よりよい生活に向けて思いや願いを実現しようとすること。",
    structure: { elementary: "学校・家庭・地域の生活に関する内容／身近な人々・社会・自然と関わる活動／自分自身の生活や成長" },
    lessonTips: [
      "具体的な活動や体験→表現（伝え合い・振り返り）の往還",
      "幼児期の教育との接続（スタートカリキュラム）を意識する",
    ],
  },
  music: {
    id: "music",
    name: "音楽",
    grades: { elementary: ALL_ELEM, juniorHigh: ALL_JH },
    perspective:
      "音楽的な見方・考え方：音楽に対する感性を働かせ、音や音楽を音楽を形づくっている要素とその働きの視点で捉え、自己のイメージや感情、生活や社会、伝統や文化などと関連付けること。",
    structure: { elementary: "A表現（歌唱・器楽・音楽づくり） B鑑賞 〔共通事項〕", juniorHigh: "A表現（歌唱・器楽・創作） B鑑賞 〔共通事項〕" },
    lessonTips: ["〔共通事項〕の音楽を形づくっている要素（音色・リズム・速度・旋律など）を本時で一つ焦点化する"],
  },
  art: {
    id: "art",
    name: "図画工作・美術",
    grades: { elementary: ALL_ELEM, juniorHigh: ALL_JH },
    perspective:
      "造形的な見方・考え方：感性や想像力を働かせ、対象や事象を造形的な視点で捉え、自分のイメージをもちながら意味や価値をつくりだすこと。",
    structure: { elementary: "A表現（造形遊び・絵や立体、工作） B鑑賞 〔共通事項〕", juniorHigh: "A表現（発想や構想・技能） B鑑賞 〔共通事項〕" },
    lessonTips: ["材料・用具の安全な扱い、片付けまでの時間配分を明記する", "作品のよさを見付け合う鑑賞の場面を位置付ける"],
  },
  homeEconomics: {
    id: "homeEconomics",
    name: "家庭・技術・家庭",
    grades: { elementary: [5, 6], juniorHigh: ALL_JH },
    perspective:
      "生活の営みに係る見方・考え方：家族や家庭、衣食住、消費や環境などに係る生活事象を、協力・協働、健康・快適・安全、生活文化の継承・創造、持続可能な社会の構築等の視点で捉え、よりよい生活を営むために工夫すること（技術分野は技術の見方・考え方）。",
    structure: {
      elementary: "A家族・家庭生活 B衣食住の生活 C消費生活・環境",
      juniorHigh: "技術分野：A材料と加工 Bエネルギー変換 C生物育成 D情報／家庭分野：A家族・家庭生活 B衣食住 C消費生活・環境",
    },
    lessonTips: ["実習の安全・衛生指導、アレルギー確認を明記する", "家庭での実践につながる課題設定"],
  },
  pe: {
    id: "pe",
    name: "体育・保健体育",
    grades: { elementary: ALL_ELEM, juniorHigh: ALL_JH },
    perspective:
      "体育や保健の見方・考え方：運動やスポーツを、その価値や特性に着目して、楽しさや喜びとともに体力の向上に果たす役割の視点から捉え、自己の適性等に応じた『する・みる・支える・知る』の多様な関わり方と関連付けること。",
    structure: {
      elementary: "体つくり運動系、器械運動系、陸上運動系、水泳運動系、ボール運動系、表現運動系、保健（3年以上）",
      juniorHigh: "体つくり運動、器械運動、陸上競技、水泳、球技、武道、ダンス、体育理論、保健分野",
    },
    lessonTips: ["運動量の確保と安全管理（場の設定図）を指導案に入れる", "苦手な子・見学者の関わり方を具体的に書く"],
  },
  english: {
    id: "english",
    name: "外国語（英語）・外国語活動",
    grades: { elementary: [3, 4, 5, 6], juniorHigh: ALL_JH },
    perspective:
      "外国語によるコミュニケーションにおける見方・考え方：外国語で表現し伝え合うため、外国語やその背景にある文化を、社会や世界、他者との関わりに着目して捉え、コミュニケーションを行う目的や場面、状況等に応じて、情報を整理しながら考えなどを形成し、再構築すること。",
    structure: {
      elementary: "3・4年：外国語活動（聞くこと・話すこと［やり取り］・話すこと［発表］）／5・6年：外国語（4技能5領域）",
      juniorHigh: "聞くこと・読むこと・話すこと［やり取り］・話すこと［発表］・書くこと の5領域",
    },
    lessonTips: ["目的・場面・状況のあるコミュニケーション活動を設定する", "Small Talk→めあて→インプット→アウトプット→振り返りの流れ"],
  },
  moral: {
    id: "moral",
    name: "特別の教科 道徳",
    grades: { elementary: ALL_ELEM, juniorHigh: ALL_JH },
    perspective:
      "道徳的諸価値についての理解を基に、自己を見つめ、物事を（広い視野から）多面的・多角的に考え、自己の（人間としての）生き方についての考えを深める。",
    structure: { elementary: "A自分自身 B人との関わり C集団や社会との関わり D生命や自然、崇高なものとの関わり", juniorHigh: "A自分自身 B人との関わり C集団や社会との関わり D生命や自然、崇高なものとの関わり" },
    lessonTips: [
      "主題名・内容項目・ねらいを明確にし、中心発問と補助発問を設計する",
      "評価は数値によらず個人内評価の記述式、大くくりなまとまりを踏まえて行う",
      "特定の価値観の押し付けにならないよう、考え議論する道徳を意識する",
    ],
  },
  integrated: {
    id: "integrated",
    name: "総合的な学習の時間",
    grades: { elementary: [3, 4, 5, 6], juniorHigh: ALL_JH },
    perspective:
      "探究的な見方・考え方：各教科等における見方・考え方を総合的に働かせて、広範な事象を多様な角度から俯瞰して捉え、実社会や実生活の文脈や自己の生き方と関連付けて問い続けること。",
    structure: { elementary: "課題の設定→情報の収集→整理・分析→まとめ・表現 の探究のプロセス", juniorHigh: "課題の設定→情報の収集→整理・分析→まとめ・表現 の探究のプロセス" },
    lessonTips: ["思考ツール（ベン図・Yチャート等）を整理・分析の場面に位置付ける"],
  },
  specialActivities: {
    id: "specialActivities",
    name: "特別活動（学級活動）",
    grades: { elementary: ALL_ELEM, juniorHigh: ALL_JH },
    perspective:
      "集団や社会の形成者としての見方・考え方：各教科等の見方・考え方を総合的に働かせながら、自己及び集団や社会の問題を捉え、よりよい人間関係の形成、よりよい集団生活の構築や社会への参画及び自己の実現に関連付けること。",
    structure: { elementary: "学級活動(1)(2)(3)、児童会活動、クラブ活動、学校行事", juniorHigh: "学級活動(1)(2)(3)、生徒会活動、学校行事" },
    lessonTips: ["議題（話し合うこと）と提案理由、話合いのめあてを明確にする", "(3)はキャリア・パスポートを活用"],
  },
};

export function getSubject(id: string): SubjectKnowledge | undefined {
  return SUBJECTS[id];
}

export function subjectAvailable(id: string, level: SchoolLevel, grade: number): boolean {
  const s = SUBJECTS[id];
  return !!s && s.grades[level].includes(grade);
}
