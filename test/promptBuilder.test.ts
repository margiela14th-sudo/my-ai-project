import { describe, expect, it } from "vitest";
import { JIRITSU_KATSUDO } from "../src/core/knowledge/specialNeeds.js";
import { SUBJECTS } from "../src/core/knowledge/subjects.js";
import { buildSystemPrompt, buildUserPrompt, validateRequest } from "../src/core/promptBuilder.js";
import { PERSONA } from "../src/core/persona.js";
import type { LessonRequest } from "../src/core/types.js";

const base: LessonRequest = {
  schoolLevel: "elementary",
  grade: 4,
  subject: "math",
  planType: "bansho",
  unitName: "わり算の筆算を考えよう",
  lessonNumber: 3,
  totalLessons: 10,
  classSetting: "regular",
};

describe("validateRequest", () => {
  it("正しい入力はエラーなし", () => {
    expect(validateRequest(base)).toEqual([]);
  });

  it("単元名が空ならエラー", () => {
    expect(validateRequest({ ...base, unitName: "  " }).map((e) => e.field)).toContain("unitName");
  });

  it("中学校に4年生はない", () => {
    expect(validateRequest({ ...base, schoolLevel: "juniorHigh" }).map((e) => e.field)).toContain("grade");
  });

  it("通常の学級で小1に理科はない", () => {
    expect(validateRequest({ ...base, grade: 1, subject: "science" }).map((e) => e.field)).toContain("subject");
  });

  it("特別支援学級では学年にない教科も選べる（特別の教育課程）", () => {
    expect(
      validateRequest({ ...base, grade: 1, subject: "science", classSetting: "specialClass" }),
    ).toEqual([]);
  });

  it("本時が総時数を超えたらエラー", () => {
    expect(validateRequest({ ...base, lessonNumber: 11 }).map((e) => e.field)).toContain("lessonNumber");
  });
});

describe("buildSystemPrompt", () => {
  it("人格を先頭ブロックに固定する（キャッシュのため）", () => {
    const [persona] = buildSystemPrompt(base);
    expect(persona).toBe(PERSONA);
    expect(buildSystemPrompt({ ...base, subject: "japanese" })[0]).toBe(PERSONA);
  });

  it("算数では専門ナレッジと学年の内容が入る", () => {
    const [, knowledge] = buildSystemPrompt(base);
    expect(knowledge).toContain("算数・数学 専門ナレッジ");
    expect(knowledge).toContain("わり算の筆算");
    expect(knowledge).toContain("C変化と関係");
  });

  it("算数以外では算数ナレッジは入らない", () => {
    const [, knowledge] = buildSystemPrompt({ ...base, subject: "japanese" });
    expect(knowledge).not.toContain("算数・数学 専門ナレッジ");
    expect(knowledge).toContain("言葉による見方・考え方");
  });

  it("中学数学は中学の領域になる", () => {
    const [, knowledge] = buildSystemPrompt({ ...base, schoolLevel: "juniorHigh", grade: 2 });
    expect(knowledge).toContain("A数と式 B図形 C関数 Dデータの活用");
    expect(knowledge).toContain("連立二元一次方程式");
  });

  it("特別支援学級では自立活動と障害種別の支援例が入る", () => {
    const [, knowledge] = buildSystemPrompt({
      ...base,
      classSetting: "specialClass",
      disabilityTypes: ["intellectual", "autismEmotional"],
      intellectualStage: "小学部2段階",
    });
    expect(knowledge).toContain("自立活動 6区分27項目");
    expect(knowledge).toContain("知的障害への支援例");
    expect(knowledge).toContain("自閉症・情緒障害への支援例");
    expect(knowledge).toContain("小学部2段階");
    expect(knowledge).toContain("第138条");
  });
});

describe("buildUserPrompt", () => {
  it("条件と指導案の構成が入る", () => {
    const p = buildUserPrompt(base);
    expect(p).toContain("板書型指導案");
    expect(p).toContain("小学校 第4学年");
    expect(p).toContain("全10時間中の第3時");
    expect(p).toContain("1単位時間：45分");
    expect(p).toContain("## 板書計画");
  });

  it("中学校の既定は50分、研究授業は細案の構成", () => {
    const p = buildUserPrompt({ ...base, schoolLevel: "juniorHigh", grade: 1, planType: "research" });
    expect(p).toContain("1単位時間：50分");
    expect(p).toContain("単元の評価規準");
    expect(p).toContain("研究協議の視点");
  });

  it("任意項目は入力したときだけ入る", () => {
    expect(buildUserPrompt(base)).not.toContain("の実態");
    expect(buildUserPrompt({ ...base, studentProfile: "28名" })).toContain("## 児童の実態");
  });
});

describe("ナレッジの整合性", () => {
  it("自立活動は6区分27項目", () => {
    expect(Object.keys(JIRITSU_KATSUDO)).toHaveLength(6);
    expect(Object.values(JIRITSU_KATSUDO).flat()).toHaveLength(27);
  });

  it("どの学年にも少なくとも国語・算数がある", () => {
    for (const g of [1, 2, 3, 4, 5, 6]) {
      expect(SUBJECTS.japanese.grades.elementary).toContain(g);
      expect(SUBJECTS.math.grades.elementary).toContain(g);
    }
  });
});
