import Anthropic from "@anthropic-ai/sdk";
import { createReadStream, existsSync } from "node:fs";
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { resolveApiKey, saveApiKey } from "./config.js";
import { GenerationStoppedError, generateLessonPlan, InvalidRequestError } from "./core/generator.js";
import { CLASS_SETTING_LABELS, DISABILITY_LABELS } from "./core/knowledge/specialNeeds.js";
import { SUBJECTS } from "./core/knowledge/subjects.js";
import { PLAN_TEMPLATES } from "./core/templates.js";
import type { LessonRequest } from "./core/types.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const PORT = Number(process.env.PORT ?? 3939);
const HOST = "127.0.0.1";

const STATIC: Record<string, [string, string]> = {
  "/": [path.join(root, "public/index.html"), "text/html; charset=utf-8"],
  "/app.js": [path.join(root, "public/app.js"), "text/javascript; charset=utf-8"],
  "/style.css": [path.join(root, "public/style.css"), "text/css; charset=utf-8"],
  "/vendor/marked.js": [
    path.join(root, "node_modules/marked/lib/marked.esm.js"),
    "text/javascript; charset=utf-8",
  ],
};

function json(res: ServerResponse, status: number, body: unknown) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(body));
}

async function readJson<T>(req: IncomingMessage): Promise<T> {
  const chunks: Buffer[] = [];
  let size = 0;
  for await (const c of req) {
    size += (c as Buffer).length;
    if (size > 200_000) throw new Error("too large");
    chunks.push(c as Buffer);
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8")) as T;
}

/** 他のWebサイトからこのローカルサーバーを操作されないよう、同一オリジン以外を拒否する */
function isSameOrigin(req: IncomingMessage): boolean {
  const origin = req.headers.origin;
  const host = req.headers.host ?? "";
  if (!/^(127\.0\.0\.1|localhost)(:\d+)?$/.test(host)) return false;
  return !origin || origin === `http://${host}`;
}

function errorMessage(err: unknown): string {
  if (err instanceof Anthropic.AuthenticationError) return "APIキーが正しくありません。設定を確認してください。";
  if (err instanceof Anthropic.RateLimitError) return "混み合っています。少し待ってから再度お試しください。";
  if (err instanceof Anthropic.APIConnectionError) return "インターネットに接続できません。";
  if (err instanceof Anthropic.APIError) return `生成中にエラーが起きました（${err.status ?? "不明"}）。`;
  if (err instanceof GenerationStoppedError) return err.message;
  return "予期しないエラーが起きました。";
}

async function handleGenerate(req: IncomingMessage, res: ServerResponse) {
  const apiKey = resolveApiKey();
  if (!apiKey) return json(res, 400, { error: "先に設定画面でAPIキーを登録してください。" });

  let body: LessonRequest;
  try {
    body = await readJson<LessonRequest>(req);
  } catch {
    return json(res, 400, { error: "入力を読み取れませんでした。" });
  }

  const abort = new AbortController();
  res.on("close", () => abort.abort());

  const client = new Anthropic({ apiKey });
  const gen = generateLessonPlan(body, client, abort.signal);
  let started = false;
  try {
    for await (const text of gen) {
      if (!started) {
        res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-cache" });
        started = true;
      }
      res.write(text);
    }
    if (!started) res.writeHead(200, { "Content-Type": "text/plain; charset=utf-8" });
    res.end();
  } catch (err) {
    if (abort.signal.aborted) return;
    if (err instanceof InvalidRequestError) {
      return json(res, 400, { error: err.message, fields: err.errors });
    }
    console.error(err);
    if (!started) return json(res, 502, { error: errorMessage(err) });
    res.end(`\n\n> ⚠️ ${errorMessage(err)}`);
  }
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url ?? "/", `http://${req.headers.host}`);

  if (url.pathname.startsWith("/api/") && !isSameOrigin(req)) {
    return json(res, 403, { error: "forbidden" });
  }

  if (req.method === "GET" && STATIC[url.pathname]) {
    const [file, type] = STATIC[url.pathname];
    if (!existsSync(file)) return json(res, 404, { error: "not found" });
    res.writeHead(200, { "Content-Type": type });
    return createReadStream(file).pipe(res);
  }

  if (req.method === "GET" && url.pathname === "/api/options") {
    return json(res, 200, {
      subjects: Object.values(SUBJECTS).map(({ id, name, grades }) => ({ id, name, grades })),
      planTypes: Object.values(PLAN_TEMPLATES).map(({ type, label, purpose }) => ({ type, label, purpose })),
      classSettings: CLASS_SETTING_LABELS,
      disabilityTypes: DISABILITY_LABELS,
    });
  }

  if (req.method === "GET" && url.pathname === "/api/settings") {
    return json(res, 200, { hasApiKey: !!resolveApiKey() });
  }

  if (req.method === "POST" && url.pathname === "/api/settings") {
    try {
      const { apiKey } = await readJson<{ apiKey?: string }>(req);
      if (!apiKey?.trim()) return json(res, 400, { error: "APIキーを入力してください。" });
      saveApiKey(apiKey.trim());
      return json(res, 200, { hasApiKey: true });
    } catch {
      return json(res, 400, { error: "保存できませんでした。" });
    }
  }

  if (req.method === "POST" && url.pathname === "/api/generate") {
    return handleGenerate(req, res);
  }

  json(res, 404, { error: "not found" });
});

server.listen(PORT, HOST, () => {
  console.log(`オンライン副担任を起動しました → http://localhost:${PORT}`);
});
