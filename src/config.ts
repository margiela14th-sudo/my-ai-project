import { chmodSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";

/** 設定は先生のパソコン内（ホームディレクトリ）にだけ保存する */
export function configDir(): string {
  return process.env.FUKUTANNIN_HOME ?? path.join(homedir(), ".online-fukutannin");
}

interface AppConfig {
  apiKey?: string;
}

function configPath(): string {
  return path.join(configDir(), "config.json");
}

export function loadConfig(): AppConfig {
  const p = configPath();
  if (!existsSync(p)) return {};
  try {
    return JSON.parse(readFileSync(p, "utf8")) as AppConfig;
  } catch {
    return {};
  }
}

export function saveApiKey(apiKey: string): void {
  mkdirSync(configDir(), { recursive: true, mode: 0o700 });
  const p = configPath();
  writeFileSync(p, JSON.stringify({ ...loadConfig(), apiKey }, null, 2), { mode: 0o600 });
  chmodSync(p, 0o600);
}

export function resolveApiKey(): string | undefined {
  return loadConfig().apiKey || process.env.ANTHROPIC_API_KEY || undefined;
}
