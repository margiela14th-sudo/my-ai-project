import type Anthropic from "@anthropic-ai/sdk";
import { describe, expect, it, vi } from "vitest";
import {
  buildMessageParams,
  GenerationStoppedError,
  generateLessonPlan,
  InvalidRequestError,
  MODEL,
} from "../src/core/generator.js";
import type { LessonRequest } from "../src/core/types.js";

const req: LessonRequest = {
  schoolLevel: "elementary",
  grade: 4,
  subject: "math",
  planType: "daily",
  unitName: "わり算の筆算",
  classSetting: "regular",
};

/** APIを呼ばずにストリームを再現する偽クライアント */
function fakeClient(texts: string[], stopReason = "end_turn") {
  const stream = vi.fn(() => ({
    async *[Symbol.asyncIterator]() {
      for (const t of texts) {
        yield { type: "content_block_delta", index: 0, delta: { type: "text_delta", text: t } };
      }
    },
    finalMessage: async () => ({ stop_reason: stopReason }),
  }));
  return { client: { beta: { messages: { stream } } } as unknown as Anthropic, stream };
}

async function collect(gen: AsyncGenerator<string>) {
  let out = "";
  for await (const t of gen) out += t;
  return out;
}

describe("generateLessonPlan", () => {
  it("本文を順に返す", async () => {
    const { client, stream } = fakeClient(["# 指導案", "\n本時の目標"]);
    expect(await collect(generateLessonPlan(req, client))).toBe("# 指導案\n本時の目標");
    expect(stream).toHaveBeenCalledOnce();
  });

  it("入力が不正ならAPIを呼ばない", async () => {
    const { client, stream } = fakeClient([]);
    await expect(collect(generateLessonPlan({ ...req, unitName: "" }, client))).rejects.toBeInstanceOf(
      InvalidRequestError,
    );
    expect(stream).not.toHaveBeenCalled();
  });

  it("refusal で止まったら分かるエラーにする", async () => {
    const { client } = fakeClient(["途中"], "refusal");
    await expect(collect(generateLessonPlan(req, client))).rejects.toBeInstanceOf(GenerationStoppedError);
  });
});

describe("buildMessageParams", () => {
  it("モデル・思考・キャッシュ・フォールバックの設定", () => {
    const p = buildMessageParams(req);
    expect(p.model).toBe(MODEL);
    expect(p.thinking).toEqual({ type: "adaptive" });
    expect(p.fallbacks).toBe("default");
    expect(p.system[1].cache_control).toEqual({ type: "ephemeral" });
    expect(p.messages[0].content).toContain("日々の学習指導案");
  });
});
