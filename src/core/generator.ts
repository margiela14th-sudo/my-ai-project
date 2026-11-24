import Anthropic from "@anthropic-ai/sdk";
import { buildSystemPrompt, buildUserPrompt, validateRequest } from "./promptBuilder.js";
import type { LessonRequest } from "./types.js";

export const MODEL = "claude-opus-5-5";

export class InvalidRequestError extends Error {
  constructor(public readonly errors: ReturnType<typeof validateRequest>) {
    super(errors.map((e) => e.message).join(" / "));
  }
}

export class GenerationStoppedError extends Error {}

export function buildMessageParams(req: LessonRequest) {
  const [persona, knowledge] = buildSystemPrompt(req);
  return {
    model: MODEL,
    max_tokens: 64000,
    thinking: { type: "adaptive" as const },
    output_config: { effort: "high" as const },
    // 安全分類器が誤って止めた場合、サーバー側で自動的に別モデルで続行する
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default" as const,
    system: [
      { type: "text" as const, text: persona },
      // 人格＋教科ナレッジまでをキャッシュ（同じ教科の2回目以降が安く速くなる）
      { type: "text" as const, text: knowledge, cache_control: { type: "ephemeral" as const } },
    ],
    messages: [{ role: "user" as const, content: buildUserPrompt(req) }],
  };
}

/**
 * 指導案を生成し、本文をテキスト片として順に返す。
 */
export async function* generateLessonPlan(
  req: LessonRequest,
  client: Anthropic,
  signal?: AbortSignal,
): AsyncGenerator<string> {
  const errors = validateRequest(req);
  if (errors.length) throw new InvalidRequestError(errors);

  const stream = client.beta.messages.stream(buildMessageParams(req), { signal });

  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      yield event.delta.text;
    }
  }

  const final = await stream.finalMessage();
  if (final.stop_reason === "refusal") {
    throw new GenerationStoppedError(
      "安全上の理由で生成が止まりました。入力内容（特に実態の記述）を見直して再度お試しください。",
    );
  }
  if (final.stop_reason === "max_tokens") {
    throw new GenerationStoppedError("出力が長すぎて途中で終わりました。条件を絞って再度お試しください。");
  }
}
