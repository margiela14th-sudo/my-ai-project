import { mathKnowledgeText } from "./knowledge/math.js";
import {
  CLASS_SETTING_LABELS,
  DISABILITY_LABELS,
  specialNeedsKnowledgeText,
} from "./knowledge/specialNeeds.js";
import { getSubject, subjectAvailable } from "./knowledge/subjects.js";
import { PERSONA } from "./persona.js";
import { PLAN_TEMPLATES } from "./templates.js";
import type { LessonRequest, ValidationError } from "./types.js";

const LEVEL_LABEL = { elementary: "小学校", juniorHigh: "中学校" } as const;
const MAX_GRADE = { elementary: 6, juniorHigh: 3 } as const;
const DEFAULT_MINUTES = { elementary: 45, juniorHigh: 50 } as const;

export function validateRequest(req: LessonRequest): ValidationError[] {
  const errors: ValidationError[] = [];
  if (!(req.schoolLevel in MAX_GRADE)) {
    errors.push({ field: "schoolLevel", message: "校種を選んでください" });
    return errors;
  }
  if (!Number.isInteger(req.grade) || req.grade < 1 || req.grade > MAX_GRADE[req.schoolLevel]) {
    errors.push({ field: "grade", message: "学年が範囲外です" });
  }
  if (!getSubject(req.subject)) {
    errors.push({ field: "subject", message: "教科を選んでください" });
  } else if (
    req.classSetting === "regular" &&
    !subjectAvailable(req.subject, req.schoolLevel, req.grade)
  ) {
    // 特別支援学級・学校は教育課程を独自に編成できるため、学年の制約をかけない
    errors.push({ field: "subject", message: "この学年にはない教科です" });
  }
  if (!(req.planType in PLAN_TEMPLATES)) {
    errors.push({ field: "planType", message: "指導案の種類を選んでください" });
  }
  if (!req.unitName?.trim()) {
    errors.push({ field: "unitName", message: "単元名を入力してください" });
  }
  if (
    req.lessonNumber !== undefined &&
    req.totalLessons !== undefined &&
    req.lessonNumber > req.totalLessons
  ) {
    errors.push({ field: "lessonNumber", message: "本時が総時数を超えています" });
  }
  return errors;
}

/** システムプロンプト：人格 → 教科ナレッジ。リクエストに依存しない人格を先頭に置きキャッシュを効かせる */
export function buildSystemPrompt(req: LessonRequest): string[] {
  const subject = getSubject(req.subject)!;
  const knowledge: string[] = [
    `## 教科ナレッジ：${subject.name}`,
    `- 見方・考え方：${subject.perspective}`,
    `- 内容の構成：${subject.structure[req.schoolLevel] ?? "（特別の教育課程に応じて設定）"}`,
    ...subject.lessonTips.map((t) => `- ${t}`),
  ];
  if (req.subject === "math") {
    knowledge.push("", mathKnowledgeText(req.schoolLevel, req.grade));
  }
  knowledge.push(
    "",
    specialNeedsKnowledgeText(req.classSetting, req.disabilityTypes, req.intellectualStage),
  );
  return [PERSONA, knowledge.join("\n")];
}

export function buildUserPrompt(req: LessonRequest): string {
  const subject = getSubject(req.subject)!;
  const template = PLAN_TEMPLATES[req.planType];
  const minutes = req.minutes ?? DEFAULT_MINUTES[req.schoolLevel];
  const studentWord = req.schoolLevel === "elementary" ? "児童" : "生徒";
  const lesson =
    req.lessonNumber && req.totalLessons
      ? `全${req.totalLessons}時間中の第${req.lessonNumber}時`
      : req.lessonNumber
        ? `第${req.lessonNumber}時`
        : "本時（時数は一般的な配当で想定）";

  const lines = [
    `次の条件で「${template.label}」を作成してください。`,
    "",
    "## 授業の条件",
    `- 校種・学年：${LEVEL_LABEL[req.schoolLevel]} 第${req.grade}学年`,
    `- 教科：${subject.name}`,
    `- 単元名・題材名：${req.unitName.trim()}`,
    `- 本時：${lesson}`,
    `- 1単位時間：${minutes}分`,
    `- 学級：${CLASS_SETTING_LABELS[req.classSetting]}`,
  ];
  if (req.disabilityTypes?.length) {
    lines.push(`- 障害種：${req.disabilityTypes.map((d) => DISABILITY_LABELS[d]).join("、")}`);
  }
  if (req.intellectualStage) lines.push(`- 知的障害の各教科の段階：${req.intellectualStage}`);
  if (req.textbook) lines.push(`- 使用教科書：${req.textbook}`);
  if (req.lessonFocus) lines.push(`- 本時で扱いたいこと：${req.lessonFocus}`);
  if (req.researchTheme) lines.push(`- 研究主題：${req.researchTheme}`);
  if (req.studentProfile) lines.push("", `## ${studentWord}の実態`, req.studentProfile);
  if (req.supportNotes) lines.push("", "## 個別の配慮・支援で考えたいこと", req.supportNotes);
  if (req.extraRequests) lines.push("", "## 先生からの要望", req.extraRequests);

  lines.push(
    "",
    `## 指導案の種類：${template.label}`,
    `目的：${template.purpose}`,
    "",
    "次の構成で書いてください（{ }は条件で置き換える。見出しの順序は守り、内容は授業に合わせて充実させる）。",
    "",
    template.outline,
  );
  return lines.join("\n");
}
