/** 校種 */
export type SchoolLevel = "elementary" | "juniorHigh";

/** 学級・学校の種別 */
export type ClassSetting =
  | "regular" // 通常の学級
  | "specialClass" // 特別支援学級
  | "specialSchool" // 特別支援学校
  | "resourceRoom"; // 通級による指導

/** 障害種（特別支援学級・学校・通級で使用） */
export type DisabilityType =
  | "intellectual" // 知的障害
  | "autismEmotional" // 自閉症・情緒障害
  | "physical" // 肢体不自由
  | "health" // 病弱・身体虚弱
  | "visual" // 弱視・視覚障害
  | "hearing" // 難聴・聴覚障害
  | "speech" // 言語障害
  | "ldAdhd"; // LD・ADHD（通級）

/** 指導案の種類 */
export type PlanType =
  | "bansho" // 板書型指導案
  | "daily" // 日々の学習指導案（略案）
  | "research"; // 研究授業の学習指導案（細案）

export interface LessonRequest {
  schoolLevel: SchoolLevel;
  /** 学年（小:1-6、中:1-3） */
  grade: number;
  /** 教科ID（knowledge/subjects.ts のキー） */
  subject: string;
  planType: PlanType;
  /** 単元名・題材名 */
  unitName: string;
  /** 本時が単元の何時間目か（例: 3） */
  lessonNumber?: number;
  /** 単元の総時数（例: 8） */
  totalLessons?: number;
  /** 本時のねらい・扱う内容（任意） */
  lessonFocus?: string;
  /** 児童生徒の実態（仮名で記入） */
  studentProfile?: string;
  /** 使用教科書（会社名など、任意） */
  textbook?: string;
  /** 1単位時間（分） */
  minutes?: number;
  classSetting: ClassSetting;
  disabilityTypes?: DisabilityType[];
  /** 知的障害の教科の段階（例: "小学部2段階"） */
  intellectualStage?: string;
  /** 個別の配慮・支援で特に考えたいこと */
  supportNotes?: string;
  /** 研究授業の研究主題（任意） */
  researchTheme?: string;
  /** その他の要望 */
  extraRequests?: string;
}

export interface ValidationError {
  field: keyof LessonRequest;
  message: string;
}
